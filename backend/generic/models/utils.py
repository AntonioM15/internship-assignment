from datetime import datetime

AVAILABLE_STATUSES = ('unassigned', 'provisional', 'assigned', 'ongoing')
DEFAULT_STATUS = 'unassigned'


def serialize_document(doc):
    """ JSON friendly representation of documents"""
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    if "created_date" in doc:
        doc["created_date"] = doc["created_date"].isoformat()
    if "last_updated" in doc:
        doc["last_updated"] = doc["last_updated"].isoformat()
    if "sender" in doc:
        doc["sender"] = str(doc["sender"])
    if "receiver" in doc:
        doc["receiver"] = str(doc["receiver"])
    return doc


class TimestampMixin(object):
    def __init__(self):
        self.created_date = datetime.utcnow()
        self.last_updated = datetime.utcnow()

    def update_last_updated(self):
        self.last_updated = datetime.utcnow()

    @classmethod
    def update_last_updated_multi(cls, instances):
        last_updated = datetime.utcnow()
        for instance in instances:
            instance.last_updated = last_updated

    def to_dict(self):
        return self.__dict__


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
        self.update_last_updated()
        mongo.db.locations.insert_one(self.to_dict())

    @classmethod
    def put(cls, mongo, location):
        location.update_last_updated()
        mongo.db.locations.insert_one(location.to_dict())

    @classmethod
    def put_multi(cls, mongo, locations):
        cls.update_last_updated(locations)
        mongo.db.locations.insert_many([location.to_dict() for location in locations])


class Notification(TimestampMixin):
    def __init__(self, title, description, role, read=False, sender=None, receiver=None):
        super().__init__()
        self.title = title
        self.description = description
        self.role = role
        self.read = read

        # Keys from other collections
        self.sender = sender
        self.receiver = receiver

    def update_sender(self, sender_id):
        if not sender_id:
            return
        self.sender = sender_id

    def remove_sender(self):
        self.sender = None

    def update_receiver(self, receiver_id):
        if not receiver_id:
            return
        self.receiver = receiver_id

    def remove_receiver(self):
        self.receiver = None

    def save(self, mongo):
        self.update_last_updated()
        mongo.db.notifications.insert_one(self.to_dict())

    @classmethod
    def put(cls, mongo, notification):
        notification.update_last_updated()
        mongo.db.notifications.insert_one(notification.to_dict())

    @classmethod
    def put_multi(cls, mongo, notifications):
        cls.update_last_updated(notifications)
        mongo.db.notifications.insert_many([notification.to_dict() for notification in notifications])


class Observation(TimestampMixin):
    def __init__(self, text, creator=None, receiver=None):
        super().__init__()
        self.text = text

        # Keys from other collections
        self.creator = creator
        self.receiver = receiver

    def update_creator(self, creator_id):
        if not creator_id:
            return
        self.creator = creator_id

    def remove_creator(self):
        self.creator = None

    def update_receiver(self, receiver_id):
        if not receiver_id:
            return
        self.receiver = receiver_id

    def remove_receiver(self):
        self.receiver = None

    def save(self, mongo):
        self.update_last_updated()
        mongo.db.observations.insert_one(self.to_dict())

    @classmethod
    def put(cls, mongo, observation):
        observation.update_last_updated()
        mongo.db.observations.insert_one(observation.to_dict())

    @classmethod
    def put_multi(cls, mongo, observations):
        cls.update_last_updated(observations)
        mongo.db.observations.insert_many([observation.to_dict() for observation in observations])
