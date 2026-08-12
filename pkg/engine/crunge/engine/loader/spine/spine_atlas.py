# spine_sprite_atlas.py

import re

from pathlib import Path

from loguru import logger

from crunge.engine.d2.sprite import Sprite
from crunge.engine.d2.skeleton.skeleton_data import SkeletonData

from ...resource.sprite.sprite_atlas import SpriteAtlas

from .spine_atlas_file import AtlasRegion

_SEQUENCE_SUFFIX = re.compile(r"^(?P<base>.+?)(?P<num>\d+)$")

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
        self._sprites: dict[str, "Sprite"] = {}
        self._indexed: dict[str, dict[int, "Sprite"]] = {}
        self._sequences: dict[str, dict[int, "Sprite"]] = {}  # base name -> {frame: sprite}

    def register_sprite(self, region: AtlasRegion, sprite) -> None:
        if region.index < 0:
            self._sprites[region.name] = sprite
            # Older exports encode image sequences in the region name itself
            # (left-wing01, left-wing02, ...) rather than via an index: field.
            # Index those under their base name too, so an attachment that
            # refers to the bare sequence name can still resolve.
            m = _SEQUENCE_SUFFIX.match(region.name)
            if m:
                base = m.group("base")
                frame = int(m.group("num"))
                self._sequences.setdefault(base, {})[frame] = sprite
        else:
            self._indexed.setdefault(region.name, {})[region.index] = sprite

    def get_sprite(self, name: str, index: int = -1):
        if index >= 0:
            sprite = self._indexed.get(name, {}).get(index)
            if sprite is not None:
                return sprite
            return self._sequences.get(name, {}).get(index)

        sprite = self._sprites.get(name)
        if sprite is not None:
            return sprite

        frames = self._indexed.get(name)
        if frames:
            return frames[min(frames)]

        frames = self._sequences.get(name)
        if frames:
            return frames[min(frames)]

        return None

    def add_page(self, page_atlas: SpriteAtlas):
        self.pages.append(page_atlas)

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
        self._sprites: dict[str, "Sprite"] = {}          # exact "name" or "name\0index"
        self._indexed: dict[str, dict[int, "Sprite"]] = {}  # name -> {index: sprite}

    def register_sprite(self, region: AtlasRegion, sprite) -> None:
        if region.index < 0:
            self._sprites[region.name] = sprite
        else:
            self._indexed.setdefault(region.name, {})[region.index] = sprite

    def get_sprite(self, name: str, index: int = -1):
        if index >= 0:
            return self._indexed.get(name, {}).get(index)

        sprite = self._sprites.get(name)
        if sprite is not None:
            return sprite

        # Indexed regions (image sequences) asked for by bare name: fall back
        # to the lowest index, which is the frame an attachment refers to when
        # it names a sequence without selecting a frame.
        frames = self._indexed.get(name)
        if frames:
            return frames[min(frames)]
        return None

    def add_page(self, page_atlas: SpriteAtlas):
        self.pages.append(page_atlas)

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

'''
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