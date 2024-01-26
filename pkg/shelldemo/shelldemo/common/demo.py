import sys, time
from loguru import logger


from crunge import as_capsule

from crunge import sdl
from crunge import shell

from crunge import wgpu
import crunge.wgpu.utils as utils

class Demo(shell.App):
    kWidth = 1024
    kHeight = 768

    def __init__(self):
        super().__init__(self.kWidth, self.kHeight, self.__class__.__name__, resizable=True)
