from flask import Request
from app.repo import class_repo, staff_repo, terms_repo, student_repo
from app.models.db_models import SchoolClass, Student, Attendance, ClassRosterEntry
from app.models.forms import ClassEditForm
from app.models.dto import ApiResultItem
from app.services import attendance_service
from datetime import datetime, timedelta
import json

### View Models ###
class ClassItem:
    def __init__(self, class_model: SchoolClass):
        self.id = class_model.id
        self.name = class_model.name
        self.term = class_model.term.name
        self.teacher_name = class_model.teacher.full_english_name()
        self.teacher_id = class_model.teacher.index
        self.room_number = class_model.room_number
        self.roster_count = len(class_model.roster)

class ClassCreateItem():
    def __init__(self, form: ClassEditForm, edit_errors: []):
        self.form = form
        self.edit_errors = edit_errors

class ClassEditItem():
    def __init__(self, form: ClassEditForm, class_model: SchoolClass, attendance: {}, non_roster: [], edit_errors: []):
        if class_model is not None:
            self.form = form
            self.class_name = class_model.name
            self.class_id = class_model.id
            self.attendance = json.dumps(attendance)
            self.roster = [RosterItem(roster_item.id, roster_item.student) for roster_item in class_model.roster]
            self.non_roster = non_roster
            self.teacher = class_model.teacher
        self.edit_errors = edit_errors

class RosterItem():
    def __init__(self, roster_item_id: int, student: Student):
        self.id = roster_item_id
        self.student = student

    def to_dict(self) -> {}:
        return {
            "id": self.id,
            "student": {
                "name": self.student.full_name(),
                "id": self.student.id
            }
        }

### Functions

def get_class_list(term_id: int) -> []:
    class_models = class_repo.retrieve_all(term_id)
    return [ClassItem(model) for model in class_models]

def get_create_model() -> ClassCreateItem:
    errors = []

    form = ClassEditForm()
    form.teacher_id.choices = get_teacher_choices()
    form.term_id.choices = get_term_choices()

    if len(form.teacher_id.choices) == 0:
        errors.append("No Teachers found, please create a Teacher before creating a class.")

    if len(form.term_id.choices) == 0:
        errors.append("No Terms found, please create a Term before creating a class.")

    return ClassCreateItem(form, [])


def get_edit_model(class_id: int) -> ClassEditItem:
    errors = []
    school_class = class_repo.retrieve(class_id)
    if school_class is None:
        errors.append("No class found.")
        return ClassEditItem(None, None, [], [], errors)
        
    students_not_on_roster = student_repo.retrieve_non_roster_students(school_class.id)
    form = to_edit_form(school_class)
    attendance = class_repo.retrieve_attendance_records(class_id)
    attendance = format_attendance_records(attendance, school_class)

    return ClassEditItem(form, school_class, attendance, students_not_on_roster, errors)

def format_attendance_records(attendance: [], class_model: SchoolClass) -> {}:
    today = datetime.now().date()
    term_start = class_model.term.start_date
    term_end = class_model.term.end_date

    start_date = term_start
    end_date = term_end

    # if the term is not over, just show up to the last two weeks
    if today >= term_start and today <= term_end:
        end_date = today
        start_date = today - timedelta(days=14)

        if start_date < term_start:
            start_date = term_start

    dates = []
    while start_date <= end_date:   
        dates.append(start_date.strftime("%Y/%m/%d"))
        start_date = start_date + timedelta(days=1)

    presents = {}
    tardies = {}
    absents = {}

    # Get set of unique dates
    for record in attendance:
        record["date"] = record["date"].strftime("%Y/%m/%d")

    # Set base line values foreach date (0)
    for date in dates:
        presents[date] = 0
        tardies[date] = 0
        absents[date] = 0

    # Find total of each attendance value per date
    for record in attendance:
        if record["value"] == "P" and record["date"] in presents:
            presents[record["date"]] = presents[record["date"]] + 1
        elif record["value"] == "T" and record["date"] in tardies:
            tardies[record["date"]] = tardies[record["date"]] + 1
        elif record["value"] == "A" and record["date"] in absents:
            absents[record["date"]] = absents[record["date"]] + 1

    return {
        "labels": list(dates),
        "presents": list(presents.values()),
        "presentsTotal":len([record["value"] for record in attendance if record["value"] == "P"]),
        "tardies": list(tardies.values()),
        "tardiesTotal": len([record["value"] for record in attendance if record["value"] == "T"]),
        "absents": list(absents.values()),
        "absentsTotal": len([record["value"] for record in attendance if record["value"] == "A"])
    }

def to_create_model(form: ClassEditForm, errors: []) -> ClassCreateItem:
    form.teacher_id.choices = get_teacher_choices()
    form.term_id.choices = get_term_choices()

    return ClassCreateItem(form, errors)

def to_edit_form(class_model: SchoolClass) -> ClassEditForm:
    if class_model is not None:
        form = ClassEditForm(
            class_id=class_model.id,
            name=class_model.name,
            room_number=class_model.room_number,
            teacher_id=class_model.teacher.id,
            term_id=class_model.term.id
        )

        form.teacher_id.choices = get_teacher_choices()
        form.term_id.choices = get_term_choices()
    
    return form if class_model is not None else None

def get_teacher_choices() -> []:
    teachers = staff_repo.retrieve_teachers()
    return [(teacher.id, teacher.full_name()) for teacher in teachers]

def get_term_choices() -> []:
    terms = terms_repo.retrieve_current()
    return [(term.id, term.name) for term in terms]

def create_class(form: ClassEditForm) -> ClassCreateItem:
    errors = []

    term = terms_repo.retrieve(form.term_id.data)
    teacher = staff_repo.retrieve(form.teacher_id.data)
    form.teacher_id.choices = get_teacher_choices()
    form.term_id.choices = get_term_choices()

    if term is None or teacher is None:
        errors.append("A new class must be assigned to a teacher and a term.")

    form.class_id.data = 1
    if not form.validate():
        errors.append("Invalid data detected. No changes have been saved.")

    if len(errors) == 0:
        result = class_repo.create_class(form, teacher, term)
        if not result:
            errors.append("Failed to create new class.")

    return to_create_model(form, errors)

def get_roster(class_id: int, get_params: {}) -> {}:
    class_model = class_repo.retrieve(class_id)

    if class_model is None:
        return None

    roster = class_repo.retrieve_roster(class_id)
    if roster.count() == 0:
        return {}

    dates = get_roster_dates(get_params)
    
    roster_info = {
        "class_id": class_id,
        "class_name": roster[0].school_class.name,
        "term_name": roster[0].school_class.term.name,
        "term_start": roster[0].school_class.term.start_date,
        "term_end": roster[0].school_class.term.end_date,
        "dates": dates,
        "students": []
    }

    for item in roster:
        roster_info["students"].append({
            "name": item.student.full_name(),
            "number": item.student.student_number
        })

    return roster_info

def get_roster_dates(get_params: {}) -> []:
    finished = False
    dates = []
    i = 0
    while len(dates) != get_params["days"]:
        next_day = get_params["start_date"] + timedelta(days=i)
        is_weekday = next_day.weekday() < 5

        if get_params["skip_weekends"] and is_weekday:
            dates.append(next_day)
        elif not get_params["skip_weekends"]:
            dates.append(next_day)
        
        i = i + 1

    return dates

def create_roster_entries(request_data: {}) -> ApiResultItem:
    class_id = request_data.get("itemId", None)
    student_ids = request_data.get("student_ids", [])

    # our return payload
    errors = []
    roster_items = []

    students = student_repo.retrieve_many(student_ids)
    class_model = class_repo.retrieve(class_id)

    # Make sure students and class exist
    if students.count() != len(student_ids) or len(student_ids) == 0 or class_model is None:
        errors.append("Class or Students were not found.")

    # Make sure this student is not already on the roster
    if class_repo.students_in_roster(students, class_id):
        errors.append("Some students are already part of this roster")
    
    if len(errors) == 0:
        roster_entries = []

        for student in students:
            entry = ClassRosterEntry()
            entry.student = student
            entry.school_class = class_model
            roster_entries.append(entry)

        result = class_repo.create_roster_entries(roster_entries)
        if not result:
            errors.append("Failed to add students to the roster")
        else:
            # return newly created roster data
            new_ids = [student.id for student in students]
            for item in class_model.roster:
                if item.student.id in new_ids:
                    roster_item = RosterItem(item.id, item.student)
                    roster_items.append(roster_item.to_dict())

    # needs to return an ApiResult
    return ApiResultItem(errors, { "roster": roster_items })

def delete_roster_entry(itemId) -> ApiResultItem:
    errors = []

    roster_item = class_repo.retrieve_roster_entry(itemId)
    if roster_item is None:
        errors.append("Roster entry not found")
    else:
        attendance_count = class_repo.retrieve_attendance_count(roster_item.school_class.id, roster_item.student.id)
        if attendance_count != 0:
            errors.append("Student has attendance records for this class, and cannot be removed.")
        
    if not errors:
        success = class_repo.delete_roster_entry(roster_item)
        if not success:
            errors.append("Failed to delete student from the roster")

    return ApiResultItem(errors, { "itemId": roster_item.id })

def update(form: ClassEditForm) -> ClassEditItem:
    errors = []
    class_model = class_repo.retrieve(form.class_id.data)

    if class_model is None:
        return None

    form.teacher_id.choices = get_teacher_choices()
    form.term_id.choices = get_term_choices()

    attendance = class_repo.retrieve_attendance_records(class_model.id)
    att_summary = format_attendance_records(attendance, class_model)

    if not form.validate():
        errors.append("Invalid data detected, no changes were saved.")

    if len(errors) == 0:
        result = class_repo.update(form, class_model)
        if not result:
            errors.append("Failed to update class info.")
        non_members = student_repo.retrieve_non_roster_students(class_model.id)

    return ClassEditItem(form, class_model, att_summary, non_members, errors)

def get_students(class_model: SchoolClass) -> []:
    students = [roster_item.student for roster_item in class_model.roster]
    return [{ "name": student.full_name(), "id": student.id } for student in students]
