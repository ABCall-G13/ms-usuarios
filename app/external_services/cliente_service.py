from yarl import URL
import httpx
from fastapi import HTTPException
from app import config
import re

async def verificar_cliente_existente(email: str, token: str) -> str:
    base_url = URL(config.URL_SERVICE_CLIENT)
    full_url = base_url / "clientes/email"

    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.post(str(full_url), json={"email": email}, headers=headers)
        
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        elif response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al verificar el cliente")
        
        cliente_data = response.json()
        nit = cliente_data.get("nit")
        if nit is None:
            raise HTTPException(status_code=500, detail="La respuesta no contiene el NIT del cliente")
        
        return nit