from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List
from pathlib import Path


from crunge.engine import Base
from .resource import Resource

T_Resource = TypeVar("T_Resource", bound=Resource)


class ResourceKit(Base, Generic[T_Resource]):
    registry: Dict[int, T_Resource] = {}
    next_id: int = 1

    def __init__(self) -> None:
        #self.resources: Dict[int, T_Resource] = {}
        self.resources_by_name: Dict[str, int] = {}
        self.resources_by_path: Dict[Path, int] = {}
        #self.next_id: int = 1

    def load(self, path: Path) -> T_Resource:
        raise NotImplementedError

    def get(self, id: int) -> T_Resource:
        #return self.resources.get(id)
        return ResourceKit.registry.get(id)

    def get_by_name(self, name: str) -> T_Resource:
        resource_id = self.resources_by_name.get(name)
        if resource_id is not None:
            #return self.resources.get(resource_id)
            #return ResourceKit.registry.get(resource_id)
            return self.get(resource_id)
        return None

    def get_by_path(self, path: Path) -> T_Resource:
        resource_id = self.resources_by_path.get(path)
        if resource_id is not None:
            #return self.resources.get(resource_id)
            #return ResourceKit.registry.get(resource_id)
            return self.get(resource_id)
        return None

    def add(self, resource: T_Resource) -> int:
        resource_id = resource.id
        if resource_id is None:
            resource_id = self.next_id
            self.next_id += 1
            resource.set_id(resource_id)

        #self.resources[resource_id] = resource
        ResourceKit.registry[resource_id] = resource
        if resource.name:
            self.resources_by_name[resource.name] = resource_id
        if resource.path:
            self.resources_by_path[resource.path] = resource_id
        return resource_id

    def remove(self, resource: T_Resource) -> None:
        #self.resources.pop(resource.id, None)
        ResourceKit.registry.pop(resource.id, None)
        self.resources_by_name.pop(resource.name, None)
        self.resources_by_path.pop(resource.path, None)

    def clear(self) -> None:
        #self.resources.clear()
        self.resources_by_name.clear()
        self.resources_by_path.clear()
