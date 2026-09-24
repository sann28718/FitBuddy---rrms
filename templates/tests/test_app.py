import os

os.environ["DEMO_MODE"] = "true"
os.environ["DATABASE_URL"] = "sqlite:///./test_fitbuddy.db"

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home_page():
    response = client.get("/")

    assert response.status_code == 200
    assert "FitBuddy" in response.text
    assert "Generate My Plan" in response.text


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_docs():
    response = client.get("/docs")

    assert response.status_code == 200


def test_generate_workout():

    response = client.post(
        "/generate-workout",
        data={
            "username": "Test User",
            "user_id": "TEST001",
            "age": "25",
            "weight": "70",
            "goal": "muscle gain",
            "intensity": "medium",
        },
    )

    assert response.status_code == 200
    assert "Test User" in response.text
    assert "DAY 1" in response.text


def test_duplicate_user():

    response = client.post(
        "/generate-workout",
        data={
            "username": "Another User",
            "user_id": "TEST001",
            "age": "25",
            "weight": "70",
            "goal": "muscle gain",
            "intensity": "medium",
        },
    )

    assert response.status_code == 400
    assert "already exists" in response.text


def test_users_api():

    response = client.get("/api/users")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_admin_page():

    response = client.get("/view-all-users")

    assert response.status_code == 200
    assert "Admin Dashboard" in response.text


def test_feedback():

    response = client.post(
        "/submit-feedback",
        data={
            "user_id": "TEST001",
            "feedback": "Please add more cardio.",
        },
    )

    assert response.status_code == 200
    assert "Plan Updated Successfully" in response.text
