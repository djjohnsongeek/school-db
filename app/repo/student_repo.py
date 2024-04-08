from app.models.db_models import Student
from app.models.forms import StudentEditForm

def retrieve_all() -> []:
    return Student.select().where(Student.deleted == False)

def retrieve(id: int) -> Student:
    return Student.get_or_none(Student.id == id)

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