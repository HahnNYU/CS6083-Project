from app.main.utils import geolocate


def register_geolocate(street, city, state, zipcode):
    return geolocate(street, city, state, zipcode)
