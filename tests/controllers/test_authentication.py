import pytest
from flask import g, session

@pytest.mark.parametrize(('url',), (
    ("/terms/create",),
    ("/terms",),
    ("/terms/edit/1",),
    ("/attendance/1",),
    ("/classes/edit/1",),
    ("/classes",),
    ("/classes/create",),
    ("/classes/roster/1",),
    ("/",),
    ("/staff",),
    ("/staff/create",),
    ("/staff/edit/1",),
    ("/students",),
    ("/students/create",),
    ("/students/edit/1",),
))
def test_endpoints_require_auth(client, url):
    with client:
        response = client.get(url)
        assert response.status_code == 302
        assert session["_flashes"][0][1] == "You must login to access this resource."


@pytest.mark.parametrize(('url', 'expected'), (
    ("/terms/edit/1", b'<span>Term - <span'),
    ("/terms/create", b'<span class="has-text-grey mr-2">Create New Term</span>'),
    ("/terms", b'<h1 class="card-header-title title is-3">Terms</h1>'),
    ("/attendance/1", b"Record Attendance"),
    ("/classes/edit/1", b"<span>Class -"),
    ("/classes", b'<h1 class="card-header-title title is-3">Classes</h1>'),
    ("/classes/create", b'<span class="has-text-grey mr-2"> Create a New Class</span>'),
    ("/classes/roster/1", b'<h1 class="title is-4">Printing Options</h1>'),
    ("/", b'<h1 class="card-header-title title is-3">Dashboard</h1>'),
    ("/staff", b'<h1 class="card-header-title title is-3">Staff</h1>'),
    ("/staff/create", b"Create New Staff Member"),
    ("/staff/edit/1", b'<div style="display: none;">Test element for Staff Edit Page</div>'),
    ("/students", b'<h1 class="card-header-title title is-3">Students</h1>'),
    ("/students/create", b'<span class="has-text-grey mr-2"> Create New Student</span>'),
    ("/students/edit/1", b'<span>Student - <span'),
))
def test_endpoints_require_auth(client, auth, url, expected):
    auth.login()
    with client:
        response = client.get(url)
        assert response.status_code == 200
        assert expected in response.data