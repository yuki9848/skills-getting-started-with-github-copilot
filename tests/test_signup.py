"""Tests for the POST /activities/{activity_name}/signup endpoint."""

import pytest


def test_successful_signup(client, reset_activities, sample_email, empty_activity):
    """Test successful signup for an activity."""
    # Arrange
    # (Using fixtures for test data)
    
    # Act
    response = client.post(
        f"/activities/{empty_activity}/signup",
        params={"email": sample_email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert sample_email in data["message"]
    assert empty_activity in data["message"]


def test_signup_adds_participant(client, reset_activities, sample_email, empty_activity):
    """Test that signup actually adds the participant to the activity."""
    # Arrange
    activities_before = client.get("/activities").json()
    initial_count = len(activities_before[empty_activity]["participants"])
    
    # Act
    response = client.post(
        f"/activities/{empty_activity}/signup",
        params={"email": sample_email}
    )
    
    # Assert
    assert response.status_code == 200
    activities_after = client.get("/activities").json()
    new_count = len(activities_after[empty_activity]["participants"])
    assert new_count == initial_count + 1
    assert sample_email in activities_after[empty_activity]["participants"]


def test_duplicate_signup_prevention(client, reset_activities, existing_participant, full_activity):
    """Test that duplicate signups are prevented with 400 error."""
    # Arrange
    # (Using fixtures for test data)
    
    # Act
    response = client.post(
        f"/activities/{full_activity}/signup",
        params={"email": existing_participant}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]


def test_signup_nonexistent_activity(client, reset_activities, sample_email):
    """Test that signing up for a nonexistent activity returns 404."""
    # Arrange
    nonexistent_activity = "Nonexistent Club"
    
    # Act
    response = client.post(
        f"/activities/{nonexistent_activity}/signup",
        params={"email": sample_email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]


def test_multiple_different_signups(client, reset_activities, empty_activity):
    """Test that multiple different students can sign up."""
    # Arrange
    emails = [
        "student1@mergington.edu",
        "student2@mergington.edu",
        "student3@mergington.edu"
    ]
    
    # Act
    for email in emails:
        response = client.post(
            f"/activities/{empty_activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Assert
    activities = client.get("/activities").json()
    participants = activities[empty_activity]["participants"]
    for email in emails:
        assert email in participants


def test_signup_response_format(client, reset_activities, sample_email, empty_activity):
    """Test that signup response has correct format."""
    # Arrange
    # (Using fixtures for test data)
    
    # Act
    response = client.post(
        f"/activities/{empty_activity}/signup",
        params={"email": sample_email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert isinstance(data["message"], str)
