import os
from peewee import *
from app.models.base_models import Person, BaseModel, SoftDelete
from app.models.enums import StaffRole
from datetime import date

class Student(Person):
    student_number = CharField(max_length=32)
    application_date = DateField()
    occupation = CharField(max_length=128, null=True)

    class Meta:
        table_name = "students"

class Staff(Person):
    username = CharField(max_length=64)
    hashed_password = CharField(max_length=256)
    role = IntegerField()
    is_admin = BooleanField(default=False)

    def full_name(self) -> str:
        if self.role == StaffRole.Teacher.value:
            return self.full_english_name()
        else:
            return super().full_name()
            
class LoginLog(BaseModel):
    staff = ForeignKeyField(Staff, backref="login_logs")
    time = DateTimeField()
    success = BooleanField()

    class Meta:
        table_name = "login_logs"

class Term(SoftDelete):
    name = CharField(max_length=128)
    start_date = DateField()
    end_date = DateField()

    class Meta:
        table_name = "terms"

class SchoolClass(BaseModel):
    name = CharField(max_length=64)
    room_number = IntegerField(null=True)
    teacher = ForeignKeyField(Staff, backref="classes")
    term = ForeignKeyField(Term, backref="classes")

    class Meta:
        table_name = "classes"

class ClassRosterEntry(BaseModel):
    student = ForeignKeyField(Student, backref="class_list")
    school_class = ForeignKeyField(SchoolClass, backref="roster")
    final_grade = DoubleField(null=True)

    class Meta:
        table_name = "class_rosters"

class Attendance(BaseModel):
    student = ForeignKeyField(Student, backref="attendance")
    school_class = ForeignKeyField(SchoolClass, backref="attendance")
    recorded_by = ForeignKeyField(Staff)
    date = DateField()
    value = CharField(max_length=1)

## To Do talk to steve about grading