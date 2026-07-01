from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.enums.invitation_status import InvitationStatus
from app.schemas.invitation import InvitationResponse
from app.services.invitation_service import InvitationService


router = APIRouter(
    prefix="/invitations",
    tags=["Invitations"],
)


@router.get(
    "",
    response_model=list[InvitationResponse],
)
def get_my_invitations(
    status: Annotated[
        InvitationStatus | None,
        Query(
            description="Filter invitations by status"
        ),
    ] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return InvitationService.get_user_invitations(
        db=db,
        current_user_id=current_user.id,
        status=status,
    )

@router.post(
    "/{token}/accept",
    response_model=InvitationResponse,
    status_code=status.HTTP_200_OK,
)
def accept_invitation(
    token: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return InvitationService.accept_invitation(
        db=db,
        token=token,
        current_user_id=current_user.id,
    )

