from typing import TYPE_CHECKING

from . import globals

if TYPE_CHECKING:
    from .gfx import Gfx

class GfxAccess:
    @property
    def gfx(self) -> "Gfx":
        if globals.gfx is None:
            from .gfx import Gfx
            return Gfx()
        return globals.gfx

    @property
    def instance(self):
        if globals.instance is None:
            return self.gfx.instance
        return globals.instance

    @property
    def device(self):
        if globals.device is None:
            return self.gfx.device
        return globals.device

    @property
    def queue(self):
        if globals.queue is None:
            return self.gfx.queue
        return globals.queue
