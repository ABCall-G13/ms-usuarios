from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import usuario
from app.db.session import engine
from app.db.base import Base

origins = [
    "http://localhost:3000",
    "https://front-abcall-345518488840.us-central1.run.app"
]


def recreate_database():
    print("Recreating the database...")
    Base.metadata.create_all(engine)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuario.router)


if __name__ == "__main__":
    recreate_database()
