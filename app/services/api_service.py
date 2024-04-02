from flask import Request, current_app
from app.services import staff_service

def delete_item(category: str, action: str, request: Request) -> []:
    errors = []

    request_data = request.get_json(silent=True)
    item_id = request_data.get("item_id", None)

    if not valid_category(category) or not valid_action(action) or request_data is None or item_id is None:
        errors.add("Invalid request.")

    if not errors:
        if action == "delete":
            if category == "staff":
                result = app_service.soft_delete(item_id)

                # update main errors object
                for error in result:
                    errors.append(error)

            elif category == "student":
                pass

    return errors

def valid_category(category: str) -> bool:
    return category.lower() in current_app.config["ALLOWED_CATEGORIES"]

def valid_action(action: str) -> bool:
    return action.lower() in current_app.config["ALLOWED_ACTIONS"]
