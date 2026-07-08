"""Shared test fixtures and configuration for the test suite."""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """FastAPI TestClient for making requests to the app."""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test."""
    # Store original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team for all skill levels",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": []
        },
        "Tennis Club": {
            "description": "Learn tennis techniques and compete in friendly matches",
            "schedule": "Tuesdays and Thursdays, 3:00 PM - 4:00 PM",
            "max_participants": 12,
            "participants": []
        },
        "Drama Club": {
            "description": "Perform in plays and musicals, develop acting skills",
            "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": []
        },
        "Art Class": {
            "description": "Explore painting, drawing, and sculpture techniques",
            "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": []
        },
        "Debate Team": {
            "description": "Develop argumentation and public speaking skills",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": []
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": []
        }
    }

    # Clear and reset activities dictionary
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Cleanup after test
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def sample_email():
    """Sample email for testing signup/unregister."""
    return "test.student@mergington.edu"


@pytest.fixture
def existing_participant():
    """Email of a participant already signed up for Chess Club."""
    return "michael@mergington.edu"


@pytest.fixture
def empty_activity():
    """Activity name with no participants."""
    return "Basketball Team"


@pytest.fixture
def full_activity():
    """Activity name with participants."""
    return "Chess Club"
