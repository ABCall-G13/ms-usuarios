from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.dependencies import get_db
from app import config

SECRET_KEY = config.SECRET_KEY
ALGORITHM = "HS256"

class UserToken:
    def __init__(self, email: str, token: str):
        self.email = email
        self.token = token

def get_current_user_token(request: Request, db: Session = Depends(get_db)) -> UserToken:
    credentials_exception = HTTPException(
        status_code=401,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Obtener el token de los encabezados
    token = request.headers.get("Authorization") or request.headers.get("X-Forwarded-Authorization")
    
    if not token or not token.startswith("Bearer "):
        raise credentials_exception
    
    # Eliminar el prefijo 'Bearer ' del token
    token = token[7:]
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    return UserToken(email=email, token=token)
