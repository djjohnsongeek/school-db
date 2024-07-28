from flask import Request, current_app, session
from app.services import staff_service, student_service, terms_service, class_service, attendance_service
from app.models.dto import ApiResultItem
from app.errors import NotSupportedError

def handle_post(category: str, action: str, request: Request) -> ApiResultItem:
    errors = []
    request_data = request.get_json()
    item_id = None

    if request_data is None:
        errors.append("Invalid request.")

    if session.get("user") is None:
        errors.append("You are not authorized to access this resource.")
    
    if request_data:
        item_id = request_data.get("itemId", None)

    result = None
    if not errors:
        if action == "delete":
            if category == "staff":
                if session["user"]["is_admin"]:
                    result = staff_service.soft_delete(item_id)
                else:
                    errors.append("You are not authorized to complete this action.")
            elif category == "student":
                result = student_service.soft_delete(item_id)
            elif category == "term":
                result = terms_service.soft_delete(item_id)
            elif category == "class":
                result = class_service.delete_roster_entry(item_id)
            else:
                errors.append("Not Supported")
        elif action == "create":
            if category == "class":
                result = class_service.create_roster_entries(request_data)
            elif category == "attendance":
                result = attendance_service.record_attendance(request_data)
            else:
                errors.append("Not Supported")
        elif action == "reset":
            if category == "password":
                result = staff_service.reset_password(request_data)
            else:
                errors.app("Not Supported")
        else:
            errors.append("Not Supported")
    
    if result is None:
        result = ApiResultItem(errors, None)

    return result

def handle_get(category: str, action: str, request: Request) -> ApiResultItem:
    errors = []
    result = None

    if session.get("user") is None:
        errors.append("You are not authorized to access this resource.")

    if len(errors) == 0:
        if action == "load":
            if category == "attendanceEvents":
                result = attendance_service.get_attendance_events(request)
            elif category == "attendanceRoster":
                result = attendance_service.get_attendance_roster(request)
            else:
                errors.append("Not supported")
        else:
            errors.append("Not Supported")

    if result is None:
        result = ApiResultItem(errors, None)

    return result
