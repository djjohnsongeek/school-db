from flask import Blueprint, render_template, request, redirect, url_for
from app.services import attendance_service, controller_service
from app.models.enums import MessageCategory
from app.auth import login_required

attendance_blueprint = Blueprint("attendance", __name__)

@attendance_blueprint.route("/attendance/<int:class_id>", methods=["GET"])
@login_required
def home(class_id: int):
    attendance_model = attendance_service.get_attendance_model(class_id)
    
    if attendance_model is None:
        controller_service.flash_message("Class not found.", MessageCategory.Error)
        return redirect(url_for("classes.home"))

    return render_template("/attendance/index.html", model=attendance_model)