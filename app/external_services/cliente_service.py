from yarl import URL
import httpx
from fastapi import HTTPException
from app import config
import re

async def verificar_cliente_existente(email: str):
    base_url = URL(config.URL_SERVICE_CLIENT)
    # Build the URL safely
    full_url = base_url / "clientes/email"

    async with httpx.AsyncClient() as client:
        response = await client.post(str(full_url), json={"email": email})
        if response.status_code == 404:
            raise HTTPException(
                status_code=404, detail="Cliente no encontrado")
        elif response.status_code != 200:
            raise HTTPException(status_code=response.status_code,
                                detail="Error al verificar el cliente")
        
        cliente_data = await response.json()
        return cliente_data.get("nit")