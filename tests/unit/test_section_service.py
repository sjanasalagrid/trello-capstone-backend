import uuid
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.models.board import Board
from app.models.board_member import BoardMember
from app.models.section import Section
from app.models.user import User
from app.schemas.section import SectionCreate, SectionUpdate
from app.services.section_service import SectionService


def test_create_section_success():

    db = MagicMock()

    owner = User(
        id=uuid.uuid4(),
        email="owner@test.com",
    )

    board = Board(
        id=uuid.uuid4(),
        owner_id=owner.id,
    )

    section = Section(
        id=uuid.uuid4(),
        board_id=board.id,
        name="Todo",
        position=1,
    )

    section_data = SectionCreate(
        name="Todo",
        description="Tasks",
    )

    with (
        patch(
            "app.services.section_service.BoardRepository.get_by_id",
            return_value=board,
        ),
        patch(
            "app.services.section_service.SectionRepository.get_next_position",
            return_value=1,
        ),
        patch(
            "app.services.section_service.SectionRepository.create",
            return_value=section,
        ),
    ):

        result = SectionService.create_section(
            db,
            board.id,
            section_data,
            owner,
        )

        assert result.name == "Todo"
        assert result.position == 1


def test_get_board_sections_success():

    db = MagicMock()

    owner = User(id=uuid.uuid4())

    board = Board(
        id=uuid.uuid4(),
        owner_id=owner.id,
    )

    sections = [
        Section(
            id=uuid.uuid4(),
            board_id=board.id,
            name="Todo",
            position=1,
        ),
        Section(
            id=uuid.uuid4(),
            board_id=board.id,
            name="Done",
            position=2,
        ),
    ]

    with (
        patch(
            "app.services.section_service.BoardRepository.get_by_id",
            return_value=board,
        ),
        patch(
            "app.services.section_service.BoardMemberRepository.get_member",
            return_value=BoardMember(),
        ),
        patch(
            "app.services.section_service.SectionRepository.get_by_board",
            return_value=sections,
        ),
    ):

        result = SectionService.get_board_sections(
            db,
            board.id,
            owner,
        )

        assert len(result) == 2


def test_update_section_success():

    db = MagicMock()

    owner = User(id=uuid.uuid4())

    board = Board(
        id=uuid.uuid4(),
        owner_id=owner.id,
    )

    section = Section(
        id=uuid.uuid4(),
        board_id=board.id,
        name="Todo",
        description="Old",
    )

    update = SectionUpdate(
        name="In Progress",
        description="Updated",
    )

    with (
        patch(
            "app.services.section_service.SectionRepository.get_by_id",
            return_value=section,
        ),
        patch(
            "app.services.section_service.BoardRepository.get_by_id",
            return_value=board,
        ),
        patch(
            "app.services.section_service.SectionRepository.update",
            return_value=section,
        ),
    ):

        result = SectionService.update_section(
            db,
            section.id,
            update,
            owner,
        )

        assert result.name == "In Progress"
        assert result.description == "Updated"


def test_delete_section_success():

    db = MagicMock()

    owner = User(id=uuid.uuid4())

    board = Board(
        id=uuid.uuid4(),
        owner_id=owner.id,
    )

    section = Section(
        id=uuid.uuid4(),
        board_id=board.id,
    )

    with (
        patch(
            "app.services.section_service.SectionRepository.get_by_id",
            return_value=section,
        ),
        patch(
            "app.services.section_service.BoardRepository.get_by_id",
            return_value=board,
        ),
        patch(
            "app.services.section_service.SectionRepository.delete",
        ) as mock_delete,
    ):

        SectionService.delete_section(
            db,
            section.id,
            owner,
        )

        mock_delete.assert_called_once_with(
            db,
            section,
        )