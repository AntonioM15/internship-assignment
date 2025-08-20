from pymongo import DESCENDING

from .utils import TimestampMixin


class Degree(TimestampMixin):
    def __init__(self, code, full_name, avatar=None):
        super().__init__()
        self.code = code
        self.full_name = full_name
        self.avatar = avatar

        # Keys from other collections
        self.institutions = []
        self.tutors = []
        self.students = []

    def add_institution(self, institution_id):
        if not institution_id or institution_id in self.institutions:
            return
        self.institutions.append(institution_id)

    def remove_institution(self, institution_id):
        if not institution_id or institution_id not in self.institutions:
            return
        self.institutions.remove(institution_id)

    def add_tutor(self, tutor_id):
        if not tutor_id or tutor_id in self.tutors:
            return
        self.tutors.append(tutor_id)

    def remove_tutor(self, tutor_id):
        if not tutor_id or tutor_id not in self.tutors:
            return
        self.tutors.remove(tutor_id)

    def add_student(self, student_id):
        if not student_id or student_id in self.students:
            return
        self.students.append(student_id)

    def remove_student(self, student_id):
        if not student_id or student_id not in self.students:
            return
        self.students.remove(student_id)

    def save(self, mongo_db):
        self.update_last_updated()
        return mongo_db.degrees.insert_one(self.to_dict())

    @classmethod
    def put(cls, mongo_db, degree):
        degree.update_last_updated()
        return mongo_db.degrees.insert_one(degree.to_dict())

    @classmethod
    def put_multi(cls, mongo_db, degrees):
        cls.update_last_updated_multi(degrees)
        return mongo_db.degrees.insert_many([degree.to_dict() for degree in degrees])

    @classmethod
    def get_by_id(cls, mongo_db, degree_id):
        return mongo_db.degrees.find_one({"_id": degree_id})

    @classmethod
    def get_multi_by_ids(cls, mongo_db, degree_ids):
        return mongo_db.degrees.find({"_id": {"$in": degree_ids}}).sort("created_date", DESCENDING)


class Institution(TimestampMixin):
    def __init__(self, email, full_name, avatar=None, location=None):
        super().__init__()
        self.email = email
        self.full_name = full_name
        self.avatar = avatar

        # Keys from other collections
        self.location = location
        self.coordinators = []
        self.degrees = []
        self.tutors = []
        self.students = []
        self.internships = []

    def update_location(self, location):
        if not location:
            return
        self.location = location

    def remove_location(self):
        self.location = None

    def add_coordinator(self, coordinator_id):
        if not coordinator_id or coordinator_id in self.coordinators:
            return
        self.coordinators.append(coordinator_id)

    def remove_coordinator(self, coordinator_id):
        if not coordinator_id or coordinator_id not in self.coordinators:
            return
        self.coordinators.remove(coordinator_id)

    def add_degree(self, degree_id):
        if not degree_id or degree_id in self.degrees:
            return
        self.degrees.append(degree_id)

    def remove_degree(self, degree_id):
        if not degree_id or degree_id not in self.degrees:
            return
        self.degrees.remove(degree_id)

    def add_tutor(self, tutor_id):
        if not tutor_id or tutor_id in self.tutors:
            return
        self.tutors.append(tutor_id)

    def remove_tutor(self, tutor_id):
        if not tutor_id or tutor_id not in self.tutors:
            return
        self.tutors.remove(tutor_id)

    def add_student(self, student_id):
        if not student_id or student_id in self.students:
            return
        self.students.append(student_id)

    def remove_student(self, student_id):
        if not student_id or student_id not in self.students:
            return
        self.students.remove(student_id)

    def add_internship(self, internship_id):
        if not internship_id or internship_id in self.internships:
            return
        self.internships.append(internship_id)

    def remove_internship(self, internship_id):
        if not internship_id or internship_id not in self.internships:
            return
        self.internships.remove(internship_id)

    def save(self, mongo_db):
        self.update_last_updated()
        return mongo_db.institutions.insert_one(self.to_dict())

    @classmethod
    def put(cls, mongo_db, institution):
        institution.update_last_updated()
        return mongo_db.institutions.insert_one(institution.to_dict())

    @classmethod
    def put_multi(cls, mongo_db, institutions):
        cls.update_last_updated_multi(institutions)
        return mongo_db.institutions.insert_many([institution.to_dict() for institution in institutions])

    @classmethod
    def get_by_id(cls, mongo_db, institution_id):
        return mongo_db.institutions.find_one({"_id": institution_id})

    @classmethod
    def get_multi_by_ids(cls, mongo_db, institution_ids):
        return mongo_db.institutions.find({"_id": {"$in": institution_ids}}).sort("created_date", DESCENDING)
