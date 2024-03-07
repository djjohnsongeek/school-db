from flask import Blueprint, render_template
from app.services import student_service

student_blueprint = Blueprint("students", __name__)

@student_blueprint.route("/students", methods=["GET"])
def home():
    students = student_service.get_student_list()
    return render_template("/students/list.html", students=students)