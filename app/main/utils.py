from app.models import (Provider, Address, Appointment, 
                        QualificationDate, AppointmentMatch,
                        Patient)
from app import db
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
from sqlalchemy import or_


def geolocate(street, city, state, zipcode):
    geolocator = Nominatim(user_agent='hgh2023-cs6083')
    input_address = f'{street} {city} {state} {zipcode}'
    try:
        location_data = geolocator.geocode(input_address)
        latitude = location_data.latitude
        longitude = location_data.longitude
        return latitude, longitude
    except Exception:
        pass
    # If API can't find the street, try again without street
    try:
        input_address = f'{city} {state} {zipcode}'
        location_data = geolocator.geocode(input_address)
        latitude = location_data.latitude
        longitude = location_data.longitude
        return latitude, longitude
    except Exception:
        return None, None


# Appointment view for patients
def construct_appointment_payload(patient, appointment):
    # Get patient lat and long
    patient_address = Address.query.filter_by(address_id=patient.address_id).first()
    patient_coord = (patient_address.latitude, patient_address.longitude)
    # Get appointment lat and long
    provider = Provider.query.filter_by(provider_id=appointment.provider_id).first()
    appointment_address = Address.query.filter_by(address_id=provider.address_id).first()
    appointment_coord = (appointment_address.latitude, appointment_address.longitude)
    # Calculate distance between the two points
    distance = geodesic(patient_coord, appointment_coord).miles
    appointment_payload = {'appointment': appointment, 'provider': provider, 'distance': round(distance, 2), 'address': appointment_address}
    return appointment_payload


def find_matches(patient):
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
        if appointment_payload.get('distance', 10000) > patient.max_distance:
            continue
        appointments_by_distance.append(appointment_payload)
    return appointments_by_distance


# Method to match all patients with an appointment that fits their schedules
def appointment_matcher():
    all_patients = Patient.query.all()
    unvaccinated_patients = [p for p in all_patients if not p.is_vaccinated()]
    priority_groups = [i.priority_group for i in QualificationDate.query.all()]
    # Set default priority group to be the highest one for patients that aren't assigned yet
    default_group = max(priority_groups)
    # Organize unvaccinated patients by priority groups
    patients_by_group = {default_group: []}
    for p in unvaccinated_patients:
        # Check to see if patient already hass accepted or pending appointment match
        if p.appointment_matches.filter(
                or_(AppointmentMatch.offer_status=='accepted', 
                      AppointmentMatch.offer_status=='pending')).first():
            continue
        if p.priority_group:
            if patients_by_group.get(p.priority_group):
                patients_by_group[p.priority_group].append(p)
            else:
                patients_by_group[p.priority_group] = [p]
        else:
            patients_by_group[default_group].append(p)
    # Assign appointments to patients in order of priority groups
    for pg in range(1, default_group+1):
        qd = QualificationDate.query.filter_by(priority_group=pg).first().qualify_date
        qualification_datetime = datetime.utcnow().replace(year=qd.year).replace(month=qd.month).replace(day=qd.day).replace(hour=0)
        # Skip priority groups that don't qualify for a vaccine yet
        if qualification_datetime > datetime.utcnow():
            continue
        patients_in_group = patients_by_group.get(pg, [])
        for p in patients_in_group:
            appointment_options = find_matches(p)
            if appointment_options:
                selected_appointment = appointment_options[0]['appointment']
                # Create new appointment match
                new_match = AppointmentMatch(
                        appointment_id=selected_appointment.appointment_id,
                        patient_id=p.patient_id,
                        offer_status='pending',
                        time_offer_made=datetime.utcnow(),
                        time_offer_expires=datetime.utcnow()+timedelta(days=1)
                        )
                if selected_appointment.available:
                    selected_appointment.available = False
                    db.session.add(selected_appointment)
                    db.session.add(new_match)
                    db.session.commit()


# Method to unmatch expired offers
def unmatch_expired_offers():
    pending_matches = AppointmentMatch.query.filter_by(offer_status='pending').all()
    for match in pending_matches:
        if match.time_offer_expires < datetime.utcnow():
            appointment = match.matched_appointment
            match.offer_status = 'declined'
            db.session.add(match)
            appointment.available = True
            db.session.add(appointment)
            db.session.commit()

