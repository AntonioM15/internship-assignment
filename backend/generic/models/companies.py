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

    def add_worker(self, worker):
        if not worker or worker in self.workers:
            return
        self.workers.append(worker)

    def remove_worker(self, worker):
        if not worker or worker not in self.workers:
            return
        self.workers.remove(worker)

    def add_observation(self, observation):
        if not observation or observation in self.observations:
            return
        self.observations.append(observation)

    def remove_observation(self, observation):
        if not observation or observation not in self.observations:
            return
        self.observations.remove(observation)
