from crunge import engine
from crunge import imgui

from ..app import App
from ..page import Page, PageChannel


SPRITE_SCALING = 0.5

FBSIZE = (512, 256)

class FramebufferPage(Page):
    def __init__(self, name, title):
        super().__init__(name, title)
        self.fullwidth = self.fullheight = True
        self.sprite = ludi.Sprite(
            ":resources:images/space_shooter/playerShip1_orange.png",
            SPRITE_SCALING,
            center_x = 256,
            center_y = 128
            )
        image = self.sprite.texture.image
        self.texture = window.ctx.texture(image.size, components=3, data=image.convert("RGB").tobytes())
        self.offscreen = window.ctx.framebuffer(color_attachments=window.ctx.texture(FBSIZE))

    def reset(self):
        self.rotation = 0
        self.scale = 1
        self.alpha = 255
        self.color_enabled = True
        self.color = 1,1,1

    def draw(self):
        super().draw()
        #gui.set_next_window_pos((self.window.width - 512 - 16, 32), imgui.COND_ONCE)
        #gui.set_next_window_size((512, 512), imgui.COND_ONCE)
        #gui.set_next_window_pos((self.window.width - (512+256) - 32, 32), imgui.COND_ONCE)
        #gui.set_next_window_size((512, 512), imgui.COND_ONCE)

        imgui.begin(self.title)

        # Rotation
        imgui.image(self.texture.glo.value, self.texture.size)
        changed, self.rotation = imgui.drag_float(
            "Rotation", self.rotation,
        )
        self.sprite.angle = self.rotation

        # Scale
        changed, self.scale = imgui.drag_float(
            "Scale", self.scale, .1
        )
        self.sprite.scale = self.scale

        # Alpha
        changed, self.alpha = imgui.drag_int(
            "Alpha", self.alpha, 1, 0, 255
        )
        self.sprite.alpha = self.alpha

        # Color
        _, self.color_enabled = imgui.checkbox("Tint", self.color_enabled)
        if self.color_enabled:
            changed, self.color = imgui.color_edit3("Color", self.color)
            self.sprite.color = (int(self.color[0] * 255), int(self.color[1] * 255), int(self.color[2] * 255))
        else:
            self.sprite.color = 255, 255, 255

        if imgui.button("Reset"):
            self.reset()

        fbtexture = self.offscreen.color_attachments[0]
        imgui.image(fbtexture.glo.value, FBSIZE)

        imgui.end()

        self.offscreen.use()
        self.offscreen.clear((0, 0, 0, 0))
        vp = ludi.get_viewport()
        ludi.set_viewport(0, FBSIZE[0], 0, FBSIZE[1])

        prj = self.window.ctx.projection_2d
        self.window.ctx.projection_2d = (0, FBSIZE[0],FBSIZE[1],0)
        self.sprite.draw()
        ludi.draw_text("Simple line of text in 20 point", 0,0 , ludi.color.WHITE, 20)
        self.window.ctx.projection_2d = prj

        self.window.ctx.screen.use()
        ludi.set_viewport(*vp)
        self.sprite.draw()


def install(app):
    app.add_page(FramebufferPage, "framebuffer", "Framebuffer")
