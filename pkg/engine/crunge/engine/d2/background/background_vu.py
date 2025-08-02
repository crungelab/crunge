from typing import TYPE_CHECKING

from loguru import logger
import glm

from crunge import wgpu

from ...renderer import Renderer

from ..sprite import SpriteVu
from ..sprite import Sprite

from .background_program import BackgroundProgram


class BackgroundVu(SpriteVu):
    program: BackgroundProgram

    def __init__(self, sprite: Sprite = None) -> None:
        super().__init__(sprite)

    def create_program(self):
        self.program = BackgroundProgram()

    def _draw(self) -> None:
        if not self.manual_draw:
            return

        renderer = Renderer.get_current()
        pass_enc = renderer.pass_enc
        pass_enc.set_pipeline(self.program.render_pipeline.get())
        self.bind(pass_enc)
        pass_enc.draw(4)
