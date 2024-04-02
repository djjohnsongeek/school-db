from flask import Blueprint, render_template, request
from app.services import staff_service, api_service
api_blueprint = Blueprint("api", __name__)

@api_blueprint.route("/api/<category>/<action>", methods=["POST"])
def staff_delete(category: str, action: str):
    # csrf token?
    # automatically calls jsonify
    errors = api_service.delete_item(category, action, request)
    return {
        "errors": errors
    }