from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.models import (TimeBlockOptions, Patient, Appointment, 
                        Provider, Address)
from app.main.forms import TimePreferenceForm, CreateAppointmentForm

import pytz
from geopy.distance import geodesic


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html', title='Home Page')


@bp.route('/time_preference', methods=['GET','POST'])
@login_required
def time_preference():
    if current_user.user_type != 'Patient':
        flash('Only patients can view that page')
        return redirect(url_for('main.index')) 
    else:
        form = TimePreferenceForm()
        # get all choices in TimeBlockOptions relation
        form.time_options.choices = [(str(option.time_block_id), str(option)) for option in TimeBlockOptions.query.all()]
        # get patient linked to user login creds
        patient = Patient.query.filter_by(login_id=current_user.id).first()
        if form.validate_on_submit():
            # Associate each selected time block with the patient
            for time_id in form.time_options.data: 
                time_block = TimeBlockOptions.query.filter_by(time_block_id=int(time_id)).first()
                patient.add_time(time_block)
            db.session.commit()
        time_preferences = [t for t in patient.time_preferences]
        return render_template('time_preference.html', title='Patient Time Preference', form=form, time_preferences=time_preferences)


@bp.route('/remove_time/<time_block_id>')
@login_required
def remove_time(time_block_id):
    if current_user.user_type != 'Patient':
        flash('Only patients can view that page')
        return redirect(url_for('main.index')) 
    else:
        # Get patient
        patient = Patient.query.filter_by(login_id=current_user.id).first()
        # Get time block
        time_block = TimeBlockOptions.query.filter_by(time_block_id=int(time_block_id)).first()
        # Remove association between time block and patient
        patient.remove_time(time_block)
        db.session.commit()
    return redirect(url_for('main.time_preference'))


@bp.route('/create_appointment', methods=['GET','POST'])
@login_required
def create_appointment():
    if current_user.user_type != 'Provider':
        flash('Only providers can view that page')
        return redirect(url_for('main.index'))
    else:
        form = CreateAppointmentForm()
        # Get provider
        provider = Provider.query.filter_by(login_id=current_user.id).first()
        if form.validate_on_submit():
            # Convert datetime to UTC
            eastern = pytz.timezone('US/Eastern')
            utc = pytz.utc
            appointment_time = eastern.localize(form.appointment_time.data) 
            utc_appointment_time = appointment_time.astimezone(utc)
            # Create new appointment
            appointment = Appointment(provider_id=provider.provider_id, appointment_time=utc_appointment_time) 
            db.session.add(appointment)
            db.session.commit()
            return redirect(url_for('main.create_appointment'))
        appointments = provider.appointments
        return render_template('create_appointment.html', title='Create Appointment', form=form, appointments=appointments)


@bp.route('/available_appointments')
@login_required
def available_appointments():
    if current_user.user_type != 'Patient':
        flash('Only patients can view that page')
        return redirect(url_for('main.index')) 
    else:
        # get patient linked to user login creds
        patient = Patient.query.filter_by(login_id=current_user.id).first()
        time_blocks = patient.time_preferences
        # get all available appointments
        available_appointments = Appointment.query.filter_by(available=True).all()
        # filter appointments based on patient's time preferences
        appointment_options = []
        for a in available_appointments:
            for t in time_blocks:
                if a.appointment_time.weekday() != t.day_of_week:
                    continue
                if (a.appointment_time.time() >= t.time_block_start 
                        and a.appointment_time.time() < t.time_block_end):
                    appointment_options.append(a)
                    break
        # filter appointments based on distance
        appointments_by_distance = []
        # get patient lat and long
        patient_address = Address.query.filter_by(address_id=patient.address_id).first()
        patient_coord = (patient_address.latitude, patient_address.longitude)
        for a in appointment_options:
            # get appointment lat and long
            provider = Provider.query.filter_by(provider_id=a.provider_id).first()
            appointment_address = Address.query.filter_by(address_id=provider.address_id).first()
            appointment_coord = (appointment_address.latitude, appointment_address.longitude)
            # calculate distance between the two points
            distance = geodesic(patient_coord, appointment_coord).miles
            if distance > patient.max_distance:
                continue
            appointment_payload = {'appointment': a, 'provider': provider, 'distance': round(distance, 2), 'address': appointment_address}
            appointments_by_distance.append(appointment_payload)
        # sort appointments by distance
        appointments_by_distance.sort(key=lambda x: x.get('distance'))
        return render_template('available_appointments.html', appointments=appointments_by_distance)


