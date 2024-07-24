import functools
from flask import redirect, session, url_for, flash

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get("user", None) is None:
            flash("You must login to access this resource.", "is-warning")
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view