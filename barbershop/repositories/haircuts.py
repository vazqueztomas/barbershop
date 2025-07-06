from uuid import UUID

from barbershop.models import Haircut

from .base import BaseRepository
from .handler_errors import NotFoundResponse


class HaircutRepository(BaseRepository[Haircut]):
    def __init__(self, connection):
        self.connection = connection

    def get_all(self) -> list[Haircut]:
        cuts = self.connection.execute("SELECT * FROM haircuts").fetchall()
        return [Haircut(id=cut[0], name=cut[1], price=cut[2]) for cut in cuts]

    def get_by_id(self, id: UUID) -> Haircut:
        cursor = self.connection.execute(
            "SELECT id, name, price FROM haircuts WHERE id = ?;", (str(id),)
        )
        cut = cursor.fetchone()
        if cut:
            return Haircut(id=UUID(cut[0]), name=cut[1], price=cut[2])
        raise NotFoundResponse(status_code=404, detail="Haircut not found")

    def create(self, item: Haircut) -> Haircut:
        self.connection.execute(
            "INSERT INTO haircuts (id, name, price) VALUES (?, ?, ?);",
            (str(item.id), item.name, item.price),
        )
        self.connection.commit()
        return item

    def update(self, item: Haircut) -> Haircut:
        self.connection.execute(
            "UPDATE haircuts SET name = ?, price = ? WHERE id = ?",
            (str(item.id), item.name, item.price),
        )
        self.connection.commit()
        return item

    def delete(self, id: UUID) -> None:
        self.connection.execute("DELETE FROM haircuts WHERE id = ?", (str(id),))
        self.connection.commit()
