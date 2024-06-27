from flask import Request, current_app
from app.services import staff_service, student_service, terms_service, class_service
from app.models.dto import ApiResultItem
from app.errors import NotSupportedError

def handle_post(category: str, action: str, request: Request) -> ApiResultItem:
    errors = []
    request_data = request.get_json()
    item_id = None
    if request_data:
        item_id = request_data.get("itemId", None)

    if request_data is None or item_id is None:
        errors.append("Invalid request.")

    result = None
    if not errors:
        if action == "delete":
            if category == "staff":
                result = staff_service.soft_delete(item_id)
            elif category == "student":
                result = student_service.soft_delete(item_id)
            elif category == "term":
                result = terms_service.soft_delete(item_id)
            else:
                errors.append("Not Supported")
        elif action == "create":
            if category == "class":
                result = class_service.create_roster_entries(request_data)
            else:
                errors.append("Not Supported")
        else:
            errors.append("Not Supported")
    
    if result is None:
        result = ApiResultItem(errors, None)

    return result