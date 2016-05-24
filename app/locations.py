import json
from geopy.distance import vincenty
from geopy.geocoders import googlev3
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import psycopg2
import configparser
from app.configuration.secrets import user, password

Config = configparser.ConfigParser()
Config.read('app/configuration/config.cfg')
Base = declarative_base()


class Location(Base):
    __tablename__ = 'location'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=True)
    address = Column(String(1000), nullable=True)
    city = Column(String(50), nullable=True)
    state = Column(String(50), nullable=True)
    country = Column(String(50), nullable=True)
    postal_code = Column(String(50), nullable=True)
    timezone = Column(String(50), nullable=True)
    lat = Column(Float(precision=32), nullable=True)
    lon = Column(Float(precision=32), nullable=True)

    # set limit for a valid separation in meters
    valid_sep = 20
    g_api_key = Config.get("google_geo", "api_key")

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

class Airport(Base):
    __tablename__ = 'airport'
    code = Column(String, primary_key=True)
    location_id = Column(Integer, ForeignKey('location.id'))
    location = relationship("Location")
    terminal = Column(String, nullable=True)
    gate = Column(Integer, nullable=True)

    def __init__(self, code='', name='', city='', country='', timezone='',
                 lat=None, lng=None, terminal='', gate=''):
        self.code = code
        self.location = Location(name=name, city=city, country=country,
                                 timezone=timezone, lat=lat, lon=lng)
        self.terminal = terminal
        self.gate = gate

engine = create_engine('sqlite:///:memory:', echo=True)

#engine = create_engine("postgresql://" + user +
#                       ":" + password + "@" +
#                       Config.get("aws_postgres", "url") + ":" + Config.get("aws_postgres", "port") +
#                       "/" + Config.get("aws_postgres", "db"))

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

with open('app/data/airport.json') as data_file:
    data = json.load(data_file)
    for d in data:
        print(d)
        airport = Airport(code=d['code'], name=d['name'], city=d['city'], country=d['country'],
                          timezone=d['timezone'], lat=d['lat'], lng=d['lng'],
                          terminal=d['terminal'], gate=d['gate'])
        session.add(airport)
        print(airport.location.name)
session.commit()
session.close()

session = Session()

for airport, location in session.query(Airport, Location).\
        filter(Airport.location_id==Location.id).\
        filter(Location.country=='United States').\
        all():
    print(airport.code, airport.location.city, airport.location.lat, airport.location.lon)



#test_airport = Location('Station 125 Heliport', city='Calabasas', state='CA', country='USA', lat=34.1502831,
#                        lon=-120.6981436)
#test_airport = Location('AT&T Center', city='Los Angeles', state='CA', country='USA', lat=34.0397344,
#                        lon=-118.2284064)
#valid = test_airport.validate()
#if valid:
#    print("location validated for location {}".format(test_airport.name))
#else:
#    print("location not validated for location {}".format(test_airport.name))
#    print("location position is listed as lat={}, lon={}".format(test_airport.lat, test_airport.lon))
#    google_locs = test_airport.google_geo()
#    for google_loc in google_locs:
#        print("google gives this location lat={}, lon{}".format(google_loc.latitude, google_loc.longitude))
#        print(google_loc.address)
