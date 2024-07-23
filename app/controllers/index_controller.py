from flask import Blueprint, render_template
from app.auth import login_required

index_blueprint = Blueprint("index", __name__)

@index_blueprint.route("/", methods=["GET"])
@login_required
def home():
    return render_template("index.html")

@index_blueprint.route("/error/<int:error_code>", methods=["GET"])
def error(error_code: int):
    error_template = f"/errors/{error_code}.html"
    return render_template(error_template, error_code=error_code)