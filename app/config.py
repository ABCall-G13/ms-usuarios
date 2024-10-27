import os
from dotenv import load_dotenv

load_dotenv()
DB_USER = os.getenv("DB_USER", "prueba")
DB_PASSWORD = os.getenv("DB_PASSWORD", "prueba")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "prueba")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_SOCKET_PATH_PRIMARY = os.getenv("DB_SOCKET_PATH_PRIMARY", "")
