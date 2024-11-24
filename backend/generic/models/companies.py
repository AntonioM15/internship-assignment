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

    def update_location(self, location):
        if not location:
            return
        self.location = location

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
