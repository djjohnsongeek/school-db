from flask import Request
from app.repo import class_repo, terms_repo
from app.models.dto import ApiResultItem

## View Models ##
class AttendancePageModel:
    def __init__(self, selected_class, classes):
        self.classes = classes
        self.selected_class = selected_class

## Buisness Logic ##
def get_attendance_model(class_id: int):
    # TODO: set up some way to actually get the current term
    selected_class = class_repo.retrieve(class_id)
    current_term = selected_class.term
    classes = class_repo.retrieve_by_term(current_term)

    return AttendancePageModel(selected_class, classes)

def get_attendance_info(request: Request) -> ApiResultItem:

    class_id = request.args.get("class_id")
    date_str = request.args.get("date")


    return ApiResultItem([], { "test": "testing the api endpoint", "date": date_str, "class_id": class_id })
