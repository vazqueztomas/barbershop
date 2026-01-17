from fastapi.testclient import TestClient
from barbershop.app import app
from barbershop.models import Haircut

client = TestClient(app)

def test_get_haircuts(haircuts_list: list[Haircut]) -> None:
    response = client.get("/haircuts")
    assert response.status_code == 200
    assert response.json() == haircuts_list
    
def test_invalid_url() -> None:
    response = client.get("/haircut")
    assert response.status_code == 404

def test_get_haircut(haircuts_list: list [Haircut]) -> None:
    response = client.get("/haircuts/1")
    assert response.status_code == 200
    assert response == haircuts_list[0]

def test_get_haircut_does_not_exist() -> None:
    response = client.get("/haircuts/12312")
    assert response.status_code == 200
    assert response.json() == "Not found"

def test_delete_haircut(haircuts_list: list[Haircut]) -> None:
    response = client.delete("/haircuts/1")
    assert response.status_code == 200
    response = client.get("/haircuts")
    assert response.status_code == 200
    assert response.json() == haircuts_list[0:]

def test_delete_haircut_does_not_exist() -> None:
    response = client.delete("/haircuts/12312")
    assert response.status_code == 200