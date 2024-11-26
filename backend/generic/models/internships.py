from bson import ObjectId
from pymongo import DESCENDING

from backend.generic.models.utils import TimestampMixin, AVAILABLE_STATUSES, DEFAULT_STATUS


class Internship(TimestampMixin):
    def __init__(self, kind, status, starting_day, finishing_day, title, description,
                 location=None, student=None, worker=None, tutor=None, company=None, institution=None):
        super().__init__()
        self.kind = kind
        self.status = status if status in AVAILABLE_STATUSES else DEFAULT_STATUS
        self.starting_day = starting_day
        self.finishing_day = finishing_day
        self.title = title
        self.description = description

        # Keys from other collections
        self.location = location
        self.student = student
        self.worker = worker
        self.tutor = tutor
        self.company = company
        self.institution = institution

    def update_location(self, location_id):
        if not location_id:
            return
        self.location = location_id

    def remove_location(self):
        self.location = None

    def update_student(self, student_id):
        if not student_id:
            return
        self.student = student_id

    def remove_student(self):
        self.student = None

    def update_worker(self, worker_id):
        if not worker_id:
            return
        self.worker = worker_id

    def remove_worker(self):
        self.worker = None

    def update_tutor(self, tutor_id):
        if not tutor_id:
            return
        self.tutor = tutor_id

    def remove_tutor(self):
        self.tutor = None

    def update_company(self, company_id):
        if not company_id:
            return
        self.company = company_id

    def remove_company(self):
        self.company = None

    def update_institution(self, institution_id):
        if not institution_id:
            return
        self.institution = institution_id

    def remove_institution(self):
        self.institution = None

    def save(self, mongo_db):
        self.update_last_updated()
        return mongo_db.internships.insert_one(self.to_dict())

    @classmethod
    def put(cls, mongo_db, internship):
        internship.update_last_updated()
        return mongo_db.internships.insert_one(internship.to_dict())

    @classmethod
    def put_multi(cls, mongo_db, internships):
        cls.update_last_updated(internships)
        return mongo_db.internships.insert_many([internship.to_dict() for internship in internships])

    @classmethod
    def retrieve_internships(cls, mongo_db, student_id=None, title=None, status=None):
        query = {}
        if student_id:
            query["student"] = ObjectId(student_id)
        if title:
            query["title"] = title
        if status and status in AVAILABLE_STATUSES:
            query["status"] = status

        return mongo_db.internships.find(query).sort("created_date", DESCENDING)

    @classmethod
    def update_internship(cls, mongo_db, internship_id, data_to_update):
        return mongo_db.internships.update_one(
            {"_id": ObjectId(internship_id)},
            {"$set": data_to_update}
        )

    @classmethod
    def retrieve_internship_relations(cls, mongo_db, student_id=None, tutor_id=None, company_id=None):
        # TODO consider using embedded values instead
        student = mongo_db.users.find_one({"_id": ObjectId(student_id)}) if student_id else None
        tutor = mongo_db.users.find_one({"_id": ObjectId(tutor_id)}) if tutor_id else None
        company = mongo_db.companies.find_one({"_id": ObjectId(company_id)}) if company_id else None

        return student, tutor, company
