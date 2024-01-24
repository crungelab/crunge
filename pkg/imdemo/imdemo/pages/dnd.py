from crunge import imgui

from imdemo.page import Page


class DnD(Page):
    def draw(self):
        super().draw()
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

def install(app):
    app.add_page(DnD, "dnd", "Drag & Drop")
