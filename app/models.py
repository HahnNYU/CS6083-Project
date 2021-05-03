from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


class UserLogin(UserMixin, db.Model):
    __tablename__ = 'userlogin'
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
    __tablename__ = 'qualificationdate'
    priority_group = db.Column(db.Integer, primary_key=True)
    qualify_date = db.Column(db.Date)

    def __repr__(self):
        return f'<QualificationDate {self.priority_group}: {self.qualify_date}>'


class Address(db.Model):
    __tablename__ = 'address'
    address_id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(120))
    city = db.Column(db.String(80))
    zipcode = db.Column(db.String(30))
    state = db.Column(db.String(30))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __repr__(self):
        return f'<Address {self.street}, {self.city} {self.state}>'


# TimePreferences association table relation
time_preference = db.Table('timepreference',
        db.Column('patient_id', db.Integer, db.ForeignKey('patient.patient_id')),
        db.Column('time_block_id', db.Integer, db.ForeignKey('timeblockoptions.time_block_id'))
    )


class Patient(db.Model):
    __tablename__ = 'patient'
    patient_id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(80))
    ssn = db.Column(db.String(11))
    date_of_birth = db.Column(db.Date)
    address_id = db.Column(db.Integer, db.ForeignKey('address.address_id'))
    phone = db.Column(db.String(30))
    email = db.Column(db.String(80))
    priority_group = db.Column(db.Integer, db.ForeignKey('qualificationdate.priority_group'), default=None)
    login_id = db.Column(db.Integer, db.ForeignKey('userlogin.id'))
    max_distance = db.Column(db.Integer)
    appointment_matches = db.relationship('AppointmentMatch', backref='matched_patient', lazy='dynamic')
    time_preferences = db.relationship(
            'TimeBlockOptions', secondary=time_preference,
            backref=db.backref('patients', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return f'<Patient {self.patient_name}>'

    def add_time(self, time_block):
        if not self.has_time_block(time_block):
            self.time_preferences.append(time_block)

    def has_time_block(self, time_block):
        return self.time_preferences.filter(
            time_preference.c.time_block_id==time_block.time_block_id).count() > 0

class Provider(db.Model):
    __tablename__ = 'provider'
    provider_id = db.Column(db.Integer, primary_key=True)
    provider_name = db.Column(db.String(80))
    phone = db.Column(db.String(30))
    address_id = db.Column(db.Integer, db.ForeignKey('address.address_id'))
    provider_type = db.Column(db.String(80))
    login_id = db.Column(db.Integer, db.ForeignKey('userlogin.id'))
    appointments = db.relationship('Appointment', backref='created_by', lazy='dynamic')

    def __repr__(self):
        return f'<Provider {self.provider_name}>'


class Appointment(db.Model):
    __tablename__ = 'appointment'
    appointment_id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.provider_id'), nullable=False)
    appointment_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    appointment = db.Column(db.Boolean, default=True)
    appointment_matches = db.relationship('AppointmentMatch', backref='matched_appointment', lazy='dynamic')

    def __repr__(self):
        return f'<Appointment {self.provider_id}: {self.appointment_time}>'


class TimeBlockOptions(db.Model):
    __tablename__ = 'timeblockoptions'
    time_block_id = db.Column(db.Integer, primary_key=True)
    time_block_start = db.Column(db.Time, nullable=False)
    time_block_end = db.Column(db.Time, nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False) # day_of_week represents Monday(0) to Sunday(6)

    def __repr__(self):
        return f'<TimeBlockOptions {self.day_of_week}: {self.time_block_start} to {self.time_block_end}>'

    def __str__(self):
        dow_mapping = {
                0: 'Monday',
                1: 'Tuesday',
                2: 'Wednesday',
                3: 'Thursday',
                4: 'Friday',
                5: 'Saturday',
                6: 'Sunday'
            }
        dow = dow_mapping.get(self.day_of_week)
        start = self.time_block_start.hour
        end = self.time_block_end.hour
        if start >= 12:
            p_start = 'PM'
            if start > 12:
                start = start - 12
        else:
            p_start = 'AM'
        if end >= 12:
            p_end = 'PM'
            if end > 12:
                end = end - 12
        else:
            p_end = 'AM'

        return f'{dow}, {start}:00{p_start} to {end}:00{p_end}'


class AppointmentMatch(db.Model):
    __tablename__ = 'appointmentmatch'
    match_id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.appointment_id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable=False)
    offer_status = db.Column(db.String(20))
    time_offer_made = db.Column(db.DateTime)
    time_offer_expires = db.Column(db.DateTime)

    def __repr__(self):
        return f'<AppointmentMatch {self.patient_id}: {self.offer_status}>'
