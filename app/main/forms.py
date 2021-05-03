from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, 
                     SubmitField, SelectMultipleField,
                     DateTimeField)
from wtforms.validators import ValidationError, DataRequired  


class TimePreferenceForm(FlaskForm):
    time_options = SelectMultipleField('Hold shift when clicking to select mutliple time blocks in a row. Hold ctrl when clicking to add another time block without losing previously clicked blocks.', choices=[])
    submit = SubmitField('Add Time Preferences')


class CreateAppointmentForm(FlaskForm):
    appointment_time = DateTimeField('Appointment Time', 
            format='%m-%d-%Y %H:%M',
            validators=[DataRequired()])
    submit = SubmitField('Create')







