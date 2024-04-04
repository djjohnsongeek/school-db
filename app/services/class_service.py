from app.repo import class_repo
from app.models.view_models import ClassItem

def get_class_list() -> []:
    class_models = class_repo.retrieve_all()
    return [ClassItem(model) for model in class_models]