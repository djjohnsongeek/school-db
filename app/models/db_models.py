import os
from peewee import *
from app.models.base_models import Person, BaseModel
from app.models.enums import StaffRole
from datetime import date

class Student(Person):
    student_number = CharField(max_length=32, unique=True)
    application_date = DateField()
    occupation = CharField(max_length=128)

    class Meta:
        table_name = "students"

class Staff(Person):
    username = CharField(max_length=64)
    hashed_password = CharField(max_length=256)
    role = IntegerField()

    def full_name(self):
        if self.role == StaffRole.Teacher.value:
            return self.full_english_name()
        else:
            return self.full_lao_name()
            
class LoginLog(BaseModel):
    staff = ForeignKeyField(Staff, backref="login_logs")
    time = DateTimeField()
    success = BooleanField()

    class Meta:
        table_name = "login_logs"

class Term(BaseModel):
    name = CharField(max_length=64)
    start_date = DateField()
    end_date = DateField()

    class Meta:
        table_name = "terms"

class SchoolClass(BaseModel):
    name = CharField(max_length=64)
    room_number = IntegerField()
    teacher = ForeignKeyField(Staff, backref="classes")
    term = ForeignKeyField(Term, backref="classes")

    def remaining_sessions(self):
        i = len(self.sessions)
        for session in self.sessions:
            if date.today() > session.date:
                i -= 1

        return i

    class Meta:
        table_name = "classes"

class ClassRosterEntry(BaseModel):
    student = ForeignKeyField(Student, backref="class_list")
    school_class = ForeignKeyField(SchoolClass, backref="roster")

    class Meta:
        table_name = "class_rosters"

class Session(BaseModel):
    name = CharField(max_length=64)
    date = DateField()
    cancelled = BooleanField()
    school_class = ForeignKeyField(SchoolClass, backref="sessions")

    class Meta:
        table_name = "sessions"

class SessionAttendance(BaseModel):
    student = ForeignKeyField(Student, backref="session_attendance")
    session = ForeignKeyField(Session, backref="attendance")
    recorded_by = ForeignKeyField(Staff, backref="recorded_attendance")
    value = CharField(max_length=1)

    class Meta:
        table_name = "attendance"

## To Do talk to steve about grading