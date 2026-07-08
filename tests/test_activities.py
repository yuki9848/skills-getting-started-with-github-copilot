"""Tests for the GET /activities endpoint."""

import pytest


def test_get_all_activities(client, reset_activities):
    """Test fetching all activities returns correct structure."""
    # Arrange
    # (Using fixtures for test data)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Gym Class" in activities


def test_activities_structure(client, reset_activities):
    """Test that activities have the correct data structure."""
    # Arrange
    # (Using fixtures for test data)
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)


def test_participants_are_strings(client, reset_activities):
    """Test that participants in the list are email strings."""
    # Arrange
    # (Using fixtures for test data)
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        for participant in activity_data["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant


def test_activities_have_correct_participant_count(client, reset_activities):
    """Test that participant counts are accurate."""
    # Arrange
    # (Using fixtures for test data)
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert len(activities["Chess Club"]["participants"]) == 2
    assert len(activities["Basketball Team"]["participants"]) == 0


def test_activities_list_is_not_empty(client, reset_activities):
    """Test that activities list contains items."""
    # Arrange
    # (Using fixtures for test data)
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert len(activities) > 0
    assert len(activities) >= 9
