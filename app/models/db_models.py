import os
from peewee import *
from app.models.base import Person, BaseModel

#todo add table name meta

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
    term = ForeignKeyField(SchoolClass, backref="classes")

    class Meta:
        table_name = "classes"

class ClassRosterEntry(BaseModel):
    student = ForeignKeyField(Student, backref="class_list")
    school_class = ForeignKeyField(SchoolClass, backref="student_list")

    class Meta:
        table_name = "class_rosters"

    