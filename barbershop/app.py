from fastapi import FastAPI

from .routes import haircuts_router

app = FastAPI()
app.include_router(haircuts_router)


@app.get("/")
def read_root():
    return {"Barbershop API": "OK"}
