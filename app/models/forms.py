from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, EmailField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email, Length

class StaffEditForm(FlaskForm):
    staff_id = HiddenField(validators=[DataRequired()])
    first_name_lao = StringField("First Name", validators=[DataRequired(), Length(min=1, max=128)])
    last_name_lao = StringField("Last Name", validators=[DataRequired(),  Length(min=1, max=128)])
    first_name = StringField("First Name (English)", validators=[DataRequired(), Length(min=1, max=128)])
    last_name = StringField("Last Name (English)", validators=[DataRequired(), Length(min=1, max=128)])
    nick_name = StringField("Nickname", validators=[DataRequired(), Length(min=1, max=128)])
    birthday = DateField("Birthday", validators=[DataRequired()])
    gender = SelectField("Gender", validators=[DataRequired()], choices=[(1, "Male"), (2, "Female")], coerce=int)
    phone_number = StringField("Phone Number", validators=[DataRequired(), Length(min=1, max=32)])
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(min=1, max=64)])
    username = StringField("Username", validators=[DataRequired(), Length(min=8, max=64)])
    address = StringField("Address", validators=[DataRequired(),  Length(min=1, max=128)])
    role = SelectField("Role", validators=[DataRequired()], choices=[(1, "Teacher"), (2, "General")], coerce=int)