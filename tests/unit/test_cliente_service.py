import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from app.external_services.cliente_service import verificar_cliente_existente

@pytest.mark.asyncio
async def test_verificar_cliente_existente_cliente_no_encontrado():
    email = "no_existe@ejemplo.com"
    url_service_client = "http://mockservice.com"

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post, \
         patch("app.config.URL_SERVICE_CLIENT", url_service_client):
        mock_post.return_value.status_code = 404

        with pytest.raises(HTTPException) as exc_info:
            await verificar_cliente_existente(email)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Cliente no encontrado"

@pytest.mark.asyncio
async def test_verificar_cliente_existente_error_al_verificar():
    email = "error@ejemplo.com"
    url_service_client = "http://mockservice.com"

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post, \
         patch("app.config.URL_SERVICE_CLIENT", url_service_client):
        mock_post.return_value.status_code = 500

        with pytest.raises(HTTPException) as exc_info:
            await verificar_cliente_existente(email)

        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Error al verificar el cliente"

@pytest.mark.asyncio
async def test_verificar_cliente_existente_exito():
    email = "existe@ejemplo.com"
    url_service_client = "http://mockservice.com"
    expected_nit = "123456789"

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post, \
         patch("app.config.URL_SERVICE_CLIENT", url_service_client):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"nit": expected_nit}

        # Verifica que la función devuelva el NIT correcto sin lanzar excepciones
        nit = await verificar_cliente_existente(email)
        assert nit == expected_nit

        # Verifica que el endpoint fue llamado correctamente
        mock_post.assert_called_once_with(f"{url_service_client}/clientes/email", json={"email": email})
