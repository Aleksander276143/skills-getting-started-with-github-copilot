"""Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern"""


def test_signup_successfully_adds_participant(client, fresh_activities):
    """
    Arrange: Client ready, test email prepared
    Act: POST signup for existing activity
    Assert: Participant added and success message returned
    """
    # Arrange
    activity_name = "Chess Club"
    email = "newemail@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_signup_updates_participant_list(client):
    """
    Arrange: Client ready, test email prepared
    Act: POST signup, then GET activities
    Assert: New participant appears in activity's participant list
    """
    # Arrange
    activity_name = "Tennis Club"
    new_email = "tennis_newcomer@mergington.edu"

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    activities_data = activities_response.json()
    assert new_email in activities_data[activity_name]["participants"]


def test_signup_returns_404_for_nonexistent_activity(client):
    """
    Arrange: Client ready, invalid activity name prepared
    Act: POST signup for non-existent activity
    Assert: 404 error returned
    """
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "test@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_increments_participant_count(client):
    """
    Arrange: Client ready, test email prepared
    Act: POST signup, then get activities
    Assert: Participant count increases
    """
    # Arrange
    activity_name = "Drama Club"
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity_name]["participants"])
    new_email = "drama_student@mergington.edu"

    # Act
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )
    final_response = client.get("/activities")
    final_count = len(final_response.json()[activity_name]["participants"])

    # Assert
    assert final_count == initial_count + 1
