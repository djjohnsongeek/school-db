from app.models.db_models import Student
from app.models.forms import StudentEditForm

def retrieve_all() -> []:
    return Student.select().where(Student.deleted == False)

def retrieve(id: int) -> Student:
    return Student.get_or_none(Student.id == id)

def retrieve_by_email(email: str) -> Student:
    return Student.get_or_none(Student.email == email)

def retrieve_by_number(student_number: str) -> Student:
    return Student.get_or_none(Student.student_number == student_number)

def email_exists(email: str) -> bool:
    return retrieve_by_email(email) != None

def student_number_exists(student_num: str) -> bool:
    return retrieve_by_number(student_num) != None

def update(student: Student, form: StudentEditForm):
    student.first_name = form.first_name.data
    student.last_name = form.last_name.data
    student.first_name_lao = form.first_name_lao.data
    student.last_name_lao = form.last_name_lao.data
    student.nick_name = form.nick_name.data
    student.gender = form.gender.data
    student.birthday = form.birthday.data
    student.address = form.address.data
    student.phone_number = form.phone_number.data
    student.email = form.email.data
    student.occupation = form.occupation.data
    student.application_date = form.application_date.data
    student.student_number = form.student_number.data

    rows_updated = student.save()
    return rows_updated == 1