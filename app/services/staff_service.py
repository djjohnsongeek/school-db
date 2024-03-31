from app.repo import staff_repo
from app.models.view_models import StaffItem, StaffEditItem
from app.models.db_models import Staff
from app.models.forms import StaffEditForm
from werkzeug.security import generate_password_hash

def get_staff_list() -> []:
    staff_models = staff_repo.retrieve_all()
    return [StaffItem(model) for model in staff_models]

def get_staff(staff_id: int) -> StaffEditItem:
    staff = staff_repo.retrieve(staff_id)

    if staff is not None:
        form = to_staff_form(staff)
        return StaffEditItem(staff, form)
    else:
        return None

def to_staff_form(staff_model: Staff) -> StaffEditForm:
    # convert to wtforms object
    if staff_model is not None:
        form = StaffEditForm(
            staff_id=staff_model.id,
            first_name=staff_model.first_name,
            last_name=staff_model.last_name,
            first_name_lao=staff_model.first_name_lao,
            last_name_lao=staff_model.last_name_lao,
            nick_name=staff_model.nick_name,
            gender=staff_model.gender,
            role=staff_model.role,
            email=staff_model.email,
            username=staff_model.username,
            phone_number=staff_model.phone_number,
            address=staff_model.address,
            birthday=staff_model.birthday,
        )
    
    return form if staff_model is not None else None

def update_staff(form: StaffEditForm) -> StaffEditItem:
    staff_model = staff_repo.retrieve(int(form.staff_id.data))

    if staff_model is not None and form.validate():
        result = staff_repo.update(form, staff_model)
        form = to_staff_form(staff_model)
    elif staff_model is None:
        return None

    return StaffEditItem(staff_model, form)

def create_staff(form: StaffEditForm) -> []:
    errors = []
    if not form.validate():
        errors.append("New staff member could not be created.")
    else:
        # TODO: Password requirements, generate password
        result = staff_repo.create(form, generate_password_hash("place-holder-password"))
        if not result:
            errors.append("Failed to create new staff member.")

    return errors