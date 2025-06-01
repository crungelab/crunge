from pathlib import Path

from crunge import imnodes

from crunge import demo

resource_root = Path(__file__).parent.parent / "resources"


class ImFloDemo(demo.Demo):
    def __init__(self):
        super().__init__("ImFlo Demo", __package__, resource_root)
        imnodes.create_context()
        imnodes.push_attribute_flag(
            imnodes.AttributeFlags.ENABLE_LINK_DETACH_WITH_DRAG_CLICK
        )
        # TODO:Looks too scary to wrap.
        # io = imnodes.get_io()
        # io.link_detach_with_modifier_click.modifier = imgui.get_io().key_ctrl
