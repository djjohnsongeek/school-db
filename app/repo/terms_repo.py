from app.models.db_models import Term
from app.models.forms import TermEditForm
from app.services import log_service
from datetime import datetime

def retrieve_all():
    return Term.select().where(Term.deleted == False)

def retrieve_current():
    now = datetime.now()
    return Term.select().where((Term.deleted == False) & (Term.end_date > now))

def retrieve(id: int):
    return Term.get_or_none(Term.id == id)

def create(form: TermEditForm):
    try:
        primary_key = Term.insert(
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            name=form.name.data
        ).execute()
        return primary_key > -1
    except Exception as e:
        log_service.record_log(f"Failed to create term: {e}", "terms_repo", "error")
        return False

def update(term_model: Term, form: TermEditForm) -> bool:
    term_model.end_date = form.end_date.data
    term_model.start_date = form.start_date.data
    term_model.name = form.name.data

    
    rows_updated = term_model.save()
    return rows_updated == 1

def soft_delete(term: Term) -> bool:
    term.deleted = True
    rows_updated = term.save()
    return rows_updated == 1