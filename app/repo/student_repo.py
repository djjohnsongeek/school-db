from app.models.db_models import Student, ClassRosterEntry, SchoolClass, Term, Attendance
from app.models.forms import StudentEditForm
from app.services import log_service
from .base_repo import Database
from flask import current_app

def retrieve_all() -> []:
    return Student.select().where(Student.deleted == False)

def retrieve(id: int) -> Student:
    return Student.get_or_none(Student.id == id)

def retrieve_attendance(student_id: int) -> []:
    return Attendance.select().join(SchoolClass).where(Attendance.student_id == student_id)

def retrieve_many(ids: []) -> []:
    return Student.select().where(Student.id.in_(ids))

def retrieve_by_email(email: str) -> Student:
    return Student.get_or_none(Student.email == email)

def retrieve_by_number(student_number: str) -> Student:
    return Student.get_or_none(Student.student_number == student_number)

def retrieve_classes(student: Student) -> []:
    return (ClassRosterEntry
        .select()
        .join(SchoolClass)
        .join(Term)
        .where(ClassRosterEntry.student == student))

def email_exists(email: str) -> bool:
    return retrieve_by_email(email) != None

def student_number_exists(student_num: str) -> bool:
    return retrieve_by_number(student_num) != None

def retrieve_last_student() -> Student:
    return Student.select().order_by(Student.id.desc()).first()

def retrieve_non_roster_students(class_id: int) -> []:
    sql = """SELECT *
            FROM `students`
            WHERE `deleted` = 0
            AND `id` NOT IN
                (SELECT S.`id`
                FROM `class_rosters` AS R
                INNER JOIN `students` AS S ON R.`student_id` = S.`id`
                WHERE R.`school_class_id` = %s)"""

    with Database(current_app.config) as db:
        db.execute(sql, (class_id,))
        return db.fetchall()

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

def create(form: StudentEditForm) -> bool:
    try:
        primary_key = Student.insert(
            first_name_lao=form.first_name_lao.data,
            last_name_lao=form.last_name_lao.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            nick_name=form.nick_name.data,
            gender=form.gender.data,
            phone_number=form.phone_number.data,
            student_number=form.student_number.data,
            email=form.email.data,
            birthday=form.birthday.data,
            address=form.address.data,
            occupation=form.occupation.data,
            application_date=form.application_date.data
        ).execute()

        return primary_key > -1
    except Exception as e:
        log_service.record_log(f"Failed to create student: {e}", "student_repo", "error")
        return False

def soft_delete(student: Student):
    student.deleted = True
    rows_updated = student.save()
    return rows_updated == 1