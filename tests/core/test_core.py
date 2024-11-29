from fastapi.testclient import TestClient
from barbershop.main import app

client = TestClient(app)

def test_healtcheck():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Barbershop API": "OK"}