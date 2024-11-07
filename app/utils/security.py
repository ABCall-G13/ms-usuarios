from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.dependencies import get_db
from app import config


SECRET_KEY = config.SECRET_KEY
ALGORITHM = "HS256"

def get_current_email(request: Request, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    print("Headers received:", request.headers)

    # Intenta obtener el token de Authorization o X-Forwarded-Authorization
    token = request.headers.get("Authorization") or request.headers.get("X-Forwarded-Authorization")
    
    if not token or not token.startswith("Bearer "):
        raise credentials_exception
    
    # Elimina el prefijo 'Bearer ' del token
    token = token[7:]
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        print("JWT payload:", payload)
    except JWTError:
        raise credentials_exception
    
    return email