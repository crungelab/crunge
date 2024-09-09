from pathlib import Path

import imageio.v3 as iio
import numpy as np
from loguru import logger

from .builder import Builder
from ..resource.image import Image

class ImageBuilder(Builder):
    def __init__(self) -> None:
        super().__init__()

    def build() -> Image:
        pass

    '''
    def load(self, path: Path) -> Image:
        data = iio.imread(path, pilmode='RGBA')
        return Image(data)
    '''