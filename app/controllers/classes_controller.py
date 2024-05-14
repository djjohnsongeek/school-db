from flask import Blueprint, render_template, request, redirect, url_for
from app.services import class_service, controller_service
from app.models.view_models import ClassCreateItem
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
    if request.method == "POST":
        create_form = ClassEditForm()
        class_edit_model = class_service.create_class(create_form)
        if class_edit_model.edit_errors:
            controller_service.flash_messages(class_edit_model.edit_errors, MessageCategory.Error)
            return render_template("classes/create.html", class_model=class_edit_model)
        else:
            controller_service.flash_message("Class created!", MessageCategory.Success)
            return redirect(url_for("classes.home"))

@classes_blueprint.route("/classes/edit/<int:class_id>", methods=["GET", "POST"])
def edit(class_id: id):
    if request.method == "GET":
        edit_model = class_service.get_edit_model(class_id)
        if edit_model.edit_errors:
            return redirect(url_for("index.error", error_code=404))
        else:
            return render_template("/classes/edit.html", class_model=edit_model)
    if request.method == "POST":
        form = ClassEditForm()
        edit_model = class_service.update(form)
        if edit_model.edit_errors:
            controller_service.flash_messages(edit_model.edit_errors, MessageCategory.Error)
        else:
            controller_service.flash_message("Class updated!", MessageCategory.Success)
        return render_template("/classes/edit.html", class_model=edit_model)