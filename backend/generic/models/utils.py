from datetime import datetime


class TimestampMixin(object):
    def __init__(self):
        self.created_date = datetime.utcnow()
        self.last_updated = datetime.utcnow()



class Location(TimestampMixin):
    def __init__(self, coordinates, country, city, postal_code, address):
        super().__init__()
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

    def add_data(self, user_id=None, institution_id=None, company_id=None, internship_id=None):
        if user_id and user_id not in self.users:
            self.users.append(user_id)
        if institution_id and institution_id not in self.institutions:
            self.institutions.append(institution_id)
        if company_id and company_id not in self.companies:
            self.companies.append(company_id)
        if internship_id and internship_id not in self.internships:
            self.internships.append(internship_id)

    def remove_data(self, user_id=None, institution_id=None, company_id=None, internship_id=None):
        if user_id and user_id in self.users:
            self.users.remove(user_id)
        if institution_id and institution_id in self.institutions:
            self.institutions.remove(institution_id)
        if company_id and company_id in self.companies:
            self.companies.remove(company_id)
        if internship_id and internship_id in self.internships:
            self.internships.remove(internship_id)

    def save(self, mongo):
        mongo.db.locations.insert_one(self.to_dict())

    @classmethod
    def put(cls, mongo, location):
        mongo.db.locations.insert_one(location.to_dict())

    @classmethod
    def put_multi(cls, mongo, locations):
        mongo.db.locations.insert_many([location.to_dict() for location in locations])
