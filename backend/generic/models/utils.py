from datetime import datetime


class TimestampMixin(object):
    def __init__(self):
        self.created_date = datetime.utcnow()
        self.last_updated = datetime.utcnow()
