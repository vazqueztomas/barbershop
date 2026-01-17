from datetime import date
from uuid import uuid4
import pytest
from barbershop.models import Haircut, HaircutCreate


@pytest.fixture
def haircut_id():
    return uuid4()


@pytest.fixture
def haircut(haircut_id):
    return Haircut(
        id=haircut_id,
        name="API Test Cut",
        price=25000.0,
        date=date.today(),
    )


@pytest.fixture
def haircuts_list():
    return [
        Haircut(
            id=uuid4(),
            name="Classic Cut",
            price=25000.0,
            date=date.today(),
        ).model_dump(),
        Haircut(
            id=uuid4(),
            name="Fade Cut",
            price=30000.0,
            date=date.today(),
        ).model_dump(),
        Haircut(
            id=uuid4(),
            name="Beard Trim",
            price=15000.0,
            date=date.today(),
        ).model_dump(),
    ]
