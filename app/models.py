from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


class UserLogin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<UserLogin {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return UserLogin.query.get(int(id))


class QualificationDate(db.Model):
    # id number = number of priority group
    id = db.Column(db.Integer, primary_key=True)
    qualify_date = db.Column(db.Date)

    def __repr__(self):
        return f'<QualificationDate {self.id}: {self.qualify_date}>'


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(120))
    city = db.Column(db.String(80))
    zipcode = db.Column(db.String(30))
    state = db.Column(db.String(30))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __repr__(self):
        return f'<Address {self.street}, {self.city} {self.state}>'


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(80))
    ssn = db.Column(db.String(11))
    date_of_birth = db.Column(db.Date)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    phone = db.Column(db.String(30))
    email = db.Column(db.String(80))
    priority_group = db.Column(db.Integer, db.ForeignKey('qualificationdate.id'), default=None)
    login_id = db.Column(db.Integer, db.ForeignKey('userlogin.id'))
    max_distance = db.Column(db.Integer)
    appointment_matches = db.relatioship('AppointmentMatch', backref='patient', lazy='dynamic')
    time_preferences = db.relationship(
            'TimeBlockOptions', secondary=time_preference,
            backref=db.backref('patients', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return f'<Patient {self.patient_name}>'


class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider_name = db.Column(db.String(80))
    phone = db.Column(db.String(30))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    provider_type = db.Column(db.String(80))
    login_id = db.Column(db.Integer, db.ForeignKey('userlogin.id'))
    appointments = db.relationship('Appointment', backref='created_by', lazy='dynamic')

    def __repr__(self):
        return f'<Provider {self.provider_name}>'


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    appointment_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    appointment = db.Column(db.Boolean, default=True)
    appointment_matches = db.relatioship('AppointmentMatch', backref='appointment', lazy='dynamic')

    def __repr__(self):
        return f'<Appointment {self.provider_id}: {self.appointment_time}>'


class TimeBlockOptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_block_start = db.Column(db.Time, nullable=False)
    time_block_end = db.Column(db.Time, nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False) # day_of_week represents Sunday(0) to Saturday(6)
    patients = db.relationship(
            'Patient', secondary=time_preference,
            backref=db.backref('time_blocks', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return f'<TimeBlockOptions {day_of_week}: {time_block_start}-{time_block_end}>'


# TimePreferences association table relation
time_preference = db.Table('timepreference',
        db.Column('patient_id', db.Integer, db.ForeignKey('patient.id')),
        db.Column('time_block_id', db.Integer, db.ForeignKey('timeblockoptions.id'))
    )


class AppointmentMatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    offer_status = db.Column(db.String(20))
    time_offer_made = db.Column(db.DateTime)
    time_offer_expires = db.Column(db.DateTime)

    def __repr__(self):
        return f'<AppointmentMatch {patient_id}: {offer_status}>'
