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

    def draw(self, renderer: Renderer) -> None:
        if not self.manual_draw:
            return
        
        '''
        frustum = renderer.camera_2d.frustum
        if not self.bounds.intersects(frustum):
            #logger.debug(f"SpriteVu: {self} is not in frustum: {frustum}")
            return
        '''
        # logger.debug("Drawing sprite")
        pass_enc = renderer.pass_enc
        pass_enc.set_pipeline(self.program.render_pipeline.get())
        self.bind(pass_enc)
        pass_enc.draw(4)
