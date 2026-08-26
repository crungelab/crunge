from typing import Iterator, Protocol, runtime_checkable

from loguru import logger

from .overlay import Overlay


@runtime_checkable
class OverlayFactory(Protocol):
    name: str
    priority: int

    def create(self) -> Overlay: ...


class FuncOverlayFactory:
    """Adapts a plain callable into an OverlayFactory."""

    def __init__(self, name: str, create, priority: int = 0) -> None:
        self.name = name
        self.priority = priority
        self._create = create

    def create(self) -> Overlay:
        return self._create()


class OverlayManufacturer:
    def __init__(self) -> None:
        self._factories: dict[str, OverlayFactory] = {}

    def __len__(self) -> int:
        return len(self._factories)

    def __contains__(self, name: str) -> bool:
        return name in self._factories

    def __iter__(self) -> Iterator[OverlayFactory]:
        return iter(self.factories)

    @property
    def factories(self) -> list[OverlayFactory]:
        return sorted(self._factories.values(), key=lambda f: f.priority)

    def add(self, factory: OverlayFactory) -> OverlayFactory:
        if factory.name in self._factories:
            logger.warning(f"Overlay factory '{factory.name}' replaced")
        self._factories[factory.name] = factory
        return factory

    def add_func(self, name: str, create, priority: int = 0) -> OverlayFactory:
        return self.add(FuncOverlayFactory(name, create, priority))

    def remove(self, name: str) -> None:
        if self._factories.pop(name, None) is None:
            logger.warning(f"Overlay factory '{name}' not found")

    def clear(self) -> None:
        self._factories.clear()

    def get(self, name: str) -> OverlayFactory | None:
        return self._factories.get(name)

    def manufacture(self, name: str) -> Overlay | None:
        factory = self._factories.get(name)
        if factory is None:
            logger.warning(f"No overlay factory named '{name}'")
            return None
        return factory.create()

    def manufacture_all(self) -> list[Overlay]:
        return [factory.create() for factory in self.factories]