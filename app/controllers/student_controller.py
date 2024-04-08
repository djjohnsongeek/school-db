from flask import Blueprint, render_template, request, redirect, url_for
from app.services import student_service, controller_service
from app.models.view_models import StudentCreateItem
from app.models.forms import StudentEditForm
from app.models.enums import MessageCategory

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
    elif request.method == "POST":
        student_form = StudentEditForm()
        student_edit_model = student_service.update_student(student_form)
        if student_edit_model is None:
            return redirect(url_for("index.error", error_code=404))
        else:
            if student_edit_model.form.errors:
                controller_service.flash_message("Failed to update student's details.", MessageCategory.Error)
            else:
                controller_service.flash_message("Student's details updated!", MessageCategory.Success)
            return render_template("/students/edit.html", student_model=student_edit_model)

@student_blueprint.route("/students/create", methods=["GET", "POST"])
def create():
    student_form = StudentEditForm()
    if request.method == "GET":
        create_model = StudentCreateItem(student_form)
        return render_template("/students/create.html", student_model=create_model)
    else:
        pass