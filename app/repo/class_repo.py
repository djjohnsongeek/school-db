from app.models.db_models import SchoolClass, Session, Staff, Student, Term
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