from flask import Blueprint, render_template, request
from app.services import class_service, controller_service
from app.models.view_models import ClassEditItem
from app.models.forms import ClassEditForm
from app.models.enums import MessageCategory

classes_blueprint = Blueprint("classes", __name__)

@classes_blueprint.route("/classes", methods=["GET"])
def home():
    classes = class_service.get_class_list()
    return render_template("/classes/list.html", classes=classes)


@classes_blueprint.route("/classes/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        class_create_model = class_service.get_create_model()
        
        if class_create_model.edit_errors:
            controller_service.flash_messages(class_create_model.edit_errors, MessageCategory.Warning)

        return render_template("classes/create.html", class_model=class_create_model)