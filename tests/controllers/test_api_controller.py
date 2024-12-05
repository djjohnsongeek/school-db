import pytest
from flask import g, session
from app.repo import class_repo

def test_login_required(client, auth):
    with client:
        response = client.post('/api/student/update', json={})
        response_json = response.get_json()
        assert response.status_code == 200
        assert "You are not authorized to access this resource." in response_json["errors"]

def test_invalid_category(client, auth):
    auth.login()
    with client:
        response = client.post('/api/invalid_category/update', json={})
        response_json = response.get_json()
        assert response.status_code == 200
        assert "Not Supported" in response_json["errors"]

def test_invalid_action(client, auth):
    auth.login()
    with client:
        response = client.post('/api/student/insert', json={})
        response_json = response.get_json()
        assert response.status_code == 200
        assert "Not Supported" in response_json["errors"]

def test_update_student_grade_invalid_data(client, auth):
    auth.login()
    with client:
        response = client.post('/api/student/update', json={})
        response_json = response.get_json()
        assert response.status_code == 200
        assert "Invalid data detected." in response_json["errors"]

def test_update_student_grade_success(client, auth, app):
    record_id = 1
    auth.login()

    # confirm current grade
    with app.app_context():
        roster_entry_record = class_repo.retrieve_roster_entry(record_id)
        assert roster_entry_record.final_grade == 200

    # Update grade
    with client:
        data = {
            "class_id": 1,
            "student_id": 1,
            "record_id": record_id,
            "final_grade": 999
        }

        response = client.post("/api/student/update", json=data)
        response_json = response.get_json()

        assert response.status_code == 200
        assert len(response_json["errors"]) == 0

    # confirm grade has been updated
    with app.app_context():
        roster_entry_record = class_repo.retrieve_roster_entry(record_id)
        assert roster_entry_record.final_grade == 999

def test_delete_student_not_found(client, auth):
    auth.login()
    with client:
        response = client.post('/api/student/delete', json={})
        response_json = response.get_json()
        assert response.status_code == 200
        assert "Student was not found." in response_json["errors"]
