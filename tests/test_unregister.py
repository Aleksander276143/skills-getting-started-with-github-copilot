"""Tests for POST /activities/{activity_name}/unregister endpoint using AAA pattern"""


def test_unregister_successfully_removes_participant(client):
    """
    Arrange: Client ready, existing participant email prepared
    Act: POST unregister for existing participant
    Assert: Participant removed and success message returned
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Known participant

    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_unregister_removes_from_participant_list(client):
    """
    Arrange: Client ready, existing participant email prepared
    Act: POST unregister, then GET activities
    Assert: Participant no longer in activity's list
    """
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"  # Known participant

    # Act
    unregister_response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    activities_response = client.get("/activities")

    # Assert
    assert unregister_response.status_code == 200
    activities_data = activities_response.json()
    assert email not in activities_data[activity_name]["participants"]


def test_unregister_returns_404_for_nonexistent_activity(client):
    """
    Arrange: Client ready, invalid activity name prepared
    Act: POST unregister for non-existent activity
    Assert: 404 error returned
    """
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "test@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_returns_400_for_nonexistent_participant(client):
    """
    Arrange: Client ready, valid activity but non-existent participant
    Act: POST unregister for participant not in activity
    Assert: 400 error returned
    """
    # Arrange
    activity_name = "Art Studio"
    email = "not_signed_up@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "Participant not found" in data["detail"]


def test_unregister_decrements_participant_count(client):
    """
    Arrange: Client ready with known participant
    Act: POST unregister, then get activities
    Assert: Participant count decreases
    """
    # Arrange
    activity_name = "Gym Class"
    email = "john@mergington.edu"  # Known participant
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity_name]["participants"])

    # Act
    client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    final_response = client.get("/activities")
    final_count = len(final_response.json()[activity_name]["participants"])

    # Assert
    assert final_count == initial_count - 1
