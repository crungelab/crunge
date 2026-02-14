from .builder_context import BuilderContext

class TiledBuilder:
    def __init__(self):
        pass

    @property
    def context(self):
        return BuilderContext.get_current()

    @property
    def map(self):
        return self.context.map