#from typing import Self
#from typing_extensions import Self

from . import globals
from .gfx import Gfx

class Base:
    def __init__(self) -> None:
        self.created = False
        self.enabled = False
        self.destroyed = False

    def config(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self

    #def create(self) -> Self: #TODO: need Python 3.11+
    def create(self):
        if self.created:
            return
        self._create()
        self.created = True
        self._post_create()
        return self

    def _create(self):
        pass

    def _post_create(self):
        self.reset()

    def reset(self) -> None:
        pass

    def destroy(self) -> None:
        if self.destroyed:
            return
        self._destroy()
        self.destroyed = True

    def _destroy(self) -> None:
        pass

    def enable(self):
        if self.enabled:
            return self
        if not self.created:
            self.create()  # Ensure the object is created
        self._enable()
        self.enabled = True
        return self

    def _enable(self) -> None:
        pass

    def disable(self):
        if not self.enabled:
            return
        self._disable()
        self.enabled = False

    def _disable(self) -> None:
        pass

    @property
    def gfx(self):
        #return globals.gfx
        return Gfx()

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
