from app.repo import class_repo, staff_repo, terms_repo
from app.models.view_models import ClassItem, ClassEditItem
from app.models.forms import ClassEditForm

def get_class_list() -> []:
    class_models = class_repo.retrieve_all()
    return [ClassItem(model) for model in class_models]


def get_create_model() -> ClassEditItem:
    errors = []

    create_form = ClassEditForm()
    create_form.teacher_id.choices = get_teacher_choices()
    create_form.term_id.choices = get_term_choices()

    if len(create_form.teacher_id.choices) == 0:
        errors.append("No Teachers found, please create a Teacher before creating a class.")

    if len(create_form.term_id.choices) == 0:
        errors.append("No Terms found, please create a Term before creating a class.")

    return ClassEditItem(create_form, [])

def get_teacher_choices() -> []:
    teachers = staff_repo.retrieve_teachers()
    return [(teacher.id, teacher.full_name()) for teacher in teachers]

def get_term_choices() -> []:
    terms = terms_repo.retrieve_current()
    return [(term.id, term.name) for term in terms]