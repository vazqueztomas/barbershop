import pytest
from barbershop.models import Haircut


@pytest.fixture
def haircuts_list() -> list[Haircut]:
    return [
        Haircut(
            id="1",
            client="Tomas",
            prize=1200,
            haircut="Degrade",
            date="12/12/12",
            selected_option="Pelo",
        ).model_dump(),
        Haircut(
            id="2",
            client="Tomas",
            prize=1200,
            haircut="Degrade",
            date="12/12/12",
            selected_option="Pelo",
        ).model_dump(),
        Haircut(
            id="3",
            client="Tomas",
            prize=1200,
            haircut="Degrade",
            date="12/12/12",
            selected_option="Pelo",
        ).model_dump(),
    ]
