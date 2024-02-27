from app.models.db_models import SchoolClass

class ClassItem:
    def __init__(self, class_model):
        self.name = class_model.name
        self.term = class_model.term.name
        self.teacher_name = class_model.teacher.full_english_name()
        self.teacher_id = class_model.teacher.index
        self.room_number = class_model.room_number
        self.sessions_count = len(class_model.sessions)
        self.remaining_sessions_count = class_model.remaining_sessions()
        self.roster_count = len(class_model.roster)