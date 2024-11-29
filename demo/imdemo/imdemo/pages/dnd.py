from crunge import imgui
from crunge.engine import Renderer

from ..app import App
from ..page import Page, PageChannel


class DnD(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Example: drag and drop")

        imgui.button('source')
        if imgui.begin_drag_drop_source():
            imgui.set_drag_drop_payload('itemtype', 'payload')
            imgui.button('dragged source')
            imgui.end_drag_drop_source()

        imgui.button('dest')
        if imgui.begin_drag_drop_target():
            payload = imgui.accept_drag_drop_payload('itemtype')
            if payload is not None:
                print('Received Payload:  ', payload)
                print('Received Payload Data:', payload.data)
            imgui.end_drag_drop_target()

        imgui.end()
        super().draw(renderer)

def install(app: App):
    #app.add_page(DnD, "dnd", "Drag & Drop")
    app.add_channel(PageChannel(DnD, "dnd", "Drag & Drop"))
