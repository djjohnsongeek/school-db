from app.models.db_models import SchoolClass, Staff, Student
from app.models.base_models import Person
from app.models.enums import PersonGender, StaffRole
from app.models.forms import StaffEditForm, StudentEditForm

class ClassItem:
    def __init__(self, class_model: SchoolClass):
        self.id = class_model.id
        self.name = class_model.name
        self.term = class_model.term.name
        self.teacher_name = class_model.teacher.full_english_name()
        self.teacher_id = class_model.teacher.index
        self.room_number = class_model.room_number
        self.sessions_count = len(class_model.sessions)
        self.remaining_sessions_count = class_model.remaining_sessions()
        self.roster_count = len(class_model.roster)

class PersonItem:
    def __init__(self, person_model: Person):
        self.id = person_model.id
        self.name = person_model.full_name()
        self.nick_name = person_model.nick_name
        self.gender = PersonGender(person_model.gender)
        self.birthday = person_model.birthday.strftime("%d/%m/%Y")
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
    def __init__(self, staff_model: Staff, edit_form: StaffEditForm):
        self.fullname = staff_model.full_name()
        self.role = StaffRole(staff_model.role)
        self.classes = staff_model.classes
        self.form = edit_form

class StaffCreateItem():
    def __init__(self, edit_form: StaffEditForm):
        self.form = edit_form

class StudentEditItem():
    def __init__(self, student_model: Student, edit_form: StudentEditForm):
        self.fullname = student_model.full_name()
        # TODO need classes
        self.form = edit_form

class StudentCreateItem():
    def __init__(self, form: StudentEditForm):
        self.form = form

class AsyncJsResponseItem():
    def __init__(self, errors: [], data: dict):
        self.errors = errors
        self.data = data

    def to_dict(self) -> {}:
        return {
            "errors": self.errors,
            "data": self.data
        }