from typing import Dict
from pathlib import Path

from crunge.core import klass


@klass.singleton
class ResourceManager:
    def __init__(self) -> None:
        # self.root = Path(__file__).parent.parent.parent.parent.parent.parent / "resources"
        self.path_variables: Dict[str, Path] = {}

    def add_path_variable(self, name: str, value: any):
        self.path_variables[name] = value

    def add_path_variables(self, **kwargs):
        for name, value in kwargs.items():
            self.add_path_variable(name, value)

    def add_path_variables_from_dict(self, path_variables: Dict[str, Path]):
        for name, value in path_variables.items():
            self.add_path_variable(name, value)

    def resolve_path(self, path: str) -> Path:
        return Path(path.format(**self.path_variables))
    
    '''
    def path(self, path: Path) -> Path:
        return self.root / path
    '''