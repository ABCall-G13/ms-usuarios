import httpx
from fastapi import HTTPException


async def verificar_cliente_existente(nit_cliente: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://ms-clientes-345518488840.us-central1.run.app/clientes/{nit_cliente}")
        if response.status_code == 404:
            raise HTTPException(
                status_code=404, detail="Cliente no encontrado")
        elif response.status_code != 200:
            raise HTTPException(status_code=response.status_code,
                                detail="Error al verificar el cliente")
