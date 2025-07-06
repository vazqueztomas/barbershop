from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from barbershop.main import app
from barbershop.models import Haircut

client = TestClient(app)


def test_get_haircuts() -> None:
    response = client.get("/haircuts")
    assert response.status_code == 200


def test_get_haircut(haircut_id: UUID, haircut: Haircut) -> None:
    response = client.post("/haircuts/create", json=haircut.model_dump(mode="json"))
    assert response.status_code == 200
    created = response.json()
    created_id = created["id"]
    assert created_id == str(haircut_id)

    response = client.get(f"/haircuts/{created_id}")
    assert response.status_code == 200
    assert response.json() == haircut.model_dump(mode="json")


def test_get_haircut_does_not_exist() -> None:
    response = client.get(f"/haircuts/{uuid4()}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Haircut not found"}


def test_delete_haircut(haircut: Haircut, haircut_id: UUID) -> None:
    response = client.post("/haircuts/create", json=haircut.model_dump(mode="json"))
    assert response.status_code == 200
    created = response.json()
    assert created["id"] == str(haircut_id)

    response = client.delete(f"/haircuts/{haircut_id}")
    assert response.status_code == 200
    assert response.json() == f"Deleted haircut with ID {haircut_id}"

    response = client.get("/haircuts")
    assert response.status_code == 200
    assert haircut_id not in [h["id"] for h in response.json()]


def test_delete_haircut_does_not_exist() -> None:
    response = client.delete(f"/haircuts/{uuid4()}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Haircut not found"}


def test_update_haircut(haircut: Haircut, haircut_id: UUID) -> None:
    response = client.post("/haircuts/create", json=haircut.model_dump(mode="json"))
    assert response.status_code == 200
    created = response.json()
    assert created["id"] == str(haircut_id)

    updated_haircut = haircut.model_copy(
        update={"id": str(uuid4()), "name": "Updated Haircut", "price": 25.0}
    )
    response = client.put(
        "/haircuts/update", json=updated_haircut.model_dump(mode="json")
    )
    assert response.status_code == 200
    assert response.json() == updated_haircut.model_dump(mode="json")
