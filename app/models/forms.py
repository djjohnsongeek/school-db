from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, HiddenInput, DateField, EmailField, SelectField
from wtforms.validators import DataRequired, Email

class StaffEditForm(FlaskForm):
    staff_id = IntegerField(widget=HiddenInput(), validators=[DataRequired()])
    first_name_lao = StringField("First Name", validators=[DataRequired()])
    last_name_lao = StringField("Last Name", validators=[DataRequired()])
    first_name = StringField("First Name (English)", validators=[DataRequired()])
    last_name = StringField("Last Name (English)", validators=[DataRequired()])
    nick_name = StringField("Nickname", validators=[DataRequired()])
    birthday = DateField("Birthday", validators=[DataRequired()])
    gender = SelectField("Gender", validators=[DataRequired()], choices=[(1, "Male"), (2, "Female")], coerce=int)
    phone_number = StringField("Phone Number", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    role = SelectField("Role", validators=[DataRequired()], choices=[(1, "Teacher"), (2, "General")], coerce=int)