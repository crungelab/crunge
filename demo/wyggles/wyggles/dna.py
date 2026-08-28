import numpy as np
import imageio.v3 as iio

from crunge.engine.resource import Image
from crunge.engine.builder.texture.sprite_texture_builder import SpriteTextureBuilder

from wyggles.engine import *

class Dna:
    id_counter: int = 0

    def __init__(self, klass):
        self.klass = klass
        self.name = self.gen_id(klass.__name__)
        self.kind = klass.__name__.lower()

    @classmethod
    def gen_id(cls, name):
        result = name + str(cls.id_counter)
        cls.id_counter += 1
        return result

    def create_texture(self, surface, imgName, imgsize):
        buf = surface.get_data()
        stride = surface.get_stride()
        width, height = imgsize

        # 4. Create a NumPy array view with the correct stride
        # This tells NumPy how to correctly navigate the padded buffer
        # Stride arguments are: (bytes_to_next_row, bytes_to_next_pixel, bytes_to_next_channel)
        array_view = np.ndarray(
            shape=(height, width, 4),
            dtype=np.uint8,
            buffer=buf,
            strides=(stride, 4, 1) # Use the stride from cairo!
        )

        # 5. Create a new array with the correct RGBA channel order
        # The channel swap [2, 1, 0, 3] creates a new, contiguous array
        # with the RGBA format that imageio expects.
        # This step is REQUIRED as you cannot change channel order with strides alone.
        array_rgba = array_view[:, :, [2, 1, 0, 3]].copy()
        image = Image(array_rgba)
        return SpriteTextureBuilder().build([image])
