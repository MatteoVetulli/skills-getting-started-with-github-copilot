from fastapi.testclient import TestClient

from src.app import activities


def test_get_activities(client: TestClient):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert expected_activity in data
    assert data[expected_activity]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]


def test_signup_for_activity(client: TestClient):
    # Arrange
    email = "newstudent@mergington.edu"
    url = "/activities/Chess%20Club/signup"

    # Act
    response = client.post(url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in activities["Chess Club"]["participants"]


def test_duplicate_signup_returns_bad_request(client: TestClient):
    # Arrange
    url = "/activities/Chess%20Club/signup"
    duplicate_email = "michael@mergington.edu"

    # Act
    response = client.post(url, params={"email": duplicate_email})

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_unregister_participant(client: TestClient):
    # Arrange
    email = "michael@mergington.edu"
    url = "/activities/Chess%20Club/unregister"

    # Act
    response = client.delete(url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from Chess Club"
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_missing_participant_returns_not_found(client: TestClient):
    # Arrange
    url = "/activities/Chess%20Club/unregister"
    missing_email = "notfound@mergington.edu"

    # Act
    response = client.delete(url, params={"email": missing_email})

    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]
