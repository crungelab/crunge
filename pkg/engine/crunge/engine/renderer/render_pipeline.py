from crunge.engine import Base
from crunge.engine.gfx_access import GfxAccess

class RenderPipeline(GfxAccess, Base):
    def __init__(self):
        super().__init__()
        self.pipeline = None

    def get(self):
        return self.pipeline