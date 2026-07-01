from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from app.enums.invitation_status import InvitationStatus


class InvitationCreate(BaseModel):
    email: EmailStr


class InvitationResponse(BaseModel):
    id: UUID
    board_id: UUID

    invited_by_id: UUID
    invited_user_id: UUID

    token: UUID

    status: InvitationStatus

    created_at: datetime
    accepted_at: datetime | None

    model_config = ConfigDict(
        from_attributes=True
    )


class InvitationListResponse(BaseModel):
    id: UUID

    board_id: UUID
    board_name: str

    owner_email: EmailStr

    status: InvitationStatus

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )