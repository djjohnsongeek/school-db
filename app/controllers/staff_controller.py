from flask import Blueprint, render_template, request, redirect, url_for
from app.services import staff_service
staff_blueprint = Blueprint("staff", __name__)

@staff_blueprint.route("/staff", methods=["GET"])
def home():
    staff = staff_service.get_staff_list()
    return render_template("/staff/list.html", staff=staff)

@staff_blueprint.route("/staff/<int:staff_id>", methods=["GET"])
def edit(staff_id: int):
    if request.method == "GET":
        staff_form = staff_service.get_staff(staff_id)

        if staff_form is None:
            return redirect(url_for("index.error", error_code=404))
        else:
            return render_template("/staff/edit.html", staff_form=staff_form)