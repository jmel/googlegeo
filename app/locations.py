from geopy.distance import vincenty
from geopy.geocoders import googlev3


class Location:

    # set limit for a valid separation in meters
    valid_sep = 20
    g_api_key = 'AIzaSyBOSJD0EZZmq1AGvxx3pnmWzaCeBio_-vM'

    def __init__(self, name='', address='', city='', state='', country='', postal_code='', timezone=None,
                 lat=None, lon=None):
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.country = country
        self.postal_code = postal_code
        self.timezone = timezone
        self.lat = lat
        self.lon = lon

    # Method to validate location with Google Geocode
    def validate(self):

        locs = self.google_geo()
        for loc in locs:
            separation = vincenty((loc.latitude, loc.longitude), (self.lat, self.lon)).meters

            if separation < self.valid_sep:
                return True

        return False

    # Method to construct address for Google Geocode
    def construct_address(self):
        return self.name + "," + self.address + "," + self.city + "," + self.state + "," + self.country

    def google_geo(self):
        geo = googlev3.GoogleV3(self.g_api_key)
        return geo.geocode(self.construct_address(), exactly_one=False)


test_airport = Location('Station 125 Heliport', city='Calabasas', state='CA', country='USA', lat=34.1502831,
                        lon=-120.6981436)
test_airport = Location('AT&T Center', city='Los Angeles', state='CA', country='USA', lat=34.0397344,
                        lon=-118.2284064)
valid = test_airport.validate()
if valid:
    print("location validated for location {}".format(test_airport.name))
else:
    print("location not validated for location {}".format(test_airport.name))
    print("location position is listed as lat={}, lon={}".format(test_airport.lat, test_airport.lon))
    google_locs = test_airport.google_geo()
    for google_loc in google_locs:
        print("google gives this location lat={}, lon{}".format(google_loc.latitude, google_loc.longitude))
        print(google_loc.address)
