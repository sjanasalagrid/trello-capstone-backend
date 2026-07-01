from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.models.user import User
from app.repositories.board_member_repository import BoardMemberRepository
from app.repositories.board_repository import BoardRepository
from app.repositories.section_repository import SectionRepository
from app.repositories.ticket_repository import TicketRepository
from app.schemas.ticket import (
    TicketAssign,
    TicketCreate,
    TicketMove,
    TicketStatusUpdate,
    TicketUpdate,
)
from app.repositories.user_repository import UserRepository

class TicketService:

    @staticmethod
    def create_ticket(
        db: Session,
        section_id: UUID,
        ticket_data: TicketCreate,
        current_user: User,
    ) -> Ticket:

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

        if board is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Board not found.",
            )

        if not BoardMemberRepository.is_member(
            db=db,
            board_id=board.id,
            user_id=current_user.id,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this board.",
            )

        ticket = Ticket(
            section_id=section.id,
            title=ticket_data.title,
            description=ticket_data.description,
            created_by_id=current_user.id,
        )

        return TicketRepository.create(
            db,
            ticket,
        )

    @staticmethod
    def get_section_tickets(
        db: Session,
        section_id: UUID,
        current_user: User,
    ) -> list[Ticket]:

        section = SectionRepository.get_by_id(
            db,
            section_id,
        )

        if section is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Section not found.",
            )

        if not BoardMemberRepository.is_member(
            db=db,
            board_id=section.board_id,
            user_id=current_user.id,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this board.",
            )

        return TicketRepository.get_by_section(
            db,
            section_id,
        )

    @staticmethod
    def get_ticket(
        db: Session,
        ticket_id: UUID,
        current_user: User,
    ) -> Ticket:

        ticket = TicketRepository.get_by_id(
            db,
            ticket_id,
        )

        if ticket is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found.",
            )

        section = SectionRepository.get_by_id(
            db,
            ticket.section_id,
        )

        if not BoardMemberRepository.is_member(
            db=db,
            board_id=section.board_id,
            user_id=current_user.id,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this board.",
            )

        return ticket

    @staticmethod
    def update_ticket(
        db: Session,
        ticket_id: UUID,
        ticket_data: TicketUpdate,
        current_user: User,
    ) -> Ticket:

        ticket = TicketRepository.get_by_id(
            db,
            ticket_id,
        )

        if ticket is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found.",
            )

        section = SectionRepository.get_by_id(
            db,
            ticket.section_id,
        )

        board = BoardRepository.get_by_id(
            db,
            section.board_id,
        )

        allowed = (
            BoardRepository.is_owner(board, current_user.id)
            or ticket.created_by_id == current_user.id
            or ticket.assigned_to_id == current_user.id
        )

        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to edit this ticket.",
            )

        if ticket_data.title is not None:
            ticket.title = ticket_data.title

        if ticket_data.description is not None:
            ticket.description = ticket_data.description

        return TicketRepository.update(
            db,
            ticket,
        )

    @staticmethod
    def delete_ticket(
        db: Session,
        ticket_id: UUID,
        current_user: User,
    ) -> None:

        ticket = TicketRepository.get_by_id(
            db,
            ticket_id,
        )

        if ticket is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found.",
            )

        section = SectionRepository.get_by_id(
            db,
            ticket.section_id,
        )

        board = BoardRepository.get_by_id(
            db,
            section.board_id,
        )

        allowed = (
            BoardRepository.is_owner(board, current_user.id)
            or ticket.created_by_id == current_user.id
        )

        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete this ticket.",
            )

        TicketRepository.delete(
            db,
            ticket,
        )
    
    @staticmethod
    def assign_ticket(
        db: Session,
        ticket_id: UUID,
        ticket_assign: TicketAssign,
        current_user: User,
    ) -> Ticket:

        ticket = TicketRepository.get_by_id(
            db,
            ticket_id,
        )

        if ticket is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found.",
            )

        section = SectionRepository.get_by_id(
            db,
            ticket.section_id,
        )

        board = BoardRepository.get_by_id(
            db,
            section.board_id,
        )

        allowed = (
            BoardRepository.is_owner(
                board,
                current_user.id,
            )
            or ticket.created_by_id == current_user.id
        )

        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the owner or ticket creator can assign tickets.",
            )

        user = UserRepository.get_by_email(
            db,
            ticket_assign.email,
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        member = BoardMemberRepository.get_member(
            db=db,
            board_id=board.id,
            user_id=user.id,
        )

        if member is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not a member of this board.",
            )

        if ticket.assigned_to_id == user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ticket is already assigned to this user.",
            )

        ticket.assigned_to_id = user.id

        return TicketRepository.update(
            db,
            ticket,
        )

    @staticmethod
    def move_ticket(
        db: Session,
        ticket_id: UUID,
        ticket_move: TicketMove,
        current_user: User,
    ) -> Ticket:

        ticket = TicketRepository.get_by_id(
            db,
            ticket_id,
        )

        if ticket is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found.",
            )

        current_section = SectionRepository.get_by_id(
            db,
            ticket.section_id,
        )

        destination_section = SectionRepository.get_by_id(
            db,
            ticket_move.section_id,
        )

        if destination_section is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Destination section not found.",
            )

        board = BoardRepository.get_by_id(
            db,
            current_section.board_id,
        )

        allowed = (
            BoardRepository.is_owner(
                board,
                current_user.id,
            )
            or ticket.created_by_id == current_user.id
            or ticket.assigned_to_id == current_user.id
        )

        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to move this ticket.",
            )

        if destination_section.board_id != current_section.board_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot move ticket to another board.",
            )

        ticket.section_id = ticket_move.section_id

        return TicketRepository.update(
            db,
            ticket,
        )

    @staticmethod
    def update_ticket_status(
        db: Session,
        ticket_id: UUID,
        ticket_status: TicketStatusUpdate,
        current_user: User,
    ) -> Ticket:

        ticket = TicketRepository.get_by_id(
            db,
            ticket_id,
        )

        if ticket is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticket not found.",
            )

        section = SectionRepository.get_by_id(
            db,
            ticket.section_id,
        )

        board = BoardRepository.get_by_id(
            db,
            section.board_id,
        )

        allowed = (
            BoardRepository.is_owner(
                board,
                current_user.id,
            )
            or ticket.created_by_id == current_user.id
            or ticket.assigned_to_id == current_user.id
        )

        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to update the ticket status.",
            )

        ticket.status = ticket_status.status

        return TicketRepository.update(
            db,
            ticket,
        )