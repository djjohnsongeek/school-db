from app.repo import student_repo
from app.models.view_models import StudentItem

def get_student_list() -> []:
    students = student_repo.retrieve_all()
    return [StudentItem(student) for student in students]