from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):  # pragma: no cover
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
