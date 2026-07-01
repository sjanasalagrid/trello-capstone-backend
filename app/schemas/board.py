from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BoardCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=255
    )

    description: str | None = Field(
        default=None,
        max_length=1000
    )


class BoardUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    description: str | None = Field(
        default=None,
        max_length=1000
    )


class BoardResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )