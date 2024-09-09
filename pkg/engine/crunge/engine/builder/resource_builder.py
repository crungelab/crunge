from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List
from pathlib import Path


# Define a generic type variable
#T_Resource = TypeVar("T_Resource", bound=Resource)
T_Resource = TypeVar("T_Resource")

from ..resource.resource_kit import ResourceKit

from ..base import Base

class ResourceBuilder(Base, Generic[T_Resource]):
    def __init__(self, kit: ResourceKit[T_Resource]) -> None:
        self.kit = kit
