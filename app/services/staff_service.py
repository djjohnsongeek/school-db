from app.repo import staff_repo
from app.models.view_models import StaffItem

def get_staff_list():
    staff_models = staff_repo.retrieve_all()
    return [StaffItem(model) for model in staff_models]