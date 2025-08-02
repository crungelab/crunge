from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class Popup(Page):
    def _draw(self):
        imgui.begin("Example: simple popup")

        if imgui.button("select"):
            imgui.open_popup("select-popup")

        imgui.same_line()

        if imgui.begin_popup("select-popup"):
            imgui.text("Select one")
            imgui.separator()
            imgui.selectable("One", False)
            imgui.selectable("Two", False)
            imgui.selectable("Three", False)
            imgui.end_popup()

        imgui.end()
        super()._draw()

class PopupContextView(Page):
    def _draw(self):
        imgui.begin("Example: popup context view")
        imgui.text("Right-click to set value.")
        if imgui.begin_popup_context_item("Item Context Menu"):
            imgui.selectable("Set to Zero", True)
            imgui.end_popup()
        imgui.end()
        super()._draw()

class PopupContextWindow(Page):
    def _draw(self):
        imgui.begin("Example: popup context window")
        if imgui.begin_popup_context_window():
            imgui.selectable("Clear", True)
            imgui.end_popup()
        imgui.end()
        super()._draw()

class PopupModal(Page):
    def _draw(self):
        imgui.begin("Example: simple popup modal")

        if imgui.button("Open Modal popup"):
            imgui.open_popup("select-popup")

        imgui.same_line()

        if imgui.begin_popup_modal("select-popup", True)[0]:
            imgui.text("Select an option:")
            imgui.separator()
            imgui.selectable("One", False)
            imgui.selectable("Two", False)
            imgui.selectable("Three", False)
            imgui.end_popup()

        imgui.end()
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(Popup, "popup", "Popup"))
    app.add_channel(PageChannel(PopupContextView, "popupcontextview", "Popup Context View"))
    app.add_channel(PageChannel(PopupContextWindow, "popupcontextwindow", "Popup Context Window"))

