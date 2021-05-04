from geopy.geocoders import Nominatim


def geolocate(street, city, state, zipcode):
    geolocator = Nominatim(user_agent='hgh2023-cs6083')
    input_address = f'{street} {city} {state} {zipcode}'
    try:
        location_data = geolocator.geocode(input_address)
        latitude = location_data.latitude
        longitude = location_data.longitude
    except Exception:
        latitude = longitude = None
    return latitude, longitude

