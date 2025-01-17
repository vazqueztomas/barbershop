from fastapi import APIRouter

from barbershop.database.database import haircuts_collection
from barbershop.models import Haircut

router = APIRouter(prefix="/haircuts")


@router.get(
    "/", response_model=list[Haircut], description="Get all haircuts", status_code=200
)
def get_haircuts() -> list[Haircut]:
    haircuts_list: list[Haircut] = []
    for haircut in haircuts_collection.find():
        haircuts_list.append(haircut)  # noqa: PERF402

    return haircuts_list


@router.get("/{haircut_id}", response_model=Haircut)
def get_haircut(haircut_id: str) -> Haircut | None:
    haircut: Haircut = haircuts_collection.find_one({"_id": haircut_id})

    return haircut


@router.post("/", response_model=Haircut, status_code=201)
def create_haircut(haircut: Haircut) -> Haircut:
    new_haircut = haircuts_collection.insert_one(haircut.model_dump())
    return haircuts_collection.find_one({"_id": new_haircut.inserted_id})


@router.delete("/{haircut_id}", response_model=Haircut)
def delete_haircut(haircut_id: str) -> Haircut | None:
    haircut: Haircut = haircuts_collection.find_one({"id": haircut_id})
    if haircut:
        haircuts_collection.delete_one({"id": haircut_id})
        return haircut
    return None
