from uuid import UUID

from sqlalchemy.orm import Session

from app.models.board import Board
from app.models.board_member import BoardMember

class BoardRepository:

    @staticmethod
    def create(
        db: Session,
        board: Board
    ) -> Board:
        db.add(board)
        db.commit()
        db.refresh(board)

        return board

    @staticmethod
    def get_by_id(
        db: Session,
        board_id: UUID
    ) -> Board | None:
        return (
            db.query(Board)
            .filter(Board.id == board_id)
            .first()
        )

    @staticmethod
    def get_by_user(
        db: Session,
        user_id: UUID,
    ) -> list[Board]:

        return (
            db.query(Board)
            .join(
                BoardMember,
                Board.id == BoardMember.board_id
            )
            .filter(
                BoardMember.user_id == user_id
            )
            .all()
        )

    @staticmethod
    def is_owner(
        board: Board,
        user_id: UUID,
    ) -> bool:
        return board.owner_id == user_id