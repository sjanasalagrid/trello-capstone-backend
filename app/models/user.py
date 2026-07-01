import uuid

from sqlalchemy import String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    owned_boards = relationship(
        "Board",
        back_populates="owner"
    )

    board_memberships = relationship(
        "BoardMember",
        back_populates="user"
    )

    created_tickets = relationship(
        "Ticket",
        foreign_keys="Ticket.created_by_id",
        back_populates="creator"
    )

    assigned_tickets = relationship(
        "Ticket",
        foreign_keys="Ticket.assigned_to_id",
        back_populates="assignee"
    )

    sent_invitations = relationship(
        "Invitation",
        foreign_keys="Invitation.invited_by_id",
        back_populates="invited_by",
    )

    received_invitations = relationship(
        "Invitation",
        foreign_keys="Invitation.invited_user_id",
        back_populates="invited_user",
    )