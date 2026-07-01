from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.board_member import BoardMember
from app.repositories.board_member_repository import BoardMemberRepository
from app.repositories.board_repository import BoardRepository


class BoardMemberService:

    @staticmethod
    def get_board_members(
        db: Session,
        board_id: UUID,
        current_user_id: UUID,
    ) -> list[BoardMember]:

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
            board_id=board_id,
            user_id=current_user_id,
        )

        if member is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this board.",
            )

        return BoardMemberRepository.get_members_by_board(
            db,
            board_id,
        )
    
    @staticmethod
    def remove_member(
        db: Session,
        board_id: UUID,
        user_id: UUID,
        current_user_id: UUID,
    ) -> None:

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
                detail="Only the board owner can remove members.",
            )

        if user_id == board.owner_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Owner cannot remove themselves.",
            )

        member = BoardMemberRepository.get_member(
            db=db,
            board_id=board_id,
            user_id=user_id,
        )

        if member is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Member not found.",
            )

        BoardMemberRepository.delete(
            db,
            member,
        )