from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.section import Section


class SectionRepository:

    @staticmethod
    def create(
        db: Session,
        section: Section,
    ) -> Section:
        db.add(section)
        db.commit()
        db.refresh(section)
        return section

    @staticmethod
    def get_by_id(
        db: Session,
        section_id: UUID,
    ) -> Section | None:
        return (
            db.query(Section)
            .filter(
                Section.id == section_id
            )
            .first()
        )

    @staticmethod
    def get_by_board(
        db: Session,
        board_id: UUID,
    ) -> list[Section]:
        return (
            db.query(Section)
            .filter(
                Section.board_id == board_id
            )
            .order_by(Section.position)
            .all()
        )

    @staticmethod
    def get_next_position(
        db: Session,
        board_id: UUID,
    ) -> int:

        max_position = (
            db.query(
                func.max(Section.position)
            )
            .filter(
                Section.board_id == board_id
            )
            .scalar()
        )

        if max_position is None:
            return 1

        return max_position + 1

    @staticmethod
    def update(
        db: Session,
        section: Section,
    ) -> Section:
        db.commit()
        db.refresh(section)
        return section

    @staticmethod
    def delete(
        db: Session,
        section: Section,
    ) -> None:
        db.delete(section)
        db.commit()