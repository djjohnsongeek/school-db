from peewee import *
# Base classes, not to be directly used as DB Models

class BaseModel(Model):
    id = AutoField()

    class Meta:
        legacy_table_names = False

class Person(BaseModel):
    first_name_lao = CharField(max_length=128, null=True)
    last_name_lao = CharField(max_length=128, null=True)
    first_name = CharField(max_length=128)
    last_name = CharField(max_length=128)
    nick_name = CharField(max_length=128, null=True)
    gender = IntegerField(null=False)
    phone_number = CharField(max_length=32)
    birthday = DateField()
    email = CharField(max_length=64, unique=True)
    address = CharField(max_length=128)

    def full_english_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def full_lao_name(self) -> str:
        return f"{self.first_name_lao} {self.last_name_lao}"

    def full_name(self) -> str:
        return f"{self.full_lao_name()} ({self.full_english_name()})"