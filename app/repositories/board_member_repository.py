from uuid import UUID

from sqlalchemy.orm import Session

from app.models.board_member import BoardMember


class BoardMemberRepository:

    @staticmethod
    def is_member(
        db: Session,
        board_id: UUID,
        user_id: UUID,
    ) -> bool:
        return (
            db.query(BoardMember)
            .filter(
                BoardMember.board_id == board_id,
                BoardMember.user_id == user_id,
            )
            .first()
            is not None
        )

    @staticmethod
    def create(
        db: Session,
        board_member: BoardMember
    ) -> BoardMember:
        db.add(board_member)
        db.commit()
        db.refresh(board_member)

        return board_member

    @staticmethod
    def get_member(
        db: Session,
        board_id: UUID,
        user_id: UUID
    ) -> BoardMember | None:
        return (
            db.query(BoardMember)
            .filter(
                BoardMember.board_id == board_id,
                BoardMember.user_id == user_id
            )
            .first()
        )

    @staticmethod
    def get_members_by_board(
        db: Session,
        board_id: UUID
    ) -> list[BoardMember]:
        return (
            db.query(BoardMember)
            .filter(
                BoardMember.board_id == board_id
            )
            .all()
        )

    @staticmethod
    def delete(
        db: Session,
        board_member: BoardMember
    ) -> None:
        db.delete(board_member)
        db.commit()