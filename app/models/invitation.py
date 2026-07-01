import uuid

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.enums.invitation_status import InvitationStatus


class Invitation(Base):
    __tablename__ = "invitations"


    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    board_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("boards.id"),
        nullable=False,
    )

    invited_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    invited_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    token: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
    )

    status: Mapped[InvitationStatus] = mapped_column(
        Enum(InvitationStatus),
        nullable=False,
        default=InvitationStatus.PENDING,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    accepted_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    board = relationship(
        "Board",
        back_populates="invitations",
    )

    invited_by = relationship(
        "User",
        foreign_keys=[invited_by_id],
        back_populates="sent_invitations",
    )

    invited_user = relationship(
        "User",
        foreign_keys=[invited_user_id],
        back_populates="received_invitations",
    )