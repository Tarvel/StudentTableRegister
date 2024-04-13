from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, Email


class StudentForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    gender = RadioField ('Gender:', choices=[('male', 'Male'), ('female', 'Female')])
    state = SelectField ('State', choices=[('kwara', 'Kwara'), ('lagos', 'Lagos'), ('kogi', 'Kogi'), ('oyo', 'Oyo')])
    submit = SubmitField('Create')

class DeleteForm(FlaskForm):
    delete = SubmitField('Delete')