import uuid
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.enums.invitation_status import InvitationStatus
from app.models.board import Board
from app.models.board_member import BoardMember
from app.models.invitation import Invitation
from app.models.user import User
from app.services.invitation_service import InvitationService


def test_invite_user_success():

    db = MagicMock()

    owner_id = uuid.uuid4()
    member_id = uuid.uuid4()
    board_id = uuid.uuid4()

    board = Board(
        id=board_id,
        owner_id=owner_id,
        name="Board",
    )

    user = User(
        id=member_id,
        email="member@test.com",
    )

    invitation = Invitation(
        id=uuid.uuid4(),
        board_id=board_id,
        invited_by_id=owner_id,
        invited_user_id=member_id,
        status=InvitationStatus.PENDING,
    )

    with (
        patch(
            "app.services.invitation_service.BoardRepository.get_by_id",
            return_value=board,
        ),
        patch(
            "app.services.invitation_service.UserRepository.get_by_email",
            return_value=user,
        ),
        patch(
            "app.services.invitation_service.BoardMemberRepository.get_member",
            return_value=None,
        ),
        patch(
            "app.services.invitation_service.InvitationRepository.pending_invitation_exists",
            return_value=False,
        ),
        patch(
            "app.services.invitation_service.InvitationRepository.create",
            return_value=invitation,
        ),
    ):

        result = InvitationService.invite_user(
            db,
            board_id,
            "member@test.com",
            owner_id,
        )

        assert result.status == InvitationStatus.PENDING


def test_invite_user_duplicate_pending():

    db = MagicMock()

    owner_id = uuid.uuid4()
    member_id = uuid.uuid4()
    board_id = uuid.uuid4()

    board = Board(id=board_id, owner_id=owner_id)

    user = User(
        id=member_id,
        email="member@test.com",
    )

    with (
        patch(
            "app.services.invitation_service.BoardRepository.get_by_id",
            return_value=board,
        ),
        patch(
            "app.services.invitation_service.UserRepository.get_by_email",
            return_value=user,
        ),
        patch(
            "app.services.invitation_service.BoardMemberRepository.get_member",
            return_value=None,
        ),
        patch(
            "app.services.invitation_service.InvitationRepository.pending_invitation_exists",
            return_value=True,
        ),
    ):

        with pytest.raises(HTTPException) as exc:
            InvitationService.invite_user(
                db,
                board_id,
                "member@test.com",
                owner_id,
            )

        assert exc.value.status_code == 400


def test_accept_invitation_success():

    db = MagicMock()

    user_id = uuid.uuid4()
    board_id = uuid.uuid4()

    invitation = Invitation(
        id=uuid.uuid4(),
        board_id=board_id,
        invited_user_id=user_id,
        status=InvitationStatus.PENDING,
    )

    with (
        patch(
            "app.services.invitation_service.InvitationRepository.get_pending_by_token",
            return_value=invitation,
        ),
        patch(
            "app.services.invitation_service.BoardMemberRepository.get_member",
            return_value=None,
        ),
        patch(
            "app.services.invitation_service.BoardMemberRepository.create",
        ),
        patch(
            "app.services.invitation_service.InvitationRepository.update",
        ),
    ):

        result = InvitationService.accept_invitation(
            db,
            uuid.uuid4(),
            user_id,
        )

        assert result.status == InvitationStatus.ACCEPTED


def test_accept_invitation_wrong_user():

    db = MagicMock()

    invitation = Invitation(
        id=uuid.uuid4(),
        board_id=uuid.uuid4(),
        invited_user_id=uuid.uuid4(),
        status=InvitationStatus.PENDING,
    )

    with patch(
        "app.services.invitation_service.InvitationRepository.get_pending_by_token",
        return_value=invitation,
    ):

        with pytest.raises(HTTPException) as exc:
            InvitationService.accept_invitation(
                db,
                uuid.uuid4(),
                uuid.uuid4(),
            )

        assert exc.value.status_code == 403


def test_revoke_invitation_success():

    db = MagicMock()

    owner_id = uuid.uuid4()
    board_id = uuid.uuid4()

    board = Board(
        id=board_id,
        owner_id=owner_id,
    )

    invitation = Invitation(
        id=uuid.uuid4(),
        board_id=board_id,
        status=InvitationStatus.PENDING,
    )

    with (
        patch(
            "app.services.invitation_service.BoardRepository.get_by_id",
            return_value=board,
        ),
        patch(
            "app.services.invitation_service.InvitationRepository.get_by_id",
            return_value=invitation,
        ),
        patch(
            "app.services.invitation_service.InvitationRepository.update",
        ),
    ):

        result = InvitationService.revoke_invitation(
            db,
            board_id,
            invitation.id,
            owner_id,
        )

        assert result.status == InvitationStatus.REVOKED