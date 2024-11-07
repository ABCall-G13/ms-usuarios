from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from app.models.usuario import Usuario
from app.dependencies import get_db
from app.db.base import Base
from unittest.mock import patch, AsyncMock
from io import BytesIO
import pandas as pd
from app.utils.security import UserToken, get_current_user_token

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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

def mock_get_current_user_token():
    return UserToken(email="example@user.com", token="test_token")

app.dependency_overrides[get_current_user_token] = mock_get_current_user_token

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
        "/usuario", params={"doc_type": "CC", "doc_number": "123456789", "client": "8812023"}
    )
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
        "/usuario", params={"doc_type": "CC", "doc_number": "987654321", "client": "test_client"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Usuario no encontrado"}

def test_sync_users_success():
    # Prepara un archivo Excel en memoria con los datos necesarios
    data = {
        "doc_type": ["CC"],
        "doc_number": ["123456789"],
        "nombre": ["Test User"],
        "email": ["example@user.com"],
        "telefono": ["1234567890"],
    }
    df = pd.DataFrame(data)
    excel_file = BytesIO()
    df.to_excel(excel_file, index=False)
    excel_file.seek(0)

    # Mock de `verificar_cliente_existente` para que pase
    with patch("app.routers.usuario.verificar_cliente_existente", new_callable=AsyncMock) as mock_verificar_cliente_existente:
        mock_verificar_cliente_existente.return_value = "8812023"  # Devuelve un `nit` válido

        # Prepara el archivo para la carga
        files = {
            "file": (
                "test.xlsx",
                excel_file,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        }

        # Realiza la petición POST
        response = client.post("/sync-users", files=files)

        # Imprime el contenido de la respuesta
        print(response.text)

        # Verifica la respuesta
        assert response.status_code == 200
        assert response.json() == {"detail": "Datos sincronizados exitosamente"}

        # Verifica que el usuario fue agregado a la base de datos
        db = TestingSessionLocal()
        user = db.query(Usuario).filter_by(documento="123456789").first()
        assert user is not None
        assert user.nombre == "Test User"
        db.close()
