import functools
from flask import redirect, session, url_for, flash

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get("user", None) is None:
            flash("You do not have permission to access this resource.", "warning")
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view