from datetime import datetime
from uuid import UUID
from app.enums.ticket_status import TicketStatus
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class TicketCreate(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        max_length=5000,
    )


class TicketUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        max_length=5000,
    )


class TicketAssign(BaseModel):
    email: EmailStr


class TicketMove(BaseModel):
    section_id: UUID

class TicketStatusUpdate(BaseModel):
    status: TicketStatus


class TicketResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID

    section_id: UUID

    title: str

    description: str | None

    created_by_id: UUID

    assigned_to_id: UUID | None

    status: TicketStatus

    created_at: datetime

    updated_at: datetime

