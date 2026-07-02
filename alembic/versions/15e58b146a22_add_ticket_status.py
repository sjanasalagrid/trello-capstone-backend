"""add ticket status

Revision ID: 15e58b146a22
Revises: f3cee37c9ad4
Create Date: 2026-07-02 07:45:31.758155

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15e58b146a22'
down_revision: Union[str, Sequence[str], None] = 'f3cee37c9ad4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    ticket_status = sa.Enum(
        "OPEN",
        "IN_PROGRESS",
        "DONE",
        "CLOSED",
        name="ticketstatus",
    )

    ticket_status.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "tickets",
        sa.Column(
            "status",
            ticket_status,
            nullable=False,
            server_default="OPEN",
        ),
    )

    op.alter_column(
        "tickets",
        "status",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "tickets",
        "status",
    )

    sa.Enum(
        "OPEN",
        "IN_PROGRESS",
        "DONE",
        "CLOSED",
        name="ticketstatus",
    ).drop(
        op.get_bind(),
        checkfirst=True,
    )