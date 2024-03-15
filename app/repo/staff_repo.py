from app.models.db_models import Staff
from app.models.forms import StaffEditForm

def retrieve_all() -> []:
    return Staff.select()

def retrieve(staff_id: int) -> Staff:
    return Staff.get_or_none(Staff.id == staff_id)


def update(form: StaffEditForm) -> bool:

    return True

    # return Staff.update(

    # )