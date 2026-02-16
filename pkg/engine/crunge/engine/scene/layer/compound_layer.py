from .layer_group import LayerGroup


class CompoundLayer(LayerGroup):
    def __init__(self, name: str = None):
        super().__init__(name)