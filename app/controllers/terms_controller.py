from flask import Blueprint, render_template, request, redirect, url_for
from app.services import terms_service, controller_service
from app.models.forms import TermEditForm
from app.models.view_models import TermCreateItem
from app.models.enums import MessageCategory

terms_blueprint = Blueprint("terms", __name__)

@terms_blueprint.route("/terms", methods=["GET"])
def home():
    terms = terms_service.get_list()
    return render_template("terms/list.html", terms=terms)

@terms_blueprint.route("/terms/create", methods=["GET", "POST"])
def create():
    form = TermEditForm()
    if request.method == "GET":
        return render_template("terms/create.html", term_model=TermCreateItem(form))
    elif request.method == "POST":
        errors = terms_service.create_term(form)
        if len(errors) > 0:
            controller_service.flash_messages(errors, MessageCategory.Error)
            return render_template("terms/create.html", term_model=TermCreateItem(form))
        else:
            controller_service.flash_message("New Term Created!", MessageCategory.Success)
            return redirect(url_for("terms.home"))