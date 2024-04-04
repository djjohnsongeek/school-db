from app.models.db_models import Student

def retrieve_all() -> []:
    return Student.select().where(Student.deleted == False)