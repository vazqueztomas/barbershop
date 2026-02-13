from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Generator
from uuid import UUID
from contextlib import contextmanager

from barbershop.database import create_connection
import os

DATABASE_URL = os.environ.get("DATABASE_URL")

T = TypeVar("T")


@contextmanager
def get_db_connection() -> Generator:
    """Context manager para obtener conexión a la base de datos."""
    conn = create_connection(DATABASE_URL)
    try:
        yield conn
    finally:
        if conn:
            conn.close()


def get_db() -> Generator:
    """Dependency para obtener conexión a la base de datos."""
    conn = create_connection(DATABASE_URL)
    try:
        yield conn
    finally:
        if conn:
            conn.close()


class BaseRepository(ABC, Generic[T]):
    """
    Abstract base class for SQL storage repositories.
    """

    @abstractmethod
    def get_all(self) -> list[T]:
        """
        Retrieve an item by its ID.
        """
        pass

    @abstractmethod
    def get_by_id(self, id) -> T | str:
        """
        Retrieve an item by its ID.
        """
        pass

    @abstractmethod
    def create(self, item: T) -> T:
        """
        Create a new item.
        """
        pass

    @abstractmethod
    def update(self, item: T) -> T:
        """
        Update an existing item.
        """
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """
        Delete an item by its ID.
        """
        pass

    @abstractmethod
    def get_by_id(self, id) -> T | str:
        """
        Retrieve an item by its ID.
        """
        pass

    @abstractmethod
    def create(self, item: T) -> T:
        """
        Create a new item.
        """
        pass

    @abstractmethod
    def update(self, item: T) -> T:
        """
        Update an existing item.
        """
        pass

    @abstractmethod
    def delete(self, id: UUID) -> None:
        """
        Delete an item by its ID.
        """
        pass
