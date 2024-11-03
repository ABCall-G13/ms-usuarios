# FILE: tests/unit/test_utils.py
import pytest
from fastapi import HTTPException
from starlette.datastructures import UploadFile
from app.utils.utils import verificar_tipo_archivo, leer_archivo_excel, verificar_columnas_requeridas
import pandas as pd
from io import BytesIO

def test_verificar_tipo_archivo():
    file_content = BytesIO(b"dummy content")
    file = UploadFile(filename="test.xlsx", file=file_content)
    
    # Simula el tipo de contenido para la prueba
    try:
        verificar_tipo_archivo(file, content_type_override="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except HTTPException:
        pytest.fail("verificar_tipo_archivo() raised HTTPException unexpectedly!")

    file = UploadFile(filename="test.txt", file=BytesIO(b"dummy content"))
    with pytest.raises(HTTPException):
        verificar_tipo_archivo(file, content_type_override="text/plain")
        
def test_leer_archivo_excel():
    # Crear un archivo Excel de prueba en memoria
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    excel_file = BytesIO()
    df.to_excel(excel_file, index=False)
    excel_file.seek(0)
    file = UploadFile(filename="test.xlsx", file=excel_file)
    file._content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    result_df = leer_archivo_excel(file.file)
    pd.testing.assert_frame_equal(result_df, df)

    # Probar con un archivo no válido
    invalid_file = BytesIO(b"not an excel file")
    file = UploadFile(filename="test.xlsx", file=invalid_file)
    file._content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    
    with pytest.raises(HTTPException):
        leer_archivo_excel(file.file)

def test_verificar_columnas_requeridas():
    df = pd.DataFrame({
        "doc_type": ["DNI", "DNI"],
        "doc_number": ["12345678", "87654321"],
        "nombre": ["Juan", "Maria"],
        "email": ["juan@example.com", "maria@example.com"],
        "telefono": ["123456789", "987654321"]
    })
    try:
        verificar_columnas_requeridas(df)
    except HTTPException:
        pytest.fail("verificar_columnas_requeridas() raised HTTPException unexpectedly!")

    df_missing_columns = pd.DataFrame({
        "doc_type": ["DNI", "DNI"],
        "doc_number": ["12345678", "87654321"],
        "nombre": ["Juan", "Maria"]
    })
    with pytest.raises(HTTPException):
        verificar_columnas_requeridas(df_missing_columns)
