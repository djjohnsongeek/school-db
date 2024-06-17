from app.models.db_models import SchoolClass, ClassSession, Staff, Student, Term
from app.models.forms import ClassEditForm
from datetime import datetime

def retrieve_all() -> []:
    return SchoolClass.select(SchoolClass, Staff, Term).join(Staff).switch(SchoolClass).join(Term)

def retrieve(class_id: int) -> SchoolClass:
        return (SchoolClass
            .select()
            .join_from(SchoolClass, Staff)
            .join_from(SchoolClass, Term)
            .where(SchoolClass.id == class_id)
            .get())

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

def session_count(class_id: int) -> int:
    return ClassSession.select().join(SchoolClass).where(ClassSession.school_class.id == class_id).count()

def create_session(class_model: SchoolClass, request_data: dict) -> ClassSession:
    print(request_data)
    try:
        class_session = ClassSession.create(
            name = request_data["session_name"],
            date = request_data["session_time"],
            cancelled = False,
            school_class = class_model
        )
        return class_session
    except Exception as e:
        print(e)
        # TODO LOG THIS ERROR
        return None

def update(form: ClassEditForm, class_model: SchoolClass) -> bool:
    class_model.name = form.name.data
    class_model.room_number = form.room_number.data
    class_model.teacher = form.teacher_id.data
    class_model.term = form.term_id.data

    return class_model.save() > 0