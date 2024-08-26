from pathlib import Path

from crunge.core import klass


@klass.singleton
class ResourceKit:
    def __init__(self) -> None:
        self.root = Path(__file__).parent.parent.parent.parent.parent.parent / "resources"

    def path(self, path: Path) -> Path:
        return self.root / path