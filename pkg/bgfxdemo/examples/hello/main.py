import os
from loguru import logger
from crunge import bgfx
from crunge.bgfx.window import Window
from crunge.bgfx.constants import *
#from crunge.bgfx.utils.debug import config_logging

import python_image

#config_logging()

class HelloWorld(Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)


    def init(self, platform_data):
        bgfx.render_frame()
        self.init_conf = init_conf = bgfx.Init()
        init_conf.platform_data = platform_data
        init_conf.type = bgfx.RendererType.COUNT
        #self.init_conf.type = bgfx.RendererType.DIRECT3_D11
        init_conf.vendor_id = BGFX_PCI_ID_NONE
        init_conf.device_id = 0
        init_conf.debug = True
        init_conf.resolution.width = self.width
        init_conf.resolution.height = self.height
        init_conf.resolution.reset = BGFX_RESET_VSYNC

        bgfx.init(init_conf)

        bgfx.set_debug(BGFX_DEBUG_TEXT)
        bgfx.set_view_clear(0, BGFX_CLEAR_COLOR | BGFX_CLEAR_DEPTH, 0x443355FF, 1.0, 0)

    def shutdown(self):
        bgfx.shutdown()

    def update(self, dt):
        mouse_x, mouse_y, buttons_states = self.get_mouse_state()

        bgfx.set_view_rect(0, 0, 0, self.width, self.height)
        bgfx.touch(0)
        bgfx.dbg_text_clear(0, False)
        
        bgfx.dbg_text_image(
            int(max(self.width / 2 / 8, 20)) - 20,
            int(max(self.height / 2 / 16, 6)) - 6,
            40,
            12,
            python_image.logo,
            160,
        )

        stats = bgfx.get_stats()

        bgfx.dbg_text_printf(
            1,
            1,
            0x0F,
            "Color can be changed with ANSI \x1b[9;me\x1b[10;ms\x1b[11;mc\x1b[12;ma\x1b[13;mp\x1b[14;me\x1b[0m code too.",
        )
        bgfx.dbg_text_printf(
            80,
            1,
            0x0F,
            "\x1b[;0m    \x1b[;1m    \x1b[; 2m    \x1b[; 3m    \x1b[; 4m    \x1b[; 5m    \x1b[; 6m    \x1b[; 7m    \x1b[0m",
        )
        bgfx.dbg_text_printf(
            80,
            2,
            0x0F,
            "\x1b[;8m    \x1b[;9m    \x1b[;10m    \x1b[;11m    \x1b[;12m    \x1b[;13m    \x1b[;14m    \x1b[;15m    \x1b[0m",
        )
        bgfx.dbg_text_printf(
            1,
            2,
            0x0F,
            f"Backbuffer {stats.width}W x {stats.height}H in pixels, debug text {stats.text_width}W x {stats.text_height}H in characters.",
        )
        bgfx.frame()

    def resize(self, width, height):
        bgfx.reset(
            self.width, self.height, BGFX_RESET_VSYNC, self.init_conf.resolution.format
        )


def main():
    test = HelloWorld(1280, 720, "examples/helloworld")
    test.run()

if __name__ == "__main__":
    main()