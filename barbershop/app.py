import loguru
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import create_connection
from .routes import haircuts_router

logger = loguru.logger
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://barbershop-frontend-o0ncu5w1r-vazqueztomas-projects.vercel.app",
        "https://barbershop-plum.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(haircuts_router)


@app.get("/")
def read_root():
    create_connection("testing.db")
    return {"Barbershop API": "OK"}
