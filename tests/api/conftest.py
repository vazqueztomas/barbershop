import os
import pytest
import sqlite3

from fastapi.testclient import TestClient
from barbershop.app import app
from barbershop.repositories import UserRepository
from barbershop.models import UserCreate


@pytest.fixture(scope="function")
def test_db():
    conn = sqlite3.connect("test_auth.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE NOT NULL,
            full_name TEXT,
            hashed_password TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            password_reset_token TEXT,
            password_reset_expires TIMESTAMP
        )
    """)
    conn.commit()
    
    yield conn
    
    cursor.execute("DROP TABLE IF EXISTS users")
    conn.commit()
    cursor.close()
    conn.close()
    if os.path.exists("test_auth.db"):
        os.remove("test_auth.db")


@pytest.fixture(scope="function")
def client(test_db):
    def override_get_db():
        yield test_db
    
    from barbershop.repositories import base
    app.dependency_overrides[base.get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_create():
    return UserCreate(
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        password="testpassword123"
    )


@pytest.fixture
def test_user_create_alt():
    return UserCreate(
        email="alt@example.com",
        username="altuser",
        full_name="Alt User",
        password="altpassword456"
    )


@pytest.fixture
def registered_user(test_db, test_user_create):
    repo = UserRepository(test_db)
    return repo.create_user(test_user_create)


@pytest.fixture
def auth_headers(client, test_db, test_user_create):
    repo = UserRepository(test_db)
    repo.create_user(test_user_create)
    
    response = client.post("/auth/login", json={
        "username": test_user_create.username,
        "password": test_user_create.password
    })
    if response.status_code == 200:
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    return {}
