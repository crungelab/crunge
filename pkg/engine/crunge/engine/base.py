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
        return self._post_create()

    '''
    #def create(self) -> Self:
    def create(self, enabled=True):
        if self.created:
            return
        self._create()
        return self._post_create(enabled)
    '''

    def _create(self):
        pass

    def _post_create(self):
        self.created = True
        self.on_create()
        return self

    '''
    def _post_create(self, enabled=True):
        self.created = True
        self.on_create()
        if enabled:
            self.enable()
        return self
    '''

    def on_create(self):
        pass

    def destroy(self):
        if not self.created:
            return
        self._destroy()
        self.on_destroy()
        self.created = False

    def _destroy(self):
        pass

    def on_destroy(self):
        pass

    def enable(self):
        #self.enabled = True
        if not self.created:
            self.create()  # Ensure the object is created
        else:
            self.enabled = True

    '''
    def enable(self):
        #self.enabled = True
        if not self.created:
            self.create(enabled=True)  # Ensure the object is created
        else:
            self.enabled = True
    '''

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
