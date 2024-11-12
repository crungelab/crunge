from pathlib import Path

from loguru import logger
from lxml import etree

from ..math import Rect2i
from ..resource.resource_manager import ResourceManager
from ..resource.texture import Texture
from ..resource.texture_atlas import TextureAtlas

from .texture_loader_base import TextureLoaderBase


class XmlTextureAtlasLoader(TextureLoaderBase[TextureAtlas]):
    def __init__(self) -> None:
        super().__init__()

    def load(self, path: Path, name: str = None) -> TextureAtlas:
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

        details = self.load_wgpu_texture([image_path])
        atlas = (
            TextureAtlas(details.texture, Rect2i(0, 0, details.width, details.height))
            .set_name(name)
            .set_path(path)
        )
        self.kit.add(atlas)

        # Iterate over each SubTexture element
        for sub_texture in root.findall("SubTexture"):
            # Extract attributes
            name = sub_texture.get("name")
            x = sub_texture.get("x")
            y = sub_texture.get("y")
            width = sub_texture.get("width")
            height = sub_texture.get("height")

            # Create a new texture
            texture = Texture(
                details.texture, Rect2i(int(x), int(y), int(width), int(height)), atlas
            ).set_name(name)
            atlas.add(texture)

        return atlas
