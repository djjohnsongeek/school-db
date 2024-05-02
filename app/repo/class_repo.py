from app.models.db_models import SchoolClass, Session, Staff, Student, Term
from app.models.forms import ClassEditForm
from datetime import datetime

def retrieve_all() -> []:
    return SchoolClass.select(SchoolClass, Staff, Term).join(Staff).switch(SchoolClass).join(Term)

def retrieve_current_or_future(staff: Staff) -> []:
    now = datetime.now()
    query = (SchoolClass
        .select(SchoolClass, Staff, Term)
        .join(Term)
        .switch(SchoolClass)
        .join(Staff)
        .where((SchoolClass.term.end_date > now) & (SchoolClass.teacher.id == staff.id)))
    
    return query

def retrieve_by_term(term: Term) -> []:
    now = datetime.now()
    query = (SchoolClass
        .select()
        .join(Term)
        .where(SchoolClass.term.id == term.id))

    return query

def create_class(form: ClassEditForm, teacher: Staff, term: Term) -> bool:
    try:
        primary_key = SchoolClass.insert(
            name = form.name.data,
            room_number = form.room_number.data,
            term = term,
            teacher = teacher
        ).execute()

        return primary_key > -1
    except Exception as e:
        print(e)
        # TODO LOG THIS ERROR
        return False