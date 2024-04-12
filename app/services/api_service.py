from flask import Request, current_app
from app.services import staff_service, student_service
from app.models.view_models import AsyncJsResponseItem

def delete_item(category: str, action: str, request: Request) -> AsyncJsResponseItem:
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
    
    # update main errors object
    for error in results:
        errors.append(error)

    return AsyncJsResponseItem(errors, {"itemId" : item_id})

def valid_category(category: str) -> bool:
    return category.lower() in current_app.config["ALLOWED_CATEGORIES"]

def valid_action(action: str) -> bool:
    return action.lower() in current_app.config["ALLOWED_ACTIONS"]
