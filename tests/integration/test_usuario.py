from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from app.models.usuario import Usuario
from app.dependencies import get_db
from app.db.base import Base
from unittest.mock import patch
from io import BytesIO
import pandas as pd
from fastapi import HTTPException

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# Configura la base de datos de prueba
Base.metadata.create_all(bind=engine)


def setup_function():
    # Reinicia la tabla de usuarios antes de cada prueba
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_get_user_success():
    # Añade un usuario a la base de datos de prueba
    db = TestingSessionLocal()
    user = Usuario(
        tipo_documento="CC",
        documento="123456789",
        nit_cliente="8812023",
        nombre="Test User",
        email="example@user.com",
        telefono="1234567890"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    # Realiza la petición de prueba
    response = client.get(
        "/usuario", params={"doc_type": "CC", "doc_number": "123456789", "client": "8812023"})
    print(response.text)
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "nombre": "Test User",
        "email": "example@user.com",
        "telefono": "1234567890",
        "tipo_documento": "CC",
        "documento": "123456789",
        "nit_cliente": "8812023",
    }


def test_get_user_not_found():
    # Realiza una petición para un usuario que no existe
    response = client.get(
        "/usuario", params={"doc_type": "CC", "doc_number": "987654321", "client": "test_client"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Usuario no encontrado"}


@patch("app.external_services.cliente_service.verificar_cliente_existente")
def test_sync_users_success(mock_verificar_cliente):
    # Mockear la verificación del cliente para que se acepte
    mock_verificar_cliente.return_value = None

    # Crear un archivo Excel en memoria
    data = {
        "doc_type": ["CC"],
        "doc_number": ["123456789"],
        "nombre": ["Test User"],
        "email": ["example@user.com"],
        "telefono": ["1234567890"]
    }
    df = pd.DataFrame(data)
    excel_file = BytesIO()
    df.to_excel(excel_file, index=False)
    excel_file.seek(0)

    # Enviar el archivo como parte de la solicitud
    response = client.post(
        "/sync-users/8812023",
        files={"file": ("usuarios.xlsx", excel_file,
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    )

    assert response.status_code == 200
    assert response.json() == {"detail": "Datos sincronizados exitosamente"}

    # Verificar que el usuario se haya creado en la base de datos
    db = TestingSessionLocal()
    user = db.query(Usuario).filter_by(documento="123456789").first()
    db.close()
    assert user is not None
    assert user.nombre == "Test User"
    assert user.email == "example@user.com"


@patch("app.external_services.cliente_service.verificar_cliente_existente")
def test_sync_users_client_not_found(mock_verificar_cliente):
    # Mockear la verificación del cliente para que falle
    mock_verificar_cliente.side_effect = HTTPException(
        status_code=404, detail="Cliente no encontrado")

    # Crear un archivo Excel en memoria
    data = {
        "doc_type": ["CC"],
        "doc_number": ["123456789"],
        "nombre": ["Test User"],
        "email": ["example@user.com"],
        "telefono": ["1234567890"]
    }
    df = pd.DataFrame(data)
    excel_file = BytesIO()
    df.to_excel(excel_file, index=False)
    excel_file.seek(0)

    # Enviar el archivo como parte de la solicitud
    response = client.post(
        "/sync-users/9999999",
        files={"file": ("usuarios.xlsx", excel_file,
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Cliente no encontrado"}
