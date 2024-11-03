from io import BytesIO
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
import pandas as pd
from app.crud.usuario import create_or_update_user_client_data

def verificar_tipo_archivo(file: UploadFile, content_type_override=None):
    content_type = content_type_override or file.content_type
    if content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        raise HTTPException(
            status_code=400, detail="El archivo debe ser de tipo Excel (.xlsx)"
        )

async def leer_archivo_excel(file: UploadFile):
    try:
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents))
        return df
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al leer el archivo Excel: {str(e)}"
        )

def verificar_columnas_requeridas(df, required_columns={"doc_type", "doc_number", "nombre", "email", "telefono"}):
    if not required_columns.issubset(df.columns):
        raise HTTPException(
            status_code=400,
            detail=f"El archivo debe contener las columnas: {', '.join(required_columns)}"
        )

def procesar_filas_y_actualizar_db(df, nit_cliente: str, db: Session):
    for _, row in df.iterrows():
        row_data = row.to_dict()
        row_data['nit_cliente'] = nit_cliente
        create_or_update_user_client_data(db, row_data)
