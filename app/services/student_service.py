from app.repo import student_repo
from app.models.db_models import Student
from app.models.view_models import StudentItem, StudentEditItem, StudentCreateItem, StudentClassItem
from app.models.forms import StudentEditForm
from app.models.dto import ApiResultItem
from datetime import datetime

def get_student_list() -> []:
    students = student_repo.retrieve_all()
    return [StudentItem(student) for student in students]

def get_student(student_id: int) -> StudentEditItem:
    student_model = student_repo.retrieve(student_id)

    if student_model is not None:
        form = to_student_form(student_model)
        classes = [StudentClassItem(roster_entry) for roster_entry in student_repo.retrieve_classes(student_model)]
        attendance = get_student_attendance(student_model)
        return StudentEditItem(student_model, form, attendance, classes, [])
    else:
        return None

def get_student_attendance(student_model: Student) -> {}:
    attendance = student_repo.retrieve_attendance(student_model.id)
    organized_attendance = {}

    for attendance in student_model.attendance:
        if attendance.school_class.name not in organized_attendance:
            organized_attendance[attendance.school_class.name] = []

        organized_attendance[attendance.school_class.name].append({ "value": attendance.value, "date": attendance.date})

    print(organized_attendance)
    return organized_attendance

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
    if student_model is None:
        return None

    errors = []
    classes = [StudentClassItem(roster_entry) for roster_entry in student_repo.retrieve_classes(student_model)]
    if student_model.email != form.email.data and student_repo.email_exists(form.email.data):
        errors.append("This email address is already in use.")

    if student_model.student_number != form.student_number.data and student_repo.student_number_exists(form.student_number.data):
        errors.append("This Student Number is already in use.")
        # TODO should this value be readonly?
    
    if not form.validate():
        errors.append("Invalid data detected. No changes have been made.")

    if len(errors) == 0:
        result = student_repo.update(student_model, form)
        form = to_student_form(student_model)
        attendance = get_student_attendance(student_model)

    return StudentEditItem(student_model, form, attendance, classes, errors)

def create_student(form: StudentEditForm) -> []:
    errors = []

    if form.student_number.data is None or form.student_number.data == "":
        form.student_number.data = generate_student_number()
    else:
        form.student_number.data = form.student_number.data.zfill(12)
    
    if student_repo.student_number_exists(form.student_number.data):
        errors.append("The supplied student number is already in use.")
    
    if student_repo.email_exists(form.email.data):
        errors.append("This supplied email address is already in use.")

    # We manually set the id so validation will pass
    # This value does not get when inserting the new record
    form.student_id.data = 1
    if not form.validate():
        errors.append("Invalid data detected. A new student was not created.")

    if len(errors) == 0:
        result = student_repo.create(form)
        if not result:
            errors.append("Failed to create new student.")

    return errors

def generate_student_number():
    last_student = student_repo.retrieve_last_student()
    next_student_id = last_student.id + 1

    now = datetime.now()

    next_student_id = str(next_student_id).zfill(6)
    month_str = str(now.month).zfill(2)
    year_str = str(now.year)

    return next_student_id + month_str + year_str


# Removes student from the dropdown list adding students to a class
# Removes student from the main list of students
def soft_delete(student_id: int) -> ApiResultItem:
    errors = []
    student = student_repo.retrieve(student_id)

    # TODO validate: if student had attendance or school work data, don't allow for deletion

    if student is None:
        errors.append("Student was not found.")

    if not errors:
        result = student_repo.soft_delete(student)
        if not result:
            errors.append("Failed to delete student.")

    return ApiResultItem(errors, { "itemId": student_id })