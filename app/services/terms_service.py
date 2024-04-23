from app.repo import terms_repo
from app.models.view_models import TermItem, TermEditItem
from app.models.forms import TermEditForm
from app.models.db_models import Term

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

def retrieve_term(term_id: int) -> TermEditItem:
    term = terms_repo.retrieve(term_id)
    form = to_term_form(term)
    if form is not None:
        return TermEditItem(form)
    else:
        return None

def to_term_form(term_model: Term) -> TermEditForm:
    # convert to wtforms object
    form = None

    if term_model is not None:
        form = TermEditForm(
            id=term_model.id,
            name=term_model.name,
            start_date=term_model.start_date,
            end_date=term_model.end_date,
        )
    
    return form