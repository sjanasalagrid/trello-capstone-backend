import uuid
from unittest.mock import MagicMock, patch

from app.enums.ticket_status import TicketStatus
from app.models.board import Board
from app.models.section import Section
from app.models.ticket import Ticket
from app.models.user import User
from app.schemas.ticket import (
    TicketAssign,
    TicketCreate,
    TicketMove,
    TicketStatusUpdate,
    TicketUpdate,
)
from app.services.ticket_service import TicketService


def test_create_ticket_success():

    db = MagicMock()

    user = User(id=uuid.uuid4())

    board = Board(id=uuid.uuid4())

    section = Section(
        id=uuid.uuid4(),
        board_id=board.id,
    )

    ticket = Ticket(
        id=uuid.uuid4(),
        section_id=section.id,
        title="Task",
        created_by_id=user.id,
    )

    with (
        patch(
            "app.services.ticket_service.SectionRepository.get_by_id",
            return_value=section,
        ),
        patch(
            "app.services.ticket_service.BoardRepository.get_by_id",
            return_value=board,
        ),
        patch(
            "app.services.ticket_service.BoardMemberRepository.is_member",
            return_value=True,
        ),
        patch(
            "app.services.ticket_service.TicketRepository.create",
            return_value=ticket,
        ),
    ):

        result = TicketService.create_ticket(
            db,
            section.id,
            TicketCreate(
                title="Task",
                description="Description",
            ),
            user,
        )

        assert result.title == "Task"


def test_update_ticket_success():

    db = MagicMock()

    owner = User(id=uuid.uuid4())

    board = Board(id=uuid.uuid4())

    section = Section(
        id=uuid.uuid4(),
        board_id=board.id,
    )

    ticket = Ticket(
        id=uuid.uuid4(),
        section_id=section.id,
        created_by_id=owner.id,
        title="Old",
    )

    with (
        patch(
            "app.services.ticket_service.TicketRepository.get_by_id",
            return_value=ticket,
        ),
        patch(
            "app.services.ticket_service.SectionRepository.get_by_id",
            return_value=section,
        ),
        patch(
            "app.services.ticket_service.BoardRepository.get_by_id",
            return_value=board,
        ),
        patch(
            "app.services.ticket_service.BoardRepository.is_owner",
            return_value=False,
        ),
        patch(
            "app.services.ticket_service.TicketRepository.update",
            return_value=ticket,
        ),
    ):

        result = TicketService.update_ticket(
            db,
            ticket.id,
            TicketUpdate(
                title="New",
                description="Updated",
            ),
            owner,
        )

        assert result.title == "New"
        assert result.description == "Updated"


def test_assign_ticket_success():

    db = MagicMock()

    owner = User(id=uuid.uuid4())

    member = User(
        id=uuid.uuid4(),
        email="member@test.com",
    )

    board = Board(id=uuid.uuid4())

    section = Section(
        id=uuid.uuid4(),
        board_id=board.id,
    )

    ticket = Ticket(
        id=uuid.uuid4(),
        section_id=section.id,
        created_by_id=owner.id,
    )

    with (
        patch(
            "app.services.ticket_service.TicketRepository.get_by_id",
            return_value=ticket,
        ),
        patch(
            "app.services.ticket_service.SectionRepository.get_by_id",
            return_value=section,
        ),
        patch(
            "app.services.ticket_service.BoardRepository.get_by_id",
            return_value=board,
        ),
        patch(
            "app.services.ticket_service.BoardRepository.is_owner",
            return_value=True,
        ),
        patch(
            "app.services.ticket_service.UserRepository.get_by_email",
            return_value=member,
        ),
        patch(
            "app.services.ticket_service.BoardMemberRepository.get_member",
            return_value=MagicMock(),
        ),
        patch(
            "app.services.ticket_service.TicketRepository.update",
            return_value=ticket,
        ),
    ):

        result = TicketService.assign_ticket(
            db,
            ticket.id,
            TicketAssign(email="member@test.com"),
            owner,
        )

        assert result.assigned_to_id == member.id


def test_move_ticket_success():

    db = MagicMock()

    owner = User(id=uuid.uuid4())

    board = Board(id=uuid.uuid4())

    source = Section(
        id=uuid.uuid4(),
        board_id=board.id,
    )

    destination = Section(
        id=uuid.uuid4(),
        board_id=board.id,
    )

    ticket = Ticket(
        id=uuid.uuid4(),
        section_id=source.id,
        created_by_id=owner.id,
    )

    with (
        patch(
            "app.services.ticket_service.TicketRepository.get_by_id",
            return_value=ticket,
        ),
        patch(
            "app.services.ticket_service.SectionRepository.get_by_id",
            side_effect=[source, destination],
        ),
        patch(
            "app.services.ticket_service.BoardRepository.get_by_id",
            return_value=board,
        ),
        patch(
            "app.services.ticket_service.BoardRepository.is_owner",
            return_value=True,
        ),
        patch(
            "app.services.ticket_service.TicketRepository.update",
            return_value=ticket,
        ),
    ):

        result = TicketService.move_ticket(
            db,
            ticket.id,
            TicketMove(section_id=destination.id),
            owner,
        )

        assert result.section_id == destination.id


def test_update_ticket_status_success():

    db = MagicMock()

    owner = User(id=uuid.uuid4())

    board = Board(id=uuid.uuid4())

    section = Section(
        id=uuid.uuid4(),
        board_id=board.id,
    )

    ticket = Ticket(
        id=uuid.uuid4(),
        section_id=section.id,
        created_by_id=owner.id,
        status=TicketStatus.OPEN,
    )

    with (
        patch(
            "app.services.ticket_service.TicketRepository.get_by_id",
            return_value=ticket,
        ),
        patch(
            "app.services.ticket_service.SectionRepository.get_by_id",
            return_value=section,
        ),
        patch(
            "app.services.ticket_service.BoardRepository.get_by_id",
            return_value=board,
        ),
        patch(
            "app.services.ticket_service.BoardRepository.is_owner",
            return_value=True,
        ),
        patch(
            "app.services.ticket_service.TicketRepository.update",
            return_value=ticket,
        ),
    ):

        result = TicketService.update_ticket_status(
            db,
            ticket.id,
            TicketStatusUpdate(
                status=TicketStatus.DONE,
            ),
            owner,
        )

        assert result.status == TicketStatus.DONE


def test_delete_ticket_success():

    db = MagicMock()

    owner = User(id=uuid.uuid4())

    board = Board(id=uuid.uuid4())

    section = Section(
        id=uuid.uuid4(),
        board_id=board.id,
    )

    ticket = Ticket(
        id=uuid.uuid4(),
        section_id=section.id,
        created_by_id=owner.id,
    )

    with (
        patch(
            "app.services.ticket_service.TicketRepository.get_by_id",
            return_value=ticket,
        ),
        patch(
            "app.services.ticket_service.SectionRepository.get_by_id",
            return_value=section,
        ),
        patch(
            "app.services.ticket_service.BoardRepository.get_by_id",
            return_value=board,
        ),
        patch(
            "app.services.ticket_service.BoardRepository.is_owner",
            return_value=False,
        ),
        patch(
            "app.services.ticket_service.TicketRepository.delete",
        ) as mock_delete,
    ):

        TicketService.delete_ticket(
            db,
            ticket.id,
            owner,
        )

        mock_delete.assert_called_once_with(
            db,
            ticket,
        )