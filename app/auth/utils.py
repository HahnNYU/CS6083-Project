from app.models import Appointment
from app.main.utils import construct_appointment_payload, geolocate


def register_geolocate(street, city, state, zipcode):
    return geolocate(street, city, state, zipcode)


def appointment_matcher(patient):
    # TODO: improve this algorithm
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
    if appointments_by_distance:
        return appointments_by_distance[0].get('appointment')
    else:
        return None
