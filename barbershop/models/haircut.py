from datetime import date as date_type
from uuid import UUID, uuid4
from typing import Optional

from pydantic import BaseModel


class ServicePrice(BaseModel):
    serviceName: str
    basePrice: int


class ServicePriceCreate(BaseModel):
    serviceName: str
    basePrice: int


class HaircutCreate(BaseModel):
    clientName: str
    serviceName: str
    price: float
    date: str
    time: Optional[str] = None
    count: int = 0
    tip: float = 0


class Haircut(BaseModel):
    id: UUID
    clientName: str
    serviceName: str
    price: float
    date: date_type
    time: Optional[str] = None
    count: int = 0
    tip: float = 0

    class Config:
        from_attributes = True
