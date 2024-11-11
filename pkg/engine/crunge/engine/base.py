#from typing import Self
#from typing_extensions import Self

from . import globals
from .gfx import Gfx

class Base:
    def __init__(self) -> None:
        self.created = False
        self.enabled = False

    def config(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self

    #def create(self) -> Self:
    def create(self):
        if self.created:
            return
        self._create()
        self.created = True
        self._post_create()
        return self

    def _create(self) -> None:
        pass

    def _post_create(self) -> None:
        pass

    def destroy(self) -> None:
        if not self.created:
            return
        self._destroy()
        self.on_destroy()
        self.created = False

    def _destroy(self) -> None:
        pass

    def on_destroy(self) -> None:
        pass

    def enable(self) -> None:
        if not self.created:
            self.create()  # Ensure the object is created
        self.enabled = True

    def disable(self):
        self.enabled = False

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
