import ctypes
from ctypes import Structure, c_float, c_uint32, sizeof, c_bool, c_int, c_void_p
import time
import sys
from pathlib import Path

from loguru import logger
import numpy as np
import imageio.v3 as iio
import glm

from crunge import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils
from crunge.engine import Renderer

from ..demo import Demo
from ...sprite import Sprite

class SpriteDemo(Demo):
    def __init__(self):
        super().__init__()
        self.sprite = Sprite()

        model = glm.mat4(1.0)  # Identity matrix
        x = self.width / 2
        y = self.height / 2
        
        model = glm.translate(model, glm.vec3(x, y, 0))
        model = glm.rotate(model, glm.radians(45.0), glm.vec3(0, 0, 1))
        model = glm.scale(model, glm.vec3(200, 200, 1))

        self.sprite.transform = model
        self.scene.add_child(self.sprite)

def main():
    SpriteDemo().create().run()


if __name__ == "__main__":
    main()
