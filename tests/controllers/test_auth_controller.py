import pytest
from flask import g, session
from app.db import get_db


def test_login_get(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'<h1 class="card-header-title title is-3 is-centered">Login</h1>' in response.data

def test_login_redirect_when_authorized(client, auth):
    auth.login()
    response = client.get("/auth/login")

    # redirect since user is already logged in
    assert response.status_code == 302

def test_unauthorized_redirect(client):
    # Test redirect
    response = client.get("/")
    assert response.status_code == 302

    # test redirect to login page
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert b"You must login to access this resource." in response.data
    assert b'<h1 class="card-header-title title is-3 is-centered">Login</h1>' in response.data

def test_successful_login(client, auth):
    response = auth.login()
    assert response.status_code == 302 # successful login should redirect to index
    # assert response.headers["Location"] == "/"

    with client:
        response = client.get('/')
        assert session["user"]["id"] == 1
        assert session["user"]["username"] == 'djohnson'
        assert b'<h1 class="card-header-title title is-3">Dashboard</h1>' in response.data


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'The username or password is invalid.'),
    ('test', 'a', b'The username or password is invalid.'),
))
def test_login_failure(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

@pytest.mark.parametrize(('username', 'password'), (
    (None, "something"),
    ("something", None),
    ("", "something"),
    ("something", "")
))
def test_invalid_login_input(auth, username, password):
    response = auth.login(username, password)
    assert b"Invalid data submitted" in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user' not in session

def test_passwords_page_requires_admin_1(client, auth):
    with client:
        response = client.get("/auth/passwords")
        assert response.status_code == 302
        assert session["_flashes"][0][1] == "You are not authorized to access this resource."

def test_passwords_page_requires_admin_2(client, auth):
    auth.login("rjohnson", "password")
    with client:
        response = client.get("/auth/passwords")
        assert response.status_code == 302
        assert session["_flashes"][1][1] == "You are not authorized to access this resource."

def test_passwords_page_requires_admin_3(client, auth):
    auth.login()
    response = client.get("/auth/passwords")
    assert response.status_code == 200
    assert b"Password Details" in response.data
