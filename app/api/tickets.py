from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.ticket import (
    TicketAssign,
    TicketCreate,
    TicketMove,
    TicketStatusUpdate,
    TicketResponse,
    TicketUpdate,
)
from app.services.ticket_service import TicketService


router = APIRouter(
    tags=["Tickets"],
)

@router.post(
    "/sections/{section_id}/tickets",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ticket(
    section_id: UUID,
    ticket_data: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return TicketService.create_ticket(
        db=db,
        section_id=section_id,
        ticket_data=ticket_data,
        current_user=current_user,
    )

@router.get(
    "/sections/{section_id}/tickets",
    response_model=list[TicketResponse],
)
def get_section_tickets(
    section_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return TicketService.get_section_tickets(
        db=db,
        section_id=section_id,
        current_user=current_user,
    )

@router.get(
    "/tickets/{ticket_id}",
    response_model=TicketResponse,
)
def get_ticket(
    ticket_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return TicketService.get_ticket(
        db=db,
        ticket_id=ticket_id,
        current_user=current_user,
    )

@router.put(
    "/tickets/{ticket_id}",
    response_model=TicketResponse,
)
def update_ticket(
    ticket_id: UUID,
    ticket_data: TicketUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return TicketService.update_ticket(
        db=db,
        ticket_id=ticket_id,
        ticket_data=ticket_data,
        current_user=current_user,
    )

@router.delete(
    "/tickets/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_ticket(
    ticket_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    TicketService.delete_ticket(
        db=db,
        ticket_id=ticket_id,
        current_user=current_user,
    )

@router.patch(
    "/tickets/{ticket_id}/assign",
    response_model=TicketResponse,
)
def assign_ticket(
    ticket_id: UUID,
    ticket_assign: TicketAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return TicketService.assign_ticket(
        db=db,
        ticket_id=ticket_id,
        ticket_assign=ticket_assign,
        current_user=current_user,
    )

@router.patch(
    "/tickets/{ticket_id}/move",
    response_model=TicketResponse,
)
def move_ticket(
    ticket_id: UUID,
    ticket_move: TicketMove,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return TicketService.move_ticket(
        db=db,
        ticket_id=ticket_id,
        ticket_move=ticket_move,
        current_user=current_user,
    )

@router.patch(
    "/tickets/{ticket_id}/status",
    response_model=TicketResponse,
)
def update_ticket_status(
    ticket_id: UUID,
    ticket_status: TicketStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return TicketService.update_ticket_status(
        db=db,
        ticket_id=ticket_id,
        ticket_status=ticket_status,
        current_user=current_user,
    )