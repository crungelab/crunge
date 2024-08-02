import trimeshv.globals

class Base:
    def __init__(self) -> None:
        pass

    @property
    def instance(self):
        return trimeshv.globals.instance

    @property
    def device(self):
        return trimeshv.globals.device
