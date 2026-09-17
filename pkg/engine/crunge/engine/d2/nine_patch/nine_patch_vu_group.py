from .base_sprite_vu_group import BaseSpriteVuGroup
from .nine_patch_group import NinePatchGroup
from .nine_patch_vu import NinePatchVu


class NinePatchVuGroup(BaseSpriteVuGroup[NinePatchVu]):
    def __init__(
        self, nine_patch_group: NinePatchGroup, is_managed: bool = False
    ) -> None:
        super().__init__(nine_patch_group, is_managed=is_managed)

    @property
    def nine_patch_group(self) -> NinePatchGroup:
        return self.model_group
