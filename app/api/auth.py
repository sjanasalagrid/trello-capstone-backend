from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserLogin
)

from app.schemas.auth import (
    TokenResponse
)

from app.services.auth_service import (
    AuthService
)

from app.dependencies.auth import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    try:
        return AuthService.register(
            db,
            user_data
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):

    try:
        token = AuthService.login(
            db,
            user_data.email,
            user_data.password
        )

        return {
            "access_token": token
        }

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )

@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user