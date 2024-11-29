from pydantic import BaseModel

class Haircut(BaseModel):
    name: str
    price: float
    description: str