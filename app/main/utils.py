from app.models import Provider, Address 
from geopy.distance import geodesic
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
