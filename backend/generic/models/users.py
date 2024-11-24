from backend.generic.models.utils import TimestampMixin


class User(TimestampMixin):
    def __init__(self, email, hashed_password, official_id, full_name, avatar=None, location=None, notifications=None):
        super().__init__()
        self.email = email
        self.hashed_password = hashed_password
        self.role = 'user'
        self.official_id = official_id
        self.full_name = full_name
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
            "avatar": self.avatar,
            "location": self.location,
            "notifications": self.notifications,
        }

    def save(self, mongo):
        mongo.db.users.insert_one(self.to_dict())

    @classmethod
    def put(cls, mongo, user):
        mongo.db.users.insert_one(user.to_dict())

    @classmethod
    def put_multi(cls, mongo, users):
        mongo.db.users.insert_many([user.to_dict() for user in users])


class Coordinator(User):
    def __init__(self, email, hashed_password, official_id, full_name, institution, observations=None, **kwargs):
        super().__init__(email, hashed_password, official_id, full_name, **kwargs)
        self.role = 'coordinator'
        self.institution = institution
        self.observations = observations or []

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "institution": self.institution,
            "observations": self.observations,
        })
        return data


class Worker(User):
    def __init__(self, email, hashed_password, official_id, full_name, company, interns=None, internships=None, **kwargs):
        super().__init__(email, hashed_password, official_id, full_name, **kwargs)
        self.role = 'worker'
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


class Student(User):
    AVAILABLE_STATUSES = ('unassigned', 'provisional','assigned', 'ongoing')

    def __init__(self, email, hashed_password, official_id, full_name, status, institution, degree, internship=None, observations=None, **kwargs):
        super().__init__(email, hashed_password, official_id, full_name, **kwargs)
        self.role = 'student'
        self.status = status if status in self.AVAILABLE_STATUSES else 'unassigned'
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


class Tutor(User):
    def __init__(self, email, hashed_password, official_id, full_name, institution, degrees=None, students=None, internships=None, **kwargs):
        super().__init__(email, hashed_password, official_id, full_name, **kwargs)
        self.role = 'tutor'
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


class Admin(User):
    def __init__(self, email, hashed_password, official_id, full_name, **kwargs):
        super().__init__(email, hashed_password, official_id, full_name, **kwargs)
        self.role = 'admin'

    def to_dict(self):
        return super().to_dict()
