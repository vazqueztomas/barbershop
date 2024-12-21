import pytest

from barbershop.models import Haircut


@pytest.fixture()
def haircuts_list() -> list[Haircut]:
    return [
        Haircut(id=1, name="Tomas", price=1200, description="Buen corte").model_dump(),
        Haircut(id=2, name="Tomas", price=1200, description="Buen corte").model_dump(),
        Haircut(id=3, name="Tomas", price=1200, description="Buen corte").model_dump(),
    ]
