from barbershop.models import Haircut
from fastapi import APIRouter

router = APIRouter(prefix="/haircuts")


@router.get("/")
def get_haircuts() -> list[Haircut]:
    return [
        Haircut(name="Tomas", price=1200, description="Buen corte"),
        Haircut(name="Tomas", price=1200, description="Buen corte"),
        Haircut(name="Tomas", price=1200, description="Buen corte"),
    ]
