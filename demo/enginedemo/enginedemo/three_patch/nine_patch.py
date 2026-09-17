import math

import glm

from .three_patch_demo_base import ThreePatchDemoBase
from .nine_patch_kit import Fill, Insets, NinePatch, load_sprite


# Texels to screen pixels: sets border thickness and the size of one repeat
BORDER_SCALE = 1.0

# Tune per image so corners (and any speech-bubble tail) sit fully inside the
# corner slices; anything in an edge slice gets repeated
SPEECH_INSETS = Insets(left=0.45, top=0.45, right=0.45, bottom=0.45)
HELP_INSETS = Insets(left=0.25, top=0.25, right=0.25, bottom=0.25)


class NinePatchDemo(ThreePatchDemoBase):
    """Two nine-patch bubbles, each stretching on both axes, one draw call each."""

    def create_patches(self):
        speech_path, help_path = self.skin_paths("SpeechBubble.png", "HelpBubble.png")

        self.speech = NinePatch(
            self.gfx,
            self.device,
            self.queue,
            load_sprite(self.device, self.queue, speech_path),
            SPEECH_INSETS,
            BORDER_SCALE,
            fill_y=Fill.STRETCH,  # vertical gradient: stretch rows, tile columns
        )
        self.help = NinePatch(
            self.gfx,
            self.device,
            self.queue,
            load_sprite(self.device, self.queue, help_path),
            HELP_INSETS,
            BORDER_SCALE,
        )
        return [self.speech, self.help]

    def layout_patches(
        self, view_projection: glm.mat4, width: float, height: float, elapsed: float
    ):
        half = width / 2

        # Width and height animate out of phase so tiling is visible on both axes
        speech_w = half * (0.55 + 0.35 * math.sin(elapsed))
        speech_h = height * (0.5 + 0.3 * math.cos(elapsed))
        self.speech.set_rect(
            view_projection,
            (half - speech_w) / 2,
            (height - speech_h) / 2,
            speech_w,
            speech_h,
        )

        # Help bubble in the right half, with the phases swapped
        help_w = half * (0.55 + 0.35 * math.cos(elapsed))
        help_h = height * (0.5 + 0.3 * math.sin(elapsed))
        self.help.set_rect(
            view_projection,
            half + (half - help_w) / 2,
            (height - help_h) / 2,
            help_w,
            help_h,
        )


def main():
    NinePatchDemo().run()


if __name__ == "__main__":
    main()