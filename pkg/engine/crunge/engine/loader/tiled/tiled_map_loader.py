from pathlib import Path
import json

from ..loader import Loader

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

    def get_tileset(self):
        return self.tileset

    def get_tileset_image(self):
        return self.tileset['image']

    def get_tileset_tilewidth(self):
        return self.tileset['tilewidth']

    def get_tileset_tileheight(self):
        return self.tileset['tileheight']

    def get_tileset_tilecount(self):
        return self.tileset['tilecount']

    def get_tileset_columns(self):
        return self.tileset['columns']

    def get_tileset_margin(self):
        return self.tileset['margin']

    def get_tileset_spacing(self):
        return self.tileset['spacing']

    def get_tileset_tile_offset(self):
        return self.tileset['tileoffset']

    def get_tileset_tile_properties(self):
        return self.tileset['tileproperties']

    def get_tileset_properties(self):
        return self.tileset['properties']

    def get_tileset_name(self):
        return self.tileset['name']

    def get_tileset_first_gid(self):
        return self.tileset['firstgid']

    def get_tileset_image_width(self):
        return self.tileset['imagewidth']

    def get_tileset_image_height(self):
        return self.tileset['imageheight']

    def get_tileset_image_source(self):
        return self.tileset['image']

    def get_tileset_image_transparent_color(self):
        return self.tileset['transparentcolor']
