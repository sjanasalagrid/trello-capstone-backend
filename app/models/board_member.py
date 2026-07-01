import uuid

from sqlalchemy import DateTime, ForeignKey, Enum, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint

from app.db.database import Base
from app.enums.roles import BoardRole


class BoardMember(Base):
    __tablename__ = "board_members"
    __table_args__ = (
        UniqueConstraint(
            "board_id",
            "user_id",
            name="uq_board_user"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    board_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("boards.id"),
        nullable=False
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    role: Mapped[BoardRole] = mapped_column(
        Enum(BoardRole),
        nullable=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    board = relationship(
        "Board",
        back_populates="members"
    )

    user = relationship(
        "User",
        back_populates="board_memberships"
    )