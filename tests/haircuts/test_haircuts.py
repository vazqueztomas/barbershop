from fastapi.testclient import TestClient
from barbershop.main import app
from barbershop.models import Haircut

client = TestClient(app)


def test_get_haircuts(haircuts_list: list[Haircut]) -> list[Haircut]:
    response = client.get("/haircuts")
    assert response.status_code == 200
    assert response.json() == haircuts_list

def test_get_haircut(haircuts_list: list [Haircut]) -> Haircut:
    response = client.get("/haircuts/1")
    assert response.status_code == 200
    assert response.json() == haircuts_list[0]

def test_get_haircut_does_not_exist() -> Haircut:
    response = client.get("/haircuts/12312")
    assert response.status_code == 200
    assert response.json() == "Not found"

def test_delete_haircut(haircuts_list: list[Haircut]) -> str:
    response = client.delete("/haircuts/1")
    assert response.status_code == 200
    assert response.json() == "Haircut with id 1 succesfully deleted"
    response = client.get("/haircuts")
    assert response.status_code == 200
    assert response.json() == haircuts_list[1:]

def test_delete_haircut_does_not_exist() -> str:
    response = client.delete("/haircuts/12312")
    assert response.status_code == 200
    assert response.json() == "Not found"