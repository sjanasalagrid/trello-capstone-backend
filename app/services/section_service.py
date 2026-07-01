from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.section import Section
from app.models.user import User
from app.repositories.board_member_repository import BoardMemberRepository
from app.repositories.board_repository import BoardRepository
from app.repositories.section_repository import SectionRepository
from app.schemas.section import SectionCreate, SectionUpdate


class SectionService:

    @staticmethod
    def create_section(
        db: Session,
        board_id: UUID,
        section_data: SectionCreate,
        current_user: User,
    ) -> Section:

        board = BoardRepository.get_by_id(
            db,
            board_id,
        )

        if board is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Board not found.",
            )

        if board.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the board owner can create sections.",
            )

        position = SectionRepository.get_next_position(
            db,
            board_id,
        )

        section = Section(
            board_id=board_id,
            name=section_data.name,
            description=section_data.description,
            position=position,
        )

        return SectionRepository.create(
            db,
            section,
        )

    @staticmethod
    def get_board_sections(
        db: Session,
        board_id: UUID,
        current_user: User,
    ) -> list[Section]:

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
            user_id=current_user.id,
        )

        if member is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this board.",
            )

        return SectionRepository.get_by_board(
            db,
            board_id,
        )

    @staticmethod
    def get_section(
        db: Session,
        section_id: UUID,
        current_user: User,
    ) -> Section:

        section = SectionRepository.get_by_id(
            db,
            section_id,
        )

        if section is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Section not found.",
            )

        member = BoardMemberRepository.get_member(
            db=db,
            board_id=section.board_id,
            user_id=current_user.id,
        )

        if member is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this board.",
            )

        return section

    @staticmethod
    def update_section(
        db: Session,
        section_id: UUID,
        section_data: SectionUpdate,
        current_user: User,
    ) -> Section:

        section = SectionRepository.get_by_id(
            db,
            section_id,
        )

        if section is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Section not found.",
            )

        board = BoardRepository.get_by_id(
            db,
            section.board_id,
        )

        if board.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the board owner can update sections.",
            )

        if section_data.name is not None:
            section.name = section_data.name

        if section_data.description is not None:
            section.description = section_data.description

        return SectionRepository.update(
            db,
            section,
        )

    @staticmethod
    def delete_section(
        db: Session,
        section_id: UUID,
        current_user: User,
    ) -> None:

        section = SectionRepository.get_by_id(
            db,
            section_id,
        )

        if section is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Section not found.",
            )

        board = BoardRepository.get_by_id(
            db,
            section.board_id,
        )

        if board.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the board owner can delete sections.",
            )

        SectionRepository.delete(
            db,
            section,
        )