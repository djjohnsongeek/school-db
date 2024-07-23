from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services import staff_service, controller_service
from app.models.forms import StaffEditForm
from app.models.enums import MessageCategory
from app.models.view_models import StaffCreateItem
from app.auth import login_required

staff_blueprint = Blueprint("staff", __name__)

@staff_blueprint.route("/staff", methods=["GET"])
@login_required
def home():
    staff = staff_service.get_staff_list()
    return render_template("/staff/list.html", staff=staff)

@staff_blueprint.route("/staff/edit/<int:staff_id>", methods=["GET", "POST"])
@login_required
def edit(staff_id: int):
    if request.method == "GET":
        staff_edit_model = staff_service.get_staff(staff_id)
        if staff_edit_model is None:
            return redirect(url_for("index.error", error_code=404))
        else:
            return render_template("/staff/edit.html", staff_model=staff_edit_model)

    elif request.method == "POST":
        staff_form = StaffEditForm()
        staff_edit_model = staff_service.update_staff(staff_form)
        if staff_edit_model is None:
            return redirect(url_for("index.error", error_code=404))
        else:
            if staff_edit_model.edit_errors:
                controller_service.flash_messages(staff_edit_model.edit_errors, MessageCategory.Error)
            else:
                controller_service.flash_message("Staff member details updated!", MessageCategory.Success)
                
            return render_template("/staff/edit.html", staff_model=staff_edit_model)

@staff_blueprint.route("/staff/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "GET":
        staff_create_model = StaffCreateItem(StaffEditForm())
        return render_template("/staff/create.html", staff_model=staff_create_model)
    elif request.method == "POST":
        edit_form = StaffEditForm()
        errors = staff_service.create_staff(edit_form)
        if len(errors) > 0:
            controller_service.flash_messages(errors, MessageCategory.Error)
            return render_template("/staff/create.html", staff_model=StaffCreateItem(edit_form))
        else:
            controller_service.flash_message("New Staff Member created!", MessageCategory.Success)
            return redirect(url_for("staff.home"))