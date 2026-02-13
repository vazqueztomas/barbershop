import pytest
from barbershop.models import UserCreate


class TestAuthEndpoints:
    """Integration tests for auth endpoints."""

    def test_register_success(self, client, test_user_create):
        response = client.post("/auth/register", json=test_user_create.model_dump())

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user_create.email
        assert data["username"] == test_user_create.username
        assert data["full_name"] == test_user_create.full_name
        assert "id" in data

    def test_register_duplicate_username(self, client, registered_user, test_user_create_alt):
        response = client.post("/auth/register", json={
            "email": "different@example.com",
            "username": registered_user.username,
            "password": "password123"
        })

        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_register_duplicate_email(self, client, registered_user, test_user_create_alt):
        response = client.post("/auth/register", json={
            "email": registered_user.email,
            "username": "different_user",
            "password": "password123"
        })

        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_login_success(self, client, registered_user, test_user_create):
        response = client.post("/auth/login", json={
            "username": test_user_create.username,
            "password": test_user_create.password
        })

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["username"] == test_user_create.username

    def test_login_wrong_password(self, client, registered_user):
        response = client.post("/auth/login", json={
            "username": registered_user.username,
            "password": "wrongpassword"
        })

        assert response.status_code == 401
        assert "Incorrect" in response.json()["detail"]

    def test_login_nonexistent_user(self, client):
        response = client.post("/auth/login", json={
            "username": "nonexistent",
            "password": "password"
        })

        assert response.status_code == 401

    def test_token_oauth2_success(self, client, registered_user, test_user_create):
        response = client.post("/auth/token", data={
            "username": test_user_create.username,
            "password": test_user_create.password
        })

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_token_oauth2_wrong_credentials(self, client, registered_user):
        response = client.post("/auth/token", data={
            "username": registered_user.username,
            "password": "wrongpassword"
        })

        assert response.status_code == 401

    def test_get_me_unauthorized(self, client):
        response = client.get("/auth/me")
        assert response.status_code == 401

    def test_get_me_authorized(self, client, auth_headers):
        response = client.get("/auth/me", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "email" in data
        assert "username" in data

    def test_password_reset_request_existing_email(self, client, registered_user):
        response = client.post("/auth/password-reset", json={
            "email": registered_user.email
        })

        assert response.status_code == 200
        data = response.json()
        assert "reset_token" in data

    def test_password_reset_request_nonexistent_email(self, client):
        response = client.post("/auth/password-reset", json={
            "email": "nonexistent@example.com"
        })

        assert response.status_code == 200
        data = response.json()
        assert "If the email exists" in data["message"]

    def test_password_reset_confirm_success(self, client, test_user_create, test_db):
        client.post("/auth/register", json=test_user_create.model_dump())

        reset_response = client.post("/auth/password-reset", json={
            "email": test_user_create.email
        })
        token = reset_response.json()["reset_token"]

        new_password = "newpassword123"
        response = client.post("/auth/password-reset/confirm", json={
            "token": token,
            "new_password": new_password
        })

        assert response.status_code == 200
        assert response.json()["message"] == "Password reset successfully"

        login_response = client.post("/auth/login", json={
            "username": test_user_create.username,
            "password": new_password
        })
        assert login_response.status_code == 200

    def test_password_reset_confirm_invalid_token(self, client):
        response = client.post("/auth/password-reset/confirm", json={
            "token": "invalid_token",
            "new_password": "newpassword"
        })

        assert response.status_code == 400
        assert "Invalid" in response.json()["detail"]

    def test_invalid_token_returns_401(self, client):
        response = client.get(
            "/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )

        assert response.status_code == 401

    def test_register_with_minimal_fields(self, client):
        response = client.post("/auth/register", json={
            "email": "minimal@example.com",
            "username": "minimaluser",
            "password": "password123"
        })

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "minimal@example.com"
        assert data["username"] == "minimaluser"
        assert data["full_name"] is None

    def test_register_invalid_email(self, client):
        response = client.post("/auth/register", json={
            "email": "invalid-email",
            "username": "user",
            "password": "password123"
        })

        assert response.status_code == 422
