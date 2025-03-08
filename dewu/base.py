import abc
from abc import ABC

NON_STATED = None

class JsonSerializable(ABC):
    @classmethod
    @abc.abstractmethod
    def from_json(cls, json_data):
        ...
