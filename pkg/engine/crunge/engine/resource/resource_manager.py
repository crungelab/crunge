from typing import Dict, Iterable
from pathlib import Path
from string import Template

from crunge.core import klass

from .resource_group import ResourceGroup


class UnknownPathVariable(KeyError):
    def __init__(self, name: str, available: Iterable[str]) -> None:
        self.name = name
        super().__init__(
            f"Unknown path variable '${{{name}}}'. Available: "
            f"{', '.join(sorted(available)) or '<none>'}"
        )


@klass.singleton
class ResourceManager(ResourceGroup):
    def __init__(self) -> None:
        super().__init__()
        self.path_variables: Dict[str, Path] = {}

    def add_path_variable(self, name: str, value: str | Path) -> None:
        self.path_variables[name] = Path(value)

    def add_path_variables(self, **kwargs: str | Path) -> None:
        self.add_path_variables_from_dict(kwargs)

    def add_path_variables_from_dict(
        self, path_variables: Dict[str, str | Path]
    ) -> None:
        for name, value in path_variables.items():
            self.add_path_variable(name, value)

    def resolve_path(self, path: str | Path) -> Path:
        if isinstance(path, Path):
            return path
        try:
            return Path(Template(path).substitute(self.path_variables))
        except KeyError as e:
            raise UnknownPathVariable(e.args[0], self.path_variables) from None

    def resolve_paths(self, *paths: str | Path) -> list[Path]:
        return [self.resolve_path(path) for path in paths]
