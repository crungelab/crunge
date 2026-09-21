import math

from loguru import logger
import glm

from crunge import yoga
from crunge import imgui

from crunge.engine.d2.nine_patch.nine_patch import NinePatch, NinePatchFill
from crunge.engine.d2.nine_patch.nine_patch_vu import NinePatchVu
from crunge.engine.d2.control import Control2D
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine import colors
from crunge.engine.d2.settings_2d import Settings2D

from crunge.engine.d2.control import WidgetControl2D
from crunge.engine.ui.button import Button
from crunge.engine.ui.text import Text


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


class ControlBubbleDemo(Demo):
    """A bubble that fits its children.

    Nothing in here sets a size or a position on anything the layout owns.
    The bubble is the layout root with no style size, calculated against
    undefined space, so yoga sizes it from its content: the two widget
    controls, stacked in the default column, plus padding equal to the
    nine-patch border so they sit inside the rounded edge rather than on it.

    The Width/Height sliders are a *minimum*, not a size. Below the content's
    size they do nothing; above it the bubble grows and the children stay
    pinned to its top-left inside the padding.

    The bubble is a root, and a root keeps its centered position, so it grows
    in every direction at once. For a bubble hanging from a speaker's head,
    restore top_left after each pass instead.

    Styles are authored in world units. Yoga does not care what the numbers
    mean, and the rest of the scene is in world units already, so nothing
    needs a PPU conversion on the way through on_layout.
    """

    def setup(self):
        super().setup()

        self.rotation = 0
        self.scale = 1.0
        self.color = colors.WHITE
        self.controls = []

        sprite = SpriteLoader().load("${resources}/skins/SpeechBubble.png")
        patch = self.patch = NinePatch.from_sprite(
            sprite, DEFAULT_INSETS, fill=DEFAULT_FILL
        )

        self.insets = glm.vec4(patch.insets)
        self.border_zoom = patch.border_zoom
        self.tile_x = bool(patch.fill & NinePatchFill.TILE_X)
        self.tile_y = bool(patch.fill & NinePatchFill.TILE_Y)

        # Minimum size, in world units. Zero lets content decide entirely.
        self.min_size = glm.vec2(0.0, 0.0)
        self.pad_to_border = True

        self.node = Control2D(model=patch).seat(NinePatchVu())

        self.button = Button(
            "Hello, World!",
            on_click=self.on_click,
            style=yoga.StyleBuilder().size(200, 50).build(),
        )

        self.add_control(WidgetControl2D(self.button))
        self.add_control(WidgetControl2D(Text("Hello, World!")))

        self.scene.attach(self.node)

        # After attach, not before: the Layout chip builds its yoga node in
        # _create, so writing style before this point writes through a None.
        #
        # Each child at its natural width. A column stretches its children
        # across by default, which would widen the text to match the button.
        self.node.layout.layout_node.set_align_items(yoga.Align.FLEX_START)
        self.apply_min_size()
        self.apply_padding()

    def add_control(self, control: WidgetControl2D) -> None:
        self.controls.append(control)
        self.node.add_child(control)

    def on_click(self):
        logger.info(f"Button clicked: {self.button.text}")

    def center_camera(self):
        pass

    def kill(self):
        self.node.destroy()
        self.node = None
        self.controls = []

    @property
    def alive(self) -> bool:
        return self.node is not None

    # -- style -------------------------------------------------------------

    def border_world(self) -> glm.vec4:
        """The nine-patch border as rendered, in world units: left, top,
        right, bottom. This is how far in the content has to sit to clear the
        rounded corners."""
        # ASSUMPTION: border_zoom scales the rendered border linearly. If it
        # doesn't, drop it and the padding will track the unscaled border.
        return glm.vec4(self.patch.border_texels) / Settings2D().ppu * self.border_zoom

    def apply_padding(self) -> None:
        if not self.alive:
            return
        border = self.border_world() if self.pad_to_border else glm.vec4(0.0)
        layout_node = self.node.layout.layout_node
        layout_node.set_padding(yoga.Edge.LEFT, border.x)
        layout_node.set_padding(yoga.Edge.TOP, border.y)
        layout_node.set_padding(yoga.Edge.RIGHT, border.z)
        layout_node.set_padding(yoga.Edge.BOTTOM, border.w)

    def apply_min_size(self) -> None:
        if not self.alive:
            return
        layout_node = self.node.layout.layout_node
        layout_node.set_min_width(self.min_size.x)
        layout_node.set_min_height(self.min_size.y)

    # -- frame -------------------------------------------------------------

    def update(self, delta_time: float) -> None:
        super().update(delta_time)
        # calculate() early-returns when nothing is dirty, so this costs a
        # flag check most frames. In the widget tree the Window drives this;
        # a scene-side control root has no such owner yet, which is a gap
        # worth closing once this pattern settles.
        if self.alive and self.node.layout.stale:
            self.node.layout.calculate()
            self.node.layout.apply()

    def _draw(self):
        imgui.set_next_window_pos((self.width - 300 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((300, 540), imgui.Cond.ONCE)

        imgui.begin("Widget Bubble")

        alive = self.alive

        # Minimum size: a floor under the content, not a size. The computed
        # size below is the answer; these only stop it going smaller.
        imgui.text("Minimum size")
        changed, width = imgui.drag_float("Min width", self.min_size.x, SIZE_STEP)
        if changed:
            self.min_size.x = max(width, 0.0)
            self.apply_min_size()

        changed, height = imgui.drag_float("Min height", self.min_size.y, SIZE_STEP)
        if changed:
            self.min_size.y = max(height, 0.0)
            self.apply_min_size()

        changed, self.pad_to_border = imgui.checkbox("Pad to border", self.pad_to_border)
        if changed:
            self.apply_padding()

        # Insets: normalized fractions of the sprite rect. The border moves,
        # so the padding has to follow it.
        imgui.separator()
        imgui.text("Insets")
        for i, label in enumerate(("Left", "Top", "Right", "Bottom")):
            changed, value = imgui.slider_float(label, self.insets[i], 0.0, 0.5)
            if changed:
                self.insets[i] = value
                self.patch.insets = self.insets
                self.apply_padding()

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
            self.border_zoom = max(self.border_zoom, 0.0)
            self.patch.border_zoom = self.border_zoom
            self.apply_padding()

        # Computed, not asked for. The bubble's size is content plus padding,
        # floored at the minimum. Each control's position is in the bubble's
        # own centered space, so the first sits at
        # (-bw/2 + pad_left + cw/2, +bh/2 - pad_top - ch/2).
        if alive:
            bubble_size = self.node.unscaled_size
            imgui.separator()
            imgui.text(f"Bubble computed {bubble_size.x:.2f}, {bubble_size.y:.2f}")
            for i, control in enumerate(self.controls):
                pos = control.position
                size = control.unscaled_size
                imgui.text(
                    f"Control {i} local {pos.x:.2f}, {pos.y:.2f} "
                    f"size {size.x:.2f}, {size.y:.2f}"
                )

        # Node transform: rotation and scale carry the borders and the
        # children with them. Yoga knows nothing about either -- it lays out in
        # the bubble's local space and the transform takes the whole thing to
        # the world.
        imgui.separator()
        imgui.text("Transform")
        changed, self.rotation = imgui.drag_float("Rotation", self.rotation, ANGLE_STEP)
        if changed and alive:
            self.node.rotation = self.rotation

        changed, self.scale = imgui.drag_float("Scale", self.scale, SCALE_STEP)
        if changed and alive:
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
    ControlBubbleDemo().run()


if __name__ == "__main__":
    main()