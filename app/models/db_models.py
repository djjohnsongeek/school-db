import os
from peewee import *

class BaseModel(Model):
    id = AutoField()

    class Meta:
        legacy_table_names = False

class Student(BaseModel):
    first_name_lao = CharField(max_length=128)
    last_name_lao = CharField(max_length=128)
    first_name = CharField(max_length=128)
    last_name = CharField(max_length=128)
    birthday = DateField()
    email = CharField(max_length=64, unique=True)