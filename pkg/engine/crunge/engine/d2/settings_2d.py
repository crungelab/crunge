from crunge.core import klass


@klass.singleton
class Settings2D:
    def __init__(self):
        #self.ppu: float = 64.0  # or whatever matches your art scale
        self.ppu: float = 128.0