from app.repo import class_repo, terms_repo

## View Models ##
class AttendancePageModel:
    def __init__(self, selected_class, classes):
        self.classes = classes
        self.selected_class = selected_class

## Buisness Logic ##
def get_attendance_model(class_id: int):
    # TODO: set up some way to actually get the current term
    selected_class = class_repo.retrieve(class_id)
    current_term = selected_class.term
    classes = class_repo.retrieve_by_term(current_term)

    return AttendancePageModel(selected_class, classes)