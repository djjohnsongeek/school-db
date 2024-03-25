from app.models.db_models import Staff
from app.models.forms import StaffEditForm

def retrieve_all() -> []:
    return Staff.select()

def retrieve(staff_id: int) -> Staff:
    return Staff.get_or_none(Staff.id == staff_id)

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