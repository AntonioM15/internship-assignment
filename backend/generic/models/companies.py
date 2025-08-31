from pymongo import DESCENDING

from .internships import Internship
from .utils import Location, Observation, TimestampMixin, AVAILABLE_STATUSES, serialize_document, to_object_id, \
    to_object_id_list


class Company(TimestampMixin):
    def __init__(self, full_name, field, description=None, avatar=None, location=None):
        super().__init__()
        self.full_name = full_name
        self.field = field
        self.hidden = False
        self.description = description
        self.avatar = avatar

        # Key ids from other collections
        self.location = to_object_id(location)
        self.workers = []
        self.observations = []
        self.internships = []

    @classmethod
    def doc_to_dict(cls, mongo_db, doc):
        # Avoid circular imports
        from .users import Worker

        # Retrieve related entities and add them to the dict
        location = Location.get_by_id(mongo_db, doc['location'])
        workers = Worker.get_multi_by_ids(mongo_db, doc['workers'])
        observations = Observation.get_multi_by_ids(mongo_db, doc['observations'])
        internships = Internship.get_multi_by_ids(mongo_db, doc['internships'])
        return {
            "full_name": doc['full_name'],
            "field": doc['field'],
            "hidden": doc['hidden'],
            "description": doc['description'],
            "avatar": doc['avatar'],
            "location": serialize_document(location) if location else None,
            "workers": [serialize_document(doc) if doc else None for doc in workers],
            "observations": [serialize_document(doc) if doc else None for doc in observations],
            "internships": [Internship.doc_to_dict(mongo_db, doc) if doc else None for doc in internships],
        }

    def update_location(self, location_id):
        if not location_id:
            return
        self.location = location_id

    def remove_location(self):
        self.location = None

    def add_worker(self, worker_id):
        if not worker_id:
            return
        worker = to_object_id(worker_id)
        if not worker or worker in self.workers:
            return
        self.workers.append(worker)

    def remove_worker(self, worker_id):
        if not worker_id:
            return
        worker = to_object_id(worker_id)
        if not worker or worker not in self.workers:
            return
        self.workers.remove(worker)

    def add_observation(self, observation_id):
        if not observation_id:
            return
        observation = to_object_id(observation_id)
        if not observation or observation in self.observations:
            return
        self.observations.append(observation)

    def remove_observation(self, observation_id):
        if not observation_id:
            return
        observation = to_object_id(observation_id)
        if not observation or observation not in self.observations:
            return
        self.observations.remove(observation)

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
        return mongo_db.companies.insert_one(self.to_dict())

    @classmethod
    def put(cls, mongo_db, company):
        company.update_last_updated()
        return mongo_db.companies.insert_one(company.to_dict())

    @classmethod
    def put_multi(cls, mongo_db, companies):
        cls.update_last_updated_multi(companies)
        return mongo_db.companies.insert_many([company.to_dict() for company in companies])

    @classmethod
    def get_by_id(cls, mongo_db, company_id):
        return mongo_db.companies.find_one({"_id": to_object_id(company_id)})

    @classmethod
    def get_multi_by_ids(cls, mongo_db, company_ids):
        return (mongo_db.companies.find({"_id": {"$in": to_object_id_list(company_ids)}})
                .sort("created_date", DESCENDING))

    @classmethod
    def retrieve_companies(cls, mongo_db, field=None, full_name=None, partial_search=False):
        query = {}
        if field:
            query["field"] = field
        if full_name and partial_search:
            query["full_name"] = {"$regex": full_name, "$options": "i"}
        elif full_name:
            query["full_name"] = full_name

        return mongo_db.companies.find(query).sort("created_date", DESCENDING)

    @classmethod
    def update_company(cls, mongo_db, company_id, data_to_update):
        return mongo_db.companies.update_one(
            {"_id": to_object_id(company_id)},
            {"$set": data_to_update}
        )

    @classmethod
    def retrieve_company_internships(cls, mongo_db, company_id, status):
        # Query the company
        company = mongo_db.companies.find_one({"_id": to_object_id(company_id)})
        internship_ids = company["internships"]
        if not internship_ids:
            return []

        # Query company internships
        query = {"_id": {"$in": to_object_id_list(internship_ids)}}
        if status and status in AVAILABLE_STATUSES:
            query["status"] = status

        return mongo_db.internship.find(query)

    @classmethod
    def add_internship_to_company(cls, mongo_db, company_id, internship_id):
        mongo_db.companies.update_one(
            {"_id": to_object_id(company_id)},
            {"$addToSet": {"internships": to_object_id(internship_id)}}
        )
