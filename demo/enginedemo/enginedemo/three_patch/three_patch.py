import math

import glm

from .three_patch_demo_base import ThreePatchDemoBase
from .three_patch_kit import Orientation, ThreePatch


class ThreePatchDemo(ThreePatchDemoBase):
    def create_patches(self):
        self.bubble = ThreePatch(
            self.gfx,
            self.device,
            self.queue,
            self.skin_paths(
                "SpeechBubble_01.png",  # left cap
                "SpeechBubble_02.png",  # stretchable middle
                "SpeechBubble_03.png",  # right cap
            ),
            Orientation.ROW,
        )
        return [self.bubble]

    def layout_patches(self, view_projection: glm.mat4, width: float, height: float, elapsed: float):
        # Animate the width so the middle patch visibly stretches and shrinks
        bubble_height = 100.0
        bubble_width = width * (0.5 + 0.25 * math.sin(elapsed))

        self.bubble.set_rect(
            view_projection,
            (width - bubble_width) / 2,
            (height - bubble_height) / 2,
            bubble_width,
            bubble_height,
        )


def main():
    ThreePatchDemo().run()


if __name__ == "__main__":
    main()
