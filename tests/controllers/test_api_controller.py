import pytest
from flask import g, session


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

def test_delete_student_not_found(client, auth):
    auth.login()
    with client:
        response = client.post('/api/student/delete', json={})
        response_json = response.get_json()
        assert response.status_code == 200
        assert "Student was not found." in response_json["errors"]
