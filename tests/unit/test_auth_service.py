import uuid
from unittest.mock import MagicMock, patch

import pytest

from app.models.user import User
from app.schemas.user import UserCreate
from app.services.auth_service import AuthService


def test_register_success():

    db = MagicMock()

    user_data = UserCreate(
        email="owner@test.com",
        password="Password123",
        first_name="Owner",
        last_name="User",
    )

    with (
        patch(
            "app.services.auth_service.UserRepository.get_by_email",
            return_value=None,
        ),
        patch(
            "app.services.auth_service.hash_password",
            return_value="hashed_password",
        ),
        patch(
            "app.services.auth_service.UserRepository.create",
        ) as mock_create,
    ):

        created_user = User(
            id=uuid.uuid4(),
            email=user_data.email,
            password_hash="hashed_password",
            first_name=user_data.first_name,
            last_name=user_data.last_name,
        )

        mock_create.return_value = created_user

        result = AuthService.register(db, user_data)

        assert result.email == user_data.email
        mock_create.assert_called_once()


def test_register_duplicate_email():

    db = MagicMock()

    user_data = UserCreate(
        email="owner@test.com",
        password="Password123",
        first_name="Owner",
        last_name="User",
    )

    existing_user = User(email=user_data.email)

    with patch(
        "app.services.auth_service.UserRepository.get_by_email",
        return_value=existing_user,
    ):

        with pytest.raises(ValueError, match="Email already registered"):
            AuthService.register(db, user_data)


def test_login_success():

    db = MagicMock()

    user = User(
        id=uuid.uuid4(),
        email="owner@test.com",
        password_hash="hashed_password",
        first_name="Owner",
        last_name="User",
    )

    with (
        patch(
            "app.services.auth_service.UserRepository.get_by_email",
            return_value=user,
        ),
        patch(
            "app.services.auth_service.verify_password",
            return_value=True,
        ),
        patch(
            "app.services.auth_service.create_access_token",
            return_value="jwt_token",
        ),
    ):

        token = AuthService.login(
            db,
            "owner@test.com",
            "Password123",
        )

        assert token == "jwt_token"


def test_login_invalid_email():

    db = MagicMock()

    with patch(
        "app.services.auth_service.UserRepository.get_by_email",
        return_value=None,
    ):

        with pytest.raises(ValueError, match="Invalid credentials"):
            AuthService.login(
                db,
                "owner@test.com",
                "Password123",
            )


def test_login_invalid_password():

    db = MagicMock()

    user = User(
        id=uuid.uuid4(),
        email="owner@test.com",
        password_hash="hashed_password",
        first_name="Owner",
        last_name="User",
    )

    with (
        patch(
            "app.services.auth_service.UserRepository.get_by_email",
            return_value=user,
        ),
        patch(
            "app.services.auth_service.verify_password",
            return_value=False,
        ),
    ):

        with pytest.raises(ValueError, match="Invalid credentials"):
            AuthService.login(
                db,
                "owner@test.com",
                "WrongPassword123",
            )