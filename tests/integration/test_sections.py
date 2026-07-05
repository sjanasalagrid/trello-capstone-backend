def test_create_section(
    owner_section,
):

    assert owner_section["name"] == "To Do"
    assert owner_section["position"] == 1
    assert "id" in owner_section

def test_get_board_sections(
    client,
    owner_headers,
    owner_board,
    owner_section,
):

    response = client.get(
        f"/boards/{owner_board['id']}/sections",
        headers=owner_headers,
    )

    assert response.status_code == 200

    sections = response.json()

    assert len(sections) == 1
    assert sections[0]["name"] == "To Do"

def test_member_create_section(
    client,
    member_headers,
    owner_board,
    accepted_invitation,
):

    response = client.post(
        f"/boards/{owner_board['id']}/sections",
        json={
            "name": "In Progress",
            "position": 2,
        },
        headers=member_headers,
    )
    assert response.status_code == 403

    assert response.json()["detail"] == "Only the board owner can create sections."

def test_update_section(
    client,
    owner_headers,
    owner_section,
):

    response = client.put(
        f"/sections/{owner_section['id']}",
        json={
            "name": "Backlog",
            "position": 1,
        },
        headers=owner_headers,
    )

    assert response.status_code == 200

    section = response.json()

    assert section["name"] == "Backlog"

def test_member_update_section(
    client,
    member_headers,
    accepted_invitation,
    owner_section,
):

    response = client.put(
        f"/sections/{owner_section['id']}",
        json={
            "name": "Ready",
            "position": 1,
        },
        headers=member_headers,
    )

    assert response.status_code == 403

    assert response.json()["detail"] == "Only the board owner can update sections."

def test_delete_empty_section(
    client,
    owner_headers,
    owner_section,
):

    response = client.delete(
        f"/sections/{owner_section['id']}",
        headers=owner_headers,
    )

    assert response.status_code == 204

from uuid import uuid4


def test_get_nonexistent_section(
    client,
    owner_headers,
):

    response = client.put(
        f"/sections/{uuid4()}",
        json={
            "name": "Test",
            "position": 1,
        },
        headers=owner_headers,
    )

    assert response.status_code == 404

def test_non_member_cannot_create_section(
    client,
    member_headers,
    owner_board,
):

    response = client.post(
        f"/boards/{owner_board['id']}/sections",
        json={
            "name": "Blocked",
            "position": 2,
        },
        headers=member_headers,
    )

    assert response.status_code == 403

def test_non_member_cannot_update_section(
    client,
    member_headers,
    owner_section,
):

    response = client.put(
        f"/sections/{owner_section['id']}",
        json={
            "name": "Blocked",
            "position": 1,
        },
        headers=member_headers,
    )

    assert response.status_code == 403

