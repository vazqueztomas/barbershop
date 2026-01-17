from datetime import date
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from barbershop.main import app
from barbershop.models import Haircut, HaircutCreate
from barbershop.database import create_connection
from barbershop.repositories import HaircutRepository

client = TestClient(app)


class TestHaircutsEndpoints:
    """Test suite for haircuts CRUD endpoints."""

    def setup_method(self):
        """Setup test database connection."""
        self.connection = create_connection("testing.db")
        self.repo = HaircutRepository(self.connection)

    def teardown_method(self):
        """Clean up test data."""
        pass

    def test_get_haircuts_empty(self):
        """Test getting haircuts when list is empty."""
        response = client.get("/haircuts")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_haircuts_with_data(self, haircuts_list):
        """Test getting all haircuts."""
        for haircut in haircuts_list:
            self.repo.create(HaircutCreate(name=haircut.name, price=haircut.price, date=haircut.date))

        response = client.get("/haircuts")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= len(haircuts_list)

    def test_get_haircut_success(self):
        """Test getting a specific haircut by ID."""
        created = self.repo.create(HaircutCreate(name="Test Cut", price=25000.0, date=date.today()))

        response = client.get(f"/haircuts/{created.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(created.id)
        assert data["name"] == "Test Cut"

    def test_get_haircut_not_found(self):
        """Test getting a non-existent haircut returns 404."""
        fake_id = uuid4()
        response = client.get(f"/haircuts/{fake_id}")
        assert response.status_code == 404
        assert response.json() == {"detail": "Haircut not found"}

    def test_get_haircut_invalid_uuid(self):
        """Test getting a haircut with invalid UUID format."""
        response = client.get("/haircuts/invalid-uuid")
        assert response.status_code == 422

    def test_create_haircut_success(self):
        """Test creating a new haircut."""
        haircut_data = {
            "name": "New Style",
            "price": 35000.0,
            "date": date.today().isoformat(),
        }
        response = client.post("/haircuts/create", json=haircut_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Style"
        assert data["price"] == 35000.0
        assert "id" in data

    def test_create_haircut_minimal_data(self):
        """Test creating a haircut with only required fields (date auto-generated)."""
        haircut_data = {
            "name": "Basic Cut",
            "price": 20000.0,
        }
        response = client.post("/haircuts/create", json=haircut_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Basic Cut"
        assert data["date"] == date.today().isoformat()

    def test_create_haircut_negative_price(self):
        """Test creating a haircut with negative price (allowed by current model)."""
        haircut_data = {
            "name": "Negative Price Cut",
            "price": -10000.0,
            "date": date.today().isoformat(),
        }
        response = client.post("/haircuts/create", json=haircut_data)
        assert response.status_code == 200

    def test_create_haircut_missing_name(self):
        """Test creating a haircut without name."""
        haircut_data = {
            "price": 25000.0,
        }
        response = client.post("/haircuts/create", json=haircut_data)
        assert response.status_code == 422

    def test_create_haircut_missing_price(self):
        """Test creating a haircut without price."""
        haircut_data = {
            "name": "No Price Cut",
        }
        response = client.post("/haircuts/create", json=haircut_data)
        assert response.status_code == 422

    def test_update_haircut_success(self):
        """Test updating an existing haircut."""
        created = self.repo.create(HaircutCreate(name="Original Cut", price=25000.0, date=date.today()))

        updated_data = {
            "id": str(created.id),
            "name": "Updated Style",
            "price": 40000.0,
            "date": date.today().isoformat(),
        }
        response = client.put("/haircuts/update", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Style"
        assert data["price"] == 40000.0

    def test_update_haircut_not_found(self):
        """Test updating a non-existent haircut (current behavior allows upsert)."""
        fake_id = uuid4()
        update_data = {
            "id": str(fake_id),
            "name": "Ghost Cut",
            "price": 50000.0,
            "date": date.today().isoformat(),
        }
        response = client.put("/haircuts/update", json=update_data)
        assert response.status_code == 200
        assert response.json()["name"] == "Ghost Cut"

    def test_update_haircut_partial(self):
        """Test updating only some fields of a haircut."""
        created = self.repo.create(HaircutCreate(name="Partial Test", price=25000.0, date=date.today()))

        update_data = {
            "id": str(created.id),
            "name": "Partial Update",
            "price": created.price,
            "date": date.today().isoformat(),
        }
        response = client.put("/haircuts/update", json=update_data)
        assert response.status_code == 200
        assert response.json()["name"] == "Partial Update"

    def test_update_price_success(self):
        """Test updating only the price of a haircut."""
        created = self.repo.create(HaircutCreate(name="Price Test", price=25000.0, date=date.today()))

        response = client.patch(f"/haircuts/{created.id}/price", json={"price": 45000.0})
        assert response.status_code == 200
        data = response.json()
        assert data["price"] == 45000.0

    def test_update_price_missing(self):
        """Test updating price without providing price."""
        fake_id = uuid4()
        response = client.patch(f"/haircuts/{fake_id}/price", json={})
        assert response.status_code == 400

    def test_delete_haircut_success(self):
        """Test deleting an existing haircut."""
        created = self.repo.create(HaircutCreate(name="To Delete", price=20000.0, date=date.today()))

        response = client.delete(f"/haircuts/{created.id}")
        assert response.status_code == 200

        response = client.get(f"/haircuts/{created.id}")
        assert response.status_code == 404

    def test_delete_haircut_not_found(self):
        """Test deleting a non-existent haircut returns 404."""
        fake_id = uuid4()
        response = client.delete(f"/haircuts/{fake_id}")
        assert response.status_code == 404
        assert response.json() == {"detail": "Haircut not found"}

    def test_delete_haircut_invalid_uuid(self):
        """Test deleting with invalid UUID format."""
        response = client.delete("/haircuts/not-a-uuid")
        assert response.status_code == 422

    def test_crud_complete_flow(self):
        """Test complete CRUD workflow."""
        new_haircut = {
            "name": "Flow Test Cut",
            "price": 45000.0,
            "date": date.today().isoformat(),
        }

        create_response = client.post("/haircuts/create", json=new_haircut)
        assert create_response.status_code == 200
        created = create_response.json()
        haircut_id = created["id"]
        assert created["name"] == "Flow Test Cut"

        read_response = client.get(f"/haircuts/{haircut_id}")
        assert read_response.status_code == 200

        update_response = client.put(
            "/haircuts/update",
            json={
                "id": haircut_id,
                "name": "Updated Flow Cut",
                "price": 50000.0,
                "date": date.today().isoformat(),
            },
        )
        assert update_response.status_code == 200
        assert update_response.json()["name"] == "Updated Flow Cut"

        delete_response = client.delete(f"/haircuts/{haircut_id}")
        assert delete_response.status_code == 200

        confirm_delete = client.get(f"/haircuts/{haircut_id}")
        assert confirm_delete.status_code == 404

    def test_haircut_price_precision(self):
        """Test that haircut prices maintain precision."""
        haircut_data = {
            "name": "Precision Test",
            "price": 19999.99,
            "date": date.today().isoformat(),
        }
        response = client.post("/haircuts/create", json=haircut_data)
        assert response.status_code == 200
        assert response.json()["price"] == 19999.99

    def test_haircut_name_special_chars(self):
        """Test creating haircut with special characters in name."""
        haircut_data = {
            "name": "Corte 'Especial' & Estilo",
            "price": 30000.0,
            "date": date.today().isoformat(),
        }
        response = client.post("/haircuts/create", json=haircut_data)
        assert response.status_code == 200
        assert "'" in response.json()["name"]

    def test_get_today_summary(self):
        """Test getting today's summary returns valid structure."""
        response = client.get("/haircuts/history/today")
        assert response.status_code == 200
        data = response.json()
        assert "date" in data
        assert "count" in data
        assert "total" in data
        assert data["count"] >= 0
        assert data["total"] >= 0

    def test_get_today_summary_with_data(self):
        """Test getting today's summary with haircuts."""
        haircut_data = {
            "name": "Summary Test Cut",
            "price": 25000.0,
            "date": date.today().isoformat(),
        }
        client.post("/haircuts/create", json=haircut_data)

        response = client.get("/haircuts/history/today")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] >= 1
        assert data["total"] >= 25000.0

    def test_get_daily_history(self):
        """Test getting daily history summary."""
        haircut_data = {
            "name": "History Test Cut",
            "price": 30000.0,
            "date": date.today().isoformat(),
        }
        client.post("/haircuts/create", json=haircut_data)

        response = client.get("/haircuts/history/daily")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert date.today().isoformat() in data

    def test_get_haircuts_by_date(self):
        """Test getting haircuts for a specific date."""
        haircut_data = {
            "name": "Date Filter Test",
            "price": 20000.0,
            "date": date.today().isoformat(),
        }
        client.post("/haircuts/create", json=haircut_data)

        response = client.get(f"/haircuts/history/date/{date.today().isoformat()}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_delete_haircuts_by_date(self):
        """Test deleting all haircuts for a specific date."""
        haircut_data = {
            "name": "Delete Test Cut",
            "price": 15000.0,
            "date": date.today().isoformat(),
        }
        client.post("/haircuts/create", json=haircut_data)

        before_response = client.get("/haircuts/history/today")
        before_count = before_response.json()["count"]

        response = client.delete(f"/haircuts/history/date/{date.today().isoformat()}")
        assert response.status_code == 200
        assert "Deleted" in response.json()["message"]

        after_response = client.get("/haircuts/history/today")
        assert after_response.json()["count"] < before_count

    def test_delete_haircuts_by_date_empty(self):
        """Test deleting haircuts for a date with no haircuts."""
        response = client.delete(f"/haircuts/history/date/{date.today().isoformat()}")
        assert response.status_code == 200
        assert "0" in response.json()["message"]
