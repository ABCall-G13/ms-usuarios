from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponse(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    telefono: str
    tipo_documento: str
    documento: str
    nit_cliente: str

    model_config = ConfigDict(from_attributes=True)
