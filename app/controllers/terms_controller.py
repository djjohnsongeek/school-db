from flask import Blueprint, render_template
from app.services import terms_service
terms_blueprint = Blueprint("terms", __name__)

@terms_blueprint.route("/terms", methods=["GET"])
def home():
    terms = terms_service.get_list()
    return render_template("terms/list.html", terms=terms)