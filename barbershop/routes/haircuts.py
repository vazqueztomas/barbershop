from fastapi import APIRouter

from barbershop.models import Haircut

router = APIRouter(prefix="/haircuts")

HAIRCUTS_LIST = [
    Haircut(id=1, name="Tomas", price=1200, description="Buen corte"),
    Haircut(id=2, name="Tomas", price=1200, description="Buen corte"),
    Haircut(id=3, name="Tomas", price=1200, description="Buen corte"),
]


@router.get("/")
def get_haircuts() -> list[Haircut]:
    return HAIRCUTS_LIST


@router.get("/{haircut_id}")
def get_haircut(haircut_id: int) -> Haircut | str:
    for haircut in HAIRCUTS_LIST:
        if haircut.id == haircut_id:
            return haircut
    return "Not found"


@router.delete("/{haircut_id}")
def delete_haircut(haircut_id: int) -> str:
    for index, haircut in enumerate(HAIRCUTS_LIST):
        if haircut.id == haircut_id:
            HAIRCUTS_LIST.pop(index)
            return f"Haircut with id {haircut.id} succesfully deleted"
    return "Not found"
