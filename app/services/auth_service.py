from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.repositories.user_repository import UserRepository
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


class AuthService:

    @staticmethod
    def register(
        db: Session,
        user_data: UserCreate
    ) -> User:

        existing_user = UserRepository.get_by_email(
            db,
            user_data.email
        )

        if existing_user:
            raise ValueError(
                "Email already registered"
            )

        user = User(
            email=user_data.email,
            password_hash=hash_password(
                user_data.password
            ),
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )

        return UserRepository.create(
            db,
            user
        )

    @staticmethod
    def login(
        db: Session,
        email: str,
        password: str
    ) -> str:

        user = UserRepository.get_by_email(
            db,
            email
        )

        if not user:
            raise ValueError(
                "Invalid credentials"
            )

        if not verify_password(
            password,
            user.password_hash
        ):
            raise ValueError(
                "Invalid credentials"
            )

        return create_access_token(
            subject=str(user.id),
            email=user.email
        )