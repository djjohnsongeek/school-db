from app.models.db_models import Staff
from app.models.enums import StaffRole

def retrieve_all():
    return Staff.select()