from app.db import get_db, db_models
from app.models.db_models import Staff, Student
from app.models.enums import StaffRole, PersonGender
from datetime import date
from werkzeug.security import generate_password_hash
import click

def init_db():
    db = get_db()
    db.connect()

    # Prepare db schema
    db.drop_tables(db_models)
    db.create_tables(db_models)

    # Insert Staff
    Staff.insert(
        first_name_lao="ດານີເອນ",
        last_name_lao="ຈອນສັນ",
        first_name="Daniel",
        last_name="Johnson",
        nick_name="DJ",
        gender=PersonGender.Male.name,
        phone_number="803 840 5077",
        username="djohnson",
        hashed_password=generate_password_hash("password"),
        email="danieleejohnson@gmail.com",
        birthday=date.today(),
        address="Midway, NC 27107",
        role=StaffRole.General.value,
    ).execute()

    Staff.insert(
        first_name_lao=None,
        last_name_lao=None,
        first_name="Rebecca",
        last_name="Johnson",
        nick_name=None,
        gender=PersonGender.Female.name,
        phone_number="336 972 5897",
        username="rjohnson",
        hashed_password=generate_password_hash("password"),
        email="rebeccalbobo@gmail.com",
        birthday=date.today(),
        address="Midway, NC 27103",
        role=StaffRole.Teacher.value,
    ).execute()

    # Insert Students
    Student.insert(
        first_name_lao="ອາລານາ",
        last_name_lao="ພົນນາສາ",
        first_name="Alana",
        last_name="Phonasa",
        nick_name="Bird",
        gender=PersonGender.Female.name,
        phone_number="856 000 000 0000",
        birthday=date.fromisoformat("1992-05-12"),
        email="alana@gmail.com",
        address="Phon Xay Rd",
        student_number="01022024",
        application_date=date.fromisoformat("2024-02-22"),
        occupation="Unknown"
    ).execute()

    Student.insert(
        first_name_lao="ເກສອນ",
        last_name_lao="ໄຊຍະວົງ",
        first_name="Kesone",
        last_name="Sayavong",
        nick_name="Rock",
        gender=PersonGender.Male.name,
        phone_number="856 000 000 0000",
        birthday=date.fromisoformat("1994-05-25"),
        email="Kesone@gmail.com",
        address="Xon Xay Rd",
        student_number="02022024",
        application_date=date.fromisoformat("2024-02-22"),
        occupation="None"
    ).execute()

    # todo: add test data

    db.close()

def init_app_commands(app):
    app.cli.add_command(init_db_command)

@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Database Initialized ...")