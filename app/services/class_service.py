from app.repo import class_repo, staff_repo, terms_repo, student_repo
from app.models.db_models import SchoolClass, Student, Attendance
from app.models.forms import ClassEditForm
from app.models.dto import ApiResultItem
from datetime import datetime

### View Models ###
class ClassItem:
    def __init__(self, class_model: SchoolClass):
        self.id = class_model.id
        self.name = class_model.name
        self.term = class_model.term.name
        self.teacher_name = class_model.teacher.full_english_name()
        self.teacher_id = class_model.teacher.index
        self.room_number = class_model.room_number
        self.sessions_count = len(class_model.sessions)
        self.remaining_sessions_count = class_model.remaining_sessions()
        self.roster_count = len(class_model.roster)

class ClassCreateItem():
    def __init__(self, form: ClassEditForm, edit_errors: []):
        self.form = form
        self.edit_errors = edit_errors

class ClassEditItem():
    def __init__(self, form: ClassEditForm, class_model: SchoolClass, sessions: [], non_roster: [], edit_errors: []):
        self.form = form
        self.class_name = class_model.name
        self.sessions = sessions
        self.roster = [roster_item.student for roster_item in class_model.roster]
        self.non_roster = non_roster
        self.teacher = class_model.teacher
        self.edit_errors = edit_errors

class SessionAttendanceItem():
    def __init__(self, student_model: Student, attendance_value: str = None):
        self.student_name = student_model.full_name()
        self.student_id = student_model.id
        self.attendance_value = attendance_value

### Functions

def get_class_list() -> []:
    class_models = class_repo.retrieve_all()
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
        return ClassEditItem(None, None, [], [], [])

    class_sessions = get_class_sessions(school_class)
    students_not_on_roster = student_repo.retrieve_non_members(school_class)
    form = to_edit_form(school_class)

    return ClassEditItem(form, school_class, class_sessions, students_not_on_roster, errors)

def get_class_sessions(class_model: SchoolClass):
    class_session_items = []
    return class_session_items

def create_attendance_lookup(attendance: []) -> {}:
    attendance_lookup = {}
    for record in attendance:
        key = f"{record.session.id}:{record.student.id}"
        attendance_lookup[key] = record.value
    return attendance_lookup

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

def update(form: ClassEditForm) -> ClassEditItem:
    errors = []
    class_model = class_repo.retrieve(form.class_id.data)

    if class_model is None:
        return None

    form.teacher_id.choices = get_teacher_choices()
    form.term_id.choices = get_term_choices()

    if not form.validate():
        errors.append("Invalid data detected, no changes were saved.")

    if len(errors) == 0:
        result = class_repo.update(form, class_model)
        if not result:
            errors.append("Failed to update class info.")
        non_members = student_repo.retrieve_non_members(class_model)

    return ClassEditItem(form, class_model, non_members, errors)

def get_students(class_model: SchoolClass) -> []:
    students = [roster_item.student for roster_item in class_model.roster]
    return [{ "name": student.full_name(), "id": student.id } for student in students]

def create_session(request_data: dict) -> ApiResultItem:
    errors = []
    class_model = None
    payload = {}

    # Validate Class Id
    try:
        class_id = int(request_data.get("class_id", None))
        class_model = class_repo.retrieve(class_id)
    except (ValueError, TypeError):
        pass

    if not class_model:
        errors.append("Could not find class.")

    # validate date
    try:
        request_data["session_time"] = datetime.strptime(request_data["session_time"], '%Y-%m-%dT%H:%M')
    except ValueError:
        errors.append("Invalid session date and time format")
    
    # Validate Session Name
    if not request_data.get("session_name") and class_model:
        session_count = class_repo.session_count(class_model.id)
        request_data["session_name"] = f"Session {session_count + 1}"

    if len(errors) == 0:
        class_session = class_repo.create_session(class_model, request_data)
        if class_session is None:
            errors.append("Failed to create a new session.")
        else:
            payload["students"] = get_students(class_model)
            payload["session_id"] = class_session.id
            payload["session_name"] = class_session.name
            payload["session_time"] = class_session.date
            payload["cancelled"] = class_session.cancelled

    return ApiResultItem(errors, payload)