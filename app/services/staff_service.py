from app.repo import staff_repo
from app.models.view_models import StaffItem
from app.models.db_models import Staff

def get_staff_list() -> []:
    staff_models = staff_repo.retrieve_all()
    return [StaffItem(model) for model in staff_models]

def get_staff(staff_id: int): # need type hint
    staff = staff_repo.retrieve(staff_id)
    

    # retreive staff from the databse
    # check for none
    # return staff_form
    pass


def to_staff_form(staff_model: Staff): #need type hint
    # convert to wtforms object
    if staff_model is not None:
        pass
    else:
        return None