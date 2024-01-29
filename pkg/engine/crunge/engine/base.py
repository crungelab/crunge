from . import globals
from .gfx import Gfx

class Base:
    def __init__(self) -> None:
        pass

    @property
    def gfx(self):
        #return globals.gfx
        return Gfx()

    @property
    def instance(self):
        return globals.instance

    @property
    def device(self):
        return globals.device

    @property
    def queue(self):
        return globals.queue
    
    @property
    def wnd(self):
        return globals.current_window

    '''
    @property
    def ctx(self):
        return globals.current_context
    '''