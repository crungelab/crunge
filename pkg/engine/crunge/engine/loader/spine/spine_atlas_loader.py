# spine_sprite_atlas_loader.py

from pathlib import Path

from loguru import logger

from ...math import Rect2i
from ...resource.resource_manager import ResourceManager
from ...resource.sprite.sprite_atlas import SpriteAtlas

from ...builder.sprite import SpriteBuilder, DefaultSpriteBuilder, SpriteAtlasBuilder

from ..texture.texture_loader import TextureLoader

from .spine_atlas_file import AtlasFile, AtlasRegion, parse_atlas
from .spine_atlas import SpineAtlas

from ...d2.sprite.sprite import SpriteFlipFlags

"""
_ROTATE_FLAGS = {
    0:   SpriteFlipFlags.NONE,
    90:  SpriteFlipFlags.DIAGONAL | SpriteFlipFlags.VERTICAL,     # swapped
    180: SpriteFlipFlags.HORIZONTAL | SpriteFlipFlags.VERTICAL,
    270: SpriteFlipFlags.DIAGONAL | SpriteFlipFlags.HORIZONTAL,   # swapped
}
"""

_ROTATE_FLAGS = {
    0: SpriteFlipFlags.NONE,
    90: SpriteFlipFlags.DIAGONAL | SpriteFlipFlags.HORIZONTAL,
    180: SpriteFlipFlags.HORIZONTAL | SpriteFlipFlags.VERTICAL,
    270: SpriteFlipFlags.DIAGONAL | SpriteFlipFlags.VERTICAL,
}

class SpineAtlasLoader(TextureLoader[SpineAtlas]):
    def __init__(
        self, sprite_builder: SpriteBuilder = DefaultSpriteBuilder()
    ) -> None:
        super().__init__()
        self.sprite_builder = sprite_builder

    def load(self, path: Path, name: str = None) -> SpineAtlas:
        path = ResourceManager().resolve_path(path)
        if not name:
            name = str(path)
        if atlas := self.kit.get_by_path(path):
            return atlas

        logger.debug(f"Loading Spine atlas: {name}")

        if not path.exists():
            raise Exception(f"Atlas file not found: {path}")

        atlas_file = parse_atlas(str(path))
        result = SpineAtlas(path)

        for page in atlas_file.pages:
            image_path = path.parent / Path(page.image_path)
            if not image_path.exists():
                raise Exception(f"Atlas page image not found: {image_path}")

            logger.debug(f"Atlas page image: {image_path}")
            image = self.image_loader.load(image_path)

            # One SpriteAtlas per page, same construction as XmlSpriteAtlasLoader.
            # Named/pathed by the page image so kit caching + lookup-by-path
            # still works per-page, distinct from the overall SpineSkeletonAtlas
            # which isn't itself kit-cached (it's a lightweight aggregate, not
            # a single loaded resource).
            page_atlas = SpriteAtlasBuilder().build(image)
            page_atlas.set_name(f"{name}#{page.image_path}").set_path(image_path)
            self.kit.add(page_atlas)

            for region in page.regions:
                if region.rotate in (90, 270):
                    # Region is stored rotated in the page, so its packed footprint is
                    # transposed relative to the logical width/height the atlas reports.
                    # The UV box must match the packed pixels; the quad keeps its
                    # logical size via attachment.width/height.
                    rect = Rect2i(region.x, region.y, region.height, region.width)
                else:
                    rect = Rect2i(region.x, region.y, region.width, region.height)

                sprite = self.sprite_builder.build(page_atlas.texture, rect).set_name(region.name)

                if region.rotate:
                    flags = _ROTATE_FLAGS.get(region.rotate)
                    if flags is None:
                        logger.warning(
                            f"Atlas region '{region.name}' has non-90°-multiple rotation "
                            f"({region.rotate}) — free rotation not supported, skipping"
                        )
                        continue
                    sprite.flip_flags = flags

                page_atlas.add(sprite)
                result.register_sprite(region, sprite)


            result.add_page(page_atlas)

        return result

"""
class SpineAtlasLoader(TextureLoader[SpineAtlas]):
    def __init__(
        self, sprite_builder: SpriteBuilder = DefaultSpriteBuilder()
    ) -> None:
        super().__init__()
        self.sprite_builder = sprite_builder

    def load(self, path: Path, name: str = None) -> SpineAtlas:
        path = ResourceManager().resolve_path(path)
        if not name:
            name = str(path)
        if atlas := self.kit.get_by_path(path):
            return atlas

        logger.debug(f"Loading Spine atlas: {name}")

        if not path.exists():
            raise Exception(f"Atlas file not found: {path}")

        atlas_file = parse_atlas(str(path))
        result = SpineAtlas(path)

        for page in atlas_file.pages:
            image_path = path.parent / Path(page.image_path)
            if not image_path.exists():
                raise Exception(f"Atlas page image not found: {image_path}")

            logger.debug(f"Atlas page image: {image_path}")
            image = self.image_loader.load(image_path)

            # One SpriteAtlas per page, same construction as XmlSpriteAtlasLoader.
            # Named/pathed by the page image so kit caching + lookup-by-path
            # still works per-page, distinct from the overall SpineSkeletonAtlas
            # which isn't itself kit-cached (it's a lightweight aggregate, not
            # a single loaded resource).
            page_atlas = SpriteAtlasBuilder().build(image)
            page_atlas.set_name(f"{name}#{page.image_path}").set_path(image_path)
            self.kit.add(page_atlas)

            for region in page.regions:
                rect = Rect2i(region.x, region.y, region.width, region.height)
                sprite = self.sprite_builder.build(page_atlas.texture, rect).set_name(region.name)

                if region.rotate:
                    flags = _ROTATE_FLAGS.get(region.rotate)
                    if flags is None:
                        logger.warning(
                            f"Atlas region '{region.name}' has non-90°-multiple rotation "
                            f"({region.rotate}) — free rotation not supported, skipping"
                        )
                        continue
                    sprite.flip_flags = flags

                page_atlas.add(sprite)
                result.register_sprite(region, sprite)

            result.add_page(page_atlas)

        return result
"""

"""
class SpineAtlasLoader(TextureLoader[SpineAtlas]):
    def __init__(
        self, sprite_builder: SpriteBuilder = DefaultSpriteBuilder()
    ) -> None:
        super().__init__()
        self.sprite_builder = sprite_builder

    def load(self, path: Path, name: str = None) -> SpineAtlas:
        path = ResourceManager().resolve_path(path)
        if not name:
            name = str(path)
        if atlas := self.kit.get_by_path(path):
            return atlas

        logger.debug(f"Loading Spine atlas: {name}")

        if not path.exists():
            raise Exception(f"Atlas file not found: {path}")

        atlas_file = parse_atlas(str(path))
        result = SpineAtlas(path)

        for page in atlas_file.pages:
            image_path = path.parent / Path(page.image_path)
            if not image_path.exists():
                raise Exception(f"Atlas page image not found: {image_path}")

            logger.debug(f"Atlas page image: {image_path}")
            image = self.image_loader.load(image_path)

            # One SpriteAtlas per page, same construction as XmlSpriteAtlasLoader.
            # Named/pathed by the page image so kit caching + lookup-by-path
            # still works per-page, distinct from the overall SpineSkeletonAtlas
            # which isn't itself kit-cached (it's a lightweight aggregate, not
            # a single loaded resource).
            page_atlas = SpriteAtlasBuilder().build(image)
            page_atlas.set_name(f"{name}#{page.image_path}").set_path(image_path)
            self.kit.add(page_atlas)

            for region in page.regions:
                if region.rotate is not False:
                    # Same limitation as before: current Sprite/rect model is
                    # axis-aligned only. Rotated-in-page regions need UV
                    # remapping SpriteBuilder doesn't do — skip rather than
                    # render wrong, and say so loudly.
                    logger.warning(
                        f"Atlas region '{region.name}' is rotated in page "
                        f"'{page.image_path}' — not yet supported, skipping"
                    )
                    continue

                rect = Rect2i(region.x, region.y, region.width, region.height)
                sprite = self.sprite_builder.build(page_atlas.texture, rect).set_name(region.name)
                page_atlas.add(sprite)

                result.register_sprite(region, sprite)

                # TODO: region.offset_x/offset_y (whitespace stripped from the
                # packed image) aren't applied to sprite/attachment positioning
                # yet — see the Whitespace-stripping section of Spine's atlas
                # format docs. Only matters if the export actually stripped
                # whitespace; unverified against a real DarkAssassin export.

            result.add_page(page_atlas)

        return result
"""
