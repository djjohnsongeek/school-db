from flask import Request
from app.repo import class_repo, terms_repo
from app.models.dto import ApiResultItem
from datetime import date
import random

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

def get_attendance_events(request: Request) -> ApiResultItem:
    class_id = request.args.get("class_id")
    date_str = request.args.get("date")

    selected_date = date.fromisoformat(date_str)
    class_id = int(class_id)
    class_model = class_repo.retrieve(class_id)
    # TODO WE NEED SOME VALIDATIN HERE

    calendar_events = get_calendar_events(class_model.id, selected_date.month)


    return ApiResultItem([], { "calendarEvents": calendar_events })

def get_attendance_roster(request: Request) -> ApiResultItem:
    class_id = request.args.get("class_id")
    date_str = request.args.get("date")

    selected_date = date.fromisoformat(date_str)
    class_id = int(class_id)
    class_model = class_repo.retrieve(class_id)
    # TODO WE NEED SOME VALIDATIN HERE

    roster_attendance = get_roster_attendance(class_model.id, selected_date)

    return ApiResultItem([], { "rosterAttendance": roster_attendance })

def get_roster_attendance(class_id: int, selected_date: date) -> []:
    roster_attendance = []
    student_roster = class_repo.retrieve_roster(class_id)
    student_attendance = class_repo.retrieve_attendance_date(class_id, selected_date)
    
    # If a student has attendance records, they cannot be deleted, so they are guarenteed to be in the roster
    # However a student can be in the roster and not have attedance data
    # There should only be one record for each student on a particular date
    for student in student_roster:
        student_attendance_record = None

        # Simple linear search should suffice
        for attendance_record in student_attendance:
            if attendance_record.student.id == student.id:
                student_attendance_record = attendance_record
                break

        attendance = {
            "student": {
                "name": student.full_name(),
                "id": student.id
            },
            "attendance_value": student_attendance_record.value if student_attendance_record is not None else "",
            "attendance_id": student_attendance_record.id if student_attendance_record is not None else 0
        }
        roster_attendance.append(attendance)

    return roster_attendance

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
    colors =  {"P": "#3ABB81", "T": "#FFB70F", "A": "#FF6685" }

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