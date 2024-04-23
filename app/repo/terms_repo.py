from app.models.db_models import Term
from app.models.forms import TermEditForm
from datetime import datetime

def retrieve_all():
    return Term.select()

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
        print(e)
        # TODO LOG THIS ERROR
        return False