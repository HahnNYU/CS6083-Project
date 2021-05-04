from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, 
                     SubmitField, DateField, IntegerField)
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import UserLogin, Patient


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign in')


class PatientRegistrationForm(FlaskForm):
    # Fields for UserLogin
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', 
            validators=[DataRequired(), EqualTo('password')])
    # Fields for Address
    street = StringField('Street', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    zipcode = StringField('Zip Code', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    # Fields for Patient
    name = StringField('Patient Name', validators=[DataRequired()])
    ssn = StringField('SSN')
    date_of_birth = DateField('Date of Birth', format='%m-%d-%Y', validators=[DataRequired()])
    phone = StringField('Phone Number')
    email = StringField('Email', validators=[DataRequired(), Email()])
    max_distance = IntegerField('Max Travel Distance', validators=[DataRequired()])

    submit = SubmitField('Register')

    def validate_username(self, username):
        user_login = UserLogin.query.filter_by(username=username.data).first()
        if user_login is not None:
            raise ValidationError('That username is already taken. Please use a different username.')

    def validate_email(self, email):
        patient = Patient.query.filter_by(email=email.data).first()
        if patient is not None:
            raise ValidationError('That email is already taken. Please use a difference email address.')


class ProviderRegistrationForm(FlaskForm):
    # Fields for UserLogin
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', 
            validators=[DataRequired(), EqualTo('password')])
    # Fields for Address
    street = StringField('Street', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    zipcode = StringField('Zip Code', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    # Fields for Provider
    name = StringField('Provider Name', validators=[DataRequired()])
    phone = StringField('Phone Number')
    provider_type = StringField('Provider Type')

    submit = SubmitField('Register')

    def validate_username(self, username):
        user_login = UserLogin.query.filter_by(username=username.data).first()
        if user_login is not None:
            raise ValidationError('That username is already taken. Please use a different username.')
