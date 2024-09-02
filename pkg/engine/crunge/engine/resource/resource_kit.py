from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List
from pathlib import Path


from crunge.engine import Base

# Define a generic type variable
#T_Resource = TypeVar("T_Node", bound=Resource)
T_Resource = TypeVar("T_Resource")


class ResourceKit(Base, Generic[T_Resource]):
    def __init__(self) -> None:
        self.resources: Dict[str, T_Resource] = {}

    def load(self, path: Path) -> T_Resource:
        raise NotImplementedError
    
    def get(self, name: str) -> T_Resource:
        #return self.resources[name]
        return self.resources.get(name)
    
    def add(self, resource: T_Resource) -> None:
        self.resources[resource.name] = resource

    def remove(self, name: str) -> None:
        #del self.resources[name]
        self.resources.pop(name, None)

    def clear(self) -> None:
        self.resources.clear()
        
