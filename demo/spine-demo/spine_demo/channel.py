from crunge.engine.factory import ClassFactory
from crunge.engine.channel import SceneChannel
from crunge.engine.d2.scene import Scene2D

from .page import Page


class SpineDemoChannel(SceneChannel):
    def __init__(self, page_type: type[Page], name: str, title: str, version: str):
        super().__init__(
            ClassFactory(page_type),
            ClassFactory(Scene2D),
            f"{name}_{version}",
            title,
        )
        self.asset_name = name
        self.version = version

    def produce_display(self, *args, **kwargs) -> Page:
        #return super().produce_display(*args, self.asset_name, self.title, self.version, **kwargs)
        return super().produce_display(self.asset_name, self.title, self.version, **kwargs)


class SpineEssChannel(SpineDemoChannel):
    def __init__(self, page_type: type[Page], name: str, title: str):
        super().__init__(page_type, name, title, "ess")


class SpineProChannel(SpineDemoChannel):
    def __init__(self, page_type: type[Page], name: str, title: str):
        super().__init__(page_type, name, title, "pro")
