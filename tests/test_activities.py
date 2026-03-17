"""Tests for GET /activities endpoint using AAA pattern"""


def test_get_activities_returns_all_activities(client):
    """
    Arrange: Client is ready
    Act: GET /activities
    Assert: Return all activities with correct structure
    """
    # Arrange - done by fixture

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert len(data) == 9  # All activities present


def test_get_activities_includes_participants(client):
    """
    Arrange: Client is ready
    Act: GET /activities
    Assert: Activities include participant lists
    """
    # Arrange - done by fixture

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    chess_club = data["Chess Club"]
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)
    assert "michael@mergington.edu" in chess_club["participants"]


def test_get_activities_includes_activity_details(client):
    """
    Arrange: Client is ready
    Act: GET /activities
    Assert: Activities include description, schedule, max_participants
    """
    # Arrange - done by fixture

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    programming = data["Programming Class"]
    assert "description" in programming
    assert "schedule" in programming
    assert "max_participants" in programming
    assert programming["max_participants"] == 20
