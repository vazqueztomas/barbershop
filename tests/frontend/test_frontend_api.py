"""Test para verificar que el frontend se conecta correctamente al backend."""

import requests
import pytest
from datetime import date
from uuid import uuid4


BASE_URL = "http://127.0.0.1:8000"


class TestFrontendApiConnection:
    """Tests para verificar la conexión frontend-backend."""

    def test_api_root_endpoint(self):
        """Test que el endpoint raíz responde."""
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        assert response.json() == {"Barbershop API": "OK"}

    def test_create_haircut(self):
        """Test de creación de corte."""
        haircut_data = {
            "name": "Corte Test Frontend",
            "price": 25000.0,
            "date": date.today().isoformat()
        }
        response = requests.post(f"{BASE_URL}/haircuts/create", json=haircut_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Corte Test Frontend"
        assert data["price"] == 25000.0
        assert "id" in data

        cleanup_id = data["id"]
        requests.delete(f"{BASE_URL}/haircuts/{cleanup_id}")
        return data["id"]

    def test_get_haircuts(self):
        """Test de obtención de todos los cortes."""
        response = requests.get(f"{BASE_URL}/haircuts/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_today_summary(self):
        """Test del resumen del día."""
        response = requests.get(f"{BASE_URL}/haircuts/history/today")
        assert response.status_code == 200
        data = response.json()
        assert "date" in data
        assert "count" in data
        assert "total" in data

    def test_get_daily_history(self):
        """Test del historial diario."""
        response = requests.get(f"{BASE_URL}/haircuts/history/daily")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_crud_complete_flow(self):
        """Test del flujo completo CRUD."""
        create_data = {
            "name": "CRUD Test Cut",
            "price": 30000.0,
            "date": date.today().isoformat()
        }
        create_response = requests.post(f"{BASE_URL}/haircuts/create", json=create_data)
        assert create_response.status_code == 200
        haircut_id = create_response.json()["id"]

        update_response = requests.put(f"{BASE_URL}/haircuts/update", json={
            "id": haircut_id,
            "name": "CRUD Updated Cut",
            "price": 35000.0,
            "date": date.today().isoformat()
        })
        assert update_response.status_code == 200
        assert update_response.json()["name"] == "CRUD Updated Cut"

        delete_response = requests.delete(f"{BASE_URL}/haircuts/{haircut_id}")
        assert delete_response.status_code == 200

        get_response = requests.get(f"{BASE_URL}/haircuts/{haircut_id}")
        assert get_response.status_code == 404

    def test_update_price(self):
        """Test de actualización de precio."""
        create_response = requests.post(f"{BASE_URL}/haircuts/create", json={
            "name": "Price Update Test",
            "price": 20000.0,
            "date": date.today().isoformat()
        })
        haircut_id = create_response.json()["id"]

        patch_response = requests.patch(f"{BASE_URL}/haircuts/{haircut_id}/price", json={"price": 45000.0})
        assert patch_response.status_code == 200
        assert patch_response.json()["price"] == 45000.0

        requests.delete(f"{BASE_URL}/haircuts/{haircut_id}")

    def test_delete_by_date(self):
        """Test de eliminación por fecha."""
        create_response = requests.post(f"{BASE_URL}/haircuts/create", json={
            "name": "Delete By Date Test",
            "price": 15000.0,
            "date": date.today().isoformat()
        })
        assert create_response.status_code == 200

        delete_response = requests.delete(f"{BASE_URL}/haircuts/history/date/{date.today().isoformat()}")
        assert delete_response.status_code == 200
        assert "Deleted" in delete_response.json()["message"]

    def test_invalid_date_format(self):
        """Test de formato de fecha inválido."""
        response = requests.get(f"{BASE_URL}/haircuts/history/date/invalid-date")
        assert response.status_code == 400

    def test_missing_price(self):
        """Test de precio faltante."""
        response = requests.post(f"{BASE_URL}/haircuts/create", json={
            "name": "No Price Cut"
        })
        assert response.status_code == 422

    def test_missing_name(self):
        """Test de nombre faltante."""
        response = requests.post(f"{BASE_URL}/haircuts/create", json={
            "price": 25000.0
        })
        assert response.status_code == 422
