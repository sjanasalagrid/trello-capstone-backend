from uuid import uuid4

def test_create_ticket(
    owner_ticket,
):

    assert owner_ticket["title"] == "Implement Login"
    assert owner_ticket["status"] == "OPEN"

def test_get_ticket(
    client,
    owner_headers,
    owner_ticket,
):

    response = client.get(
        f"/tickets/{owner_ticket['id']}",
        headers=owner_headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == owner_ticket["id"]

def test_update_ticket(
    client,
    owner_headers,
    owner_ticket,
):

    response = client.put(
        f"/tickets/{owner_ticket['id']}",
        json={
            "title": "Updated Ticket",
            "description": "Updated Description",
        },
        headers=owner_headers,
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Ticket"

def test_move_ticket(
    client,
    owner_headers,
    owner_ticket,
    second_section,
):

    response = client.patch(
        f"/tickets/{owner_ticket['id']}/move",
        json={
            "section_id": second_section["id"],
        },
        headers=owner_headers,
    )

    print(response.json())

    assert response.status_code == 200
    assert response.json()["section_id"] == second_section["id"]

def test_assign_ticket(
    client,
    owner_headers,
    owner_ticket,
    accepted_invitation,
):

    response = client.patch(
        f"/tickets/{owner_ticket['id']}/assign",
        json={
            "email": "member@test.com",
        },
        headers=owner_headers,
    )

    print(response.json())

    assert response.status_code == 200

    assert (
        response.json()["assigned_to_id"]
        == accepted_invitation["invited_user_id"]
    )

def test_member_cannot_assign_ticket(
    client,
    member_headers,
    owner_ticket,
    accepted_invitation,
):

    response = client.patch(
        f"/tickets/{owner_ticket['id']}/assign",
        json={
            "email": "member@test.com",
        },
        headers=member_headers,
    )

    assert response.status_code == 403

def test_update_ticket_status(
    client,
    owner_headers,
    owner_ticket,
):

    response = client.patch(
        f"/tickets/{owner_ticket['id']}/status",
        json={
            "status": "IN_PROGRESS",
        },
        headers=owner_headers,
    )

    assert response.status_code == 200
    assert response.json()["status"] == "IN_PROGRESS"

def test_close_ticket(
    client,
    owner_headers,
    owner_ticket,
):

    response = client.patch(
        f"/tickets/{owner_ticket['id']}/status",
        json={
            "status": "CLOSED",
        },
        headers=owner_headers,
    )

    assert response.status_code == 200
    assert response.json()["status"] == "CLOSED"


def test_get_nonexistent_ticket(
    client,
    owner_headers,
):

    response = client.get(
        f"/tickets/{uuid4()}",
        headers=owner_headers,
    )

    assert response.status_code == 404

def test_non_member_cannot_create_ticket(
    client,
    member_headers,
    owner_section,
):

    response = client.post(
        f"/sections/{owner_section['id']}/tickets",
        json={
            "title": "Blocked",
            "description": "Blocked",
        },
        headers=member_headers,
    )

    print(response.json())

    assert response.status_code == 403

def test_assigned_member_can_update_ticket(
    client,
    owner_headers,
    member_headers,
    owner_ticket,
    accepted_invitation,
):

    client.patch(
        f"/tickets/{owner_ticket['id']}/assign",
        json={
            "email": "member@test.com",
        },
        headers=owner_headers,
    )

    response = client.put(
        f"/tickets/{owner_ticket['id']}",
        json={
            "title": "Edited by Member",
            "description": "Updated",
        },
        headers=member_headers,
    )

    assert response.status_code == 200

