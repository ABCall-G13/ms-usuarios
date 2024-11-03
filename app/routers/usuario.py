from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.external_services.cliente_service import verificar_cliente_existente
from app.schemas.usuario import UserResponse
from app.crud.usuario import get_user_by_document_and_client
from app.dependencies import get_db
import pandas as pd
import httpx
from app.utils.utils import verificar_tipo_archivo, leer_archivo_excel, verificar_columnas_requeridas, procesar_filas_y_actualizar_db

router = APIRouter()


@router.get("/usuario", response_model=UserResponse)
async def get_user(
    doc_type: str,
    doc_number: str,
    client: str,
    db: Session = Depends(get_db)
):
    user = get_user_by_document_and_client(db, doc_type, doc_number, client)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.post("/sync-users/{nit_cliente}")
async def sync_users(
    nit_cliente: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    await verificar_cliente_existente(nit_cliente)
    verificar_tipo_archivo(file)

    df = await leer_archivo_excel(file)
    verificar_columnas_requeridas(df)
    procesar_filas_y_actualizar_db(df, nit_cliente, db)

    return {"detail": "Datos sincronizados exitosamente"}