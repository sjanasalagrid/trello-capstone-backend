from uuid import uuid4

def test_create_board(
    owner_board,
):

    assert owner_board["name"] == "Sprint Board"
    assert owner_board["description"] == "Testing board"
    assert "id" in owner_board

def test_get_my_boards(
    client,
    owner_headers,
    owner_board,
):

    response = client.get(
        "/boards",
        headers=owner_headers,
    )

    assert response.status_code == 200

    boards = response.json()

    assert len(boards) == 1
    assert boards[0]["name"] == "Sprint Board"

def test_get_board_by_id(
    client,
    owner_headers,
    owner_board,
):

    response = client.get(
        f"/boards/{owner_board['id']}",
        headers=owner_headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == owner_board["id"]


def test_get_nonexistent_board(
    client,
    owner_headers,
):

    response = client.get(
        f"/boards/{uuid4()}",
        headers=owner_headers,
    )

    assert response.status_code == 404

def test_get_boards_without_token(
    client,
):

    response = client.get("/boards")

    assert response.status_code == 401

def test_member_cannot_access_owner_board(
    client,
    member_headers,
    owner_board,
):

    response = client.get(
        f"/boards/{owner_board['id']}",
        headers=member_headers,
    )

    assert response.status_code == 403

def test_member_has_no_boards(
    client,
    member_headers,
):

    response = client.get(
        "/boards",
        headers=member_headers,
    )

    assert response.status_code == 200
    assert response.json() == []