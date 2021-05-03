from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired  


class TimePreferenceForm(FlaskForm):
    time_options = SelectMultipleField('Hold shift when clicking to select mutliple time blocks in a row. Hold ctrl when clicking to add another time block without losing previously clicked blocks.', choices=[])
    submit = SubmitField('Add Time Preferences')







