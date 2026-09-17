from loguru import logger
import glm

from crunge import imgui

from crunge.engine.d2.nine_patch.nine_patch import NinePatch, NinePatchFill
from crunge.engine.d2.nine_patch.nine_patch_vu import NinePatchVu
from crunge.engine.d2.sized_node_2d import SizedNode2D
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine import Color, colors

from ..demo import Demo

ANGLE_STEP = glm.radians(1)
SCALE_STEP = 0.01
SIZE_STEP = 0.05
ZOOM_STEP = 0.01

# Run find_insets.py on the image for the real values: the caps must contain
# the whole rounded corner, and anything left in an edge slice gets repeated
DEFAULT_INSETS = glm.vec4(0.45, 0.45, 0.45, 0.45)

# The bubble has a vertical gradient, so rows stretch and only columns tile
DEFAULT_FILL = NinePatchFill.TILE_X


class NinePatchDemo(Demo):
    def setup(self):
        super().setup()

        self.rotation = 0
        self.scale = 1.0
        self.color = colors.WHITE

        # ASSUMPTION: a ${skins} token, matching ${images}
        sprite = SpriteLoader().load("${resources}/skins/SpeechBubble.png")
        patch = self.patch = NinePatch.from_sprite(
            sprite, DEFAULT_INSETS, fill=DEFAULT_FILL
        )

        self.insets = glm.vec4(patch.insets)
        self.border_zoom = patch.border_zoom
        self.tile_x = bool(patch.fill & NinePatchFill.TILE_X)
        self.tile_y = bool(patch.fill & NinePatchFill.TILE_Y)

        # The node owns the drawn size; the patch only supplies the borders
        self.patch_size = glm.vec2(patch.size) * 2.0

        self.node = SizedNode2D(model=patch, size=self.patch_size).seat(NinePatchVu())
        self.scene.attach(self.node)

    def center_camera(self):
        pass

    def kill(self):
        self.node.destroy()
        self.node = None

    def _draw(self):
        imgui.set_next_window_pos((self.width - 300 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((300, 420), imgui.Cond.ONCE)

        imgui.begin("Nine Patch")

        # Size: what the node was told to be, which is what the patch fills
        imgui.text("Size")
        changed, width = imgui.drag_float("Width", self.patch_size.x, SIZE_STEP)
        if changed:
            self.patch_size.x = max(width, 0.0)
            self.node.size = self.patch_size

        changed, height = imgui.drag_float("Height", self.patch_size.y, SIZE_STEP)
        if changed:
            self.patch_size.y = max(height, 0.0)
            self.node.size = self.patch_size

        # Insets: normalized fractions of the sprite rect
        imgui.separator()
        imgui.text("Insets")
        for i, label in enumerate(("Left", "Top", "Right", "Bottom")):
            changed, value = imgui.slider_float(label, self.insets[i], 0.0, 0.5)
            if changed:
                self.insets[i] = value
                self.patch.insets = self.insets

        texels = self.patch.border_texels
        imgui.text(f"{int(texels.x)}, {int(texels.y)}, {int(texels.z)}, {int(texels.w)} texels")

        # Fill: unset axes stretch, which is what a gradient needs
        imgui.separator()
        imgui.text("Fill")
        changed_x, self.tile_x = imgui.checkbox("Tile X", self.tile_x)
        changed_y, self.tile_y = imgui.checkbox("Tile Y", self.tile_y)
        if changed_x or changed_y:
            fill = NinePatchFill.STRETCH
            if self.tile_x:
                fill |= NinePatchFill.TILE_X
            if self.tile_y:
                fill |= NinePatchFill.TILE_Y
            self.patch.fill = fill

        changed, self.border_zoom = imgui.drag_float(
            "Border Zoom", self.border_zoom, ZOOM_STEP
        )
        if changed:
            self.patch.border_zoom = max(self.border_zoom, 0.0)

        # Node transform: rotation and scale carry the borders with them
        imgui.separator()
        imgui.text("Transform")
        changed, self.rotation = imgui.drag_float("Rotation", self.rotation, ANGLE_STEP)
        if changed:
            self.node.rotation = self.rotation

        changed, self.scale = imgui.drag_float("Scale", self.scale, SCALE_STEP)
        if changed:
            self.node.scale = glm.vec2(self.scale, self.scale)

        changed, color = imgui.color_edit4("Tint", self.color)
        if changed:
            self.color = color
            self.patch.color = color

        imgui.separator()
        if imgui.button("Reset"):
            self.reset()

        if imgui.button("Kill"):
            self.kill()

        imgui.end()

        super()._draw()


def main():
    NinePatchDemo().run()


if __name__ == "__main__":
    main()