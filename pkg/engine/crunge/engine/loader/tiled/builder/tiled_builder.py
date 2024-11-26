from .builder_context import BuilderContext

class TiledBuilder:
    def __init__(self, context: BuilderContext):
        self.context = context

    @property
    def map(self):
        return self.context.map