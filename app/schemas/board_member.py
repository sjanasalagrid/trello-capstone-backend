from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.enums.roles import BoardRole


class BoardMemberResponse(BaseModel):
    id: UUID

    user_id: UUID
    board_id: UUID

    role: BoardRole

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )