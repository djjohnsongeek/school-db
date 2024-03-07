from app.models.db_models import SchoolClass, Session, Staff, Student, Term

def retrieve_all() -> []:
    return SchoolClass.select(SchoolClass, Staff, Term).join(Staff).switch(SchoolClass).join(Term)