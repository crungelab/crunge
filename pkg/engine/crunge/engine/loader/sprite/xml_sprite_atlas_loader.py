from pathlib import Path

from loguru import logger
from lxml import etree

from ...math import Rect2i
from ...resource.resource_manager import ResourceManager
from ...resource.sprite.sprite_atlas import SpriteAtlas

from ...builder.sprite import SpriteBuilder, DefaultSpriteBuilder, SpriteAtlasBuilder, CollidableSpriteBuilder

from ..texture.texture_loader import TextureLoader


class XmlSpriteAtlasLoader(TextureLoader[SpriteAtlas]):
    def __init__(
        #self, sprite_builder: SpriteBuilder = DefaultSpriteBuilder()
        self, sprite_builder: SpriteBuilder = CollidableSpriteBuilder()
    ) -> None:
        super().__init__()
        self.sprite_builder = sprite_builder

    def load(self, path: Path, name: str = None) -> SpriteAtlas:
        path = ResourceManager().resolve_path(path)
        if not name:
            name = str(path)
        if atlas := self.kit.get_by_path(path):
            return atlas

        # Load the XML file
        logger.debug(f"Loading TextureAtlas: {name}")

        if not path.exists():
            raise Exception(f"XML file not found: {path}")

        tree = etree.parse(path)
        root = tree.getroot()

        # Extract the imagePath attribute from the TextureAtlas element
        image_path = root.attrib["imagePath"]
        image_path = path.parent / Path(image_path)

        if not image_path.exists():
            image_path = path.parent / Path(path.stem + ".png")
            if not image_path.exists():
                raise Exception(f"Image file not found: {image_path}")

        logger.debug(f"Image Path: {image_path}")

        # Load the image
        image = self.image_loader.load(image_path)

        # Create a new SpriteAtlas
        atlas = SpriteAtlasBuilder().build(image)
        atlas.set_name(name).set_path(path)

        self.kit.add(atlas)

        # Iterate over each SubTexture element
        for sub_texture in root.findall("SubTexture"):
            # Extract attributes
            name = sub_texture.get("name")
            x = sub_texture.get("x")
            y = sub_texture.get("y")
            width = sub_texture.get("width")
            height = sub_texture.get("height")

            sprite = self.sprite_builder.build(
                atlas.texture, Rect2i(int(x), int(y), int(width), int(height))
            ).set_name(name)

            atlas.add(sprite)

        return atlas
