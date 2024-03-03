from flask import Blueprint, render_template
from app.services import students_service

students_blueprint = Blueprint("students", __name__)

@students_blueprint.route("/students", methods=["GET"])
def home():
    return render_template("students.html")