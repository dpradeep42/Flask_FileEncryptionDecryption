from flask_wtf import FlaskForm
from wtforms import SubmitField, TextField


class ReadPath(FlaskForm):
    path = TextField('File Path')
    submit = SubmitField('Submit')