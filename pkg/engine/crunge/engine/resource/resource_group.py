from .texture_kit import TextureKit
from .texture_atlas_kit import TextureAtlasKit

class ResourceGroup:
    def __init__(self) -> None:
        self.texture_kit = TextureKit()
        self.texture_atlas_kit = TextureAtlasKit()