from pathlib import Path

import imageio.v3 as iio
from loguru import logger

from .loader import Loader
from ..resource.image import Image

class ImageLoader(Loader):
    def __init__(self, path: Path) -> None:
        super().__init__()
        self.path = path

    def load(self) -> Image:
        data = iio.imread(self.path, pilmode='RGBA')
        return Image(data)
