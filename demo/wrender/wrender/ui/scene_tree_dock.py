from crunge import imgui
import glm

from crunge.engine.d3.scene.layer import GraphLayer3D


class SceneTreeDock:
    def __init__(self):
        self.selected_node = None
        self.origin_epsilon = 1e-4  # flag nodes whose global position is ~(0,0,0)

    def draw(self, scene):
        imgui.begin("Scene")
        self.draw_layer_node(scene)
        imgui.end()

        # Separate inspector window for whatever's selected in the tree -
        # keeps the tree itself uncluttered while still surfacing detail.
        imgui.begin("Node Inspector")
        if self.selected_node is not None:
            self.draw_inspector(self.selected_node)
        else:
            imgui.text("Select a node in the Scene panel.")
        imgui.end()

    # ------------------------------------------------------------------
    # Tree
    # ------------------------------------------------------------------

    def draw_layer_node(self, layer):
        if imgui.tree_node(layer.name):
            for child in layer.children:
                if isinstance(child, GraphLayer3D):
                    self.draw_graph_layer_node(child)
                else:
                    self.draw_layer_node(child)
            imgui.tree_pop()

    def draw_graph_layer_node(self, layer):
        self.draw_scene_node(layer.root)

    def draw_scene_node(self, node):
        label = self._node_label(node)
        at_origin = self._is_at_origin(node)

        # ASSUMPTION: imgui.push_style_color / pop_style_color are exposed
        # the way pyimgui exposes them (COLOR_TEXT constant + RGBA tuple).
        if at_origin:
            imgui.push_style_color(imgui.Col.TEXT, (1.0, 0.35, 0.35, 1.0))

        node_open = imgui.tree_node(f"{label}###node_{id(node)}")

        if at_origin:
            imgui.pop_style_color()

        # Click the label (not just the arrow) to select for the inspector.
        if imgui.is_item_clicked():
            self.selected_node = node

        if node_open:
            for i, child in enumerate(node.children):
                imgui.push_id(i)
                self.draw_scene_node(child)
                imgui.pop_id()
            imgui.tree_pop()

    def _node_label(self, node) -> str:
        name = node.__class__.__name__
        pos = self._global_position(node)
        if pos is not None:
            return f"{name}  ({pos.x:.2f}, {pos.y:.2f}, {pos.z:.2f})"
        return name

    def _global_position(self, node):
        # ASSUMPTION: Node3D-family nodes expose global_transform; nodes
        # without a spatial transform (pure grouping nodes, etc.) won't.
        transform = getattr(node, "global_transform", None)
        if transform is None:
            return None
        return glm.vec3(transform[3].x, transform[3].y, transform[3].z)

    def _is_at_origin(self, node) -> bool:
        pos = self._global_position(node)
        if pos is None:
            return False
        return glm.length(pos) < self.origin_epsilon

    # ------------------------------------------------------------------
    # Inspector
    # ------------------------------------------------------------------

    def draw_inspector(self, node):
        imgui.text(f"Type: {node.__class__.__name__}")
        imgui.separator()

        self._draw_vec_row("Local position", getattr(node, "position", None))
        self._draw_vec_row("Global position", self._global_position(node))

        rotation = getattr(node, "rotation", None)
        if rotation is not None:
            imgui.text(f"Rotation: {rotation:.4f} rad")

        orientation = getattr(node, "orientation", None)
        if orientation is not None:
            imgui.text(
                f"Orientation: ({orientation.x:.3f}, {orientation.y:.3f}, "
                f"{orientation.z:.3f}, {orientation.w:.3f})"
            )

        self._draw_vec_row("Scale", getattr(node, "scale", None))

        imgui.separator()

        # Dirty-flag / caching state - directly relevant to the transform
        # bugs we've been chasing (stale caches, listeners registered late).
        local_dirty = getattr(node, "_local_dirty", None)
        global_dirty = getattr(node, "_global_dirty", None)
        bounds_dirty = getattr(node, "_bounds_dirty", None)
        if local_dirty is not None:
            imgui.text(f"local_dirty: {local_dirty}")
        if global_dirty is not None:
            imgui.text(f"global_dirty: {global_dirty}")
        if bounds_dirty is not None:
            imgui.text(f"bounds_dirty: {bounds_dirty}")

        imgui.separator()

        listeners = getattr(node, "listeners", None)
        if listeners is not None:
            imgui.text(f"Listeners ({len(listeners)}):")
            for listener in listeners:
                imgui.text(f"  - {listener.__class__.__name__}")

        vu = getattr(node, "vu", None)
        if vu is not None:
            imgui.separator()
            imgui.text(f"Vu: {vu.__class__.__name__}")
            vu_transform = getattr(vu, "transform", None)
            if vu_transform is not None:
                vu_pos = glm.vec3(vu_transform[3].x, vu_transform[3].y, vu_transform[3].z)
                imgui.text(
                    f"Vu cached transform pos: "
                    f"({vu_pos.x:.2f}, {vu_pos.y:.2f}, {vu_pos.z:.2f})"
                )

        if imgui.button("Force refresh (touch global_transform)"):
            # Handy one-click way to confirm whether a stale value is a
            # caching bug (this fixes it) vs a real upstream data issue
            # (this does nothing).
            _ = node.global_transform

    def _draw_vec_row(self, label: str, vec):
        if vec is None:
            return
        if hasattr(vec, "z"):
            imgui.text(f"{label}: ({vec.x:.3f}, {vec.y:.3f}, {vec.z:.3f})")
        elif hasattr(vec, "y"):
            imgui.text(f"{label}: ({vec.x:.3f}, {vec.y:.3f})")
        else:
            imgui.text(f"{label}: {vec}")