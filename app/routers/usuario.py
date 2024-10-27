from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.usuario import UserResponse
from app.crud.usuario import get_user_by_document_and_client
from app.dependencies import get_db

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
