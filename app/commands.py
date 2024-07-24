from app.db import get_db, db_models
from app.models.db_models import Staff, Student, Term, SchoolClass, ClassRosterEntry, Attendance
from app.models.enums import StaffRole, PersonGender
from datetime import date
from werkzeug.security import generate_password_hash
import click

def init_db(no_populate):
    db = get_db()
    db.connect()

    # Prepare db schema
    db.drop_tables(db_models)
    db.create_tables(db_models)

    if no_populate is False:
        # Insert Staff
        Staff.insert(
            first_name_lao="ດານີເອນ",
            last_name_lao="ຈອນສັນ",
            first_name="Daniel",
            last_name="Johnson",
            nick_name="DJ",
            gender=int(PersonGender.Male.value),
            phone_number="803 840 5077",
            username="djohnson",
            hashed_password=generate_password_hash("password"),
            email="danieleejohnson@gmail.com",
            birthday=date.fromisoformat("1992-05-25"),
            address="Midway, NC 27107",
            role=StaffRole.Staff.value,
            is_admin=True
        ).execute()

        teacher = Staff.create(
            first_name_lao=None,
            last_name_lao=None,
            first_name="Rebecca",
            last_name="Johnson",
            nick_name=None,
            gender=int(PersonGender.Female.value),
            phone_number="336 972 5897",
            username="rjohnson",
            hashed_password=generate_password_hash("password"),
            email="rebeccalbobo@gmail.com",
            birthday=date.fromisoformat("1992-05-12"),
            address="Midway, NC 27103",
            role=StaffRole.Teacher.value,
        )

        # Insert Students
        student_1 = Student.create(
            first_name_lao="ອາລານາ",
            last_name_lao="ພົນນາສາ",
            first_name="Alana",
            last_name="Phonasa",
            nick_name="Bird",
            gender=int(PersonGender.Female.value),
            phone_number="856 000 000 0000",
            birthday=date.fromisoformat("1992-05-12"),
            email="alana@gmail.com",
            address="Phon Xay Rd",
            student_number="01022024",
            application_date=date.fromisoformat("2024-02-22"),
            occupation="Unknown"
        )

        student_2 = Student.create(
            first_name_lao="ເກສອນ",
            last_name_lao="ໄຊຍະວົງ",
            first_name="Kesone",
            last_name="Sayavong",
            nick_name="Rock",
            gender=int(PersonGender.Male.value),
            phone_number="856 000 000 0000",
            birthday=date.fromisoformat("1994-05-25"),
            email="Kesone@gmail.com",
            address="Xon Xay Rd",
            student_number="02022024",
            application_date=date.fromisoformat("2024-02-22"),
            occupation="None"
        )

        Student.insert(
            first_name_lao="ເອນ",
            last_name_lao="ຍະວົງ",
            first_name="KEvin",
            last_name="Ser",
            nick_name="Romble",
            gender=int(PersonGender.Male.value),
            phone_number="000 000 0000",
            birthday=date.fromisoformat("1999-07-03"),
            email="rombie@gmail.com",
            address="SOme Rd",
            student_number="03022024",
            application_date=date.fromisoformat("2024-01-22"),
            occupation="None"
        ).execute()

        Student.insert(
            first_name_lao="ເກສ",
            last_name_lao="ໄຊຍະ",
            first_name="Kent",
            last_name="Sungman",
            nick_name="Rin",
            gender=int(PersonGender.Male.value),
            phone_number="000 000 0000",
            birthday=date.fromisoformat("2005-04-10"),
            email="rin@gmail.com",
            address="Unknown",
            student_number="04022024",
            application_date=date.fromisoformat("2024-02-01"),
            occupation="None"
        ).execute()

        # Insert terms
        term = Term.create(
            name="Fall 2024",
            start_date=date.fromisoformat("2024-08-01"),
            end_date=date.fromisoformat("2024-12-01")
        )

        term_2 = Term.create(
            name="Spring 2025",
            start_date=date.fromisoformat("2025-01-01"),
            end_date=date.fromisoformat("2025-05-01")
        )

        # Insert classes, store a few for later
        algebra = SchoolClass.create(
            name='Algebra 1',
            room_number=5,
            teacher=teacher,
            term=term_2
        )

        physics = SchoolClass.create(
            name="Physics",
            room_number=12,
            teacher=teacher,
            term=term_2
        )

        SchoolClass.insert(
            name="English",
            room_number=9,
            teacher=teacher,
            term=term_2
        ).execute()

        # Fill out the class roster
        ClassRosterEntry.insert(
            student = student_1,
            school_class = algebra,
        ).execute()

        ClassRosterEntry.insert(
            student = student_2,
            school_class = algebra,
        ).execute()

        ClassRosterEntry.insert(
            student = student_1,
            school_class = physics
        ).execute()

        ClassRosterEntry.insert(
            student = student_2,
            school_class = physics
        ).execute()

        # Student 1 Attendance Records
        Attendance.insert(
            school_class=algebra,
            date=date.fromisoformat("2024-07-24"),
            student=student_1,
            value="P",
            recorded_by=teacher
        ).execute()

        Attendance.insert(
            school_class=algebra,
            date=date.fromisoformat("2024-07-25"),
            student=student_1,
            value="T",
            recorded_by=teacher
        ).execute()

        Attendance.insert(
            school_class=algebra,
            date=date.fromisoformat("2024-07-26"),
            student=student_1,
            value="A",
            recorded_by=teacher
        ).execute()

        # Student 2 Attendance Records
        Attendance.insert(
            school_class=algebra,
            date=date.fromisoformat("2024-07-24"),
            student=student_2,
            value="P",
            recorded_by=teacher
        ).execute()

        Attendance.insert(
            school_class=algebra,
            date=date.fromisoformat("2024-07-25"),
            student=student_2,
            value="P",
            recorded_by=teacher
        ).execute()

        Attendance.insert(
            school_class=algebra,
            date=date.fromisoformat("2024-07-26"),
            student=student_2,
            value="P",
            recorded_by=teacher
        ).execute()

        Attendance.insert(
            school_class=physics,
            date=date.fromisoformat("2024-07-24"),
            student=student_2,
            value="P",
            recorded_by=teacher
        ).execute()

        Attendance.insert(
            school_class=physics,
            date=date.fromisoformat("2024-07-25"),
            student=student_2,
            value="T",
            recorded_by=teacher
        ).execute()

        Attendance.insert(
            school_class=physics,
            date=date.fromisoformat("2024-07-26"),
            student=student_2,
            value="A",
            recorded_by=teacher
        ).execute()

    db.close()

def init_app_commands(app):
    app.cli.add_command(init_db_command)

@click.command("init-db")
@click.option("--no-populate", is_flag=True)
def init_db_command(no_populate):
    init_db(no_populate)
    click.echo("Database Initialized ...")
    if not no_populate:
        click.echo("Database Populated ...")