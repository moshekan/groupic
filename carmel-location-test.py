from geopy.geocoders import Nominatim
geolocator = Nominatim()

def return_place(location):
	latitude, longitude = location
 	address = ""
	if latitude is not None:
		address = geolocator.reverse(latitude, longitude).address
	return address

