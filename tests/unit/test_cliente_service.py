import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from app.external_services.cliente_service import verificar_cliente_existente

@pytest.mark.asyncio
async def test_verificar_cliente_existente_cliente_no_encontrado():
    email = "no_existe@ejemplo.com"
    token = "test"
    url_service_client = "http://mockservice.com"

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post, \
         patch("app.config.URL_SERVICE_CLIENT", url_service_client):
        mock_post.return_value.status_code = 404

        with pytest.raises(HTTPException) as exc_info:
            await verificar_cliente_existente(email,token)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Cliente no encontrado"

@pytest.mark.asyncio
async def test_verificar_cliente_existente_error_al_verificar():
    email = "error@ejemplo.com"
    token = "test"
    url_service_client = "http://mockservice.com"

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post, \
         patch("app.config.URL_SERVICE_CLIENT", url_service_client):
        mock_post.return_value.status_code = 500

        with pytest.raises(HTTPException) as exc_info:
            await verificar_cliente_existente(email, token)

        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Error al verificar el cliente"



