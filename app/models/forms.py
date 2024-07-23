from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, EmailField, SelectField, HiddenField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from app.models.validators import StudentNumber

class PersonForm(FlaskForm):
    first_name_lao = StringField("First Name", validators=[DataRequired(), Length(min=1, max=128)])
    last_name_lao = StringField("Last Name", validators=[DataRequired(),  Length(min=1, max=128)])
    first_name = StringField("First Name (English)", validators=[DataRequired(), Length(min=1, max=128)])
    last_name = StringField("Last Name (English)", validators=[DataRequired(), Length(min=1, max=128)])
    nick_name = StringField("Nickname", validators=[DataRequired(), Length(min=1, max=128)])
    birthday = DateField("Birthday", validators=[DataRequired()])
    gender = SelectField("Gender", validators=[DataRequired()], choices=[(1, "Male"), (2, "Female")], coerce=int)
    phone_number = StringField("Phone Number", validators=[DataRequired(), Length(min=1, max=32)])
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(min=1, max=64)])
    address = StringField("Address", validators=[DataRequired(),  Length(min=1, max=128)])

class StaffEditForm(PersonForm):
    staff_id = HiddenField(validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired(), Length(min=8, max=64)])
    role = SelectField("Role", validators=[DataRequired()], choices=[(1, "Teacher"), (2, "General")], coerce=int)

class StudentEditForm(PersonForm):
    student_id = HiddenField(validators=[DataRequired()])
    student_number = StringField("Student Number", validators=[DataRequired(), StudentNumber()])
    application_date = DateField("Application Date", validators=[DataRequired()])
    occupation = StringField("Occupation", validators=[DataRequired(), Length(min=1, max=128)])

class TermEditForm(FlaskForm):
    term_id = HiddenField(validators=[DataRequired()])
    name = StringField("Term Name", validators=[DataRequired()])
    start_date = DateField("Start Date", validators=[DataRequired()])
    end_date = DateField("End Date", validators=[DataRequired()])

class ClassEditForm(FlaskForm):
    class_id = HiddenField(validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    room_number = IntegerField("Room Number", validators=[DataRequired()])
    teacher_id = SelectField("Teacher", validators=[DataRequired()], coerce=int, choices=[])
    term_id = SelectField("Term", validators=[DataRequired()], coerce=int, choices=[])

class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])