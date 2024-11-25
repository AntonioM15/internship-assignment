from bson import ObjectId
from pymongo import DESCENDING

from backend.generic.models.utils import TimestampMixin, AVAILABLE_STATUSES, DEFAULT_STATUS


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

    def to_dict(self):
        return {
            "created_date": self.created_date,
            "last_updated": self.last_updated,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "role": self.role,
            "official_id": self.official_id,
            "full_name": self.full_name,
            "hidden": self.hidden,
            "avatar": self.avatar,
            "location": self.location,
            "notifications": self.notifications,
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
        cls.update_last_updated(users)
        return mongo_db.users.insert_many([user.to_dict() for user in users])


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
    def retrieve_latest_notifications(cls, mongo_db, user_id):
        """ Retrieve the latest notifications of only its user """
        # Query the user first
        user = mongo_db.users.find_one({"_id": ObjectId(user_id)})
        # Query related notifications
        notifications_ids = user['notifications'][:cls.MAX_NOTIFICATIONS_REGULAR]
        return mongo_db.notifications.find({"_id": {"$in": notifications_ids}}).sort("created_date", DESCENDING)


class Student(User):
    def __init__(self, email, hashed_password, official_id, full_name, status, institution, degree, internship=None, observations=None, **kwargs):
        super().__init__(email, hashed_password, official_id, full_name, **kwargs)
        self.role = 'student'
        self.status = status if status in AVAILABLE_STATUSES else DEFAULT_STATUS
        self.internship_type = None

        # Keys from other collections
        self.institution = institution
        self.degree = degree
        self.internship = internship
        self.observations = observations or []

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "status": self.status,
            "institution": self.institution,
            "degree": self.degree,
            "internship": self.internship,
            "observations": self.observations,
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
    def retrieve_students(cls, mongo_db, degree_id=None, full_name=None, status=None):
        query = {"role": "student"}
        if degree_id:
            query["degree"] = ObjectId(degree_id)
        if full_name:
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

    @classmethod
    def hide_student(cls, mongo_db):
        return

    @classmethod
    def restore_student(cls, mongo_db):
        return


class Tutor(User):
    def __init__(self, email, hashed_password, official_id, full_name, institution, degrees=None, students=None, internships=None, **kwargs):
        super().__init__(email, hashed_password, official_id, full_name, **kwargs)
        self.role = 'tutor'

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
    def retrieve_latest_notifications(cls, mongo_db, user_id):
        """ Retrieve the latest notifications of only its user """
        # Query the user first
        user = mongo_db.users.find_one({"_id": ObjectId(user_id)})
        # Query related notifications
        notifications_ids = user['notifications'][:cls.MAX_NOTIFICATIONS_REGULAR]
        return mongo_db.notifications.find({"_id": {"$in": notifications_ids}}).sort("created_date", DESCENDING)


class Admin(User):
    def __init__(self, email, hashed_password, official_id, full_name, **kwargs):
        super().__init__(email, hashed_password, official_id, full_name, **kwargs)
        self.role = 'admin'

    def to_dict(self):
        return super().to_dict()

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