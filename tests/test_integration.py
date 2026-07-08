"""Integration tests for signup/unregister workflows."""

import pytest


def test_signup_unregister_workflow(client, reset_activities, sample_email, empty_activity):
    """Test complete workflow: signup → verify → unregister → verify."""
    # Arrange
    # (Using fixtures for test data)
    
    # Act - Sign up
    signup_response = client.post(
        f"/activities/{empty_activity}/signup",
        params={"email": sample_email}
    )
    
    # Assert - Sign up successful
    assert signup_response.status_code == 200
    activities = client.get("/activities").json()
    assert sample_email in activities[empty_activity]["participants"]
    
    # Act - Unregister
    unregister_response = client.post(
        f"/activities/{empty_activity}/unregister",
        params={"email": sample_email}
    )
    
    # Assert - Unregister successful
    assert unregister_response.status_code == 200
    activities = client.get("/activities").json()
    assert sample_email not in activities[empty_activity]["participants"]


def test_multiple_signups_to_same_activity(client, reset_activities, empty_activity):
    """Test multiple students signing up to the same activity."""
    # Arrange
    students = [
        "alice@mergington.edu",
        "bob@mergington.edu",
        "charlie@mergington.edu"
    ]
    
    # Act - All students sign up
    for student in students:
        response = client.post(
            f"/activities/{empty_activity}/signup",
            params={"email": student}
        )
        assert response.status_code == 200
    
    # Assert - All are registered
    activities = client.get("/activities").json()
    for student in students:
        assert student in activities[empty_activity]["participants"]
    assert len(activities[empty_activity]["participants"]) == len(students)


def test_student_signup_multiple_activities(client, reset_activities, sample_email):
    """Test a student signing up for multiple activities."""
    # Arrange
    activities_to_join = ["Basketball Team", "Drama Club", "Science Club"]
    
    # Act - Sign up for all activities
    for activity in activities_to_join:
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": sample_email}
        )
        assert response.status_code == 200
    
    # Assert - Student is in all activities
    activities = client.get("/activities").json()
    for activity in activities_to_join:
        assert sample_email in activities[activity]["participants"]


def test_unregister_specific_student_from_crowded_activity(client, reset_activities, full_activity):
    """Test unregistering one student from an activity with multiple participants."""
    # Arrange
    activities_before = client.get("/activities").json()
    participants_before = activities_before[full_activity]["participants"].copy()
    initial_count = len(participants_before)
    first_participant = participants_before[0]
    
    # Act - Unregister first participant
    response = client.post(
        f"/activities/{full_activity}/unregister",
        params={"email": first_participant}
    )
    
    # Assert - Only one was removed
    assert response.status_code == 200
    activities_after = client.get("/activities").json()
    participants_after = activities_after[full_activity]["participants"]
    assert len(participants_after) == initial_count - 1
    assert first_participant not in participants_after
    
    # Assert - Others are still there
    for participant in participants_before[1:]:
        assert participant in participants_after


def test_signup_unregister_cycle(client, reset_activities, sample_email, empty_activity):
    """Test multiple signup/unregister cycles for the same student and activity."""
    # Arrange - Test 3 cycles
    num_cycles = 3
    
    for cycle in range(num_cycles):
        # Act - Sign up
        signup = client.post(
            f"/activities/{empty_activity}/signup",
            params={"email": sample_email}
        )
        
        # Assert - Sign up successful
        assert signup.status_code == 200
        activities = client.get("/activities").json()
        assert sample_email in activities[empty_activity]["participants"]
        
        # Act - Unregister
        unregister = client.post(
            f"/activities/{empty_activity}/unregister",
            params={"email": sample_email}
        )
        
        # Assert - Unregister successful
        assert unregister.status_code == 200
        activities = client.get("/activities").json()
        assert sample_email not in activities[empty_activity]["participants"]
