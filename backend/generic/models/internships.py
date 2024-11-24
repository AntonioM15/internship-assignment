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

    def update_location(self, location):
        if not location:
            return
        self.location = location

    def remove_location(self):
        self.location = None

    def update_student(self, student):
        if not student:
            return
        self.student = student

    def remove_student(self):
        self.student = None

    def update_worker(self, worker):
        if not worker:
            return
        self.worker = worker

    def remove_worker(self):
        self.worker = None

    def update_tutor(self, tutor):
        if not tutor:
            return
        self.tutor = tutor

    def remove_tutor(self):
        self.tutor = None

    def update_company(self, company):
        if not company:
            return
        self.company = company

    def remove_company(self):
        self.company = None

    def update_institution(self, institution):
        if not institution:
            return
        self.institution = institution

    def remove_institution(self):
        self.institution = None
