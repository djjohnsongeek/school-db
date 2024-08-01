from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from app.services import class_service, controller_service, terms_service
from app.models.forms import ClassEditForm
from app.models.enums import MessageCategory
from app.auth import login_required

classes_blueprint = Blueprint("classes", __name__)


@classes_blueprint.route("/classes", methods=["GET"])
@login_required
def home():
    term_filter = request.args.get("term_id", None)

    try:
        term_filter = int(term_filter)
    except (ValueError, TypeError):
        term_filter = None

    classes = class_service.get_class_list(term_filter)
    terms = terms_service.get_list()
    return render_template("/classes/list.html", classes=classes, terms=terms, selected_term=term_filter)

@classes_blueprint.route("/classes/create", methods=["GET", "POST"])
@login_required
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
@login_required
def edit(class_id: int):
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

@classes_blueprint.route("/classes/roster/<int:class_id>", methods=["GET"])
@login_required
def roster(class_id: int):
    errors = []
    try:
        start_date = datetime.fromisoformat(request.args.get("start_date", f"{datetime.now().date()}"))
        days = int(request.args.get("days", "1"))
    except ValueError:
        start_date = datetime.now()
        days = 1
        errors.append("Invalid data recieved. Double check start date format is YYYY-MM-DD.")

    if days < 1 or days > 100:
        days = 1
        errors.append("Invalid data recieved. Number of days cannot be less then 1 or greater then 100")

    controller_service.flash_messages(errors, MessageCategory.Warn)

    skip_weekends = request.args.get("skip_weekends", "true") == "true"

    get_params = {
        "start_date": start_date.date(),
        "days": days,
        "skip_weekends": skip_weekends
    }

    roster = class_service.get_roster(class_id, get_params)
    return render_template("/classes/roster.html", roster=roster, get_params=get_params)