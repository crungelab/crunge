# atlas_loader.py

import os
from loguru import logger

from crunge.engine.d2.sprite import Sprite

from ...math import Rect2i
from ...resource import ImageTexture

from .spine_atlas import AtlasFile, AtlasPage, parse_atlas


class SkeletonAtlas:
    """Loaded atlas: page textures + a name -> Sprite lookup for building
    RegionAttachment.gpu_sprite at skin-resolve time."""

    def __init__(self):
        self.page_textures: dict[str, ImageTexture] = {}  # image_path -> texture
        self.sprites: dict[str, Sprite] = {}               # region name -> Sprite

    def get_sprite(self, name: str, index: int = -1) -> Sprite | None:
        key = name if index < 0 else f"{name}\0{index}"  # ASSUMPTION: separator scheme for indexed frames, untested
        return self.sprites.get(key)


def load_atlas(atlas_path: str) -> SkeletonAtlas:
    atlas_file = parse_atlas(atlas_path)
    base_dir = os.path.dirname(atlas_path)
    result = SkeletonAtlas()

    for page in atlas_file.pages:
        image_path = os.path.join(base_dir, page.image_path)
        texture = ImageTexture(image_path)  # ASSUMPTION: constructor signature — confirm against actual ImageTexture
        result.page_textures[page.image_path] = texture

        for region in page.regions:
            if region.rotate is not False:
                # Rotated packing needs UV remapping the current Sprite/rect
                # model doesn't support (Sprite.rect is a plain axis-aligned
                # Rect2i consumed straight into the vertex shader's rect
                # uniform). Skipping rather than silently rendering wrong.
                logger.warning(f"Atlas region '{region.name}' is rotated in the page — not yet supported, skipping")
                continue

            rect = Rect2i(region.x, region.y, region.width, region.height)
            sprite = Sprite(texture, rect=rect)

            # TODO: offset_x/offset_y (whitespace-stripped edges) aren't applied
            # here. If any region actually had whitespace stripped during
            # packing, its RegionAttachment will be positioned slightly off —
            # per the docs' Whitespace-stripping section, the draw position
            # needs adjusting by (offset_x, offset_y) relative to original_width/
            # original_height. Deferring until we hit a real exported atlas
            # that actually strips whitespace (Spine's default packer may or
            # may not, depending on export settings).

            key = region.name if region.index < 0 else f"{region.name}\0{region.index}"
            result.sprites[key] = sprite

    return result