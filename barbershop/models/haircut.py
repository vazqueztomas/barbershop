from uuid import UUID

from pydantic import BaseModel


class Haircut(BaseModel):
    id: UUID
    name: str
    price: float
