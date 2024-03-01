from app.models.db_models import SchoolClass

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

class StaffItem:
    def __init__(self, staff_model):
        self.id = staff_model.id
        self.name = staff_model.full_name()
        self.nick_name = staff_model.nick_name
        self.role = staff_model.get_role()
        self.gender = staff_model.gender
        self.birthday = staff_model.birthday.strftime("%d/%m/%Y")
        self.phone_number = staff_model.phone_number
        self.address = staff_model.address