import os
import tempfile

import pytest
from app import create_app
from app.db import get_db
from app.commands import init_db
from flask import g, session

# Run tests with py -m pytest

@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "DB_NAME": "school_db_test",
        "DB_USER": "root",
        "DB_PORT": 3306,
        "DB_HOST": "localhost",
        "DB_PASSWORD": "admin",
        "LOG_FILE_PATH": "logs/error_logs.txt"
    })

    with app.app_context():
        init_db(False)

    yield app


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='djohnson', password='password'):
        with self._client:
            self._client.get("/auth/login")
            token = g.get("csrf_token")
            return self._client.post("/auth/login", data={ "username": username, "password": password, "csrf_token": token })

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)