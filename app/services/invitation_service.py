from uuid import UUID
from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.enums.roles import BoardRole
from app.enums.invitation_status import InvitationStatus
from app.models.invitation import Invitation
from app.models.board_member import BoardMember
from app.repositories.board_member_repository import BoardMemberRepository
from app.repositories.board_repository import BoardRepository
from app.repositories.invitation_repository import InvitationRepository
from app.repositories.user_repository import UserRepository


class InvitationService:

    @staticmethod
    def invite_user(
        db: Session,
        board_id: UUID,
        email: str,
        current_user_id: UUID
    ) -> Invitation:

        # Check if board exists
        board = BoardRepository.get_by_id(
            db,
            board_id
        )

        if not board:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Board not found."
            )

        # Only owner can invite
        if board.owner_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the board owner can invite users."
            )

        # Find invited user
        user = UserRepository.get_by_email(
            db,
            email
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        # Prevent self invitation
        if user.id == current_user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot invite yourself."
            )

        # Already a member?
        member = BoardMemberRepository.get_member(
            db,
            board_id,
            user.id
        )

        if member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already a board member."
            )

        # Pending invitation already exists?
        if InvitationRepository.pending_invitation_exists(
            db,
            board_id,
            user.id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already has a pending invitation."
            )

        # Create invitation
        invitation = Invitation(
            board_id=board.id,
            invited_by_id=current_user_id,
            invited_user_id=user.id,
            status=InvitationStatus.PENDING
        )

        return InvitationRepository.create(
            db,
            invitation
        )
    @staticmethod
    def get_user_invitations(
        db: Session,
        current_user_id: UUID,
        status: InvitationStatus | None = None,
    ):

        return InvitationRepository.get_user_invitations(
            db=db,
            user_id=current_user_id,
            status=status,
        )
    @staticmethod
    def get_board_invitations(
        db: Session,
        board_id: UUID,
        current_user_id: UUID,
    ):

        board = BoardRepository.get_by_id(
            db,
            board_id,
        )

        if board is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Board not found.",
            )

        if board.owner_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the board owner can view sent invitations.",
            )

        return InvitationRepository.get_board_invitations(
            db,
            board_id,
        )
    @staticmethod
    def accept_invitation(
        db: Session,
        token: UUID,
        current_user_id: UUID,
    ):

        invitation = InvitationRepository.get_pending_by_token(
            db,
            token,
        )

        if invitation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invitation not found.",
            )

        if invitation.invited_user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This invitation does not belong to you.",
            )

        existing_member = BoardMemberRepository.get_member(
            db,
            invitation.board_id,
            current_user_id,
        )

        if existing_member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are already a board member.",
            )

        board_member = BoardMember(
            board_id=invitation.board_id,
            user_id=current_user_id,
            role=BoardRole.MEMBER,
        )

        BoardMemberRepository.create(
            db,
            board_member,
        )

        invitation.status = InvitationStatus.ACCEPTED
        invitation.accepted_at = datetime.now(timezone.utc)

        InvitationRepository.update(
            db,
            invitation,
        )

        return invitation
    @staticmethod
    def revoke_invitation(
        db: Session,
        board_id: UUID,
        invitation_id: UUID,
        current_user_id: UUID,
    ) -> Invitation:

        board = BoardRepository.get_by_id(
            db,
            board_id,
        )

        if board is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Board not found.",
            )

        if board.owner_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the board owner can revoke invitations.",
            )

        invitation = InvitationRepository.get_by_id(
            db,
            invitation_id,
        )

        if invitation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invitation not found.",
            )

        if invitation.board_id != board.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invitation does not belong to this board.",
            )

        if invitation.status == InvitationStatus.ACCEPTED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Accepted invitations cannot be revoked.",
            )

        if invitation.status == InvitationStatus.REVOKED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invitation is already revoked.",
            )

        invitation.status = InvitationStatus.REVOKED

        InvitationRepository.update(
            db,
            invitation,
        )

        return invitation