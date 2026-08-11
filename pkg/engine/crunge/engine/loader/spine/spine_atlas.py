# spine_sprite_atlas.py

from pathlib import Path

from loguru import logger

from crunge.engine.d2.sprite import Sprite
from crunge.engine.d2.skeleton.skeleton_data import SkeletonData

from ...resource.sprite.sprite_atlas import SpriteAtlas

from .spine_atlas_file import AtlasRegion

class SpineAtlas:
    """Spine .atlas files can span multiple page images, unlike the XML
    format's single imagePath. SpriteAtlas (per your reference) appears to
    wrap exactly one texture, so each page becomes its own SpriteAtlas —
    this wrapper just aggregates the name -> Sprite lookup across all of
    them, since a skeleton's attachments reference regions by name only,
    with no notion of which page they came from."""

    def __init__(self, path: Path):
        self.path = path
        self.pages: list[SpriteAtlas] = []
        self._sprites: dict[str, Sprite] = {}  # "name" or "name\0index" -> Sprite

    def add_page(self, page_atlas: SpriteAtlas):
        self.pages.append(page_atlas)

    def register_sprite(self, region: AtlasRegion, sprite: Sprite) -> None:
        key = region.name if region.index < 0 else f"{region.name}\0{region.index}"
        self._sprites[key] = sprite

    def get_sprite(self, name: str, index: int = -1):
        key = name if index < 0 else f"{name}\0{index}"
        return self._sprites.get(key)

    def resolve(self, skeleton_data: "SkeletonData") -> None:
        for skin_attachments in skeleton_data.skins.values():
            for slot_name, attachments_by_name in skin_attachments.items():
                for att_name, attachment in attachments_by_name.items():
                    sprite = self.get_sprite(attachment.path)
                    if sprite is None:
                        logger.warning(
                            f"No atlas region found for attachment path '{attachment.path}' "
                            f"(slot '{slot_name}', attachment '{att_name}')"
                        )
                        continue
                    attachment.gpu_sprite = sprite

    '''
    def resolve(self, skeleton_data: "SkeletonData") -> None:
        """Wire this atlas's sprites into every RegionAttachment across all
        skins in skeleton_data. Called once after both are loaded."""
        for skin_attachments in skeleton_data.skins.values():
            for slot_name, attachment in skin_attachments.items():
                sprite = self.get_sprite(attachment.path)
                if sprite is None:
                    logger.warning(
                        f"No atlas region found for attachment path '{attachment.path}' (slot '{slot_name}')"
                    )
                    continue
                attachment.gpu_sprite = sprite
    '''