from backend.generic.models.utils import TimestampMixin


class Company(TimestampMixin):
    def __init__(self, full_name, field, avatar=None, location=None):
        super().__init__()
        self.full_name = full_name
        self.field = field
        self.avatar = avatar

        # Keys from other collections
        self.location = location
        self.workers = []
        self.observations = []

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
