from pydantic import BaseModel


class Haircut(BaseModel):
    id: int
    name: str
    price: float
    description: str
