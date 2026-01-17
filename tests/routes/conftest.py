import uuid

import pytest

from barbershop.models import Haircut


@pytest.fixture
def haircut_id() -> str:
    """Fixture to provide a sample haircut ID."""
    return str(uuid.uuid4())


@pytest.fixture
def haircut(haircut_id: str) -> Haircut:
    """Fixture to provide a sample haircut object."""
    return Haircut(
        id=uuid.UUID(haircut_id),
        name="Test Haircut",
        price=20.0,
    )
