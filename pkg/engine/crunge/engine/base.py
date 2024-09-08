#from typing import Self
#from typing_extensions import Self
from . import globals
from .gfx import Gfx

class Base:
    def __init__(self) -> None:
        self.created = False

    #def create(self) -> Self:
    def create(self):
        if self.created:
            return
        self._create()
        self.on_create()
        self.created = True
        return self

    def _create(self):
        pass

    def on_create(self):
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
