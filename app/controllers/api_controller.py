from flask import Blueprint, render_template, request
from app.services import staff_service, api_service
api_blueprint = Blueprint("api", __name__)

@api_blueprint.route("/api/<category>/<action>", methods=["POST"])
def post(category: str, action: str):
    # csrf token?
    # automatically calls jsonify
    test = request.get_json()
    print(test)
    print(category)
    print(action)
    
    response = api_service.handle_post(category, action, request)
    return response.to_dict()