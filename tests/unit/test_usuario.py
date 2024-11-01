import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.crud.usuario import get_user_by_document_and_client

def test_get_user_by_document_and_client_found():
    # Arrange
    db = MagicMock(spec=Session)
    doc_type = "CC"
    doc_number = "123456789"
    nit_cliente = "987654321"
    
    expected_user = Usuario(
        tipo_documento=doc_type,
        documento=doc_number,
        nit_cliente=nit_cliente
    )
    
    db.query().filter().first.return_value = expected_user
    
    # Act
    result = get_user_by_document_and_client(db, doc_type, doc_number, nit_cliente)
    
    # Assert
    assert result == expected_user
    db.query().filter().first.assert_called_once()

def test_get_user_by_document_and_client_not_found():
    # Arrange
    db = MagicMock(spec=Session)
    doc_type = "CC"
    doc_number = "123456789"
    nit_cliente = "987654321"
    
    db.query().filter().first.return_value = None
    
    # Act
    result = get_user_by_document_and_client(db, doc_type, doc_number, nit_cliente)
    
    # Assert
    assert result is None
    db.query().filter().first.assert_called_once()

def test_validate_email_invalid_format():
    # Arrange
    invalid_email = "usuario-sin-arroba-y-punto"
    
    # Act & Assert
    with pytest.raises(ValueError, match="El correo electrónico no es válido."):
        usuario = Usuario(email=invalid_email)

def test_validate_email_duplicate():
    # Arrange
    db = MagicMock(spec=Session)
    email = "usuario@ejemplo.com"
    
    # Simula que el correo ya existe en la base de datos
    db.query().filter().first.return_value = Usuario(email=email)
    
    # Act & Assert
    with pytest.raises(ValueError, match="El usuario con ese correo ya está registrado."):
        usuario = Usuario(email=email, session=db)