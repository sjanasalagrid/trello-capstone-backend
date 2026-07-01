from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.section import (
    SectionCreate,
    SectionUpdate,
    SectionResponse,
)
from app.services.section_service import SectionService


router = APIRouter(
    tags=["Sections"],
)


@router.post(
    "/boards/{board_id}/sections",
    response_model=SectionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_section(
    board_id: UUID,
    section_data: SectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return SectionService.create_section(
        db=db,
        board_id=board_id,
        section_data=section_data,
        current_user=current_user,
    )


@router.get(
    "/boards/{board_id}/sections",
    response_model=list[SectionResponse],
)
def get_board_sections(
    board_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return SectionService.get_board_sections(
        db=db,
        board_id=board_id,
        current_user=current_user,
    )


@router.get(
    "/sections/{section_id}",
    response_model=SectionResponse,
)
def get_section(
    section_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return SectionService.get_section(
        db=db,
        section_id=section_id,
        current_user=current_user,
    )


@router.put(
    "/sections/{section_id}",
    response_model=SectionResponse,
)
def update_section(
    section_id: UUID,
    section_data: SectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return SectionService.update_section(
        db=db,
        section_id=section_id,
        section_data=section_data,
        current_user=current_user,
    )


@router.delete(
    "/sections/{section_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_section(
    section_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    SectionService.delete_section(
        db=db,
        section_id=section_id,
        current_user=current_user,
    )