from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class TreePage(Page):
    def draw(self, renderer: Renderer):
        imgui.begin(self.title)
        #if imgui.tree_node("Expand me!", imgui.TREE_NODE_DEFAULT_OPEN):
        if imgui.tree_node("Expand me!"):
            imgui.text("Lorem Ipsum")
            imgui.tree_pop()
        imgui.end()
        super().draw(renderer)

def install(app: App):
    app.add_channel(PageChannel(TreePage, "tree", "Tree"))
