from flask import Blueprint, render_template, request, redirect, url_for
from app.services import terms_service, controller_service
from app.models.forms import TermEditForm
from app.models.view_models import TermEditItem
from app.models.enums import MessageCategory
from app.auth import login_required

terms_blueprint = Blueprint("terms", __name__)

@terms_blueprint.route("/terms", methods=["GET"])
@login_required
def home():
    terms = terms_service.get_list()
    return render_template("terms/list.html", terms=terms)

@terms_blueprint.route("/terms/create", methods=["GET", "POST"])
@login_required
def create():
    form = TermEditForm()
    if request.method == "GET":
        return render_template("terms/create.html", term_model=TermEditItem(None, form, []))
    elif request.method == "POST":
        errors = terms_service.create_term(form)
        if len(errors) > 0:
            controller_service.flash_messages(errors, MessageCategory.Error)
            return render_template("terms/create.html", term_model=TermEditItem(None, form, []))
        else:
            controller_service.flash_message("New Term Created!", MessageCategory.Success)
            return redirect(url_for("terms.home"))


@terms_blueprint.route("/terms/edit/<int:term_id>", methods=["GET", "POST"])
@login_required
def edit(term_id: int):
    if request.method == "GET":
        term_edit_model = terms_service.retrieve_term(term_id)
        if term_edit_model is None:
            return redirect(url_for("index.error", error_code=404))
        else:
            return render_template("terms/edit.html", term_model=term_edit_model)
    elif request.method == "POST":
        term_form = TermEditForm()
        term_edit_model = terms_service.update_term(term_form)

        if term_edit_model is None:
            return redirect(url_for("index.error", error_code=404))
        else:
            if term_edit_model.edit_errors:
                controller_service.flash_messages(term_edit_model.edit_errors, MessageCategory.Error)
            else:
                controller_service.flash_message("The Term's details were updated!", MessageCategory.Success)
            return render_template("/terms/edit.html", term_model=term_edit_model)