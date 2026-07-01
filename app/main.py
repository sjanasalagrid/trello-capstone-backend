from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.boards import router as board_router
from app.api.invitations import router as invitation_router
from app.api.sections import router as section_router
from app.api.tickets import router as ticket_router

app = FastAPI(
    title="Trello Capstone API"
)

app.include_router(auth_router)
app.include_router(board_router)
app.include_router(invitation_router)
app.include_router(section_router)
app.include_router(ticket_router)


@app.get("/")
def root():
    return {
        "message": "Trello Capstone API"
    }