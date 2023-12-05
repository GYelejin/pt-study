from service.config import settings


class BaseRepo:
    def __init__(self):
        self.db = settings.DATABASE.db_obj
