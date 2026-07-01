from uuid import UUID

from sqlalchemy.orm import Session

from app.models.ticket import Ticket


class TicketRepository:

    @staticmethod
    def create(
        db: Session,
        ticket: Ticket,
    ) -> Ticket:
        db.add(ticket)
        db.commit()
        db.refresh(ticket)

        return ticket

    @staticmethod
    def get_by_id(
        db: Session,
        ticket_id: UUID,
    ) -> Ticket | None:
        return (
            db.query(Ticket)
            .filter(
                Ticket.id == ticket_id
            )
            .first()
        )

    @staticmethod
    def get_by_section(
        db: Session,
        section_id: UUID,
    ) -> list[Ticket]:
        return (
            db.query(Ticket)
            .filter(
                Ticket.section_id == section_id
            )
            .order_by(
                Ticket.created_at
            )
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        ticket: Ticket,
    ) -> Ticket:
        db.commit()
        db.refresh(ticket)

        return ticket

    @staticmethod
    def delete(
        db: Session,
        ticket: Ticket,
    ) -> None:
        db.delete(ticket)
        db.commit()