from flask import Blueprint, render_template
from app.services import staff_service
staff_blueprint = Blueprint("staff", __name__)

@staff_blueprint.route("/staff", methods=["GET"])
def home():
    staff = staff_service.get_staff_list()
    return render_template("staff.html", staff=staff)