from flask import Blueprint, render_template
from app.services import class_service
classes_blueprint = Blueprint("classes", __name__)

@classes_blueprint.route("/classes", methods=["GET"])
def home():
    classes = class_service.get_class_list()
    return render_template("classes.html", classes=classes)