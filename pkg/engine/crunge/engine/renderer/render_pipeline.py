from crunge.engine import Base


class RenderPipeline(Base):
    def __init__(self):
        super().__init__()
        self.pipeline = None

    def get(self):
        return self.pipeline