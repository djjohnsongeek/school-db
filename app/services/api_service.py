from flask import Request, current_app
from app.services import staff_service, student_service, terms_service, class_service, attendance_service
from app.models.dto import ApiResultItem
from app.errors import NotSupportedError

def handle_post(category: str, action: str, request: Request) -> ApiResultItem:
    errors = []
    request_data = request.get_json()
    item_id = None
    if request_data:
        item_id = request_data.get("itemId", None)

    if request_data is None:
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
        else:
            errors.append("Not Supported")
    
    if result is None:
        result = ApiResultItem(errors, None)

    return result

def handle_get(category: str, action: str, request: Request) -> ApiResultItem:
    errors = []

    result = None
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
