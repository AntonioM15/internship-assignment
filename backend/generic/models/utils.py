from datetime import datetime


class TimestampMixin(object):
    def __init__(self):
        self.created_date = datetime.utcnow()
        self.last_updated = datetime.utcnow()


class Location:
    def __init__(self, coordinates, country, city, postal_code, address):
        self.coordinates = coordinates
        self.country = country
        self.city = city
        self.postal_code = postal_code
        self.address = address

        # Keys from other collections
        self.users = []
        self.institutions = []
        self.companies = []
        self.internships = []

    def to_dict(self):
        return self.__dict__

    def add_data_to_location(self, user=None, institution=None, company=None, internship=None):
        if user and user not in self.users:
            self.users.append(user)
        if institution and institution not in self.institutions:
            self.institutions.append(institution)
        if company and company not in self.companies:
            self.companies.append(company)
        if internship and internship not in self.internships:
            self.internships.append(internship)

    def remove_data_from_location(self, user=None, institution=None, company=None, internship=None):
        if user and user not in self.users:
            self.users.remove(user)
        if institution and institution not in self.institutions:
            self.institutions.remove(institution)
        if company and company not in self.companies:
            self.companies.remove(company)
        if internship and internship not in self.internships:
            self.internships.remove(internship)

    def save(self, mongo):
        mongo.db.locations.insert_one(self.to_dict())

    @classmethod
    def put(cls, mongo, location):
        mongo.db.locations.insert_one(location.to_dict())

    @classmethod
    def put_multi(cls, mongo, locations):
        mongo.db.locations.insert_many([location.to_dict() for location in locations])
