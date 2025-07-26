from typing import TYPE_CHECKING

from loguru import logger
import glm

from crunge import wgpu

from ..sprite import SpriteVu
from ..sprite import Sprite

from .background_program import BackgroundProgram


class BackgroundVu(SpriteVu):
    program: BackgroundProgram

    def __init__(self, sprite: Sprite = None) -> None:
        super().__init__(sprite)

    def create_program(self):
        self.program = BackgroundProgram()
