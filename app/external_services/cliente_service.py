from yarl import URL
import httpx
from fastapi import HTTPException
from app import config
import re

def validate_nit_cliente(nit_cliente: str):
    if not re.match(r'^[a-zA-Z0-9]+$', nit_cliente):
        raise HTTPException(status_code=400, detail="Invalid nit_cliente")

async def verificar_cliente_existente(nit_cliente: str):
    validate_nit_cliente(nit_cliente)

    base_url = URL(config.URL_SERVICE_CLIENT)
    # Build the URL safely
    full_url = base_url / "clientes" / nit_cliente

    async with httpx.AsyncClient() as client:
        response = await client.get(str(full_url))
        if response.status_code == 404:
            raise HTTPException(
                status_code=404, detail="Cliente no encontrado")
        elif response.status_code != 200:
            raise HTTPException(status_code=response.status_code,
                                detail="Error al verificar el cliente")
