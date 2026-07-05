def test_owner_registration(
    owner_user,
):

    assert owner_user["email"] == "owner@test.com"

def test_owner_login(
    owner_headers,
):

    assert "Authorization" in owner_headers