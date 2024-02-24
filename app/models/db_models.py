import os
from peewee import *
from app.models.base import Person, BaseModel

class Student(Person):
    student_number = CharField(max_length=32, unique=True)
    application_date = DateField()
    occupation = CharField(max_length=128)

class Staff(Person):
    hashed_password = CharField(max_length=256)
    pass

class Term(BaseModel):
    name = CharField(max_length=64)

class SchoolClass(BaseModel):
    name = CharField(max_length=64)
    teacher = ForeignKeyField(Staff, backref="classes")
    room_number = IntegerField()

class ClassRosterItem(BaseModel):
    student = ForeignKeyField(Student, backref="class_list")
    school_class = ForeignKeyField(SchoolClass, backref="student_list")
    