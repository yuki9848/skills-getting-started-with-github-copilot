"""Tests for the POST /activities/{activity_name}/unregister endpoint."""

import pytest


def test_successful_unregister(client, reset_activities, existing_participant, full_activity):
    """Test successful unregister from an activity."""
    # Arrange
    # (Using fixtures for test data)
    
    # Act
    response = client.post(
        f"/activities/{full_activity}/unregister",
        params={"email": existing_participant}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered" in data["message"]
    assert existing_participant in data["message"]


def test_unregister_removes_participant(client, reset_activities, existing_participant, full_activity):
    """Test that unregister actually removes the participant from the activity."""
    # Arrange
    activities_before = client.get("/activities").json()
    initial_count = len(activities_before[full_activity]["participants"])
    
    # Act
    response = client.post(
        f"/activities/{full_activity}/unregister",
        params={"email": existing_participant}
    )
    
    # Assert
    assert response.status_code == 200
    activities_after = client.get("/activities").json()
    new_count = len(activities_after[full_activity]["participants"])
    assert new_count == initial_count - 1
    assert existing_participant not in activities_after[full_activity]["participants"]


def test_unregister_nonexistent_participant(client, reset_activities, sample_email, full_activity):
    """Test that unregistering a non-participating student returns 400."""
    # Arrange
    # (Using fixtures for test data)
    
    # Act
    response = client.post(
        f"/activities/{full_activity}/unregister",
        params={"email": sample_email}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"]


def test_unregister_from_nonexistent_activity(client, reset_activities, sample_email):
    """Test that unregistering from nonexistent activity returns 404."""
    # Arrange
    nonexistent_activity = "Nonexistent Club"
    
    # Act
    response = client.post(
        f"/activities/{nonexistent_activity}/unregister",
        params={"email": sample_email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]


def test_unregister_response_format(client, reset_activities, existing_participant, full_activity):
    """Test that unregister response has correct format."""
    # Arrange
    # (Using fixtures for test data)
    
    # Act
    response = client.post(
        f"/activities/{full_activity}/unregister",
        params={"email": existing_participant}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert isinstance(data["message"], str)


def test_unregister_then_register_again(client, reset_activities, existing_participant, full_activity):
    """Test that a student can re-register after unregistering."""
    # Arrange
    # (Using fixtures for test data)
    
    # Act - Unregister
    response1 = client.post(
        f"/activities/{full_activity}/unregister",
        params={"email": existing_participant}
    )
    
    # Assert - Unregister successful and participant gone
    assert response1.status_code == 200
    activities = client.get("/activities").json()
    assert existing_participant not in activities[full_activity]["participants"]
    
    # Act - Re-register
    response2 = client.post(
        f"/activities/{full_activity}/signup",
        params={"email": existing_participant}
    )
    
    # Assert - Re-register successful and participant back
    assert response2.status_code == 200
    activities = client.get("/activities").json()
    assert existing_participant in activities[full_activity]["participants"]
