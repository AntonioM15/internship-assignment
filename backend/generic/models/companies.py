from bson import ObjectId
from pymongo import DESCENDING

from backend.generic.models.utils import TimestampMixin, AVAILABLE_STATUSES


class Company(TimestampMixin):
    def __init__(self, full_name, field, avatar=None, location=None):
        super().__init__()
        self.full_name = full_name
        self.field = field
        self.hidden = False
        self.avatar = avatar

        # Keys from other collections
        self.location = location
        self.workers = []
        self.observations = []
        self.internships = []

    def update_location(self, location_id):
        if not location_id:
            return
        self.location = location_id

    def remove_location(self):
        self.location = None

    def add_worker(self, worker_id):
        if not worker_id or worker_id in self.workers:
            return
        self.workers.append(worker_id)

    def remove_worker(self, worker_id):
        if not worker_id or worker_id not in self.workers:
            return
        self.workers.remove(worker_id)

    def add_observation(self, observation_id):
        if not observation_id or observation_id in self.observations:
            return
        self.observations.append(observation_id)

    def remove_observation(self, observation_id):
        if not observation_id or observation_id not in self.observations:
            return
        self.observations.remove(observation_id)

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
        return mongo_db.companies.insert_one(self.to_dict())

    @classmethod
    def put(cls, mongo_db, company):
        company.update_last_updated()
        return mongo_db.companies.insert_one(company.to_dict())

    @classmethod
    def put_multi(cls, mongo_db, companies):
        cls.update_last_updated(companies)
        return mongo_db.companies.insert_many([company.to_dict() for company in companies])

    @classmethod
    def retrieve_companies(cls, mongo_db, field=None, full_name=None):
        query = {}
        if field:
            query["degree"] = field
        if full_name:
            query["full_name"] = full_name

        return mongo_db.companies.find(query).sort("created_date", DESCENDING)

    @classmethod
    def update_company(cls, mongo_db, company_id, data_to_update):
        return mongo_db.companies.update_one(
            {"_id": ObjectId(company_id)},
            {"$set": data_to_update}
        )

    @classmethod
    def retrieve_company_internships(cls, mongo_db, company_id, status):
        # Query the company
        company = mongo_db.companies.find_one({"_id": ObjectId(company_id)})
        internship_ids = company["internships"]
        if not internship_ids:
            return []

        # Query company internships
        query = {"_id": {"$in": internship_ids}}
        if status and status in AVAILABLE_STATUSES:
            query["status"] = status

        return mongo_db.internship.find(query)

    @classmethod
    def add_internship_to_company(cls, mongo_db, company_id, internship_id):
        mongo_db.companies.update_one(
            {"_id": company_id},
            {"$addToSet": {"internships": internship_id}}
        )
