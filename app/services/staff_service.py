from app.repo import staff_repo
from app.models.view_models import StaffItem
from app.models.db_models import Staff
from app.models.forms import StaffEditForm

def get_staff_list() -> []:
    staff_models = staff_repo.retrieve_all()
    return [StaffItem(model) for model in staff_models]

def get_staff(staff_id: int) -> StaffEditForm:
    staff = staff_repo.retrieve(staff_id)
    form = to_staff_form(staff)
    return form

def to_staff_form(staff_model: Staff) -> StaffEditForm:
    # convert to wtforms object
    if staff_model is not None:
        form = StaffEditForm(
            first_name=staff_model.first_name,
            last_name=staff_model.first_namelast_name,
            first_name_lao=staff_model.first_name_lao,
            last_name_lao=staff_model.last_name_lao,
            nickname=staff_model.nick_name,
            gender=staff_model.gender,
            role=staff_model.role,
            email=staff_model.email,
            username=staff_model.username,
            phone_number=staff_model.phone_number,
            address=staff_model.address,
            birthday=staff_model.birthday,
        )

        return form
    else:
        return None