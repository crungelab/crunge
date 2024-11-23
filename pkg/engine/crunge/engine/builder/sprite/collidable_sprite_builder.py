import imageio
import cv2
import numpy as np

from loguru import logger
import glm

from ...math import Rect2i
from ...resource.texture import ImageTexture
from ...d2.sprite import Sprite

from .sprite_builder import SpriteBuilder

class CollidableSpriteBuilder(SpriteBuilder):
    def build(self, texture: ImageTexture, rect: Rect2i = None, color=glm.vec4(1.0, 1.0, 1.0, 1.0)) -> Sprite:
        #logger.debug(f"Building Sprite: {texture.image.name}")

        x = rect.x
        y = rect.y
        height = rect.height
        width = rect.width
        region = texture.image.data[y:y+height, x:x+width]

        #Extract the alpha channel
        if region.shape[2] < 4:
            logger.warning("Image does not have an alpha channel.")
            return Sprite(texture, rect, color)  # Return without contours

        alpha_channel = region[:, :, 3]  # Extract the alpha channel

        #Apply thresholding to keep only non-transparent pixels
        _, thresh = cv2.threshold(alpha_channel, 1, 255, cv2.THRESH_BINARY)

        #Find contours using OpenCV
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #print(f"contours: {contours}")

        # contours is a list of arrays; each array contains coordinates of a contour
        if len(contours) == 0:
            return Sprite(texture, rect, color)

        # Get the first contour and reshape it to a 2D float array
        points = contours[0].reshape(-1, 2).astype(float)

        #Recenter the points using half the width and height of the region
        points[:, 0] -= width / 2  # Shift x-coordinates by half the width
        points[:, 1] -= height / 2  # Shift y-coordinates by half the height

        #Flip the y-coordinates
        points[:, 1] = -points[:, 1]  # Negate the y-coordinates

        return Sprite(texture, rect, color, points)