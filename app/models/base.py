from peewee import *
# Base classes, not to be directly used as DB Models

class BaseModel(Model):
    id = AutoField()

    class Meta:
        legacy_table_names = False

class Person(BaseModel):
    first_name_lao = CharField(max_length=128)
    last_name_lao = CharField(max_length=128)
    first_name = CharField(max_length=128)
    last_name = CharField(max_length=128)
    nick_name = CharField(max_length=128)
    gender = CharField(max_length=1)
    phone_number = CharField(max_length=32)
    birthday = DateField()
    email = CharField(max_length=64, unique=True)
    address = CharField(max_length=128)