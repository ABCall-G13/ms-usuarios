from sqlalchemy.orm import Session
from app.models.usuario import Usuario

def get_user_by_document_and_client(db: Session,
                                    doc_type: str,
                                    doc_number: str,
                                    nit_cliente: str):
    return (
        db.query(Usuario)
        .filter(Usuario.tipo_documento == doc_type,
                Usuario.documento == doc_number,
                Usuario.nit_cliente == nit_cliente)
        .first()
    )
