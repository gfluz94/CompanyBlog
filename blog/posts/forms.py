from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired

class BlogForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    text = TextField("Title", validators=[DataRequired()])
    submit = SubmitField("Post")