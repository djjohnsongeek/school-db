from app.models.db_models import SchoolClass, Staff, Student, Term, Attendance
from app.models.forms import ClassEditForm
from datetime import datetime
import pymysql
from flask import current_app

def retrieve_all() -> []:
    return SchoolClass.select(SchoolClass, Staff, Term).join(Staff).switch(SchoolClass).join(Term)

def retrieve(class_id: int) -> SchoolClass:
        return (SchoolClass
            .select()
            .join_from(SchoolClass, Staff)
            .join_from(SchoolClass, Term)
            .where(SchoolClass.id == class_id)
            .get())

def retrieve_current_or_future(staff: Staff) -> []:
    now = datetime.now()
    query = (SchoolClass
        .select(SchoolClass, Staff, Term)
        .join(Term)
        .switch(SchoolClass)
        .join(Staff)
        .where((SchoolClass.term.end_date > now) & (SchoolClass.teacher.id == staff.id)))
    
    return query

def retrieve_by_term(term: Term) -> []:
    now = datetime.now()
    query = (SchoolClass
        .select()
        .join(Term)
        .where(SchoolClass.term.id == term.id))

    return query

def retrieve_attendance_record(attendance_id: int) -> Attendance:
    query = (Attendance
        .select()
        .where(Attendance.id == attendance_id)
        .get())

    return query

def retrieve_attendance_summary(class_id: int) -> []:
    config = current_app.config
    connection = pymysql.connect(
        host=config["DB_HOST"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        database=config["DB_NAME"],
        charset='utf8mb4',
        port=config["DB_PORT"],
        cursorclass=pymysql.cursors.DictCursor
    )

    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT `value`, count(*) AS `count` FROM `school_db`.`attendance` WHERE `school_class_id` = %s GROUP BY `value`"
            cursor.execute(sql, (class_id,))
            result = cursor.fetchall()
            return result

def create_class(form: ClassEditForm, teacher: Staff, term: Term) -> bool:
    try:
        primary_key = SchoolClass.insert(
            name = form.name.data,
            room_number = form.room_number.data,
            term = term,
            teacher = teacher
        ).execute()

        return primary_key > -1
    except Exception as e:
        print(e)
        # TODO LOG THIS ERROR
        return False

def create_attendance_record(school_class: SchoolClass, student: Student, staff: Staff, value: str) -> bool:
    try:
        Attendance.insert(
            student=student,
            school_class=school_class,
            recorded_by=staff,
            value=value,
            date=datetime.now().date,
        ).execute()
    except Exception as e:
        return False

    return True

def update(form: ClassEditForm, class_model: SchoolClass) -> bool:
    class_model.name = form.name.data
    class_model.room_number = form.room_number.data
    class_model.teacher = form.teacher_id.data
    class_model.term = form.term_id.data

    return class_model.save() > 0