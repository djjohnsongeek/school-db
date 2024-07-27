from flask import Request, session
from app.repo import class_repo, terms_repo, student_repo, staff_repo
from app.models.dto import ApiResultItem
from app.models.db_models import SchoolClass
from datetime import date
import random
import pprint


permitted_attendance_values = ['P', 'T', 'A']

## View Models ##
class AttendancePageModel:
    def __init__(self, selected_class, classes):
        self.classes = classes
        self.selected_class = selected_class

## Business Logic ##
def get_attendance_model(class_id: int):
    selected_class = class_repo.retrieve(class_id)
    current_term = selected_class.term
    classes = class_repo.retrieve_by_term(current_term)

    return AttendancePageModel(selected_class, classes)

def get_attendance_events(request: Request) -> ApiResultItem:
    errors = []
    class_id = request.args.get("class_id")
    date_str = request.args.get("date")

    try:
        selected_date = date.fromisoformat(date_str)
        class_id = int(class_id)
        class_model = class_repo.retrieve(class_id)
        calendar_events = get_calendar_events(class_model.id, selected_date.month)
    except (TypeError, ValueError):
        errors.append("Invalid data.")
        calendar_events = {}

    return ApiResultItem(errors, { "calendarEvents": calendar_events })

def get_attendance_roster(request: Request) -> ApiResultItem:
    errors = []
    class_id = request.args.get("class_id")
    date_str = request.args.get("date")

    try:
        selected_date = date.fromisoformat(date_str)
        class_id = int(class_id)
        class_model = class_repo.retrieve(class_id)
        roster_attendance = get_roster_attendance(class_model.id, selected_date)
    except (TypeError, ValueError):
        errors.append("Invalid data.")
        roster_attendance = []

    return ApiResultItem(errors, { "rosterAttendance": roster_attendance })

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

def record_attendance(request_data: dict) -> ApiResultItem:
    errors = []
    # Validating class
    class_model = extract_class(request_data)
    if class_model is None:
        return errors.append("Class not found.")

    # Validate date
    selected_date = extract_date(request_data)
    if selected_date is None:
        errors.append("Invalid data.")

    # Validate attendance
    attendance = request_data.get("attendance", [])
    if len(attendance) == 0:
        errors.append("No attendance data recieved.")

    staff_id = session.get("user", {}).get("id", 0)
    staff = staff_repo.retrieve(staff_id)
    if staff is None:
        errors.append("Staff not found.")

    if len(errors) == 0:
        for item in attendance:
            attendance_id, student_id, attendance_value = extract_attendance_info(item)

            if None in [attendance_id, student_id, attendance_value]:
                errors.append("Invalid Data.")
                break

            # Attendance does not already exist
            if attendance_id == 0:
                student = student_repo.retrieve(student_id)
                attendance_created = class_repo.create_attendance_record(
                    class_model, student, staff, attendance_value, selected_date
                )
            # Attendance record already exists
            else:
                attendance_record = class_repo.retrieve_attendance_record(attendance_id)
                if attendance_record is None:
                    errors.append("Existing attendance record not found.")
                    break

                # TODO verfy existing info
                # date, student, class_model

                attendance_record.recorded_by = staff
                attendance_record.value = attendance_value
                attendance_updated = class_repo.update_attendance_record(attendance_record)

    return ApiResultItem(errors, {})


def extract_class(request_data: dict) -> SchoolClass:
    class_model = None

    try:
        class_id = int(request_data.get("classId", "0"))
    except ValueError:
        class_id = 0

    if class_id != 0:
        class_model = class_repo.retrieve(class_id)

    return class_model

def extract_date(request_data: dict) -> date:
    date_str = request_data.get("date", "")
    selected_date = None
    try:
        selected_date = date.fromisoformat(date_str)
    except ValueError:
        selected_date = None

    return selected_date

def extract_attendance_info(attendance_data: dict) -> ():
    try:
        attendance_id = int(attendance_data.get("attendanceId"))
        student_id = int(attendance_data.get("studentId"))
        attendance_value = attendance_data.get("attendanceValue")
    except ValueError:
        attendance_id = None
        student_id = None
        attendance_value = None

    if attendance_value not in permitted_attendance_values:
        attendance_value = None

    return (attendance_id, student_id, attendance_value)