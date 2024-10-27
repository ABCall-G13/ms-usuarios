from sqlalchemy.orm import Session
from app.db.session import SessionLocal

# Crea una sesión de base de datos que se utilizará en las rutas


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
