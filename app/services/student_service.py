from app.repo import student_repo
from app.models.db_models import Student
from app.models.view_models import StudentItem, StudentEditItem
from app.models.forms import StudentEditForm

def get_student_list() -> []:
    students = student_repo.retrieve_all()
    return [StudentItem(student) for student in students]

def get_student(student_id: int) -> StudentEditItem:
    student_model = student_repo.retrieve(student_id)

    if student_model is not None:
        form = to_student_form(student_model)
        return StudentEditItem(student_model, form)
    else:
        return None

def to_student_form(student_model: Student) -> StudentEditForm:
    # convert to wtforms object
    if student_model is not None:
        form = StudentEditForm(
            student_id=student_model.id,
            first_name=student_model.first_name,
            last_name=student_model.last_name,
            first_name_lao=student_model.first_name_lao,
            last_name_lao=student_model.last_name_lao,
            nick_name=student_model.nick_name,
            gender=student_model.gender,
            occupation=student_model.occupation,
            email=student_model.email,
            student_number=student_model.student_number,
            phone_number=student_model.phone_number,
            address=student_model.address,
            birthday=student_model.birthday,
            application_date=student_model.application_date,
        )
    
    return form if student_model is not None else None

def update_student(form: StudentEditForm) -> StudentEditItem:
    student_model = student_repo.retrieve(int(form.student_id.data))
    if student_model is not None and form.validate():
        # TODO check if update actull worked
        # TODO validate that email, if changed, is still unique
        # TODO validate that student number cannot be changed
        result = student_repo.update(student_model, form)
        form = to_student_form(student_model)
    elif student_model is None:
        return None

    return StudentEditItem(student_model, form)