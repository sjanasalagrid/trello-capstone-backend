import re

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)
from uuid import UUID


class UserCreate(BaseModel):
    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128
    )

    first_name: str = Field(
        min_length=1,
        max_length=100
    )

    last_name: str = Field(
        min_length=1,
        max_length=100
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):

        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(r"[a-z]", value):
            raise ValueError(
                "Password must contain at least one lowercase letter."
            )

        if not re.search(r"\d", value):
            raise ValueError(
                "Password must contain at least one digit."
            )

        return value


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str