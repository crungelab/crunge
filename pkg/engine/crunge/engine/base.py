# from typing import Self
# from typing_extensions import Self

from loguru import logger

from enum import Enum, auto

from . import globals
from .gfx import Gfx


class Lifetime(Enum):
    INITIAL = auto()
    CREATING = auto()
    CREATED = auto()
    DESTROYING = auto()
    DESTROYED = auto()


class Base:
    def __init__(self) -> None:
        self._lifetime = Lifetime.INITIAL
        self._is_enabled = False

    @property
    def is_created(self) -> bool:
        return self._lifetime is Lifetime.CREATED

    @property
    def is_creating(self) -> bool:
        return self._lifetime is Lifetime.CREATING

    @property
    def is_destroyed(self) -> bool:
        return self._lifetime is Lifetime.DESTROYED

    @property
    def is_destroying(self) -> bool:
        return self._lifetime is Lifetime.DESTROYING

    @property
    def is_enabled(self) -> bool:
        return self._is_enabled

    def config(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self

    # def create(self) -> Self: #TODO: need Python 3.11+
    def create(self):
        if self._lifetime is not Lifetime.INITIAL:
            return self
        self._lifetime = Lifetime.CREATING
        self._create()
        self.create_children()
        self._lifetime = Lifetime.CREATED
        self._created()
        return self

    def _create(self) -> None:
        """Top-down. Own resources. Children NOT created yet."""
        pass

    def create_children(self) -> None:
        """Containers override."""
        pass

    def _created(self) -> None:
        """Bottom-up. Children created and reachable."""
        pass

    def reset(self) -> None:
        """Reset the object to its initial state."""
        self._reset()
        self.reset_children()

    def _reset(self) -> None:
        """Reset the object to its initial state."""
        pass

    def reset_children(self) -> None:
        """Containers override."""
        pass

    def destroy(self) -> None:
        if self.is_destroyed:
            return
        self._destroy()
        self.destroy_children()
        self._lifetime = Lifetime.DESTROYED

    def _destroy(self) -> None:
        pass

    def destroy_children(self) -> None:
        """Containers override."""
        pass

    def enable(self):
        if self._is_enabled:
            return self
        if self.is_creating:
            logger.warning(f"enable() during create: {self}")
            return self
        if not self.is_created:
            self.create()
        self._is_enabled = True
        self._enable()
        self.enable_children()
        return self

    def _enable(self) -> None:
        pass

    def enable_children(self) -> None:
        """Containers override."""
        pass

    def disable(self):
        if not self._is_enabled:
            return self
        self._is_enabled = False
        self._disable()
        return self

    def _disable(self) -> None:
        pass

    def _sync_lifetime(self, obj: "Base"):
        """Bring obj up to this node's lifetime state."""
        if self.is_created:
            obj.create()
        if self._is_enabled:
            obj.enable()

    @property
    def gfx(self):
        if globals.gfx is None:
            return Gfx()
        return globals.gfx

    @property
    def instance(self):
        if globals.instance is None:
            return Gfx().instance
        return globals.instance

    @property
    def device(self):
        if globals.device is None:
            return Gfx().device
        return globals.device

    @property
    def queue(self):
        if globals.queue is None:
            return Gfx().queue
        return globals.queue

    @property
    def wnd(self):
        return globals.current_window
