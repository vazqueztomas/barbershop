from fastapi import APIRouter

from barbershop.database.database import haircuts_collection
from barbershop.models import Haircut

router = APIRouter(prefix="/haircuts")


@router.get(
    "/", response_model=list[Haircut], description="Get all haircuts", status_code=200
)
async def get_haircuts() -> list[Haircut]:
    haircuts: list[Haircut] = await haircuts_collection.find().to_list(None)
    return haircuts


@router.get("/{haircut_id}", response_model=Haircut)
async def get_haircut(haircut_id: str) -> Haircut | None:
    haircut: Haircut = await haircuts_collection.find_one({"_id": haircut_id})

    return haircut


@router.post("/", response_model=Haircut, status_code=201)
async def create_haircut(haircut: Haircut) -> Haircut:
    new_haircut = await haircuts_collection.insert_one(haircut.model_dump())
    return await haircuts_collection.find_one({"_id": new_haircut.inserted_id})


@router.delete("/{haircut_id}", response_model=Haircut)
async def delete_haircut(haircut_id: str) -> Haircut | None:
    haircut: Haircut = await haircuts_collection.find_one({"id": haircut_id})
    if haircut:
        await haircuts_collection.delete_one({"id": haircut_id})
        return haircut
    return None
