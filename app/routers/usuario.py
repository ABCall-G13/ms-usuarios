from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.external_services.cliente_service import verificar_cliente_existente
from app.schemas.usuario import UserResponse
from app.crud.usuario import get_user_by_document_and_client, create_or_update_user_client_data
from app.dependencies import get_db
import pandas as pd
import httpx

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

    if file.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        raise HTTPException(
            status_code=400, detail="El archivo debe ser de tipo Excel (.xlsx)")

    try:

        df = pd.read_excel(file.file)

        required_columns = {"doc_type", "doc_number",
                            "nombre", "email", "telefono"}
        if not required_columns.issubset(df.columns):
            raise HTTPException(
                status_code=400,
                detail=f"El archivo debe contener las columnas: {', '.join(required_columns)}"
            )

        for _, row in df.iterrows():
            row_data = row.to_dict()

            row_data['nit_cliente'] = nit_cliente
            create_or_update_user_client_data(db, row_data)

        return {"detail": "Datos sincronizados exitosamente"}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al procesar el archivo: {str(e)}")
