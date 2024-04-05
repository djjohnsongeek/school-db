from flask import Blueprint, render_template, request, redirect, url_for
from app.services import student_service

student_blueprint = Blueprint("students", __name__)

@student_blueprint.route("/students", methods=["GET"])
def home():
    students = student_service.get_student_list()
    return render_template("/students/list.html", students=students)


@student_blueprint.route("/students/edit/<int:student_id>", methods=["GET", "POST"])
def edit(student_id: int):
    if request.method == "GET":
        student_edit_model = student_service.get_student(student_id)
        if student_edit_model is None:
            return redirect(url_for("index.error", error_code=404))
        else:
            return render_template("/students/edit.html", student_model=student_edit_model)
    else:
        pass