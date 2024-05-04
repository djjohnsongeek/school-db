from app.repo import class_repo, staff_repo, terms_repo
from app.models.view_models import ClassItem, ClassCreateItem, ClassEditItem
from app.models.forms import ClassEditForm

def get_class_list() -> []:
    class_models = class_repo.retrieve_all()
    return [ClassItem(model) for model in class_models]


def get_create_model() -> ClassCreateItem:
    errors = []

    create_form = ClassEditForm()
    create_form.teacher_id.choices = get_teacher_choices()
    create_form.term_id.choices = get_term_choices()

    if len(create_form.teacher_id.choices) == 0:
        errors.append("No Teachers found, please create a Teacher before creating a class.")

    if len(create_form.term_id.choices) == 0:
        errors.append("No Terms found, please create a Term before creating a class.")

    return ClassCreateItem(create_form, [])

def to_create_model(form: ClassEditForm, errors: []) -> ClassCreateItem:
    form.teacher_id.choices = get_teacher_choices()
    form.term_id.choices = get_term_choices()

    return ClassCreateItem(form, errors)

def to_edit_model(form: ClassEditForm, errors: []) -> ClassEditItem:

    return ClassEditItem(form=None, class_model=None, edit_errors=[])

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