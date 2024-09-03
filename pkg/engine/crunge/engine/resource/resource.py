from pathlib import Path

from .. import Base

class Resource(Base):
    def __init__(self):
        self.id = None
        self.name = None
        self.path = None

    def __str__(self):
        return f"Resource(id={self.id}, name={self.name}, path={self.path})"

    def __repr__(self):
        return str(self)

    def set_id(self, id: int):
        self.id = id
        return self

    def set_name(self, name: str):
        self.name = name
        return self
    
    def set_path(self, path: Path):
        self.path = path
        return self

    '''
    def __eq__(self, other):
        return self.name == other.name and self.path == other.path

    def __hash__(self):
        return hash((self.name, self.path))
    '''