from uuid import uuid4

def test_send_invitation(
    pending_invitation,
):

    assert pending_invitation["status"] == "PENDING"
    assert pending_invitation["accepted_at"] is None
    assert "id" in pending_invitation
    assert "token" in pending_invitation
    assert "board_id" in pending_invitation

def test_member_get_pending_invitations(
    client,
    member_headers,
    pending_invitation,
):

    response = client.get(
        "/invitations",
        headers=member_headers,
    )

    assert response.status_code == 200

    invitations = response.json()

    assert len(invitations) == 1
    assert invitations[0]["status"] == "PENDING"

def test_owner_get_sent_invitations(
    client,
    owner_headers,
    owner_board,
    pending_invitation,
):

    response = client.get(
        f"/boards/{owner_board['id']}/sent_invitations",
        headers=owner_headers,
    )

    assert response.status_code == 200

    invitations = response.json()

    assert len(invitations) == 1
    assert invitations[0]["status"] == "PENDING"

def test_accept_invitation(
    client,
    member_headers,
    pending_invitation,
):

    response = client.post(
        f"/invitations/{pending_invitation['token']}/accept",
        headers=member_headers,
    )

    assert response.status_code == 200

    invitation = response.json()

    assert invitation["status"] == "ACCEPTED"
    assert invitation["accepted_at"] is not None    

def test_member_board_after_accepting_invitation(
    client,
    member_headers,
    pending_invitation,
):

    client.post(
        f"/invitations/{pending_invitation['token']}/accept",
        headers=member_headers,
    )

    response = client.get(
        "/boards",
        headers=member_headers,
    )

    assert response.status_code == 200

    boards = response.json()

    assert len(boards) == 1
    assert boards[0]["name"] == "Sprint Board"

def test_revoke_pending_invitation(
    client,
    owner_headers,
    owner_board,
    pending_invitation,
):

    response = client.delete(
        f"/boards/{owner_board['id']}/sent_invitations/{pending_invitation['id']}",
        headers=owner_headers,
    )

    assert response.status_code == 200

def test_accept_revoked_invitation(
    client,
    owner_headers,
    member_headers,
    owner_board,
    pending_invitation,
):

    client.delete(
        f"/boards/{owner_board['id']}/sent_invitations/{pending_invitation['id']}",
        headers=owner_headers,
    )

    response = client.post(
        f"/invitations/{pending_invitation['token']}/accept",
        headers=member_headers,
    )

    assert response.status_code == 404

def test_accept_invalid_invitation_token(
    client,
    member_headers,
):

    response = client.post(
        f"/invitations/{uuid4()}/accept",
        headers=member_headers,
    )

    assert response.status_code == 404