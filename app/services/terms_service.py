from app.repo import terms_repo
from app.models.view_models import TermItem

def get_list():
    return [TermItem(model) for model in terms_repo.retrieve_all()]