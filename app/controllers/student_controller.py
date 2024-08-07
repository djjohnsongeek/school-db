from flask import Blueprint, render_template, request, redirect, url_for
from app.services import student_service, controller_service
from app.models.view_models import StudentCreateItem
from app.models.forms import StudentEditForm
from app.models.enums import MessageCategory
from app.auth import login_required

student_blueprint = Blueprint("students", __name__)

@student_blueprint.route("/students", methods=["GET"])
@login_required
def home():
    students = student_service.get_student_list()
    return render_template("/students/list.html", students=students)


@student_blueprint.route("/students/edit/<int:student_id>", methods=["GET", "POST"])
@login_required
def edit(student_id: int):
    if request.method == "GET":
        student_edit_model = student_service.get_student(student_id)
        if student_edit_model is None:
            controller_service.flash_message("Student not found.", MessageCategory.Error)
            return redirect(url_for("students.home"))
        else:
            return render_template("/students/edit.html", student_model=student_edit_model)
    elif request.method == "POST":
        student_form = StudentEditForm()
        student_edit_model = student_service.update_student(student_form)
        if student_edit_model is None:
            controller_service.flash_message("Student not found.", MessageCategory.Error)
            return redirect(url_for("students.home"))
        else:
            if student_edit_model.edit_errors:
                controller_service.flash_messages(student_edit_model.edit_errors, MessageCategory.Error)
            else:
                controller_service.flash_message("Student's details updated!", MessageCategory.Success)
            return render_template("/students/edit.html", student_model=student_edit_model)

@student_blueprint.route("/students/create", methods=["GET", "POST"])
@login_required
def create():
    student_form = StudentEditForm()
    if request.method == "GET":
        create_model = StudentCreateItem(student_form)
        return render_template("/students/create.html", student_model=create_model)
    else:
        form = StudentEditForm()
        errors = student_service.create_student(form)
        if len(errors) > 0:
            controller_service.flash_messages(errors, MessageCategory.Error)
            return render_template("/students/create.html", student_model=StudentCreateItem(form))
        else:
            controller_service.flash_message("New student created!", MessageCategory.Success)
            return redirect(url_for("students.home"))