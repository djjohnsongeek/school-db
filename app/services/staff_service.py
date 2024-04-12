from app.repo import staff_repo, class_repo
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
        return StaffEditItem(staff, form, [])
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

    # validation
    if staff_model is None:
        return None

    errors = []
    if form.email.data != staff_model.email and staff_repo.email_exists(form.email.data):
        errors.append("The email supplied is already in use.")

    if form.username.data != staff_model.username and staff_repo.username_exists(form.username.data):
        errors.append("The username supplied is already in use.")

    if not form.validate():
        errors.append("Invalid data detected. No changes have been saved.")

    if len(errors) == 0:
        result = staff_repo.update(form, staff_model)
        form = to_staff_form(staff_model)

    return StaffEditItem(staff_model, form, errors)

def create_staff(form: StaffEditForm) -> []:
    errors = []
    username_exists = staff_repo.username_exists(form.username.data)
    email_exists = staff_repo.email_exists(form.email.data)

    if username_exists or email_exists:
        errors.append("This email address or username is already in use.")

    # we manually set the id so it will pass validatoin
    # the id is not used to insert
    form.staff_id.data = 1
    if not form.validate():
        errors.append("Invalid data detected. A new staff member was not created.")

    if len(errors) == 0:
        # TODO: Password requirements, generate password
        result = staff_repo.create(form, generate_password_hash("place-holder-password"))
        if not result:
            errors.append("Failed to create new staff member.")

    return errors

# Removes staff from the dropdown list when assigning a class to a teacher
# Removes staff from the main list of staff
# Can later be restored (TODO)
def soft_delete(staff_id: int) -> []:
    errors = []
    staff = staff_repo.retrieve(staff_id)

    if staff is None:
        errors.append("Staff member was not found.")
    else:
        classes = class_repo.retrieve_current_or_future(staff)
        if classes.count() > 0:
            errors.append("This Teacher is teaching current or future classes and cannot be deleted.")

    if not errors:
        result = staff_repo.soft_delete(staff)
        if not result:
            errors.append("Failed to delete staff memeber")

    return errors
