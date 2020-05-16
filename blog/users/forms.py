from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from flask_login import current_user
from blog.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password = StringField("Password:", validators=[DataRequired(), EqualTo("confirm_pass", message="Passwords must match")])
    confirm_pass = StringField("Confirm password:", validators=[DataRequired()])
    submit = SubmitField("Register")

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Your email has already been registered!")

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Your username has already been registered!")


class UpdateUserForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired(), Email()])
    picture = FileField("Update profile picture:", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Update")

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Your email has already been registered!")

class LoginForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password = StringField("Password:", validators=[DataRequired()])
    submit = SubmitField("Log in")