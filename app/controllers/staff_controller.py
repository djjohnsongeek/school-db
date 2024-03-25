from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services import staff_service, controller_service
from app.models.forms import StaffEditForm
from app.models.enums import MessageCategory
staff_blueprint = Blueprint("staff", __name__)

@staff_blueprint.route("/staff", methods=["GET"])
def home():
    staff = staff_service.get_staff_list()
    return render_template("/staff/list.html", staff=staff)

@staff_blueprint.route("/staff/<int:staff_id>", methods=["GET", "POST"])
def edit(staff_id: int):
    if request.method == "GET":
        staff_edit_model = staff_service.get_staff(staff_id)
        if staff_edit_model is None:
            return redirect(url_for("index.error", error_code=404))
        else:
            return render_template("/staff/edit.html", staff_model=staff_edit_model)

    if request.method == "POST":
        staff_form = StaffEditForm()
        staff_edit_model = staff_service.update_staff(staff_form)
        if staff_edit_model is None:
            return redirect(url_for("index.error", error_code=404))
        else:

            if staff_edit_model.form.errors:
                controller_service.flash_message("Failed to update staff member details.", MessageCategory.Error)
            else:
                controller_service.flash_message("Staff member details updated!", MessageCategory.Success)
            return render_template("/staff/edit.html", staff_model=staff_edit_model)