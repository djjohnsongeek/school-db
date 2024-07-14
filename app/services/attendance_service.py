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

    # convert date_str to date
    # convert class_id to int
    # valdiate tehse results

    # fetch class
    # fetch class's attendance records for the selected date (month)
        # build a list of 'events' to summerize that month's attendance information
            # Each event should count the number of Presents, Tardys, or Absents
            # { title: "P:1", start: "2024-07-14" }
            # { title: "T:2", start: "2024-07-14" }
            # { title: "A:0", start: "2024-07-14" }
    # fetch class's roster of students
        # build a representation of the class rosters attendance for the selected date
        # [
        #   { student: student_obj, attendance_value: "P", attendance_id: 1 }
            # include attendance_id in case the user decides to update a previously set attendance value
            # this means an update or insert
        # ]


    return ApiResultItem([], { "test": "testing the api endpoint", "date": date_str, "class_id": class_id })
