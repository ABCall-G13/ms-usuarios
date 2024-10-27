from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    telefono: str
    tipo_documento: str
    documento: str
    nit_cliente: str

    class Config:
        from_attributes = True
