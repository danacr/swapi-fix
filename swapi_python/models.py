import json
import time

import six
from utils import query


class BaseModel(object):

    def __init__(self, raw_data):
        json_data = json.loads(raw_data)
        for key, value in six.iteritems(json_data):
            setattr(self, key, value)


class BaseQuerySet(object):

    def __init__(self):
        self.items = []


class StarshipQuerySet(BaseQuerySet):

    def __init__(self, list_of_urls):
        super(StarshipQuerySet, self).__init__()
        for url in list_of_urls:
            response = query(url)
            self.items.append(Starship(response.content))

    def __repr__(self):
        return '<StarshipQuerySet - {0}>'.format(str(len(self.items)))


class Starship(BaseModel):

    def __init__(self, raw_data):
        super(Starship, self).__init__(raw_data)

    def __repr__(self):
        return '<Starship - {0}>'.format(self.name)


class VehicleQuerySet(BaseQuerySet):

    def __init__(self, list_of_urls):
        super(VehicleQuerySet, self).__init__()
        for url in list_of_urls:
            response = query(url)
            self.items.append(Vehicle(response.content))

    def __repr__(self):
        return '<VehicleQuerySet - {0}>'.format(str(len(self.items)))


class Vehicle(BaseModel):

    def __init__(self, raw_data):
        super(Vehicle, self).__init__(raw_data)

    def __repr__(self):
        return '<Vehicle - {0}>'.format(self.name)


class FilmQuerySet(BaseQuerySet):

    def __init__(self, list_of_urls):
        super(FilmQuerySet, self).__init__()
        for url in list_of_urls:
            response = query(url)
            self.items.append(Film(response.content))

    def __repr__(self):
        return '<StarshipQuerySet - {0}>'.format(str(len(self.items)))


class Film(BaseModel):

    def __init__(self, raw_data):
        super(Film, self).__init__(raw_data)

    def __repr__(self):
        return '<Film - {0}>'.format(self.title)

    def get_starships(self):
        return StarshipQuerySet(self.starships)

    def get_characters(self):
        return PeopleQuerySet(self.people)

    def get_vehicles(self):
        return VehicleQuerySet(self.vehicles)

    def get_planets(self):
        return PlanetQuerySet(self.planets)

    def get_species(self):
        return SpeciesQuerySet(self.species)

    def gen_crawl(self):
        ''' Return a generator yielding each line of the opening crawl'''
        for line in self.opening_crawl.split('\n'):
            yield line

    def print_crawl(self):
        ''' Print the opening crawl one line at a time '''
        for line in self.gen_crawl():
            time.sleep(.5)
            print line


class PlanetQuerySet(BaseQuerySet):

    def __init__(self, list_of_urls):
        super(PlanetQuerySet, self).__init__()
        for url in list_of_urls:
            response = query(url)
            self.items.append(Planet(response.content))

    def __repr__(self):
        return '<StarshipQuerySet - {0}>'.format(str(len(self.items)))


class Planet(BaseModel):

    def __init__(self, raw_data):
        super(Planet, self).__init__(raw_data)

    def __repr__(self):
        return '<Planet - {0}>'.format(self.name)


class SpeciesQuerySet(BaseQuerySet):

    def __init__(self, list_of_urls):
        super(SpeciesQuerySet, self).__init__()
        for url in list_of_urls:
            response = query(url)
            self.items.append(Species(response.content))

    def __repr__(self):
        return '<StarshipQuerySet - {0}>'.format(str(len(self.items)))


class Species(BaseModel):

    def __init__(self, raw_data):
        super(Species, self).__init__(raw_data)

    def __repr__(self):
        return '<Species - {0}>'.format(self.name)


class PeopleQuerySet(BaseQuerySet):

    def __init__(self, list_of_urls):
        super(PeopleQuerySet, self).__init__()
        for url in list_of_urls:
            response = query(url)
            self.items.append(People(response.content))

    def __repr__(self):
        return '<PeopleQuerySet - {0}>'.format(str(len(self.items)))


class People(BaseModel):
    ''' Representing a single person '''

    def __init__(self, raw_data):
        super(People, self).__init__(raw_data)
        # patch this because it is buggy
        self.species = self.species[0]

    def __repr__(self):
        return '<Person - {0}>'.format(self.name)

    def get_starships(self):
        return StarshipQuerySet(self.starships)

    def get_films(self):
        return FilmQuerySet(self.films)

    def get_vehicles(self):
        return VehicleQuerySet(self.vehicles)

    def get_homeworld(self):
        response = query(self.homeworld)
        return Planet(response.content)

    def get_species(self):
        response = query(self.species)
        return Species(response.content)