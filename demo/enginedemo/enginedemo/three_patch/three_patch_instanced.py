import math

import glm

from .three_patch_demo_base import ThreePatchDemoBase
from .three_patch_kit import InstancedThreePatch, Orientation


class ThreePatchInstancedDemo(ThreePatchDemoBase):
    """A row bubble in the left half and a column bubble in the right half, one draw call each."""

    def create_patches(self):
        self.row = InstancedThreePatch(
            self.gfx,
            self.device,
            self.queue,
            self.skin_paths(
                "SpeechBubble_01.png",
                "SpeechBubble_02.png",
                "SpeechBubble_03.png",
            ),
            Orientation.ROW,
        )
        self.column = InstancedThreePatch(
            self.gfx,
            self.device,
            self.queue,
            self.skin_paths(
                "CatalogBubble_01.png",
                "CatalogBubble_02.png",
                "CatalogBubble_03.png",
            ),
            Orientation.COLUMN,
        )
        return [self.row, self.column]

    def layout(self, view_projection: glm.mat4, width: float, height: float, elapsed: float):
        half = width / 2

        # Row: stretches horizontally, centered in the left half
        row_height = 100.0
        row_width = half * (0.5 + 0.35 * math.sin(elapsed))
        self.row.set_rect(
            view_projection,
            (half - row_width) / 2,
            (height - row_height) / 2,
            row_width,
            row_height,
        )

        # Column: stretches vertically, centered in the right half, out of phase
        column_width = 200.0
        column_height = height * (0.5 + 0.25 * math.cos(elapsed))
        self.column.set_rect(
            view_projection,
            half + (half - column_width) / 2,
            (height - column_height) / 2,
            column_width,
            column_height,
        )


def main():
    ThreePatchInstancedDemo().run()


if __name__ == "__main__":
    main()
