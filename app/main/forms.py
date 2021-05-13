from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, IntegerField, 
                     SubmitField, SelectMultipleField,
                     DateTimeField, DateField, SelectField)
from wtforms.validators import ValidationError, DataRequired, Email
from app.models import UserLogin, Patient



STATE_OPTIONS = [
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY')
        ]


class TimePreferenceForm(FlaskForm):
    time_options = SelectMultipleField('Hold shift when clicking to select mutliple time blocks in a row. Hold ctrl when clicking to add another time block without losing previously clicked blocks.', choices=[])
    submit = SubmitField('Add Time Preferences')


class CreateAppointmentForm(FlaskForm):
    appointment_time = DateTimeField('Appointment Time', 
            format='%m-%d-%Y %H:%M',
            validators=[DataRequired()])
    submit = SubmitField('Create')


class EditPatientProfileForm(FlaskForm):
    # Fields for UserLogin
    username = StringField('Username', validators=[DataRequired()])
    # Fields for Address
    street = StringField('Street', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    zipcode = StringField('Zip Code', validators=[DataRequired()])
    state = SelectField('State', choices=STATE_OPTIONS, validators=[DataRequired()])
    # Fields for Patient
    name = StringField('Patient Name', validators=[DataRequired()])
    ssn = StringField('SSN')
    date_of_birth = DateField('Date of Birth', format='%m-%d-%Y', validators=[DataRequired()])
    phone = StringField('Phone Number')
    email = StringField('Email', validators=[DataRequired(), Email()])
    max_distance = IntegerField('Max Travel Distance', validators=[DataRequired()])

    submit = SubmitField('Update')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditPatientProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user_login = UserLogin.query.filter_by(username=username.data).first()
            if user_login is not None:
                raise ValidationError('That username is already taken. Please use a different username.')

    def validate_email(self, email):
        if email.data != self.original_email:
            patient = Patient.query.filter_by(email=email.data).first()
            if patient is not None:
                raise ValidationError('That email is already taken. Please use a difference email address.')


class UpdatePriorityForm(FlaskForm):
    priority_options = SelectField('New Priority Group', choices=[], validators=[DataRequired()])
    submit = SubmitField('Update Priority Group')





