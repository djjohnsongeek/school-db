from peewee import *
# Base classes, not to be directly used as DB Models

class BaseModel(Model):
    id = AutoField()

    class Meta:
        legacy_table_names = False

class SoftDelete(BaseModel):
    deleted = BooleanField(null=False, default=False)

# Only first_name, last_name, and gender
class Person(SoftDelete):
    first_name_lao = CharField(max_length=128, null=True)
    last_name_lao = CharField(max_length=128, null=True)
    first_name = CharField(max_length=128)
    last_name = CharField(max_length=128)
    nick_name = CharField(max_length=128, null=True)
    gender = IntegerField(null=False)
    phone_number = CharField(max_length=32, null=True)
    birthday = DateField(null=True)
    email = CharField(max_length=64, null=True)
    address = CharField(max_length=128, null=True)

    def full_english_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def full_lao_name(self) -> str:
        return f"{self.first_name_lao} {self.last_name_lao}"

    def full_name(self) -> str:
        eng_name = self.full_english_name().replace(" ", "")
        lao_name = self.full_lao_name().replace(" ", "")

        if lao_name == "" and eng_name != "":
            return self.full_english_name()
        elif eng_name == "" and lao_name != "":
            return self.full_lao_name()
        elif lao_name != "" and eng_name != "":
            return f"{self.full_lao_name()} ({self.full_english_name()})"
        else:
            return ""