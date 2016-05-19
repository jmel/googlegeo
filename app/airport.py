import json
from app.locations import Location


class Airport:

    def __init__(self, code='', name='', city='', country='', timezone='',
                 lat=None, lng=None, terminal='', gate=''):
        self.code = code
        self.location = Location(name=name, city=city, country=country,
                                 timezone=timezone, lat=lat, lon=lng)
        self.terminal = terminal
        self.gate = gate

with open('data/airport.json') as data_file:
    data = json.load(data_file)
    for d in data:
        print(d)
        airport = Airport(code=d['code'], name=d['name'], city=d['city'], country=d['country'],
                          timezone=d['timezone'], lat=d['lat'], lng=d['lng'],
                          terminal=d['terminal'], gate=d['gate'])
        print(airport.location.name)
