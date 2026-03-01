def test_get_activities(client):
    # Arrange: none (seed data present)

    # Act
    r = client.get("/activities")

    # Assert
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_successful(client):
    # Arrange
    activity = "Chess Club"
    email = "testuser@example.com"
    # ensure clean state
    participants = client.get("/activities").json()[activity]["participants"]
    if email in participants:
        client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Act
    r = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert r.status_code == 200
    assert r.json()["message"] == f"Signed up {email} for {activity}"
    assert email in client.get("/activities").json()[activity]["participants"]


def test_signup_duplicate(client):
    # Arrange: use an email known to be in the seed data
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    r = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert r.status_code == 400
    assert r.json().get("detail") == "Student already signed up"


def test_delete_participant_success(client):
    # Arrange
    activity = "Basketball Team"
    email = "alex@mergington.edu"

    # Pre-check: ensure participant exists
    assert email in client.get("/activities").json()[activity]["participants"]

    # Act
    r = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert r.status_code == 200
    assert r.json()["message"] == f"Removed {email} from {activity}"
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_delete_participant_not_found(client):
    # Arrange
    activity = "Basketball Team"
    email = "nonexistent@example.com"

    # Act
    r = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert r.status_code == 400
    assert r.json().get("detail") == "Student not signed up"
