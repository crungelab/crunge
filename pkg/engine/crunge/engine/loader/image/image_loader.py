from pathlib import Path

import imageio.v3 as iio
import numpy as np
from loguru import logger

from ..loader import Loader
from ...resource.image import Image

class ImageLoader(Loader):
    def __init__(self) -> None:
        super().__init__()

    def load(self, path: Path) -> Image:
        logger.debug(f"Loading image: {path}")
        data = iio.imread(path, pilmode='RGBA')
        image = Image(data).set_name(path.name).set_path(path)
        return image

class HdrImageLoader(Loader):
    def __init__(self) -> None:
        super().__init__()

    def load(self, path: Path) -> Image:
        data = iio.imread(path)
        im_height, im_width, im_channels = data.shape
        if im_channels == 3:
            # Add an alpha channel
            data = np.concatenate([data, np.ones((im_height, im_width, 1), dtype=data.dtype)], axis=-1)
        return Image(data).set_name(path.name).set_path(path)
