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


def create_or_update_user_client_data(db: Session, data: dict):
    doc_type = data.get("doc_type")
    doc_number = data.get("doc_number")
    nit_cliente = data.get("nit_cliente")

    # Verificar si el usuario ya existe
    user = (
        db.query(Usuario)
        .filter(
            Usuario.tipo_documento == doc_type,
            Usuario.documento == doc_number,
            Usuario.nit_cliente == nit_cliente
        )
        .first()
    )

    if user:

        user.nombre = data.get("nombre", user.nombre)
        user.email = data.get("email", user.email)
        user.telefono = data.get("telefono", user.telefono)
    else:

        user = Usuario(
            tipo_documento=doc_type,
            documento=doc_number,
            nit_cliente=nit_cliente,
            nombre=data.get("nombre"),
            email=data.get("email"),
            telefono=data.get("telefono")
        )
        db.add(user)

    db.commit()
    db.refresh(user)
    return user
