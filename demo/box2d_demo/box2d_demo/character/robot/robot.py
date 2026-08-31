import glm

from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.builder.sprite import CollidableSpriteBuilder
from crunge.engine.loader.sprite.xml_sprite_atlas_loader import XmlSpriteAtlasLoader

from ..character.dynamic_character import DynamicCharacter

from .robot_brain import RobotBrain


class Robot(DynamicCharacter):
    def __init__(self, position=glm.vec2()):
        model = SpriteLoader(sprite_builder=CollidableSpriteBuilder()).load(
            "${resources}/tiled/characters/robot_idle.png"
        )
        super().__init__(position, model=model)

    def _seat(self):
        super()._seat()
        atlas = XmlSpriteAtlasLoader(sprite_builder=CollidableSpriteBuilder()).load(
            "${resources}/tiled/characters/robot/sheet.xml"
        )
        self.add(RobotBrain(atlas))

    @classmethod
    def produce(self, position=glm.vec2()):
        return Robot(position)  # TODO: Needs a brain
