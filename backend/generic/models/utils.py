from bson import ObjectId
from datetime import datetime
from pymongo import DESCENDING

AVAILABLE_STATUSES = ('unassigned', 'provisional', 'assigned', 'ongoing')
DEFAULT_STATUS = 'unassigned'

KEYS_WITH_OBJECT_IDS = ('_id', 'sender', 'creator', 'receiver', 'degree', 'location', 'institution', 'internship',
                        'student', 'worker', 'tutor', 'company')
KEYS_WITH_LIST_OF_OBJECT_IDS = ('notifications', 'observations', 'degrees', 'internships', 'students', 'workers',
                                'tutors', 'interns')
KEYS_WITH_DATES = ('created_date', 'last_updated', 'starting_day', 'finishing_day')


def serialize_document(doc):
    """ JSON friendly representation of documents """
    if not doc:
        return {}
    for key in doc:
        if key in KEYS_WITH_OBJECT_IDS and doc[key]:
            doc[key] = str(doc[key])
        elif key in KEYS_WITH_LIST_OF_OBJECT_IDS and doc[key]:
            doc[key] = [str(item) for item in doc[key]]
        elif key in KEYS_WITH_DATES and doc[key]:
            doc[key] = doc[key].isoformat()

    return doc


def str_date_to_datetime(date_str):
    if not date_str:
        return None
    return datetime.strptime(date_str, "%Y-%m-%d")


def to_object_id(value):
    if not value:
        return None
    if isinstance(value, ObjectId):
        return value
    return ObjectId(str(value))


def to_object_id_list(values):
    if not values:
        return []
    return [to_object_id(v) for v in values]



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
        self.coordinates = coordinates  # List of two float values to mimic decimal representation
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

    def save(self, mongo_db):
        self.update_last_updated()
        return mongo_db.locations.insert_one(self.to_dict())

    @classmethod
    def put(cls, mongo_db, location):
        location.update_last_updated()
        return mongo_db.locations.insert_one(location.to_dict())

    @classmethod
    def put_multi(cls, mongo_db, locations):
        cls.update_last_updated_multi(locations)
        return mongo_db.locations.insert_many([location.to_dict() for location in locations])

    @classmethod
    def get_by_id(cls, mongo_db, location_id):
        return mongo_db.locations.find_one({"_id": location_id})

    @classmethod
    def get_multi_by_ids(cls, mongo_db, location_ids):
        return mongo_db.locations.find({"_id": {"$in": location_ids}}).sort("created_date", DESCENDING)


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

    def save(self, mongo_db):
        self.update_last_updated()
        return mongo_db.notifications.insert_one(self.to_dict())

    @classmethod
    def put(cls, mongo_db, notification):
        notification.update_last_updated()
        return mongo_db.notifications.insert_one(notification.to_dict())

    @classmethod
    def put_multi(cls, mongo_db, notifications):
        cls.update_last_updated_multi(notifications)
        return mongo_db.notifications.insert_many([notification.to_dict() for notification in notifications])

    @classmethod
    def get_by_id(cls, mongo_db, notification_id):
        return mongo_db.notifications.find_one({"_id": notification_id})

    @classmethod
    def get_multi_by_ids(cls, mongo_db, notification_ids):
        return mongo_db.notifications.find({"_id": {"$in": notification_ids}}).sort("created_date", DESCENDING)


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

    def save(self, mongo_db):
        self.update_last_updated()
        return mongo_db.observations.insert_one(self.to_dict())

    @classmethod
    def put(cls, mongo_db, observation):
        observation.update_last_updated()
        return mongo_db.observations.insert_one(observation.to_dict())

    @classmethod
    def put_multi(cls, mongo_db, observations):
        cls.update_last_updated_multi(observations)
        return mongo_db.observations.insert_many([observation.to_dict() for observation in observations])

    @classmethod
    def get_by_id(cls, mongo_db, notification_id):
        return mongo_db.notifications.find_one({"_id": notification_id})

    @classmethod
    def get_multi_by_ids(cls, mongo_db, notification_ids):
        return mongo_db.notifications.find({"_id": {"$in": notification_ids}}).sort("created_date", DESCENDING)
