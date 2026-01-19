from datetime import date as date_type
from uuid import UUID, uuid4
from typing import Optional

from pydantic import BaseModel


class HaircutCreate(BaseModel):
    clientName: str
    serviceName: str
    price: float
    date: str
    time: Optional[str] = None


class Haircut(BaseModel):
    id: UUID
    clientName: str
    serviceName: str
    price: float
    date: date_type
    time: Optional[str] = None

    class Config:
        from_attributes = True
