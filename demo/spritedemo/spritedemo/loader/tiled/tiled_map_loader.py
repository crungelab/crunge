from pathlib import Path

from loguru import logger
import glm
from pytmx import TiledMap, TiledTileLayer, TiledObjectGroup

from crunge.engine.loader import Loader


class TiledMapLoader(Loader):
    def __init__(self):
        super().__init__()
        self.map = None
        self.tileset = None

    def load(self, filename: Path):
        with open(filename, 'r') as f:
            data = json.load(f)

        self.map = data
        self.tileset = self.map['tilesets'][0]

        return self.map
