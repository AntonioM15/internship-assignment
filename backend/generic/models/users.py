from bson import ObjectId
from pymongo import DESCENDING

from .internships import Internship
from .companies import Company
from .institutions import Institution, Degree
from .utils import Notification, Observation, Location, AVAILABLE_STATUSES, DEFAULT_STATUS, serialize_document, \
                   TimestampMixin


class User(TimestampMixin):
    MAX_NOTIFICATIONS_REGULAR = 10
    MAX_NOTIFICATIONS_SU = 40

    def __init__(self, email, hashed_password, official_id, full_name, avatar=None, location=None, notifications=None):
        super().__init__()
        self.email = email
        self.hashed_password = hashed_password
        self.role = 'user'
        self.official_id = official_id
        self.full_name = full_name
        self.hidden = False

        # Keys from other collections
        self.avatar = avatar
        self.location = location or {}
        self.notifications = notifications or []

    @classmethod
    def doc_to_dict(cls, mongo_db, doc):
        # Retrieve related entities and add them to the dict
        notifications = Notification.get_multi_by_ids(mongo_db, doc['notifications'][:cls.MAX_NOTIFICATIONS_REGULAR])
        location = Location.get_by_id(mongo_db, doc['location'])
        return {
            "email": doc['email'],
            "hashed_password": doc['hashed_password'],
            "role": doc['role'],
            "official_id": doc['official_id'],
            "full_name": doc['full_name'],
            "hidden": doc['hidden'],
            "avatar": doc['avatar'],
            "notifications": [serialize_document(doc) if doc else None for doc in notifications],
            "location": serialize_document(location) if location else None,
        }

    def update_location(self, location_id):
        if not location_id:
            return
        self.location = location_id

    def remove_location(self):
        self.location = None

    def save(self, mongo_db):
        self.update_last_updated()
        return mongo_db.users.insert_one(self.to_dict())

    @classmethod
    def put(cls, mongo_db, user):
        user.update_last_updated()
        return mongo_db.users.insert_one(user.to_dict())

    @classmethod
    def put_multi(cls, mongo_db, users):
        cls.update_last_updated_multi(users)
        return mongo_db.users.insert_many([user.to_dict() for user in users])

    @classmethod
    def get_by_id(cls, mongo_db, user_id):
        return mongo_db.users.find_one({"_id": user_id})

    @classmethod
    def get_multi_by_ids(cls, mongo_db, user_ids):
        return mongo_db.users.find({"_id": {"$in": user_ids}}).sort("created_date", DESCENDING)

    @classmethod
    def retrieve_latest_notifications(cls, mongo_db, _):
        """ Retrieve the latest notifications of all related user collections """
        return []  # Implement me in subclasses!


class Coordinator(User):
    def __init__(self, email, hashed_password, official_id, full_name, institution, observations=None, **kwargs):
        super().__init__(email, hashed_password, official_id, full_name, **kwargs)
        self.role = 'coordinator'

        # Keys from other collections
        self.institution = institution
        self.observations = observations or []

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "institution": self.institution,
            "observations": self.observations,
        })
        return data

    @classmethod
    def doc_to_dict(cls, mongo_db, doc):
        data = super().doc_to_dict(mongo_db, doc)
        # Retrieve related entities and add them to the dict
        institution = Institution.get_by_id(mongo_db, doc['institution'])
        observations = Observation.get_multi_by_ids(mongo_db, doc['observations'])
        data.update({
            "institution": serialize_document(institution) if institution else None,
            "observations": [serialize_document(doc) if doc else None for doc in observations],
        })
        return data

    @classmethod
    def retrieve_latest_notifications(cls, mongo_db, _):
        """ Retrieve the latest notifications of all related user collections """
        return mongo_db.notifications.find().sort("created_date", DESCENDING).limit(cls.MAX_NOTIFICATIONS_SU)


class Worker(User):
    def __init__(self, email, hashed_password, official_id, full_name, company, interns=None, internships=None, **kwargs):
        super().__init__(email, hashed_password, official_id, full_name, **kwargs)
        self.role = 'worker'

        # Keys from other collections
        self.company = company
        self.interns = interns or []
        self.internships = internships or []

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "company": self.company,
            "interns": self.interns,
            "internships": self.internships,
        })
        return data

    @classmethod
    def doc_to_dict(cls, mongo_db, doc):
        data = super().doc_to_dict(mongo_db, doc)
        # Retrieve related entities and add them to the dict
        company = Company.get_by_id(mongo_db, doc['company'])
        interns = User.get_multi_by_ids(mongo_db, doc['interns'])
        internships = Internship.get_multi_by_ids(mongo_db, doc['internships'])
        data.update({
            "company": serialize_document(company) if company else None,
            "interns": [serialize_document(doc) if doc else None for doc in interns],
            "internships": [serialize_document(doc) if doc else None for doc in internships],
        })
        return data

    @classmethod
    def retrieve_latest_notifications(cls, mongo_db, user_id):
        """ Retrieve the latest notifications of only its user """
        # Query the user first
        user = mongo_db.users.find_one({"_id": ObjectId(user_id)})
        # Query related notifications
        notifications_ids = user['notifications'][:cls.MAX_NOTIFICATIONS_REGULAR]
        return mongo_db.notifications.find({"_id": {"$in": notifications_ids}}).sort("created_date", DESCENDING)


class Student(User):
    def __init__(self, email, hashed_password, official_id, full_name, status, institution, degree, description=None, internship=None, observations=None, **kwargs):
        super().__init__(email, hashed_password, official_id, full_name, **kwargs)
        self.role = 'student'
        self.status = status if status in AVAILABLE_STATUSES else DEFAULT_STATUS
        self.internship_type = None
        self.description = description

        # Keys from other collections
        self.institution = institution
        self.degree = degree
        self.internship = internship
        self.observations = observations or []

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "status": self.status,
            "internship_type": self.internship_type,
            "description": self.description,
            "institution": self.institution,
            "degree": self.degree,
            "internship": self.internship,
            "observations": self.observations,
        })
        return data

    @classmethod
    def doc_to_dict(cls, mongo_db, doc):
        data = super().doc_to_dict(mongo_db, doc)
        # Retrieve related entities and add them to the dict
        institution = Institution.get_by_id(mongo_db, doc['institution'])
        degree = Degree.get_by_id(mongo_db, doc['degree'])
        internship = Internship.get_by_id(mongo_db, doc['internship'])
        observations = Observation.get_multi_by_ids(mongo_db, doc['observations'])
        data.update({
            "status": doc['status'],
            "internship_type": doc['internship_type'],
            "description": doc['description'],
            "institution": serialize_document(institution) if institution else None,
            "degree": serialize_document(degree) if degree else None,
            "internship": serialize_document(internship) if internship else None,
            "observations": [serialize_document(doc) if doc else None for doc in observations],
        })
        return data

    def add_observation(self, observation_id):
        if observation_id and observation_id not in self.observations:
            self.observations.append(ObjectId(observation_id))

    @classmethod
    def retrieve_latest_notifications(cls, mongo_db, user_id):
        """ Retrieve the latest notifications of only its user """
        # Query the user first
        user = mongo_db.users.find_one({"_id": ObjectId(user_id)})
        # Query related notifications
        notifications_ids = user['notifications'][:cls.MAX_NOTIFICATIONS_REGULAR]
        return mongo_db.notifications.find({"_id": {"$in": notifications_ids}}).sort("created_date", DESCENDING)

    @classmethod
    def retrieve_students(cls, mongo_db, degree_id=None, full_name=None, status=None, partial_search=False):
        query = {"role": "student"}
        if degree_id:
            query["degree"] = ObjectId(degree_id)
        if full_name and partial_search:
            # Regular expressions for partial matching
            query["full_name"] = {"$regex": full_name, "$options": "i"}
        elif full_name:
            query["full_name"] = full_name
        if status and status in AVAILABLE_STATUSES:
            query["status"] = status

        return mongo_db.users.find(query).sort("created_date", DESCENDING)

    @classmethod
    def update_student(cls, mongo_db, user_id, data_to_update):
        # TODO process data_to_update so that non invalid values are removed
        return mongo_db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": data_to_update}
        )


class Tutor(User):
    def __init__(self, email, hashed_password, official_id, full_name, status, institution, degrees=None, students=None, internships=None, **kwargs):
        super().__init__(email, hashed_password, official_id, full_name, **kwargs)
        self.role = 'tutor'
        self.status = status if status in AVAILABLE_STATUSES else DEFAULT_STATUS

        # Keys from other collections
        self.institution = institution
        self.degrees = degrees or []
        self.students = students or []
        self.internships = internships or []

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "institution": self.institution,
            "degrees": self.degrees,
            "students": self.students,
            "internships": self.internships,
        })
        return data

    @classmethod
    def doc_to_dict(cls, mongo_db, doc):
        data = super().doc_to_dict(mongo_db, doc)
        # Retrieve related entities and add them to the dict
        institution = Institution.get_by_id(mongo_db, doc['institution'])
        degrees = Degree.get_multi_by_ids(mongo_db, doc['degrees'])
        students = Student.get_multi_by_ids(mongo_db, doc['students'])
        internships = Internship.get_multi_by_ids(mongo_db, doc['internships'])
        data.update({
            "status": doc['status'],
            "institution": serialize_document(institution) if institution else None,
            "degrees": [serialize_document(doc) if doc else None for doc in degrees],
            "students": [serialize_document(doc) if doc else None for doc in students],
            "internships": [serialize_document(doc) if doc else None for doc in internships],
        })
        return data

    @classmethod
    def retrieve_latest_notifications(cls, mongo_db, user_id):
        """ Retrieve the latest notifications of only its user """
        # Query the user first
        user = mongo_db.users.find_one({"_id": ObjectId(user_id)})
        # Query related notifications
        notifications_ids = user['notifications'][:cls.MAX_NOTIFICATIONS_REGULAR]
        return mongo_db.notifications.find({"_id": {"$in": notifications_ids}}).sort("created_date", DESCENDING)

    @classmethod
    def retrieve_tutors(cls, mongo_db, degree_id=None, full_name=None, status=None):
        query = {"role": "tutor"}
        if degree_id:
            query["degree"] = {"$in": [ObjectId(degree_id)]}
        if full_name:
            query["full_name"] = full_name
        if status and status in AVAILABLE_STATUSES:
            query["status"] = status

        return mongo_db.users.find(query).sort("created_date", DESCENDING)

    @classmethod
    def update_tutor(cls, mongo_db, tutor_id, data_to_update):
        return mongo_db.users.update_one(
            {"_id": ObjectId(tutor_id)},
            {"$set": data_to_update}
        )


class Admin(User):
    def __init__(self, email, hashed_password, official_id, full_name, **kwargs):
        super().__init__(email, hashed_password, official_id, full_name, **kwargs)
        self.role = 'admin'

    def to_dict(self):
        return super().to_dict()

    @classmethod
    def doc_to_dict(cls, mongo_db, doc):
        data = super().doc_to_dict(mongo_db, doc)
        return data

    @classmethod
    def retrieve_latest_notifications(cls, mongo_db, _):
        """ Retrieve the latest notifications of all related user collections """
        return mongo_db.notifications.find().sort("created_date", DESCENDING).limit(cls.MAX_NOTIFICATIONS_SU)


USER_MAPPING = {
    'user': User,
    'coordinator': Coordinator,
    'worker': Worker,
    'student': Student,
    'tutor': Tutor,
    'admin': Admin
}