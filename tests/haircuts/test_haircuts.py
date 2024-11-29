from fastapi.testclient import TestClient
from barbershop.main import app
from barbershop.models import Haircut

client = TestClient(app)


def test_get_haircuts() -> list[Haircut]:
    response = client.get("/haircuts")
    assert response.status_code == 200
    assert response.json() == [
        Haircut(name="Tomas", price=1200, description="Buen corte").model_dump(),
        Haircut(name="Tomas", price=1200, description="Buen corte").model_dump(),
        Haircut(name="Tomas", price=1200, description="Buen corte").model_dump(),
    ]

def test_get_haircut() -> Haircut:
    response = client.get("/haircuts/1")
    assert response.status_code == 200
    assert response.json() == Haircut(name="Tomas", price=1200, description="Buen corte").model_dump()