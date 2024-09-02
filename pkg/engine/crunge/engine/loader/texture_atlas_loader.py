from pathlib import Path

from loguru import logger
from lxml import etree

from crunge.engine import RectI

from .texture_loader_base import TextureLoaderBase

from ..resource.resource_manager import ResourceManager
from ..resource.texture import Texture
from ..resource.texture_atlas import TextureAtlas


class TextureAtlasLoader(TextureLoaderBase[TextureAtlas]):
    def __init__(self) -> None:
        super().__init__()
    
    def load(self, path: Path, name: str = None) -> TextureAtlas:
        path = ResourceManager().resolve_path(path)
        if not name:
            name = str(path)
        if atlas:= self.kit.get(name):
            return atlas

        # Load the XML file
        logger.debug(f"Loading TextureAtlas: {name}")

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

        wgpu_texture, width, height = self.load_wgpu_texture([image_path])
        atlas = TextureAtlas(name, RectI(0, 0, width, height), wgpu_texture)
        self.kit.add(atlas)

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
    