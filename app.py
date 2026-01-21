import loguru
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from barbershop.database import create_connection
from barbershop.routes import haircuts_router

logger = loguru.logger
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(haircuts_router)


@app.get("/")
def read_root():
    create_connection()
    return {"Barbershop API": "OK"}
