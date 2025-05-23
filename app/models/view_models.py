from app.models.db_models import SchoolClass, Staff, Student, ClassRosterEntry, Term, SchoolClass, Attendance
from app.models.base_models import Person
from app.models.enums import PersonGender, StaffRole
from app.models.forms import StaffEditForm, StudentEditForm, TermEditForm, ClassEditForm

class PersonItem:
    def __init__(self, person_model: Person):
        self.id = person_model.id
        self.name = person_model.full_name()
        self.nick_name = person_model.nick_name
        self.gender = PersonGender(person_model.gender)
        self.birthday = person_model.birthday.strftime("%d/%m/%Y") if person_model.birthday is not None else ""
        self.phone_number = person_model.phone_number
        self.address = person_model.address
        self.email = person_model.email

class StaffItem(PersonItem):
    def __init__(self, staff_model: Staff):
        super().__init__(staff_model)
        self.role = StaffRole(staff_model.role)

class StudentItem(PersonItem):
    def __init__(self, student_model: Student):
        super().__init__(student_model)
        self.occupation = student_model.occupation
        self.application_date = student_model.application_date.strftime("%d/%m/%Y")
        self.student_number = student_model.student_number

class StaffEditItem():
    def __init__(self, staff_model: Staff, edit_form: StaffEditForm, edit_errors: []):
        self.fullname = staff_model.full_name()
        self.role = StaffRole(staff_model.role)
        self.classes = staff_model.classes
        self.form = edit_form
        self.edit_errors = edit_errors

class StaffCreateItem():
    def __init__(self, edit_form: StaffEditForm):
        self.form = edit_form

class StudentEditItem():
    def __init__(self, student_model: Student, edit_form: StudentEditForm, attendance: {}, classes: [], edit_errors: []):
        self.fullname = student_model.full_name()
        self.classes = classes
        self.attendance = attendance
        self.form = edit_form
        self.edit_errors = edit_errors

class StudentCreateItem():
    def __init__(self, form: StudentEditForm):
        self.form = form

class StudentClassItem():
    def __init__(self, class_info: ClassRosterEntry):
        self.class_id = class_info.school_class.id
        self.term = class_info.school_class.term.name
        self.name = class_info.school_class.name
        self.final_grade = class_info.final_grade
        self.record_id = class_info.id

class AsyncJsResponseItem():
    def __init__(self, errors: [], data: dict):
        self.errors = errors
        self.data = data

    def to_dict(self) -> {}:
        return {
            "errors": self.errors,
            "data": self.data
        }

class TermItem():
    def __init__(self, term: Term):
        self.id = term.id
        self.start_date = term.start_date
        self.end_date = term.end_date
        self.name = term.name

class TermEditItem():
    def __init__(self, term: Term, form: TermEditForm, edit_errors: []):
        self.term = term
        self.form = form
        self.edit_errors = edit_errors

