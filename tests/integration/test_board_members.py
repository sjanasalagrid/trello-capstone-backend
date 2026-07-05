def test_owner_get_board_members(
    client,
    owner_headers,
    owner_board,
    accepted_invitation,
):

    response = client.get(
        f"/boards/{owner_board['id']}/members",
        headers=owner_headers,
    )

    assert response.status_code == 200

    members = response.json()

    assert len(members) == 2

def test_member_get_board_members(
    client,
    member_headers,
    owner_board,
    accepted_invitation,
):

    response = client.get(
        f"/boards/{owner_board['id']}/members",
        headers=member_headers,
    )

    assert response.status_code == 200

    assert len(response.json()) == 2

def test_owner_remove_member(
    client,
    owner_headers,
    owner_board,
    accepted_invitation,
):

    response = client.delete(
        f"/boards/{owner_board['id']}/members/{accepted_invitation['invited_user_id']}",
        headers=owner_headers,
    )

    assert response.status_code == 204

def test_removed_member_cannot_access_board(
    client,
    owner_headers,
    member_headers,
    owner_board,
    accepted_invitation,
):

    client.delete(
        f"/boards/{owner_board['id']}/members/{accepted_invitation['invited_user_id']}",
        headers=owner_headers,
    )

    response = client.get(
        f"/boards/{owner_board['id']}",
        headers=member_headers,
    )

    assert response.status_code == 403

def test_removed_member_board_list(
    client,
    owner_headers,
    member_headers,
    owner_board,
    accepted_invitation,
):

    client.delete(
        f"/boards/{owner_board['id']}/members/{accepted_invitation['invited_user_id']}",
        headers=owner_headers,
    )

    response = client.get(
        "/boards",
        headers=member_headers,
    )

    assert response.status_code == 200
    assert response.json() == []

def test_member_cannot_remove_board_member(
    client,
    member_headers,
    owner_board,
    accepted_invitation,
):

    response = client.delete(
        f"/boards/{owner_board['id']}/members/{accepted_invitation['invited_user_id']}",
        headers=member_headers,
    )

    assert response.status_code == 403

from uuid import uuid4


def test_remove_nonexistent_member(
    client,
    owner_headers,
    owner_board,
):

    response = client.delete(
        f"/boards/{owner_board['id']}/members/{uuid4()}",
        headers=owner_headers,
    )

    assert response.status_code == 404