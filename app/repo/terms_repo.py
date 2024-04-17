from app.models.db_models import Term
from datetime import datetime

def retrieve_all():
    return Term.select()