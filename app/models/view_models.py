from app.models.db_models import SchoolClass
from app.models.enums import PersonGender, StaffRole

class ClassItem:
    def __init__(self, class_model):
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
    def __init__(self, person_model):
        self.id = person_model.id
        self.name = person_model.full_name()
        self.nick_name = person_model.nick_name
        self.gender = PersonGender(person_model.gender)
        self.birthday = person_model.birthday.strftime("%d/%m/%Y")
        self.phone_number = person_model.phone_number
        self.address = person_model.address

class StaffItem(PersonItem):
    def __init__(self, staff_model):
        super().__init__(staff_model)
        self.role = StaffRole(staff_model.role)

class StudentItem(PersonItem):
    def __init__(self, student_model):
        super().__init__(student_model)
        self.occupation = student_model.occupation
        self.application_date = student_model.application_date.strftime("%d/%m/%Y")
        self.student_number = student_model.student_number