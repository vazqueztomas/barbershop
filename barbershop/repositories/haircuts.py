from datetime import date
from uuid import UUID, uuid4

from barbershop.models import Haircut, HaircutCreate
from .handler_errors import NotFoundResponse


class HaircutRepository:
    def __init__(self, connection):
        self.connection = connection

    def get_all(self) -> list[Haircut]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, client_name, service_name, price, date, time, count, tip FROM haircuts ORDER BY date DESC, id DESC")
        cuts = cursor.fetchall()
        return [
            Haircut(
                id=UUID(cut["id"]),
                clientName=cut["client_name"],
                serviceName=cut["service_name"],
                price=cut["price"],
                date=date.fromisoformat(cut["date"]) if cut["date"] else date.today(),
                time=cut["time"],
                count=cut["count"] if cut["count"] else 0,
                tip=cut["tip"] if cut["tip"] else 0
            )
            for cut in cuts
        ]

    def get_by_id(self, id: UUID) -> Haircut:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT id, client_name, service_name, price, date, time, count, tip FROM haircuts WHERE id = %s;", (str(id),)
        )
        cut = cursor.fetchone()
        if cut:
            return Haircut(
                id=UUID(cut["id"]),
                clientName=cut["client_name"],
                serviceName=cut["service_name"],
                price=cut["price"],
                date=date.fromisoformat(cut["date"]) if cut["date"] else date.today(),
                time=cut["time"],
                count=cut["count"] if cut["count"] else 0,
                tip=cut["tip"] if cut["tip"] else 0
            )
        raise NotFoundResponse(status_code=404, detail="Haircut not found")

    def get_by_date(self, cutoff_date: date) -> list[Haircut]:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT id, client_name, service_name, price, date, time, count, tip FROM haircuts WHERE date = %s ORDER BY id DESC;", (cutoff_date.isoformat(),)
        )
        cuts = cursor.fetchall()
        return [
            Haircut(
                id=UUID(cut["id"]),
                clientName=cut["client_name"],
                serviceName=cut["service_name"],
                price=cut["price"],
                date=date.fromisoformat(cut["date"]) if cut["date"] else date.today(),
                time=cut["time"],
                count=cut["count"] if cut["count"] else 0,
                tip=cut["tip"] if cut["tip"] else 0
            )
            for cut in cuts
        ]

    def get_daily_summary(self) -> dict[date, float]:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT date, SUM(price) FROM haircuts GROUP BY date ORDER BY date DESC"
        )
        results = cursor.fetchall()
        return {date.fromisoformat(row["date"]): row["sum"] for row in results if row["date"]}

    def create(self, item: HaircutCreate) -> Haircut:
        item_date = item.date
        if isinstance(item_date, str):
            parts = item_date.split('/')
            if len(parts) == 3:
                item_date = date(int(parts[2]), int(parts[1]), int(parts[0]))
            else:
                item_date = date.fromisoformat(item_date)
        
        haircut = Haircut(
            id=uuid4(),
            clientName=item.clientName,
            serviceName=item.serviceName,
            price=item.price,
            date=item_date,
            time=item.time,
            count=item.count,
            tip=getattr(item, 'tip', 0)
        )
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO haircuts (id, client_name, service_name, price, date, time, count, tip) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
            (str(haircut.id), haircut.clientName, haircut.serviceName, haircut.price, haircut.date.isoformat(), haircut.time, haircut.count, haircut.tip),
        )
        self.connection.commit()
        return haircut

    def update(self, item: Haircut) -> Haircut:
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE haircuts SET client_name = %s, service_name = %s, price = %s, date = %s, time = %s, count = %s, tip = %s WHERE id = %s",
            (item.clientName, item.serviceName, item.price, item.date.isoformat(), item.time, item.count, item.tip, str(item.id)),
        )
        self.connection.commit()
        return item

    def update_price(self, id: UUID, new_price: float) -> Haircut:
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE haircuts SET price = %s WHERE id = %s",
            (new_price, str(id)),
        )
        self.connection.commit()
        return self.get_by_id(id)

    def delete(self, id: UUID) -> None:
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM haircuts WHERE id = %s", (str(id),))
        self.connection.commit()

    def delete_by_date(self, cutoff_date: date) -> int:
        cursor = self.connection.cursor()
        cursor.execute(
            "DELETE FROM haircuts WHERE date = %s", (cutoff_date.isoformat(),)
        )
        self.connection.commit()
        return cursor.rowcount
