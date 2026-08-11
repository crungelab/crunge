from crunge.engine.factory import ClassFactory
from crunge.engine.channel import SceneChannel
from crunge.engine.d2.view import SceneView2D
from crunge.engine.d2.scene import Scene2D

from .page import Page

class SpineDemoChannel(SceneChannel):
    def __init__(self, page: Page, name: str, title: str):
        super().__init__(
            ClassFactory(page),
            ClassFactory(Scene2D),
            name,
            title,
        )

