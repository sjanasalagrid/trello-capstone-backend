from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SectionCreate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )


class SectionUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )


class SectionResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID
    board_id: UUID

    name: str
    description: str | None

    position: int

    created_at: datetime
    updated_at: datetime