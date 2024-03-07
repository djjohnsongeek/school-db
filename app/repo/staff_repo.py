from app.models.db_models import Staff

def retrieve_all():
    return Staff.select()