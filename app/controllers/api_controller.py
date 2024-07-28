from flask import Blueprint, render_template, request, session
from app.services import staff_service, api_service
from app.models.dto import ApiResultItem

api_blueprint = Blueprint("api", __name__)

@api_blueprint.route("/api/<category>/<action>", methods=["POST", "GET"])
def api_endpoint(category: str, action: str):
    if request.method == "GET":
        result = api_service.handle_get(category, action, request)
    else:
        result = api_service.handle_post(category, action, request)
    
    return result.to_dict()