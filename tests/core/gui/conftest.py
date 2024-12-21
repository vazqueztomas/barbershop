import pytest

from barbershop.gui.constants import FILE_PATH


@pytest.fixture()
def file_path() -> str:
    return FILE_PATH
