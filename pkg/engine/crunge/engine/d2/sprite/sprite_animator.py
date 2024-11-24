from loguru import logger

from ..node_2d import Node2D
from .sprite_animation import SpriteAnimation


class SpriteAnimator:
    def __init__(self, node: Node2D) -> None:
        super().__init__()
        self.node = node
        self.animations: dict[str, SpriteAnimation] = {}
        self.current_animation: SpriteAnimation = None

    def add_animation(self, animation: SpriteAnimation) -> None:
        self.animations[animation.name] = animation

    def play(self, name: str) -> None:
        animation = self.animations.get(name)
        if animation is None:
            logger.debug(f"Animation not found: {name}")
            return
        self.current_animation = animation
        animation.play()

    def stop(self, name: str) -> None:
        animation = self.animations.get(name)
        if animation is None:
            return
        animation.stop()

    def update(self, dt: float) -> None:
        if self.current_animation is not None:
            self.current_animation.update(dt)
            if self.current_animation.playing:
                self.node.model = self.current_animation.frames[self.current_animation.current_frame].sprite
