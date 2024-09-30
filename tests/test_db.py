import pytest
from app.db import get_db
from app.repo import student_repo


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    # TODO test that outside of the app context executing a query resilts in a connection error