from crunge import imgui

from crunge.engine.d3.graph_layer_3d import GraphLayer3D


class SceneTreeDock:
    def __init__(self):
        pass

    def draw(self, scene):
        imgui.begin("Scene")
        # imgui.text(f"Scene: {self.scene.name}")
        self.draw_layer_node(scene)
        imgui.end()

    def draw_layer_node(self, layer):
        if imgui.tree_node(layer.name):
            for child in layer.children:
                #self.draw_layer_node(child)
                if isinstance(child, GraphLayer3D):
                    self.draw_graph_layer_node(child)
                else:
                    self.draw_layer_node(child)
            imgui.tree_pop()

    def draw_graph_layer_node(self, layer):
        self.draw_scene_node(layer.root)

    def draw_scene_node(self, node):
        #if imgui.tree_node(f"##{id(node)}"):
        if imgui.tree_node(f"{node.__class__.__name__}"):
            for child in node.children:
                self.draw_scene_node(child)
            imgui.tree_pop()
