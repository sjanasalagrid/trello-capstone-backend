import uuid
from unittest.mock import MagicMock, patch

from app.models.board import Board
from app.models.user import User
from app.schemas.board import BoardCreate
from app.services.board_service import BoardService


def test_create_board():

    db = MagicMock()

    owner = User(
        id=uuid.uuid4(),
        email="owner@test.com",
        first_name="Owner",
        last_name="User",
    )

    board_data = BoardCreate(
        name="Project Board",
        description="Capstone Project",
    )

    board = BoardService.create_board(
        db=db,
        board_data=board_data,
        owner=owner,
    )

    assert board.name == "Project Board"
    assert board.description == "Capstone Project"
    assert board.owner_id == owner.id

    assert db.add.call_count == 2
    db.flush.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(board)


def test_get_user_boards():

    db = MagicMock()

    owner = User(
        id=uuid.uuid4(),
        email="owner@test.com",
    )

    boards = [
        Board(
            id=uuid.uuid4(),
            name="Board 1",
            owner_id=owner.id,
        ),
        Board(
            id=uuid.uuid4(),
            name="Board 2",
            owner_id=owner.id,
        ),
    ]

    with patch(
        "app.services.board_service.BoardRepository.get_by_user",
        return_value=boards,
    ) as mock_get:

        result = BoardService.get_user_boards(
            db=db,
            owner=owner,
        )

        assert len(result) == 2
        assert result[0].name == "Board 1"
        assert result[1].name == "Board 2"

        mock_get.assert_called_once_with(
            db,
            owner.id,
        )


def test_get_user_boards_empty():

    db = MagicMock()

    owner = User(
        id=uuid.uuid4(),
        email="owner@test.com",
    )

    with patch(
        "app.services.board_service.BoardRepository.get_by_user",
        return_value=[],
    ):

        result = BoardService.get_user_boards(
            db=db,
            owner=owner,
        )

        assert result == []