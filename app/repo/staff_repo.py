from app.models.db_models import Staff, SchoolClass
from app.models.forms import StaffEditForm
from app.models.enums import StaffRole
from app.services import log_service
from datetime import datetime

## SELECT
def retrieve_all() -> []:
    return Staff.select().where(Staff.deleted == False)

def retrieve(staff_id: int) -> Staff:
    return Staff.get_or_none(Staff.id == staff_id)

def retrieve_by_email(email: str) -> Staff:
    return Staff.get_or_none(Staff.email == email)

def retrieve_by_username(username: str) -> Staff:
    return Staff.get_or_none(Staff.username == username)

def retrieve_teachers() -> []:
    return Staff.select().where((Staff.role == int(StaffRole.Teacher)) & (Staff.deleted == False))

def email_exists(email: str) -> bool:
    staff = retrieve_by_email(email)
    return staff is not None

def username_exists(username: str) -> bool:
    staff = retrieve_by_username(username)
    return staff is not None

## UPDATE
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

def update_password(staff: Staff, hashed_pw: str) -> bool:
    staff.hashed_password = hashed_pw
    rows_updated = staff.save()
    return rows_updated == 1

def soft_delete(staff: Staff) -> bool:
    staff.deleted = True
    rows_updated = staff.save()
    return rows_updated == 1

## INSERT
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
        log_service.record_log(f"Failed to create staff: {e}", "staff_repo", "error")
        return False

