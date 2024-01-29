from crunge import engine

class Base(engine.Base):
    pass

'''
from crunge.engine.gfx import Gfx

class Base:
    def __init__(self) -> None:
        pass

    @property
    def gfx(self):
        return Gfx()

    @property
    def instance(self):
        return self.gfx.instance

    @property
    def device(self):
        return self.gfx.device
'''