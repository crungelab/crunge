from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class DnD(Page):
    def _draw(self):
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
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(DnD, "dnd", "Drag & Drop"))
