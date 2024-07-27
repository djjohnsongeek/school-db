from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.forms import LoginForm
from app.repo import staff_repo
from app.services import controller_service
from app.models.enums import MessageCategory
from werkzeug.security import check_password_hash

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/auth/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if request.method == "GET":
        if "user" in session:
            return redirect(url_for("index.home"))
        else:
            return render_template("/auth/login.html", form=login_form)

    if request.method == "POST":
        errors = []
        user_account = None

        if not login_form.validate():
            errors.append("Invalid data submitted")

        if len(errors) == 0:
            user_account = staff_repo.retrieve_by_username(login_form.username.data)
            if user_account is None or not check_password_hash(user_account.hashed_password, login_form.password.data):
                errors.append("The username or password is invalid.")

        if len(errors) == 0:
            session["user"] = {
                "name": user_account.full_name(), 
                "id": user_account.id,
                "role": user_account.role,
                "is_admin": user_account.is_admin
            }
            controller_service.flash_message(f"Welcome, {user_account.full_name()}!", MessageCategory.Success)
            return redirect(url_for("index.home"))
        else:
            controller_service.flash_messages(errors, MessageCategory.Error)
            return render_template("/auth/login.html", form=login_form)

@auth_blueprint.route("/auth/logout", methods=["GET"])
def logout():
    session.clear()
    controller_service.flash_message("You have been logged out successfully.", MessageCategory.Success)
    return redirect(url_for('auth.login'))

@auth_blueprint.route("/auth/passwords", methods=["GET"])
def passwords():
    if not session.get("user").get("is_admin") == True:
        controller_service.flash_message("You are not authorized to access this resource.", MessageCategory.Warn)
        return redirect(url_for("index.home"))

    return render_template("/auth/passwords.html")