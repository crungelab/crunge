import imageio
import cv2
import numpy as np

from loguru import logger
import glm

from ... import colors
from ...math import Rect2i
from ...resource.texture import ImageTexture
from ...resource import Sampler
from ...d2.sprite import Sprite

from .sprite_builder import SpriteBuilder

class CollidableSpriteBuilder(SpriteBuilder):
    def build(self, texture: ImageTexture, rect: Rect2i = None, sampler: Sampler = None, color=colors.WHITE) -> Sprite:
        x = rect.x
        y = rect.y
        height = rect.height
        width = rect.width

        # region = texture.image.data[y:y+height, x:x+width]
        region = texture.images[0].data[y:y+height, x:x+width]

        # Must be RGBA for alpha-based masking
        if region.ndim < 3 or region.shape[2] < 4:
            logger.warning("Image does not have an alpha channel.")
            return Sprite(texture, rect, sampler, color)

        # --- 1) Build binary mask from alpha (robust to anti-aliasing) ---
        alpha = region[:, :, 3]
        alpha = cv2.GaussianBlur(alpha, (3, 3), 0)  # soften stair-step edges slightly
        _, mask = cv2.threshold(alpha, 10, 255, cv2.THRESH_BINARY)

        # --- 2) Pad so shapes touching edges aren't clipped ---
        PAD = 2
        mask_padded = cv2.copyMakeBorder(mask, PAD, PAD, PAD, PAD, cv2.BORDER_CONSTANT, value=0)

        # --- 3) Morphology: close pinholes, open specks ---
        kernel = np.ones((3, 3), np.uint8)
        mask_padded = cv2.morphologyEx(mask_padded, cv2.MORPH_CLOSE, kernel, iterations=1)
        mask_padded = cv2.morphologyEx(mask_padded, cv2.MORPH_OPEN,  kernel, iterations=1)

        # --- 4) Optional upscale to stabilize tiny, bumpy edges ---
        scale = 1
        h0, w0 = mask_padded.shape[:2]
        if min(h0, w0) < 128:
            scale = 2
            mask_work = cv2.resize(mask_padded, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)
        else:
            mask_work = mask_padded

        # --- 5) Find contours (outer only, keep detail) ---
        contours, _hier = cv2.findContours(mask_work, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if not contours:
            return Sprite(texture, rect, sampler, color)

        # --- 6) Filter out specks by area & pick the largest (typical for a single tile) ---
        min_area = max(4, int(0.0005 * mask_work.shape[0] * mask_work.shape[1]))  # ~0.05% of tile area
        contours = [c for c in contours if cv2.contourArea(c) >= min_area]
        if not contours:
            return Sprite(texture, rect, sampler, color)

        # Choose the largest outer contour
        contour = max(contours, key=cv2.contourArea)

        # --- 7) Light simplification to reduce insane vertex counts but keep bumps ---
        peri = cv2.arcLength(contour, True)
        eps = 0.003 * peri  # 0.3% of perimeter; tweak if needed
        contour = cv2.approxPolyDP(contour, eps, True)

        # --- 8) Undo scaling & padding so coordinates are back in region space (0..w, 0..h) ---
        if scale != 1:
            contour = (contour / scale).astype(np.float32)
        contour[:, 0, 0] -= PAD
        contour[:, 0, 1] -= PAD

        # Clamp to region bounds just in case morphology/pad nudged edges slightly negative
        contour[:, 0, 0] = np.clip(contour[:, 0, 0], 0, width  - 1)
        contour[:, 0, 1] = np.clip(contour[:, 0, 1], 0, height - 1)

        # --- 9) Collision rect from contour (in region coordinates) ---
        bx, by, bw, bh = cv2.boundingRect(contour.astype(np.int32))
        collision_rect = Rect2i(bx, by, bw, bh)

        # --- 10) Recenter & flip Y to your sprite's coordinate convention ---
        points = contour.reshape(-1, 2).astype(np.float32)
        points[:, 0] -= width / 2.0
        points[:, 1] -= height / 2.0
        points[:, 1] = -points[:, 1]  # flip Y

        return Sprite(texture, rect, sampler, color, points, collision_rect)

    '''
    def build(self, texture: ImageTexture, rect: Rect2i = None, sampler:Sampler = None, color=colors.WHITE) -> Sprite:
        #logger.debug(f"Building Sprite: {texture.image.name}")

        x = rect.x
        y = rect.y
        height = rect.height
        width = rect.width
        #region = texture.image.data[y:y+height, x:x+width]
        region = texture.images[0].data[y:y+height, x:x+width]

        #Extract the alpha channel
        if region.shape[2] < 4:
            logger.warning("Image does not have an alpha channel.")
            return Sprite(texture, rect, sampler, color)  # Return without contours

        alpha_channel = region[:, :, 3]  # Extract the alpha channel

        #Apply thresholding to keep only non-transparent pixels
        _, thresh = cv2.threshold(alpha_channel, 1, 255, cv2.THRESH_BINARY)

        #Find contours using OpenCV
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #print(f"contours: {contours}")

        # contours is a list of arrays; each array contains coordinates of a contour
        if len(contours) == 0:
            return Sprite(texture, rect, sampler, color)
        
        x, y, w, h = cv2.boundingRect(contours[0])
        collision_rect = Rect2i(x, y, w, h)


        # Get the first contour and reshape it to a 2D float array
        points = contours[0].reshape(-1, 2).astype(float)

        #Recenter the points using half the width and height of the region
        points[:, 0] -= width / 2  # Shift x-coordinates by half the width
        points[:, 1] -= height / 2  # Shift y-coordinates by half the height

        #Flip the y-coordinates
        points[:, 1] = -points[:, 1]  # Negate the y-coordinates

        return Sprite(texture, rect, sampler, color, points, collision_rect)
        '''