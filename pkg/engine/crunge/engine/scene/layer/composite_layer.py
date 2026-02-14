from .layer_group import LayerGroup


class CompositeLayer(LayerGroup):
    def __init__(self, name: str = None):
        super().__init__(name)