from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel



class TreePage(Page):
    def draw(self, renderer: Renderer):
        imgui.begin(self.title)
        if imgui.tree_node("Expand me!"):
            imgui.text("Lorem Ipsum")
            imgui.tree_pop()
        imgui.end()
        super().draw(renderer)

class TreeExPage(Page):
    def draw(self, renderer: Renderer):
        imgui.begin(self.title)
        if imgui.tree_node_ex("Root", imgui.TreeNodeFlags.DEFAULT_OPEN):
            imgui.text("Lorem Ipsum")
            if imgui.tree_node_ex("LeafNode", imgui.TreeNodeFlags.DEFAULT_OPEN | imgui.TreeNodeFlags.LEAF):
                imgui.text("No Children")
                imgui.tree_pop()    
            imgui.tree_pop()
        imgui.end()
        super().draw(renderer)

def install(app: App):
    app.add_channel(PageChannel(TreePage, "tree", "Tree"))
    app.add_channel(PageChannel(TreeExPage, "tree_ex", "TreeEx"))
