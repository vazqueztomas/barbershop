from datetime import date
from uuid import UUID, uuid4
import pytest
from barbershop.models import Haircut, HaircutCreate


@pytest.fixture
def haircut_id():
    return uuid4()


@pytest.fixture
def haircut(haircut_id):
    return Haircut(
        id=haircut_id,
        name="Classic Cut",
        price=25000.0,
        date=date.today(),
    )


@pytest.fixture
def haircut_create():
    return HaircutCreate(
        name="New Cut",
        price=30000.0,
        date=date.today(),
    )


@pytest.fixture
def haircuts_list(haircut_id):
    return [
        Haircut(
            id=haircut_id,
            name="Classic Cut",
            price=25000.0,
            date=date.today(),
        ),
        Haircut(
            id=uuid4(),
            name="Fade Cut",
            price=30000.0,
            date=date.today(),
        ),
        Haircut(
            id=uuid4(),
            name="Beard Trim",
            price=15000.0,
            date=date.today(),
        ),
    ]
