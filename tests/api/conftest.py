import pytest
from barbershop.models import Haircut
from typing import Any


@pytest.fixture
def haircuts_list() -> list[dict[str, Any]]:
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
