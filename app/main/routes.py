from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.models import (TimeBlockOptions, Patient, Appointment, 
                        Provider, Address, AppointmentMatch)
from app.main.forms import (TimePreferenceForm, 
                            CreateAppointmentForm,
                            EditPatientProfileForm)
from app.main.utils import construct_appointment_payload, geolocate
from sqlalchemy import or_

import pytz
from datetime import datetime


@bp.route('/')
@bp.route('/home')
def index():
    appointment_data = {'accepted': 0, 
                        'pending': 0,
                        'declined': 0,
                        'cancelled': 0,
                        'no show': 0,
                        'vaccinated': 0
                       }
    provider = None
    patient = None
    if current_user.is_anonymous:
        pass
    elif current_user.user_type == 'Patient':
        patient = Patient.query.filter_by(login_id=current_user.id).first()
    elif current_user.user_type == 'Provider':
        provider = Provider.query.filter_by(login_id=current_user.id).first()
        appointments = provider.appointments
        for apt in appointments:
            matches = apt.appointment_matches
            for match in matches:
                appointment_data[match.offer_status] += 1

    return render_template('index.html', title='Home Page', appointment_data=appointment_data, provider=provider, patient=patient)


@bp.route('/time_preference', methods=['GET','POST'])
@login_required
def time_preference():
    if current_user.user_type != 'Patient':
        flash('Only patients can view that page')
        return redirect(url_for('main.index')) 
    else:
        form = TimePreferenceForm()
        # Get all choices in TimeBlockOptions relation
        form.time_options.choices = [(str(option.time_block_id), str(option)) for option in TimeBlockOptions.query.all()]
        # Get patient linked to user login creds
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
        return render_template('create_appointment.html', title='Create Appointment', form=form)


@bp.route('/view_appointments', methods=['GET','POST'])
@login_required
def view_appointments():
    if current_user.user_type != 'Provider':
        flash('Only providers can view that page')
        return redirect(url_for('main.index'))
    else:
        provider = Provider.query.filter_by(login_id=current_user.id).first()
        appointments = [{'appointment': a} for a in provider.appointments]
        for apt_dict in appointments:
            apt = apt_dict['appointment']
            # Check if appointment has an active match
            match = apt.appointment_matches.filter(
                            or_(AppointmentMatch.offer_status=='accepted', 
                                    AppointmentMatch.offer_status=='pending')).first()
            if match:
                apt_dict['match'] = match
        return render_template('view_appointments.html', title='View Appointments', appointments=appointments)


@bp.route('/available_appointments')
@login_required
def available_appointments():
    if current_user.user_type != 'Patient':
        flash('Only patients can view that page')
        return redirect(url_for('main.index')) 
    else:
        # Get patient linked to user login creds
        patient = Patient.query.filter_by(login_id=current_user.id).first()
        time_blocks = patient.time_preferences
        # Get all available appointments
        available_appointments = Appointment.query.filter_by(available=True).all()
        # Filter appointments based on patient's time preferences
        appointment_options = []
        for a in available_appointments:
            for t in time_blocks:
                if a.appointment_time.weekday() != t.day_of_week:
                    continue
                if (a.appointment_time.time() >= t.time_block_start 
                        and a.appointment_time.time() < t.time_block_end):
                    appointment_options.append(a)
                    break
        # Filter appointments based on distance
        appointments_by_distance = []
        for a in appointment_options:
            appointment_payload = construct_appointment_payload(patient, a)
            if appointment_payload.get('distance', 1000) > patient.max_distance:
                continue
            appointments_by_distance.append(appointment_payload)
        # Sort appointments by distance
        appointments_by_distance.sort(key=lambda x: x.get('distance'))
        return render_template('available_appointments.html', title='Available Appointments', appointments=appointments_by_distance)


@bp.route('/select_appointment/<appointment_id>')
@login_required
def select_appointment(appointment_id):
    if current_user.user_type != 'Patient':
        flash('Only patients can view that page')
        return redirect(url_for('main.index')) 
    else:
        # Get patient
        patient = Patient.query.filter_by(login_id=current_user.id).first()
        # Check if patient already has an accepted appointment
        if AppointmentMatch.query.filter_by(offer_status='accepted').filter_by(patient_id=patient.patient_id).first():
            flash('You cannot register for more than one appointment. Please cancel any other appointments before registering for a new one') 
            return redirect(url_for('main.available_appointments')) 
        elif AppointmentMatch.query.filter_by(offer_status='pending').filter_by(patient_id=patient.patient_id).first():
            flash('You cannot register for an appointment while you have a pending suggested appointment. Please decline your suggested appointment before registering for a new one') 
            return redirect(url_for('main.manage_appointment')) 
        # Get appointment
        appointment = Appointment.query.filter_by(appointment_id=appointment_id).first()
        # Create AppointmentMatch with status 'accepted'
        new_match = AppointmentMatch(appointment_id=appointment_id, patient_id=patient.patient_id, offer_status='accepted', time_offer_made=datetime.utcnow())
        # Check if appointment is still available
        if appointment.available:
            appointment.available = False
            db.session.add(appointment)
            db.session.add(new_match)
            db.session.commit()
            flash(f'You successfully registered for the appointment on {appointment} at {appointment.created_by.provider_name}')
        else:
            flash('Sorry, the appointment you tried to register for is no longer available')
        return redirect(url_for('main.available_appointments')) 


@bp.route('/manage_appointment')
@login_required
def manage_appointment():
    if current_user.user_type != 'Patient':
        flash('Only patients can view that page')
        return redirect(url_for('main.index')) 
    else:
        # Get patient
        patient = Patient.query.filter_by(login_id=current_user.id).first()
        # Get appointment matches if any
        accepted_match = patient.appointment_matches.filter_by(offer_status='accepted').first()
        accepted_match_payload = {}
        suggested_match_payload = {}
        if accepted_match:
            appointment = accepted_match.matched_appointment
            accepted_match_payload = construct_appointment_payload(patient, appointment)
            accepted_match_payload['match'] = accepted_match
        else:
        # Get suggested appointment if one exists
            suggested_match = patient.appointment_matches.filter_by(offer_status='pending').first()
            if suggested_match:
                appointment = suggested_match.matched_appointment
                suggested_match_payload = construct_appointment_payload(patient, appointment)
                suggested_match_payload['match'] = suggested_match

        return render_template('manage_appointment.html', title='Manage Appointment', accepted_match=accepted_match_payload, suggested_match=suggested_match_payload)


@bp.route('/cancel_appointment/<match_id>')
@login_required
def cancel_appointment(match_id):
    if current_user.user_type != 'Patient':
        flash('Only patients can view that page')
        return redirect(url_for('main.index')) 
    else:
        current_match = AppointmentMatch.query.filter_by(match_id=match_id).first()
        current_appointment = current_match.matched_appointment
        # Cancel current match and add change to db session
        current_match.offer_status = 'cancelled'
        db.session.add(current_match)
        # Make cancelled appointment available and add change to db session
        current_appointment.available = True
        db.session.add(current_appointment)
        # Commit the db session
        db.session.commit()
        flash('You have successfully cancelled your appointment.')
        return redirect(url_for('main.manage_appointment'))


@bp.route('/accept_appointment/<match_id>')
@login_required
def accept_appointment(match_id):
    if current_user.user_type != 'Patient':
        flash('Only patients can view that page')
        return redirect(url_for('main.index')) 
    else:
        match = AppointmentMatch.query.filter_by(match_id=match_id).first()
        match.offer_status = 'accepted'
        db.session.add(match)
        db.session.commit()
        flash('You have successfully accepted the appointment')
        return redirect(url_for('main.manage_appointment'))


@bp.route('/decline_appointment/<match_id>')
@login_required
def decline_appointment(match_id):
    if current_user.user_type != 'Patient':
        flash('Only patients can view that page')
        return redirect(url_for('main.index')) 
    else:
        match = AppointmentMatch.query.filter_by(match_id=match_id).first()
        appointment = match.matched_appointment
        match.offer_status = 'declined'
        db.session.add(match)
        appointment.available = True
        db.session.add(appointment)
        db.session.commit()
        flash('You have successfully declined the appointment')
        return redirect(url_for('main.manage_appointment'))


@bp.route('/edit_patient_profile', methods=['GET','POST'])
@login_required
def edit_patient_profile():
    if current_user.user_type != 'Patient':
        flash('Only pateints can view that page')
        return redirect(url_for('main.index'))
    else:
        patient = Patient.query.filter_by(login_id=current_user.id).first()
        address = Address.query.filter_by(address_id=patient.address_id).first()
        form = EditPatientProfileForm(current_user.username, patient.email)
        if form.validate_on_submit():
            # Update login data
            current_user.username = form.username.data
            # Update address data
            address.street = form.street.data
            address.city = form.city.data
            address.zipcode = form.zipcode.data
            address.state = form.state.data
            latitude, longitude = geolocate(address.street, address.city, address.state, address.zipcode)
            address.latitude = latitude
            address.longitude = longitude
            # Update patient data
            patient.patient_name = form.name.data
            patient.ssn = form.ssn.data
            patient.date_of_birth = form.date_of_birth.data
            patient.phone = form.phone.data
            patient.email = form.email.data
            patient.max_distance = form.max_distance.data
            db.session.add_all([current_user, patient, address])
            db.session.commit()
            flash('Your profile changes have been saved')
            return redirect(url_for('main.edit_patient_profile'))
        elif request.method=='GET':
            # Initialize login data
            form.username.data = current_user.username
            # Initialize address data
            form.street.data = address.street
            form.city.data = address.city
            form.zipcode.data = address.zipcode
            form.state.data = address.state
            # Initialize patient data
            form.name.data = patient.patient_name
            form.ssn.data = patient.ssn
            form.date_of_birth.data = patient.date_of_birth
            form.phone.data = patient.phone
            form.email.data = patient.email
            form.max_distance.data = patient.max_distance
        return render_template('edit_patient_profile.html', title='Edit Profile', form=form)
