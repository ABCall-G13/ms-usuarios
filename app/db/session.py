from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import config

if config.DB_SOCKET_PATH_PRIMARY:
    SQLALCHEMY_DATABASE_URL = (
        f"mysql+mysqlconnector://{config.DB_USER}:{config.DB_PASSWORD}@/{config.DB_NAME}"
        f"?unix_socket={config.DB_SOCKET_PATH_PRIMARY}"
    )
else:
    SQLALCHEMY_DATABASE_URL = (
        f"mysql+mysqlconnector://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
    )

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
