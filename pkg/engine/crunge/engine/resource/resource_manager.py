from typing import Dict
from pathlib import Path

from crunge.core import klass

from .resource_group import ResourceGroup

@klass.singleton
class ResourceManager(ResourceGroup):
    def __init__(self) -> None:
        super().__init__()
        self.path_variables: Dict[str, Path] = {}

    def add_path_variable(self, name: str, value: any):
        self.path_variables[name] = value

    def add_path_variables(self, **kwargs):
        for name, value in kwargs.items():
            self.add_path_variable(name, value)

    def add_path_variables_from_dict(self, path_variables: Dict[str, Path]):
        for name, value in path_variables.items():
            self.add_path_variable(name, value)

    def resolve_path(self, path: str | Path) -> Path:
        if isinstance(path, Path):
            return path
        return Path(path.format(**self.path_variables))

    def resolve_paths(self, *paths: str | Path) -> Path:
        return [self.resolve_path(path) for path in paths]