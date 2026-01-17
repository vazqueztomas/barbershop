from datetime import date as date_type
from uuid import UUID

from fastapi import APIRouter

from barbershop.database import create_connection
from barbershop.models import Haircut, HaircutCreate
from barbershop.repositories import HaircutRepository
from barbershop.repositories.handler_errors import NotFoundResponse

router = APIRouter(prefix="/haircuts")

connection = create_connection("testing.db")


@router.get("/")
def get_haircuts() -> list[Haircut]:
    return HaircutRepository(connection).get_all()


@router.get("/{haircut_id}")
def get_haircut(haircut_id: UUID) -> Haircut:
    return HaircutRepository(connection).get_by_id(haircut_id)


@router.post("/create")
def create_haircut(haircut: HaircutCreate) -> Haircut:
    repo = HaircutRepository(connection)
    return repo.create(haircut)


@router.put("/update")
def update_haircut(haircut: Haircut) -> Haircut:
    repo = HaircutRepository(connection)
    return repo.update(haircut)


@router.patch("/{haircut_id}/price")
def update_haircut_price(haircut_id: UUID, body: dict) -> Haircut:
    repo = HaircutRepository(connection)
    new_price = body.get("price")
    if new_price is None:
        raise NotFoundResponse(status_code=400, detail="Price is required")
    return repo.update_price(haircut_id, new_price)


@router.delete("/{haircut_id}")
def delete_haircut(haircut_id: UUID) -> dict:
    repo = HaircutRepository(connection)
    repo.get_by_id(haircut_id)
    repo.delete(haircut_id)
    return {"message": f"Haircut {haircut_id} deleted"}


@router.delete("/history/date/{cutoff_date}")
def delete_haircuts_by_date(cutoff_date: str) -> dict:
    parsed_date = date_type.fromisoformat(cutoff_date)
    repo = HaircutRepository(connection)
    count = repo.delete_by_date(parsed_date)
    return {"message": f"Deleted {count} haircuts for date {cutoff_date}"}


@router.get("/history/daily")
def get_daily_history() -> dict[str, float]:
    summary = HaircutRepository(connection).get_daily_summary()
    return {d.isoformat(): total for d, total in summary.items()}


@router.get("/history/date/{cutoff_date}")
def get_haircuts_by_date(cutoff_date: str) -> list[Haircut]:
    parsed_date = date_type.fromisoformat(cutoff_date)
    return HaircutRepository(connection).get_by_date(parsed_date)


@router.get("/history/today")
def get_today_summary() -> dict:
    repo = HaircutRepository(connection)
    today_haircuts = repo.get_by_date(date_type.today())
    total = sum(h.price for h in today_haircuts)
    return {
        "date": date_type.today().isoformat(),
        "count": len(today_haircuts),
        "total": total
    }
