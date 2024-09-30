import pytest
from flask import g, session

def test_terms_index_requires_auth(client):
    with client:
        response = client.get("/terms")
        assert response.status_code == 302
        assert session["_flashes"][0][1] == "You must login to access this resource."

def test_terms_index_requires_auth_1(client, auth):
    auth.login()
    with client:
        response = client.get("/terms")
        assert response.status_code == 200
        assert b'<h1 class="card-header-title title is-3">Terms</h1>' in response.data

def test_terms_create_requires_auth(client):
    with client:
        response = client.get("/terms/create")
        assert response.status_code == 302
        assert session["_flashes"][0][1] == "You must login to access this resource."

def test_terms_create_requires_auth_1(client, auth):
    auth.login()
    with client:
        response = client.get("/terms/create")
        assert response.status_code == 200
        assert b'<span class="has-text-grey mr-2">Create New Term</span>' in response.data