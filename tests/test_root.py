"""Tests for GET / endpoint using AAA pattern"""


def test_root_redirects_to_static_index(client):
    """
    Arrange: Client ready
    Act: GET /
    Assert: Redirects to /static/index.html
    """
    # Arrange - done by fixture

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_location_correct(client):
    """
    Arrange: Client ready
    Act: GET / with follow_redirects=True
    Assert: Final route contains static/index.html reference
    """
    # Arrange - done by fixture

    # Act
    response = client.get("/", follow_redirects=True)

    # Assert
    assert response.status_code == 200
    # If redirect is followed successfully, we get static content
    assert "text/html" in response.headers.get("content-type", "")
