from pymongo import DESCENDING

from .utils import TimestampMixin, to_object_id, to_object_id_list


class Degree(TimestampMixin):
    def __init__(self, code, full_name, avatar=None):
        super().__init__()
        self.code = code
        self.full_name = full_name
        self.avatar = avatar

        # Key ids from other collections
        self.institutions = []
        self.tutors = []
        self.students = []

    def add_institution(self, institution_id):
        if not institution_id:
            return
        institution = to_object_id(institution_id)
        if not institution or institution in self.institutions:
            return
        self.institutions.append(institution)

    def remove_institution(self, institution_id):
        if not institution_id:
            return
        institution = to_object_id(institution_id)
        if not institution or institution not in self.institutions:
            return
        self.institutions.remove(institution)

    def add_tutor(self, tutor_id):
        if not tutor_id:
            return
        tutor = to_object_id(tutor_id)
        if not tutor or tutor in self.tutors:
            return
        self.tutors.append(tutor)

    def remove_tutor(self, tutor_id):
        if not tutor_id:
            return
        tutor = to_object_id(tutor_id)
        if not tutor or tutor not in self.tutors:
            return
        self.tutors.remove(tutor)

    def add_student(self, student_id):
        if not student_id:
            return
        student = to_object_id(student_id)
        if not student or student in self.students:
            return
        self.students.append(student)

    def remove_student(self, student_id):
        if not student_id:
            return
        student = to_object_id(student_id)
        if not student or student not in self.students:
            return
        self.students.remove(student)

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
        return mongo_db.degrees.find_one({"_id": to_object_id(degree_id)})

    @classmethod
    def get_multi_by_ids(cls, mongo_db, degree_ids):
        return (mongo_db.degrees.find({"_id": {"$in": to_object_id_list(degree_ids)}})
                .sort("created_date", DESCENDING))

    @classmethod
    def get_latest(cls, mongo_db, institution_id=None, full_name=None):
        query = {}
        if institution_id:
            query["institution"] = to_object_id(institution_id)
        if full_name:
            query["full_name"] = full_name
        return mongo_db.degrees.find(query).sort("created_date", DESCENDING)

    @classmethod
    def get_by_code(cls, mongo_db, code):
        return mongo_db.degrees.find_one({"code": code})

    @classmethod
    def get_multi_by_codes(cls, mongo_db, codes):
        return mongo_db.degrees.find({"code": {"$in": codes}})


class Institution(TimestampMixin):
    def __init__(self, email, full_name, avatar=None, location=None):
        super().__init__()
        self.email = email
        self.full_name = full_name
        self.avatar = avatar

        # Key ids from other collections
        self.location = to_object_id(location)
        self.coordinators = []
        self.degrees = []
        self.tutors = []
        self.students = []
        self.internships = []

    def update_location(self, location_id):
        if not location_id:
            return
        self.location = to_object_id(location_id)

    def remove_location(self):
        self.location = None

    def add_coordinator(self, coordinator_id):
        if not coordinator_id:
            return
        coordinator = to_object_id(coordinator_id)
        if not coordinator or coordinator in self.coordinators:
            return
        self.coordinators.append(coordinator)

    def remove_coordinator(self, coordinator_id):
        if not coordinator_id:
            return
        coordinator = to_object_id(coordinator_id)
        if not coordinator or coordinator not in self.coordinators:
            return
        self.coordinators.remove(coordinator)

    def add_degree(self, degree_id):
        if not degree_id:
            return
        degree = to_object_id(degree_id)
        if not degree or degree in self.degrees:
            return
        self.degrees.append(degree)

    def remove_degree(self, degree_id):
        if not degree_id:
            return
        degree = to_object_id(degree_id)
        if not degree or degree not in self.degrees:
            return
        self.degrees.remove(degree)

    def add_tutor(self, tutor_id):
        if not tutor_id:
            return
        tutor = to_object_id(tutor_id)
        if not tutor or tutor in self.tutors:
            return
        self.tutors.append(tutor)

    def remove_tutor(self, tutor_id):
        if not tutor_id:
            return
        tutor = to_object_id(tutor_id)
        if not tutor or tutor not in self.tutors:
            return
        self.tutors.remove(tutor)

    def add_student(self, student_id):
        if not student_id:
            return
        student = to_object_id(student_id)
        if not student or student in self.students:
            return
        self.students.append(student)

    def remove_student(self, student_id):
        if not student_id:
            return
        student = to_object_id(student_id)
        if not student or student not in self.students:
            return
        self.students.remove(student)

    def add_internship(self, internship_id):
        if not internship_id:
            return
        internship = to_object_id(internship_id)
        if not internship or internship in self.internships:
            return
        self.internships.append(internship)

    def remove_internship(self, internship_id):
        if not internship_id:
            return
        internship = to_object_id(internship_id)
        if not internship or internship not in self.internships:
            return
        self.internships.remove(internship)

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
        return mongo_db.institutions.find_one({"_id": to_object_id(institution_id)})

    @classmethod
    def get_multi_by_ids(cls, mongo_db, institution_ids):
        return mongo_db.institutions.find({"_id": {"$in": to_object_id_list(institution_ids)}}).sort("created_date", DESCENDING)
