import os
from peewee import *
from app.models.base import Person, BaseModel

class Student(Person):
    student_number = CharField(max_length=32, unique=True)
    application_date = DateField()
    occupation = CharField(max_length=128)

class Staff(Person):
    hashed_password = CharField()
    pass