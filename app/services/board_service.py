from sqlalchemy.orm import Session

from app.enums.roles import BoardRole
from app.models.board import Board
from app.models.board_member import BoardMember
from app.models.user import User
from app.repositories.board_repository import BoardRepository
from app.schemas.board import BoardCreate


class BoardService:

    @staticmethod
    def create_board(
        db: Session,
        board_data: BoardCreate,
        owner: User,
    ) -> Board:

        board = Board(
            name=board_data.name,
            description=board_data.description,
            owner_id=owner.id,
        )

        db.add(board)
        db.flush()

        membership = BoardMember(
            board_id=board.id,
            user_id=owner.id,
            role=BoardRole.OWNER,
        )

        db.add(membership)

        db.commit()

        db.refresh(board)

        return board

    @staticmethod
    def get_user_boards(
        db: Session,
        owner: User,
    ) -> list[Board]:

        return BoardRepository.get_by_user(
            db,
            owner.id,
        )