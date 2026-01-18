from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List
from pathlib import Path

from ..resource.resource_kit import ResourceKit
from ..resource import Resource

from ..base import Base

T_Resource = TypeVar("T_Resource", bound=Resource)


class ResourceBuilder(Base, Generic[T_Resource]):
    def __init__(self, kit: ResourceKit[T_Resource]) -> None:
        self.kit = kit
