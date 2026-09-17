import math

import glm

from .three_patch_demo_base import ThreePatchDemoBase
from .three_patch_kit import Orientation, ThreePatch


class ThreePatchColumnDemo(ThreePatchDemoBase):
    def create_patches(self):
        self.bubble = ThreePatch(
            self.gfx,
            self.device,
            self.queue,
            self.skin_paths(
                "CatalogBubble_01.png",  # top cap
                "CatalogBubble_02.png",  # stretchable middle
                "CatalogBubble_03.png",  # bottom cap
            ),
            Orientation.COLUMN,
        )
        return [self.bubble]

    def layout_patches(self, view_projection: glm.mat4, width: float, height: float, elapsed: float):
        # Animate the height so the middle patch visibly stretches and shrinks
        column_width = 200.0
        column_height = height * (0.5 + 0.25 * math.sin(elapsed))

        self.bubble.set_rect(
            view_projection,
            (width - column_width) / 2,
            (height - column_height) / 2,
            column_width,
            column_height,
        )


def main():
    ThreePatchColumnDemo().run()


if __name__ == "__main__":
    main()
