from flask import Request, current_app
from app.services import staff_service
from app.models.view_models import AsyncJsResponseItem

def delete_item(category: str, action: str, request: Request) -> AsyncJsResponseItem:
    errors = []
    # TODO: figure out how to properly parse json
    request_data = request.get_json()
    if request_data:
        item_id = request_data.get("item_id", None)

    if not valid_category(category) or not valid_action(action) or request_data is None or item_id is None:
        errors.append("Invalid request.")

    if not errors:
        if action == "delete":
            if category == "staff":
                result = app_service.soft_delete(item_id)

                # update main errors object
                for error in result:
                    errors.append(error)

            elif category == "student":
                pass

    return AsyncJsResponseItem(error=error, data={"itemId" : item_id})

def valid_category(category: str) -> bool:
    return category.lower() in current_app.config["ALLOWED_CATEGORIES"]

def valid_action(action: str) -> bool:
    return action.lower() in current_app.config["ALLOWED_ACTIONS"]
