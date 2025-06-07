from loguru import logger

import numpy as np

from ....resource.image import Image

from ..debug import debug_image
from . import GltfBuilder
from .builder_context import BuilderContext


class ImageBuilder(GltfBuilder):
    def __init__(
        self, context: BuilderContext,  image_index: int
    ) -> None:
        super().__init__(context)
        self.image_index = image_index

    def build(self) -> Image:
        if self.image_index in self.context.image_cache:
            return self.context.image_cache[self.image_index]

        tf_image = self.tf_model.images[self.image_index]
        #debug_image(tf_image)

        #im = tf_image.get_array()
        im = Image(tf_image.get_array())

        '''
        shape = im.shape
        logger.debug(f"im.shape: {shape}")
        logger.debug(f"im.dtype: {im.dtype}")
        logger.debug(f"im.nbytes: {im.nbytes}")
        logger.debug(f"im.size: {im.size}")
        logger.debug(f"im.itemsize: {im.itemsize}")
        logger.debug(f"im.ndim: {im.ndim}")
        logger.debug(f"im.strides: {im.strides}")
        '''

        self.context.image_cache[self.image_index] = im
        return im
