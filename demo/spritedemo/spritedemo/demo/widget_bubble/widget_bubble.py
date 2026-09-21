from loguru import logger
import glm

from crunge import yoga
from crunge import imgui

from crunge.engine.d2.nine_patch.nine_patch import NinePatch, NinePatchFill
from crunge.engine.d2.nine_patch.nine_patch_vu import NinePatchVu
from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.d2.control import Control2D
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine import Color, colors
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


class WidgetBubbleDemo(Demo):
    """The bubble's children are placed by yoga, not by hand.

    Nothing in here sets a child position. The bubble is the layout root and
    its size is driven from the sliders; the ships are flex children with a
    fixed size, so yoga stacks them in the default column starting at the
    bubble's top-left corner. Drag Width and Height and watch them stay pinned
    to that corner while the bubble grows away from them.

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

        # Sizing intent, in world units. The node's actual unscaled_size arrives
        # from yoga through on_layout -- this is only what we ask for.
        self.patch_size = glm.vec2(patch.size) * 2.0

        # The bubble is the layout root: its Layout2D chip finds no ancestor
        # carrying one, so on_layout leaves its position alone and only takes
        # its size. That is what keeps it centered in the world here.
        #self.node = Control2D(model=patch, size=self.patch_size).seat(NinePatchVu())
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
        # _create, so set_size before this point would write through a None.
        self.node.layout.set_size(self.patch_size.x, self.patch_size.y)

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

    def update(self, delta_time: float) -> None:
        super().update(delta_time)
        # ASSUMPTION: Demo.update exists and this runs before the scene is
        # drawn. calculate() early-returns when nothing is dirty, so calling
        # it every frame costs a flag check. In the widget tree the Window
        # drives this; a scene-side control root has no such owner yet, which
        # is a gap worth closing once this pattern settles.
        if self.alive and self.node.layout.stale:
            width, height = self.node.size
            #self.node.layout.calculate(width, height) # no effect?
            self.node.layout.calculate()
            self.node.layout.apply()

            for i, control in enumerate(self.controls):
                l = control.layout
                logger.debug(
                    f"control {i} root={l.is_root} parent_size={l.parent_size} "
                    f"left={l.left} top={l.top} size={l.size} local={control.unscaled_size}"
                )
            logger.debug(f"bubble children={len(self.node.children)}")

    def _draw(self):
        imgui.set_next_window_pos((self.width - 300 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((300, 500), imgui.Cond.ONCE)

        imgui.begin("Widget Bubble")

        alive = self.alive

        # Size: sizing intent goes to the style, never to the node. The node's
        # unscaled_size is a result now, which is why there is a readout for it
        # below rather than a slider bound straight to it.
        imgui.text("Size")
        changed, width = imgui.drag_float("Width", self.patch_size.x, SIZE_STEP)
        if changed:
            self.patch_size.x = max(width, 0.0)
            if alive:
                self.node.layout.set_width(self.patch_size.x)

        changed, height = imgui.drag_float("Height", self.patch_size.y, SIZE_STEP)
        if changed:
            self.patch_size.y = max(height, 0.0)
            if alive:
                self.node.layout.set_height(self.patch_size.y)

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

        # Computed, not asked for. The bubble's unscaled_size should track the
        # Width/Height sliders; each control's position is whatever yoga decided,
        # in the bubble's own centered space, so the first one sits at
        # (-bw/2 + sw/2, +bh/2 - sh/2) and the second one a control-height lower.
        if alive:
            bubble_size = self.node.unscaled_size
            imgui.text(f"Bubble computed {bubble_size.x:.2f}, {bubble_size.y:.2f}")
            for i, control in enumerate(self.controls):
                pos = control.position
                imgui.text(f"Control {i} local {pos.x:.2f}, {pos.y:.2f}")

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
    #Settings2D().ppu = 1.0
    WidgetBubbleDemo().run()


if __name__ == "__main__":
    main()