from abc import ABCMeta, abstractmethod

class AbstractBaseRepository:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __repr__(self):
        raise NotImplementedError()

    @abstractmethod
    def get(self, idx):
        raise NotImplementedError()

    @abstractmethod
    def insert(self, data):
        raise NotImplementedError()

    @abstractmethod
    def update(self, old_data_model, new_data_model):
        raise NotImplementedError()

    @abstractmethod
    def delete(self, idx):
        raise NotImplementedError()
