from app.repo import terms_repo
from app.models.view_models import TermItem, TermCreateItem
from app.models.forms import TermEditForm

def get_list() -> []:
    return [TermItem(model) for model in terms_repo.retrieve_all()]

def create_term(form: TermEditForm) -> []:
    errors = []

    # We manually set the id so validation will pass
    # This value does not get used when inserting the new record
    form.term_id.data = 1
    if not form.validate():
        errors.append("Invalid data detected. A new term was not created.")

    if len(errors) == 0:
        result = terms_repo.create(form)
        if not result:
            errors.append("Failed to create new term.")

    return errors