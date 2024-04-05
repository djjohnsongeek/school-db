from app.models.db_models import Student

def retrieve_all() -> []:
    return Student.select().where(Student.deleted == False)

def retrieve(id: int) -> Student:
    return Student.get_or_none(Student.id == id)