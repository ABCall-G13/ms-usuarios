import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from app.external_services.cliente_service import verificar_cliente_existente

@pytest.mark.asyncio
async def test_verificar_cliente_existente_cliente_no_encontrado():
    nit_cliente = "123456789"
    url_service_client = "http://mockservice.com"

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get, \
         patch("app.config.URL_SERVICE_CLIENT", url_service_client):
        mock_get.return_value.status_code = 404

        with pytest.raises(HTTPException) as exc_info:
            await verificar_cliente_existente(nit_cliente)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Cliente no encontrado"

@pytest.mark.asyncio
async def test_verificar_cliente_existente_error_al_verificar():
    nit_cliente = "123456789"
    url_service_client = "http://mockservice.com"

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get, \
         patch("app.config.URL_SERVICE_CLIENT", url_service_client):
        mock_get.return_value.status_code = 500

        with pytest.raises(HTTPException) as exc_info:
            await verificar_cliente_existente(nit_cliente)

        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Error al verificar el cliente"

@pytest.mark.asyncio
async def test_verificar_cliente_existente_exito():
    nit_cliente = "123456789"
    url_service_client = "http://mockservice.com"

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get, \
         patch("app.config.URL_SERVICE_CLIENT", url_service_client):
        mock_get.return_value.status_code = 200

        # No debería lanzar ninguna excepción
        await verificar_cliente_existente(nit_cliente)

        mock_get.assert_called_once_with(f"{url_service_client}/clientes/{nit_cliente}")