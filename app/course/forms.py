from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class course_form(FlaskForm):
     course_code = StringField('CODE', validators=[DataRequired()])
     course_name = StringField('NAME', validators=[DataRequired(), Length(min=3, max=20)])
     submit = SubmitField("SUBMIT")
