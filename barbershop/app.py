import loguru
from fastapi import FastAPI

from .database import create_connection
from .routes import haircuts_router

logger = loguru.logger
app = FastAPI()

app.include_router(haircuts_router)


@app.get("/")
def read_root():
    create_connection("testing.db")
    return {"Barbershop API": "OK"}
