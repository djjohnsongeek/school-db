from app.models.db_models import Staff
from app.models.forms import StaffEditForm

def retrieve_all() -> []:
    return Staff.select()

def retrieve(staff_id: int) -> Staff:
    return Staff.get_or_none(Staff.id == staff_id)

def retrieve_by_email(email: str) -> Staff:
    return Staff.get_or_none(Staff.email == email)

def retrieve_by_username(username: str) -> Staff:
    return Staff.get_or_none(Staff.username == username)

def email_exists(email: str) -> bool:
    staff = retrieve_by_email(email)
    return staff is not None

def username_exists(username: str) -> bool:
    staff = retrieve_by_username(username)
    return staff is not None

def update(form: StaffEditForm, staff: Staff) -> bool:
    staff.first_name = form.first_name.data
    staff.first_name_lao = form.first_name_lao.data
    staff.last_name = form.last_name.data
    staff.last_name_lao = form.last_name_lao.data
    staff.username = form.username.data
    staff.email = form.email.data
    staff.nick_name = form.nick_name.data
    staff.phone_number = form.phone_number.data
    staff.address = form.address.data
    staff.birthday = form.birthday.data
    staff.gender = form.gender.data
    staff.role = form.role.data
    
    rows_updated = staff.save()
    return rows_updated == 1

def create(form: StaffEditForm, password: str) -> bool:
    try:
        primary_key = Staff.insert(
            first_name_lao=form.first_name_lao.data,
            last_name_lao=form.last_name_lao.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            nick_name=form.nick_name.data,
            gender=form.gender.data,
            phone_number=form.phone_number.data,
            username=form.username.data,
            hashed_password=password,
            email=form.email.data,
            birthday=form.birthday.data,
            address=form.address.data,
            role=form.role.data,
        ).execute()

        return primary_key > -1
    except Exception as e:
        print(e)
        # TODO LOG THIS ERROR
        return False

def soft_delete(staff: Staff) -> bool:
    pass