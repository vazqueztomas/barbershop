from datetime import date as date_type
from uuid import UUID, uuid4
from contextlib import contextmanager
from typing import Generator

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from barbershop.database import create_connection
from barbershop.models import Haircut, HaircutCreate, ServicePrice, ServicePriceCreate
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
    print("=" * 60)
    print("=== REQUEST RECIBIDA EN /haircuts/create ===")
    print(f"haircut: {haircut}")
    print(f"  clientName: {haircut.clientName} (type: {type(haircut.clientName)})")
    print(f"  serviceName: {haircut.serviceName} (type: {type(haircut.serviceName)})")
    print(f"  price: {haircut.price} (type: {type(haircut.price)})")
    print(f"  date: {haircut.date} (type: {type(haircut.date)})")
    print(f"  time: {haircut.time} (type: {type(haircut.time) if haircut.time is not None else 'None'})")
    print(f"  count: {haircut.count} (type: {type(haircut.count)})")
    print("=" * 60)
    try:
        repo = HaircutRepository(conn)
        result = repo.create(haircut)
        print(f"SUCCESS: Created haircut with id: {result.id}")
        return result
    except ValueError as e:
        print(f"DATE ERROR: {e}")
        raise HTTPException(status_code=422, detail=f"Formato de fecha inválido: {str(e)}. Use formato DD/MM/YYYY")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error creating haircut: {str(e)}")


@router.post("/debug-create")
def debug_create_haircut(raw_body: dict, conn=Depends(get_db)) -> dict:
    """
    Endpoint temporal para debuggear el create
    Acepta cualquier JSON y lo打印 sin validación
    """
    print("=" * 60)
    print("=== DEBUG CREATE - RAW BODY ===")
    print(f"raw_body: {raw_body}")
    print(f"types:")
    for key, value in raw_body.items():
        print(f"  {key}: {value} (type: {type(value)})")
    print("=" * 60)
    
    # Intentar crear el objeto manualmente
    try:
        haircut = HaircutCreate(**raw_body)
        print(f"SUCCESS: HaircutCreate validado: {haircut}")
    except Exception as e:
        print(f"ERROR validando HaircutCreate: {e}")
        return {"error": str(e), "raw_body": raw_body}
    
    try:
        repo = HaircutRepository(conn)
        result = repo.create(haircut)
        return {"success": True, "id": str(result.id)}
    except Exception as e:
        return {"error": str(e)}


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
def get_daily_history(conn=Depends(get_db)) -> list[dict]:
    try:
        repo = HaircutRepository(conn)
        all_haircuts = repo.get_all()
        
        # Agrupar por fecha
        by_date: dict[str, dict] = {}
        for haircut in all_haircuts:
            date_key = haircut.date.isoformat()
            if date_key not in by_date:
                by_date[date_key] = {"total": 0, "count": 0, "tip": 0, "clients": []}
            by_date[date_key]["total"] += haircut.price
            by_date[date_key]["count"] += haircut.count
            by_date[date_key]["tip"] += haircut.tip
            by_date[date_key]["clients"].append(haircut.clientName)
        
        # Convertir a lista ordenada por fecha descendente
        result = [
            {
                "date": date_key,
                "total": data["total"],
                "count": data["count"],
                "tip": data["tip"],
                "clients": data["clients"]
            }
            for date_key, data in by_date.items()
        ]
        result.sort(key=lambda x: x["date"], reverse=True)
        
        return result
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
        count = sum(h.count for h in today_haircuts)
        tip = sum(h.tip for h in today_haircuts)
        return {
            "date": date_type.today().isoformat(),
            "count": count,
            "total": total,
            "tip": tip
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting summary: {str(e)}")


# Service Prices Endpoints
@router.get("/services/prices")
def get_service_prices(conn=Depends(get_db)) -> list[ServicePrice]:
    cursor = conn.execute("SELECT service_name, base_price FROM service_prices ORDER BY service_name")
    rows = cursor.fetchall()
    return [ServicePrice(serviceName=row[0], basePrice=row[1]) for row in rows]


@router.put("/services/prices/{service_name}")
def update_service_price(service_name: str, body: dict, conn=Depends(get_db)) -> ServicePrice:
    base_price = body.get("basePrice")
    if base_price is None:
        raise HTTPException(status_code=400, detail="basePrice is required")
    
    cursor = conn.execute(
        "UPDATE service_prices SET base_price = ? WHERE service_name = ?",
        (base_price, service_name)
    )
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Service not found")
    conn.commit()
    
    cursor = conn.execute(
        "SELECT service_name, base_price FROM service_prices WHERE service_name = ?",
        (service_name,)
    )
    row = cursor.fetchone()
    return ServicePrice(serviceName=row[0], basePrice=row[1])


@router.post("/services/prices")
def create_service_price(service_price: ServicePriceCreate, conn=Depends(get_db)) -> ServicePrice:
    cursor = conn.execute(
        "INSERT INTO service_prices (id, service_name, base_price) VALUES (?, ?, ?)",
        (str(uuid4()), service_price.serviceName, service_price.basePrice)
    )
    conn.commit()
    return ServicePrice(serviceName=service_price.serviceName, basePrice=service_price.basePrice)


@router.delete("/services/prices/{service_name}")
def delete_service_price(service_name: str, conn=Depends(get_db)) -> dict:
    cursor = conn.execute(
        "DELETE FROM service_prices WHERE service_name = ?",
        (service_name,)
    )
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Service not found")
    conn.commit()
    return {"message": f"Service {service_name} deleted"}


@router.get("/services/price/{service_name}")
def get_service_price(service_name: str, conn=Depends(get_db)) -> ServicePrice:
    cursor = conn.execute(
        "SELECT service_name, base_price FROM service_prices WHERE service_name = ?",
        (service_name,)
    )
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return ServicePrice(serviceName=row[0], basePrice=row[1])
