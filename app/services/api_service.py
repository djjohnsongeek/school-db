from flask import Request, current_app
from app.services import staff_service, student_service, terms_service, class_service
from app.models.view_models import AsyncJsResponseItem
from app.errors import NotSupportedError

def handle_post(category: str, action: str, request: Request) -> AsyncJsResponseItem:
    errors = []
    request_data = request.get_json()
    if request_data:
        item_id = request_data.get("itemId", None)

    if not valid_category(category) or not valid_action(action) or request_data is None or item_id is None:
        errors.append("Invalid request.")

    results = []
    if not errors:
        if action == "delete":
            if category == "staff":
                results = staff_service.soft_delete(item_id)
            elif category == "student":
                results = student_service.soft_delete(item_id)
            elif category == "term":
                results = terms_service.soft_delete(item_id)
            elif category == "session":
                raise NotImplementedError("Delete Session Not Implemented")
        if action == "create":
            if category == "session":
                request_data["class_id"] = request_data["itemId"]
                results = class_service.create_session(request_data)
            elif category == "staff":
                results.append("Staff creation is not supported")
            elif category == "student":
                results.append("Student creation not supported")
            elif category == "term":
                results.append("Term creation is not supported")
            
    
    # update main errors object
    for error in results:
        errors.append(error)

    return AsyncJsResponseItem(errors, {"itemId" : item_id})

def valid_category(category: str) -> bool:
    return category.lower() in current_app.config["ALLOWED_CATEGORIES"]

def valid_action(action: str) -> bool:
    return action.lower() in current_app.config["ALLOWED_ACTIONS"]
