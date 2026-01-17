from datetime import date
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from barbershop.app import app
from barbershop.models import Haircut, HaircutCreate
from barbershop.database import create_connection
from barbershop.repositories import HaircutRepository

client = TestClient(app)


class TestApiHaircuts:
    """Test suite for API haircuts endpoints."""

    def setup_method(self):
        """Setup test database connection."""
        self.connection = create_connection("testing.db")
        self.repo = HaircutRepository(self.connection)

    def test_root_endpoint(self):
        """Test root endpoint returns welcome message."""
        response = client.get("/")
        assert response.status_code == 200

    def test_get_haircuts(self):
        """Test getting all haircuts returns list."""
        response = client.get("/haircuts")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_haircut_success(self):
        """Test getting a specific haircut by ID."""
        created = self.repo.create(HaircutCreate(name="API Test Cut", price=35000.0, date=date.today()))

        response = client.get(f"/haircuts/{created.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "API Test Cut"

    def test_get_haircut_not_found(self):
        """Test getting a non-existent haircut returns 404."""
        fake_id = uuid4()
        response = client.get(f"/haircuts/{fake_id}")
        assert response.status_code == 404
        assert response.json() == {"detail": "Haircut not found"}

    def test_create_haircut(self):
        """Test creating a new haircut."""
        haircut_data = {
            "name": "New API Cut",
            "price": 40000.0,
            "date": date.today().isoformat(),
        }
        response = client.post("/haircuts/create", json=haircut_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New API Cut"
        assert "id" in data

    def test_create_haircut_without_date(self):
        """Test creating a haircut without date (auto-generated)."""
        haircut_data = {
            "name": "Auto Date Cut",
            "price": 30000.0,
        }
        response = client.post("/haircuts/create", json=haircut_data)
        assert response.status_code == 200
        data = response.json()
        assert data["date"] == date.today().isoformat()

    def test_update_haircut(self):
        """Test updating a haircut."""
        created = self.repo.create(HaircutCreate(name="Original Cut", price=25000.0, date=date.today()))

        update_data = {
            "id": str(created.id),
            "name": "Updated Cut",
            "price": 30000.0,
            "date": date.today().isoformat(),
        }
        response = client.put("/haircuts/update", json=update_data)
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Cut"

    def test_update_price(self):
        """Test updating only the price."""
        created = self.repo.create(HaircutCreate(name="Price Test Cut", price=20000.0, date=date.today()))

        response = client.patch(f"/haircuts/{created.id}/price", json={"price": 35000.0})
        assert response.status_code == 200
        assert response.json()["price"] == 35000.0

    def test_delete_haircut(self):
        """Test deleting a haircut."""
        created = self.repo.create(HaircutCreate(name="To Delete", price=20000.0, date=date.today()))
        haircut_id = str(created.id)

        response = client.delete(f"/haircuts/{haircut_id}")
        assert response.status_code == 200

    def test_delete_haircut_not_found(self):
        """Test deleting a non-existent haircut returns 404."""
        fake_id = uuid4()
        response = client.delete(f"/haircuts/{fake_id}")
        assert response.status_code == 404

    def test_invalid_url(self):
        """Test that invalid URLs return 404."""
        response = client.get("/haircut")
        assert response.status_code == 404

    def test_get_today_summary(self):
        """Test getting today's summary."""
        self.repo.create(HaircutCreate(name="Summary Cut", price=50000.0, date=date.today()))

        response = client.get("/haircuts/history/today")
        assert response.status_code == 200
        data = response.json()
        assert "date" in data
        assert "count" in data
        assert "total" in data

    def test_get_daily_history(self):
        """Test getting daily history."""
        self.repo.create(HaircutCreate(name="History Cut", price=45000.0, date=date.today()))

        response = client.get("/haircuts/history/daily")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_get_haircuts_by_date(self):
        """Test getting haircuts by specific date."""
        self.repo.create(HaircutCreate(name="Date Filter Cut", price=35000.0, date=date.today()))

        response = client.get(f"/haircuts/history/date/{date.today().isoformat()}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_delete_haircuts_by_date(self):
        """Test deleting haircuts by date."""
        self.repo.create(HaircutCreate(name="Delete By Date Cut", price=15000.0, date=date.today()))

        response = client.delete(f"/haircuts/history/date/{date.today().isoformat()}")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Deleted" in data["message"]
