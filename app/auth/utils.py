from app.models import Appointment
from app.main.utils import construct_appointment_payload

from geopy.geocoders import Nominatim


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
