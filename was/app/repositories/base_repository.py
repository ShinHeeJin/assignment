from . import AbstractBaseRepository
from app import db

class BaseRepository(AbstractBaseRepository):
    def __init__(self, entity):
        self.__entity = entity

    def __repr__(self):
        f"{self.__class__.__name__}({self.__entity.__class__.__name__})"

    def get(self, idx):
        return self.__entity.query.get(idx)

    def insert(self, obj):
        db.session.add(obj)
        db.session.flush()
        return obj

    def update(self, old_data_model, new_data_model):
        new_data_model.id = old_data_model.id
        db.session.merge(new_data_model)
        db.session.commit()

    def delete(self, obj):
        db.session.delete(obj)
        return True
