from .base_sprite_vu_group import BaseSpriteVuGroup
from .sprite_group import SpriteGroup
from .sprite_vu import SpriteVu


class SpriteVuGroup(BaseSpriteVuGroup[SpriteVu]):
    def __init__(self, sprite_group: SpriteGroup, is_managed: bool = False) -> None:
        super().__init__(sprite_group, is_managed=is_managed)

    @property
    def sprite_group(self) -> SpriteGroup:
        return self.model_group
