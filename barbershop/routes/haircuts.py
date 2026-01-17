from uuid import UUID

from fastapi import APIRouter

from barbershop.database import create_connection
from barbershop.models import Haircut
from barbershop.repositories import HaircutRepository

router = APIRouter(prefix="/haircuts")

connection = create_connection("testing.db")


@router.get("/")
def get_haircuts() -> list[Haircut]:
    return HaircutRepository(connection).get_all()


@router.get("/{haircut_id}")
def get_haircut(haircut_id: UUID) -> Haircut:
    return HaircutRepository(connection).get_by_id(haircut_id)


@router.post("/create")
def create_haircut(haircut: Haircut) -> Haircut | str:
    repo = HaircutRepository(connection)
    return repo.create(haircut)


@router.put("/update")
def update_haircut(haircut: Haircut) -> Haircut:
    repo = HaircutRepository(connection)
    return repo.update(haircut)


@router.delete("/{haircut_id}")
def delete_haircut(haircut_id: UUID) -> str:
    repo = HaircutRepository(connection)
    repo.get_by_id(haircut_id)
    repo.delete(haircut_id)
    return f"Deleted haircut with ID {haircut_id}"
