from app.models import Provider, Address 
from geopy.distance import geodesic


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
