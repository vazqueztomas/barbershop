import uuid

from pydantic import BaseModel
from pydantic.fields import Field


class Haircut(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client: str
    haircut: str
    prize: float
    date: str
    selected_option: str
