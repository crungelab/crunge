from crunge import imgui
from crunge.engine import Renderer

from imdemo.page import Page


class Popup(Page):
    def draw(self, renderer: Renderer):
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
        super().draw(renderer)

class PopupContextView(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Example: popup context view")
        imgui.text("Right-click to set value.")
        if imgui.begin_popup_context_item("Item Context Menu"):
            imgui.selectable("Set to Zero", True)
            imgui.end_popup()
        imgui.end()
        super().draw(renderer)

class PopupContextWindow(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Example: popup context window")
        if imgui.begin_popup_context_window():
            imgui.selectable("Clear", True)
            imgui.end_popup()
        imgui.end()
        super().draw(renderer)

class PopupModal(Page):
    def draw(self, renderer: Renderer):
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
        super().draw(renderer)

def install(app):
    app.add_page(Popup, "popup", "Popup")
    app.add_page(PopupContextView, "popupcontextview", "Popup Context View")
    app.add_page(PopupContextWindow, "popupcontextwindow", "Popup Context Window")
    app.add_page(PopupModal, "popupmodal", "Popup Modal")

