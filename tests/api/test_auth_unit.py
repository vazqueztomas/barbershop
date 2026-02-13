import pytest
from barbershop.repositories import UserRepository
from barbershop.models import UserCreate


class TestUserRepository:
    """Unit tests for UserRepository."""

    def test_create_user(self, test_db, test_user_create):
        repo = UserRepository(test_db)
        user = repo.create_user(test_user_create)

        assert user is not None
        assert user.email == test_user_create.email
        assert user.username == test_user_create.username
        assert user.full_name == test_user_create.full_name
        assert user.is_active is True
        assert user.hashed_password != test_user_create.password

    def test_get_user_by_username(self, test_db, registered_user):
        repo = UserRepository(test_db)
        user = repo.get_user_by_username(registered_user.username)

        assert user is not None
        assert user.username == registered_user.username
        assert user.email == registered_user.email

    def test_get_user_by_username_not_found(self, test_db):
        repo = UserRepository(test_db)
        user = repo.get_user_by_username("nonexistent")
        assert user is None

    def test_get_user_by_email(self, test_db, registered_user):
        repo = UserRepository(test_db)
        user = repo.get_user_by_email(registered_user.email)

        assert user is not None
        assert user.email == registered_user.email

    def test_get_user_by_email_not_found(self, test_db):
        repo = UserRepository(test_db)
        user = repo.get_user_by_email("nonexistent@example.com")
        assert user is None

    def test_authenticate_user_success(self, test_db, test_user_create):
        repo = UserRepository(test_db)
        repo.create_user(test_user_create)

        user = repo.authenticate_user(
            test_user_create.username,
            test_user_create.password
        )

        assert user is not None
        assert user.username == test_user_create.username

    def test_authenticate_user_wrong_password(self, test_db, test_user_create):
        repo = UserRepository(test_db)
        repo.create_user(test_user_create)

        user = repo.authenticate_user(
            test_user_create.username,
            "wrongpassword"
        )

        assert user is None

    def test_authenticate_user_not_found(self, test_db):
        repo = UserRepository(test_db)
        user = repo.authenticate_user("nonexistent", "password")
        assert user is None

    def test_create_duplicate_username_fails(self, test_db, test_user_create):
        repo = UserRepository(test_db)
        repo.create_user(test_user_create)

        with pytest.raises(Exception):
            repo.create_user(test_user_create)

    def test_create_duplicate_email_fails(self, test_db, test_user_create, test_user_create_alt):
        repo = UserRepository(test_db)
        repo.create_user(test_user_create)

        duplicate_email = UserCreate(
            email=test_user_create.email,
            username="different_user",
            password="password123"
        )
        with pytest.raises(Exception):
            repo.create_user(duplicate_email)

    def test_password_hash_is_different_from_plain(self, test_db, test_user_create):
        repo = UserRepository(test_db)
        user = repo.create_user(test_user_create)

        assert user.hashed_password != test_user_create.password

    def test_password_verification(self, test_db, test_user_create):
        repo = UserRepository(test_db)
        repo.create_user(test_user_create)

        user = repo.get_user_by_username(test_user_create.username)
        assert repo.verify_password(
            test_user_create.password,
            user.hashed_password
        ) is True

    def test_password_reset_token_creation(self, test_db, registered_user):
        repo = UserRepository(test_db)
        token = repo.create_password_reset_token(registered_user.email)

        assert token is not None
        assert len(token) > 20

    def test_password_reset_token_for_nonexistent_email(self, test_db):
        repo = UserRepository(test_db)
        token = repo.create_password_reset_token("nonexistent@example.com")
        assert token is None

    def test_password_reset_success(self, test_db, test_user_create):
        repo = UserRepository(test_db)
        repo.create_user(test_user_create)

        token = repo.create_password_reset_token(test_user_create.email)
        new_password = "newpassword123"
        result = repo.reset_password(token, new_password)

        assert result is True

        user = repo.authenticate_user(
            test_user_create.username,
            new_password
        )
        assert user is not None

    def test_password_reset_invalid_token(self, test_db):
        repo = UserRepository(test_db)
        result = repo.reset_password("invalid_token", "newpassword")
        assert result is False

    def test_create_access_token(self, test_db, registered_user):
        repo = UserRepository(test_db)
        token = repo.create_access_token({"sub": registered_user.username})

        assert token is not None
        assert len(token) > 0

    def test_get_user_by_id(self, test_db, registered_user):
        repo = UserRepository(test_db)
        user = repo.get_user_by_id(registered_user.id)

        assert user is not None
        assert user.id == registered_user.id
