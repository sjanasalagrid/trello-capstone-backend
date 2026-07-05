from fastapi import responses
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import event
from app.main import app
from app.db.session import get_db

from sqlalchemy.orm import Session

from tests.test_db import (
    engine,
    TestingSessionLocal,
    create_test_database,
    drop_test_database,
)

@pytest.fixture(scope="session", autouse=True)
def setup_database():

    drop_test_database()
    create_test_database()

    yield

    drop_test_database()

@pytest.fixture
def client(db: Session):

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

@pytest.fixture
def db() -> Session:

    connection = engine.connect()

    transaction = connection.begin()

    session = TestingSessionLocal(
        bind=connection
    )

    session.begin_nested()
    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session, trans):

        if trans.nested and not trans._parent.nested:
            session.begin_nested()

    yield session

    session.close()

    transaction.rollback()

    connection.close()

# ---------------------------
# User Authentication
# ---------------------------

@pytest.fixture
def owner_user(client):

    payload = {
        "email": "owner@test.com",
        "password": "Password123",
        "first_name": "Owner",
        "last_name": "User",
    }

    response = client.post(
        "/auth/register",
        json=payload,
    )

    assert response.status_code == 200

    return response.json()

@pytest.fixture
def member_user(client):

    payload = {
        "email": "member@test.com",
        "password": "Password123",
        "first_name": "Member",
        "last_name": "User",
    }

    response = client.post(
        "/auth/register",
        json=payload,
    )

    assert response.status_code == 200

    return response.json()

@pytest.fixture
def owner_headers(client, owner_user):

    response = client.post(
        "/auth/login",
        json={
            "email": "owner@test.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }

@pytest.fixture
def member_headers(client,member_user):

    response = client.post(
        "/auth/login",
        json={
            "email": "member@test.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }

# --------------------------
# Board Test fixtures
# --------------------------

@pytest.fixture
def owner_board(
    client,
    owner_headers,
):

    response = client.post(
        "/boards",
        json={
            "name": "Sprint Board",
            "description": "Testing board",
        },
        headers=owner_headers,
    )

    assert response.status_code == 201

    return response.json()

# -------------------------------
# Invitation Fixtures
# -------------------------------

@pytest.fixture
def pending_invitation(
    client,
    owner_headers,
    owner_board,
    member_user,
):

    response = client.post(
        f"/boards/{owner_board['id']}/invite",
        json={
            "email": "member@test.com",
        },
        headers=owner_headers,
    )

    assert response.status_code == 201

    return response.json()

@pytest.fixture
def accepted_invitation(
    client,
    member_headers,
    pending_invitation,
):

    response = client.post(
        f"/invitations/{pending_invitation['token']}/accept",
        headers=member_headers,
    )

    assert response.status_code == 200

    return response.json()

# -------------------------------
# Section Fixtures
# -------------------------------

@pytest.fixture
def owner_section(
    client,
    owner_headers,
    owner_board,
):

    response = client.post(
        f"/boards/{owner_board['id']}/sections",
        json={
            "name": "To Do",
            "position": 1,
        },
        headers=owner_headers,
    )

    assert response.status_code == 201

    return response.json()

# ---------------------------
# Ticket Fixtures
# ---------------------------

@pytest.fixture
def owner_ticket(
    client,
    owner_headers,
    owner_section,
):

    response = client.post(
        f"/sections/{owner_section['id']}/tickets",
        json={
            "title": "Implement Login",
            "description": "Implement JWT authentication",
        },
        headers=owner_headers,
    )

    assert response.status_code == 201

    return response.json()

@pytest.fixture
def second_section(
    client,
    owner_headers,
    owner_board,
):

    response = client.post(
        f"/boards/{owner_board['id']}/sections",
        json={
            "name": "Done",
            "position": 2,
        },
        headers=owner_headers,
    )

    print(response.json())

    assert response.status_code == 201

    return response.json()