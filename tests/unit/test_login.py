def test_showSummary_with_invalid_credentials(client):
    response = client.post(
        "/showSummary", data={"email": "philippe@poutou.fr"}
    )
    assert b"Invalid credentials" in response.data


def test_showSummary_with_valid_credentials(client):
    response = client.post(
        "/showSummary", data={"email": "admin@irontemple.com"}
    )
    assert b"Welcome, admin@irontemple.com" in response.data
