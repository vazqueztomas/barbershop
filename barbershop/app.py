import loguru
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from .database import create_connection
from .routes import haircuts_router

logger = loguru.logger
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response


app.include_router(haircuts_router)


@app.get("/")
def read_root():
    create_connection("testing.db")
    return {"Barbershop API": "OK"}
