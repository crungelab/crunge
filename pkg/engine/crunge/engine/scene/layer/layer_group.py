from .scene_layer import SceneLayer

class LayerGroup(SceneLayer):
    pass

"""
class GroupLayer(SceneLayer):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        #self.layers: list[SceneLayer] = []
        self.layers_by_name: dict[str, SceneLayer] = {}
    
    def add_layer(self, layer: SceneLayer):
        layer.scene = self
        #self.layers.append(layer)
        self.add_child(layer)
        self.layers_by_name[layer.name] = layer
        layer.enable()
        return layer
    
    def remove_layer(self, layer: SceneLayer):
        #self.layers.remove(layer)
        self.remove_child(layer)
        del self.layers_by_name[layer.name]
        return layer

    def get_layer(self, name: str):
        return self.layers_by_name.get(name)

    '''
    def clear(self):
        for layer in self.layers:
            layer.clear()

    def _draw(self):
        for layer in self.layers:
            layer.draw()

    def update(self, dt: float):
        for layer in self.layers:
            layer.update(dt)
    '''
"""