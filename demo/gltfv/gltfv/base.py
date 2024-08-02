import gltfv.globals

class Base:
    def __init__(self) -> None:
        pass

    @property
    def instance(self):
        return gltfv.globals.instance

    @property
    def device(self):
        return gltfv.globals.device
