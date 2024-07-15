from flask import Request
from app.repo import class_repo, terms_repo
from app.models.dto import ApiResultItem
from datetime import date

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

    selected_date = date.fromisoformat(date_str)
    class_id = int(class_id)
    class_model = class_repo.retrieve(class_id)

    calendar_events = get_calendar_events(class_model.id, selected_date.month)
    # fetch class's roster of students
        # build a representation of the class rosters attendance for the selected date
        # [
        #   { student: student_obj, attendance_value: "P", attendance_id: 1 }
            # include attendance_id in case the user decides to update a previously set attendance value
            # this means an update or insert
        # ]


    return ApiResultItem([], { "calendarEvents": calendar_events })

def get_calendar_events(class_id: int, month: int) -> []:
    # This just helps us organize db data
    daily_att_summary = {}

    # Keeps track of keys for the above dict for easier looping later
    keys = []

    # The list of calender events that we are going to return
    calendar_events = []

    # The only valid attendance values
    attendance_vals = ["P", "T", "A"]

    # Colors that match those attendance values
    colors =  {"P": "#4258FF", "T": "#FFB70F", "A": "#FF6685" }

    months_attendance = class_repo.retrieve_attendance(class_id, month)

    # Organize attendance records, summerize values by date
    for record in months_attendance:
        date_key = record.date.strftime("%Y-%m-%d")
        if date_key not in daily_att_summary:
            daily_att_summary[date_key] = { "A": 0, "P": 0, "T": 0}
            keys.append(date_key)

        daily_att_summary[date_key][record.value.upper()] += 1

    # Convert the daily summeries into 'calendar events' (based on front end calendar lib)
    for date_key in keys:
        for v in attendance_vals:
            calendar_events.append({
                "title": f"{v}:{daily_att_summary[date_key][v]}",
                "start": date_key,
                "backgroundColor": colors[v],
                "borderColor": colors[v]
            })

    return calendar_events