from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.repositories.board_repository import BoardRepository
from app.repositories.board_member_repository import BoardMemberRepository
from app.schemas.board import (
    BoardCreate,
    BoardResponse,
)
from app.services.board_service import BoardService
from app.schemas.invitation import (
    InvitationCreate,
    InvitationResponse,
)

from app.schemas.board_member import BoardMemberResponse
from app.services.board_member_service import BoardMemberService

from app.services.invitation_service import InvitationService

router = APIRouter(
    prefix="/boards",
    tags=["Boards"],
)


@router.post(
    "",
    response_model=BoardResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_board(
    board_data: BoardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return BoardService.create_board(
        db=db,
        board_data=board_data,
        owner=current_user,
    )

@router.post(
    "/{board_id}/invite",
    response_model=InvitationResponse,
    status_code=status.HTTP_201_CREATED,
)
def invite_user(
    board_id: UUID,
    invitation_data: InvitationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return InvitationService.invite_user(
        db=db,
        board_id=board_id,
        email=invitation_data.email,
        current_user_id=current_user.id,
    )

@router.get(
    "/{board_id}/sent_invitations",
    response_model=list[InvitationResponse],
)
def get_sent_invitations(
    board_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return InvitationService.get_board_invitations(
        db=db,
        board_id=board_id,
        current_user_id=current_user.id,
    )

@router.get(
    "",
    response_model=list[BoardResponse],
)
def get_my_boards(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return BoardService.get_user_boards(
        db,
        current_user,
    )


@router.get(
    "/{board_id}",
    response_model=BoardResponse,
)
def get_board(
    board_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
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

    member = BoardMemberRepository.get_member(
    db=db,
    board_id=board.id,
    user_id=current_user.id,
)

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this board.",
        )

    return board

@router.delete(
    "/{board_id}/sent_invitations/{invitation_id}",
    response_model=InvitationResponse,
)
def revoke_invitation(
    board_id: UUID,
    invitation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return InvitationService.revoke_invitation(
        db=db,
        board_id=board_id,
        invitation_id=invitation_id,
        current_user_id=current_user.id,
    )

@router.get(
    "/{board_id}/members",
    response_model=list[BoardMemberResponse],
)
def get_board_members(
    board_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return BoardMemberService.get_board_members(
        db=db,
        board_id=board_id,
        current_user_id=current_user.id,
    )

@router.delete(
    "/{board_id}/members/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_member(
    board_id: UUID,
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return BoardMemberService.remove_member(
        db=db,
        board_id=board_id,
        user_id=user_id,
        current_user_id=current_user.id,
    )