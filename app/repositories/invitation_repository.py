from uuid import UUID

from sqlalchemy.orm import Session

from app.enums.invitation_status import InvitationStatus
from app.models.invitation import Invitation


class InvitationRepository:

    @staticmethod
    def create(
        db: Session,
        invitation: Invitation
    ) -> Invitation:
        db.add(invitation)
        db.commit()
        db.refresh(invitation)

        return invitation

    @staticmethod
    def get_by_id(
        db: Session,
        invitation_id: UUID
    ) -> Invitation | None:
        return (
            db.query(Invitation)
            .filter(Invitation.id == invitation_id)
            .first()
        )

    @staticmethod
    def get_by_token(
        db: Session,
        token: UUID
    ) -> Invitation | None:
        return (
            db.query(Invitation)
            .filter(Invitation.token == token)
            .first()
        )

    @staticmethod
    def get_user_invitations(
        db: Session,
        user_id: UUID,
        status: InvitationStatus | None = None,
    ) -> list[Invitation]:

        query = (
            db.query(Invitation)
            .filter(
                Invitation.invited_user_id == user_id
            )
        )

        if status:
            query = query.filter(
                Invitation.status == status
            )

        return (
            query.order_by(
                Invitation.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_board_invitations(
        db: Session,
        board_id: UUID
    ) -> list[Invitation]:
        return (
            db.query(Invitation)
            .filter(
                Invitation.board_id == board_id
            )
            .order_by(
                Invitation.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def pending_invitation_exists(
        db: Session,
        board_id: UUID,
        invited_user_id: UUID
    ) -> bool:
        invitation = (
            db.query(Invitation)
            .filter(
                Invitation.board_id == board_id,
                Invitation.invited_user_id == invited_user_id,
                Invitation.status == InvitationStatus.PENDING
            )
            .first()
        )

        return invitation is not None

    @staticmethod
    def get_pending_by_token(
        db: Session,
        token: UUID
    ) -> Invitation | None:
        return (
            db.query(Invitation)
        .filter(
            Invitation.token == token,
            Invitation.status == InvitationStatus.PENDING
        )
        .first()
    )

    @staticmethod
    def update(
        db: Session,
        invitation: Invitation
    ) -> Invitation:
        db.commit()
        db.refresh(invitation)

        return invitation
