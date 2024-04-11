from datetime import datetime
from wtforms import ValidationError

class StudentNumber(object):
    def __init__(self, message=None):
        if not message:
            message = "The format for this student number is invalid."
        self.message = message

    def __call__(self, form, field):
        valid = True
        student_number = field.data

        if student_number is None:
            raise ValidateError

        year = int(student_number[-4:])
        month = int(student_number[-6:][:2])

        valid = (student_number.isdigit() and
                len(student_number) >= 8 and len(student_number) < 33 and
                year <= datetime.now().year and year > 2023
                and month > 0 and month < 13)

        if not valid:
            raise ValidationError(self.message)