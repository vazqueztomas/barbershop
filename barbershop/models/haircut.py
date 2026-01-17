from datetime import date as date_type
from uuid import UUID, uuid4

from pydantic import BaseModel


class HaircutCreate(BaseModel):
    name: str
    price: float
    date: date_type = date_type.today()


class Haircut(BaseModel):
    id: UUID
    name: str
    price: float
    date: date_type = date_type.today()

    class Config:
        from_attributes = True
