from sqlalchemy import Column, Integer, String
from app.db.base import Base
from sqlalchemy.orm import validates


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(60), index=True)
    email = Column(String(60), unique=True, index=True)
    telefono = Column(String(60))
    tipo_documento = Column(String(60))
    documento = Column(String(60))
    nit_cliente = Column(String(60), unique=True, index=True)

    def __init__(self, **kwargs):
        self.session = kwargs.pop('session', None)
        super().__init__(**kwargs)

    @validates('email')
    def validate_email(self, key, value):
        if "@" not in value or "." not in value:
            raise ValueError("El correo electrónico no es válido.")
        
        if self.session:
            existing_email = self.session.query(Usuario).filter(Usuario.email == value).first()
            if existing_email:
                raise ValueError("El usuario con ese correo ya está registrado.")
        
        return value

    @validates('nit_cliente')
    def validate_nit_cliente(self, key, value):
        if not value.isdigit():
            raise ValueError("El NIT del cliente debe ser numérico.")
        
        if self.session:
            existing_nit = self.session.query(Usuario).filter(Usuario.nit_cliente == value).first()
            if existing_nit:
                raise ValueError("El usuario con ese NIT de cliente ya está registrado.")
        
        return value