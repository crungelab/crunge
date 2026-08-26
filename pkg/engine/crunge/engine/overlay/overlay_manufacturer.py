from typing import Any, Callable, Iterable, Iterator, Protocol, runtime_checkable

from loguru import logger

from crunge.core import klass

from .overlay import Overlay


@runtime_checkable
class OverlayFactory(Protocol):
    name: str

    def create(self) -> Overlay: ...


OverlayConfig = str | dict[str, Any] | OverlayFactory


@klass.singleton
class OverlayRegistry:
    def __init__(self) -> None:
        self._makers: dict[str, Callable[..., Overlay]] = {}

    def __contains__(self, name: str) -> bool:
        return name in self._makers

    def register(self, name: str, maker: Callable[..., Overlay] = None):
        def decorate(maker):
            if name in self._makers:
                logger.warning(f"Overlay '{name}' re-registered")
            self._makers[name] = maker
            return maker

        return decorate(maker) if maker else decorate

    def get(self, name: str) -> Callable[..., Overlay] | None:
        return self._makers.get(name)


class DictOverlayFactory:
    def __init__(self, name: str, **kwargs: Any) -> None:
        self.name = name
        self.kwargs = kwargs

    def create(self) -> Overlay | None:
        maker = OverlayRegistry().get(self.name)
        if maker is None:
            logger.error(f"No overlay registered as '{self.name}'")
            return None
        return maker(**self.kwargs)


def as_overlay_factory(config: OverlayConfig) -> OverlayFactory:
    if isinstance(config, str):
        return DictOverlayFactory(config)
    if isinstance(config, dict):
        return DictOverlayFactory(**config)
    return config


class OverlayManufacturer:
    def __init__(self, configs: Iterable[OverlayConfig] = ()) -> None:
        self._factories: dict[str, OverlayFactory] = {}
        self.extend(configs)

    def __len__(self) -> int:
        return len(self._factories)

    def __contains__(self, name: str) -> bool:
        return name in self._factories

    def __iter__(self) -> Iterator[OverlayFactory]:
        return iter(self._factories.values())

    def add(self, config: OverlayConfig) -> OverlayFactory:
        factory = as_overlay_factory(config)
        if factory.name in self._factories:
            logger.warning(f"Overlay factory '{factory.name}' replaced")
        self._factories[factory.name] = factory
        return factory

    def extend(self, configs: Iterable[OverlayConfig]) -> None:
        for config in configs:
            self.add(config)

    def remove(self, name: str) -> None:
        if self._factories.pop(name, None) is None:
            logger.warning(f"Overlay factory '{name}' not found")

    def get(self, name: str) -> OverlayFactory | None:
        return self._factories.get(name)

    def manufacture(self, name: str) -> Overlay | None:
        factory = self._factories.get(name)
        if factory is None:
            logger.warning(f"No overlay factory named '{name}'")
            return None
        return factory.create()

    def manufacture_all(self) -> list[Overlay]:
        overlays = (factory.create() for factory in self._factories.values())
        return [overlay for overlay in overlays if overlay is not None]

    def validate(self) -> list[str]:
        """Names with no registered maker. Call at startup to fail loud."""
        registry = OverlayRegistry()
        return [name for name in self._factories if name not in registry]
