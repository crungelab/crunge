import imageio
import cv2
import numpy as np

from loguru import logger
import glm

from ...math import Rect2i
from ...resource.resource_manager import ResourceManager
from ...resource.material import MaterialKit
from ...resource.texture import ImageTexture
from ...d2.sprite import Sprite

from ..resource_builder import ResourceBuilder


class SpriteBuilder(ResourceBuilder[Sprite]):
    #def __init__(self, kit: SpriteKit = ResourceManager().sprite_kit) -> None:
    def __init__(self, kit: MaterialKit = ResourceManager().material_kit) -> None:
        super().__init__(kit)

    def build(self, texture: ImageTexture, rect: Rect2i = None, color=glm.vec4(1.0, 1.0, 1.0, 1.0)) -> Sprite:
        #return Sprite(texture, rect, color)
        #logger.debug(f"Building Sprite: {texture.image.name}")

        # Step 1: Read the image using imageio
        #img = texture.image.data
        x = rect.x
        y = rect.y
        height = rect.height
        width = rect.width
        region = texture.image.data[y:y+height, x:x+width]

        # Step 2: Convert the image to grayscale
        gray_img = cv2.cvtColor(region, cv2.COLOR_RGB2GRAY)

        # Step 3: Apply thresholding to convert the image to binary
        _, thresh = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)

        # Step 4: Find contours using OpenCV
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #print(f"contours: {contours}")

        # contours is a list of arrays; each array contains coordinates of a contour
        '''
        points = []
        for contour in contours:
            #print(contour.reshape(-1, 2))  # Reshape for easier interpretation
            points.append(contour.reshape(-1, 2))
        #exit()
        '''
        if len(contours) == 0:
            return Sprite(texture, rect, color)

        # Get the first contour and reshape it to a 2D float array
        points = contours[0].reshape(-1, 2).astype(float)

        # Step 1: Recenter the points
        centroid = points.mean(axis=0)
        points = points - centroid

        # Step 2: Flip the points on the y-axis
        points[:, 1] = -points[:, 1]  # Negate the y-coordinates
        '''
        # Sort points counter-clockwise
        def sort_counter_clockwise(points, center):
            angles = np.arctan2(points[:, 1] - center[1], points[:, 0] - center[0])
            return points[np.argsort(angles)]

        points = sort_counter_clockwise(points, centroid)
        '''

        return Sprite(texture, rect, color, points)