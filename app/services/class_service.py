from app.repo import class_repo, staff_repo, terms_repo, student_repo
from app.models.view_models import ClassItem, ClassCreateItem, ClassEditItem
from app.models.db_models import SchoolClass
from app.models.forms import ClassEditForm
from app.models.dto import ApiResultItem
from datetime import datetime

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
    students_not_on_roster = student_repo.retrieve_non_members(school_class)

    if school_class is None:
        errors.append("No class found.")

    form = to_edit_form(school_class)
    return to_edit_model(form, school_class, students_not_on_roster, errors)

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


def to_edit_model(form: ClassEditForm, model: SchoolClass, non_members: [], errors: []) -> ClassEditItem:
    return ClassEditItem(form, model, non_members, errors)

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