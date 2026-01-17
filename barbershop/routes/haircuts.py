from datetime import date as date_type
from uuid import UUID, uuid4
from contextlib import contextmanager
from typing import Generator

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from barbershop.database import create_connection
from barbershop.models import Haircut, HaircutCreate
from barbershop.repositories import HaircutRepository


@contextmanager
def get_db_connection() -> Generator:
    """Context manager para obtener conexión a la base de datos."""
    conn = create_connection("testing.db")
    try:
        yield conn
    finally:
        pass


def get_db() -> Generator:
    """Dependency para obtener conexión a la base de datos."""
    conn = create_connection("testing.db")
    try:
        yield conn
    finally:
        pass


router = APIRouter(prefix="/haircuts")


@router.get("/")
def get_haircuts(conn=Depends(get_db)) -> list[Haircut]:
    return HaircutRepository(conn).get_all()


@router.get("/{haircut_id}")
def get_haircut(haircut_id: UUID, conn=Depends(get_db)) -> Haircut:
    return HaircutRepository(conn).get_by_id(haircut_id)


@router.post("/create")
def create_haircut(haircut: HaircutCreate, conn=Depends(get_db)) -> Haircut:
    try:
        repo = HaircutRepository(conn)
        return repo.create(haircut)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating haircut: {str(e)}")


@router.put("/update")
def update_haircut(haircut: Haircut, conn=Depends(get_db)) -> Haircut:
    try:
        repo = HaircutRepository(conn)
        return repo.update(haircut)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating haircut: {str(e)}")


@router.patch("/{haircut_id}/price")
def update_haircut_price(haircut_id: UUID, body: dict, conn=Depends(get_db)) -> Haircut:
    repo = HaircutRepository(conn)
    new_price = body.get("price")
    if new_price is None:
        raise HTTPException(status_code=400, detail="Price is required")
    try:
        return repo.update_price(haircut_id, new_price)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating price: {str(e)}")


@router.delete("/{haircut_id}")
def delete_haircut(haircut_id: UUID, conn=Depends(get_db)) -> dict:
    repo = HaircutRepository(conn)
    try:
        repo.get_by_id(haircut_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Haircut not found")
    try:
        repo.delete(haircut_id)
        return {"message": f"Haircut {haircut_id} deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting haircut: {str(e)}")


@router.delete("/history/date/{cutoff_date}")
def delete_haircuts_by_date(cutoff_date: str, conn=Depends(get_db)) -> dict:
    try:
        parsed_date = date_type.fromisoformat(cutoff_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    repo = HaircutRepository(conn)
    try:
        count = repo.delete_by_date(parsed_date)
        return {"message": f"Deleted {count} haircuts for date {cutoff_date}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting haircuts: {str(e)}")


@router.get("/history/daily")
def get_daily_history(conn=Depends(get_db)) -> dict[str, float]:
    try:
        summary = HaircutRepository(conn).get_daily_summary()
        return {d.isoformat(): total for d, total in summary.items()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting history: {str(e)}")


@router.get("/history/date/{cutoff_date}")
def get_haircuts_by_date(cutoff_date: str, conn=Depends(get_db)) -> list[Haircut]:
    try:
        parsed_date = date_type.fromisoformat(cutoff_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    try:
        return HaircutRepository(conn).get_by_date(parsed_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting haircuts: {str(e)}")


@router.get("/history/today")
def get_today_summary(conn=Depends(get_db)) -> dict:
    try:
        repo = HaircutRepository(conn)
        today_haircuts = repo.get_by_date(date_type.today())
        total = sum(h.price for h in today_haircuts)
        return {
            "date": date_type.today().isoformat(),
            "count": len(today_haircuts),
            "total": total
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting summary: {str(e)}")
