from pathlib import Path
import json
from data.structures import RoadEngager

class JsonDict(dict):
    """
    General json object that allows attributes 
    to be bound to and also behaves like a dict.
    """
    def __getattr__(self, attr: str):
        return self.get(attr)

    def __setattr__(self, attr: str, value):
        self[attr] = value
