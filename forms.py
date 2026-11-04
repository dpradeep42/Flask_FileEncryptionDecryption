from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class ReadPath(FlaskForm):
    path = StringField('File Path')
    submit = SubmitField('Submit')
