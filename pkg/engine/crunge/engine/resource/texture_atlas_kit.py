from typing import Dict
from pathlib import Path

from loguru import logger
from lxml import etree
import glm

from crunge.core import klass
from crunge.engine import RectI

from .texture_kit_base import TextureKitBase
from .texture import Texture
from .texture_atlas import TextureAtlas

@klass.singleton
class TextureAtlasKit(TextureKitBase):
    def __init__(self):
        super().__init__()

    def load_xml(self, path: Path) -> TextureAtlas:
        if path in self.textures:
            return self.textures[path]

        # Load the XML file
        if not path.exists():
            raise Exception(f'XML file not found: {path}')

        tree = etree.parse(path)
        root = tree.getroot()

        # Extract the imagePath attribute from the TextureAtlas element
        image_path = root.attrib['imagePath']
        image_path = path.parent / Path(image_path)
        if not image_path.exists():
            image_path = path.parent / Path(path.stem + '.png')
            if not image_path.exists():
                raise Exception(f'Image file not found: {image_path}')
        logger.debug(f"Image Path: {image_path}")

        wgpu_texture, width, height = self.load_wgpu_texture(image_path)
        #atlas = TextureAtlas(wgpu_texture, width, height)
        atlas = TextureAtlas(str(path.stem), RectI(0, 0, width, height), wgpu_texture)
        self.textures[path] = atlas

        # Iterate over each SubTexture element
        for sub_texture in root.findall('SubTexture'):
            # Extract attributes
            name = sub_texture.get('name')
            x = sub_texture.get('x')
            y = sub_texture.get('y')
            width = sub_texture.get('width')
            height = sub_texture.get('height')

            # Create a new texture
            texture = Texture(name, RectI(int(x), int(y), int(width), int(height)), wgpu_texture, atlas)
            atlas.add(texture)

        return atlas
    