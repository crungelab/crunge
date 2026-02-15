import os
from pathlib import Path
import tkinter
import tkinter.filedialog

from loguru import logger
import glm

from crunge import sdl
from crunge import imgui
from crunge import engine

from crunge.engine.viewport import SurfaceViewport
from crunge.engine import Scheduler
from crunge.engine.render_options import RenderOptions

from crunge.engine.loader.gltf import GltfLoader

from crunge.engine.d3.scene import Scene3D
from crunge.engine.d3.controller.camera.arcball import ArcballCameraController
from crunge.engine.d3.view import SceneView3D
from crunge.engine.d3.director_3d import Director3D

from .ui.scene_tree_dock import SceneTreeDock


models_root = Path(os.environ.get("GLTF_SAMPLE_MODELS"))


class Viewer(engine.App):
    view: SceneView3D

    def __init__(self):
        super().__init__(title="WRender", resizable=True)
        self.delta_time = 0
        self.director: Director3D = None
        self.render_options = RenderOptions(
            use_depth_stencil=True, use_msaa=True, use_snapshot=True
        )

        self.stats_dock_visible = True
        self.scene_tree_dock = SceneTreeDock()
        self.scene_tree_dock_visible = True
        self.lighting_dock_visible = True

    @property
    def camera(self):
        return self.view.camera

    def create_viewport(self):
        self.viewport = SurfaceViewport(self.size, self.window, self.render_options)

    def create_view(self, scene: Scene3D):
        logger.debug("Creating view")
        self.view = SceneView3D(scene)

    def open(self):
        logger.debug("Opening scene")
        scene_path = tkinter.filedialog.askopenfilename(
            initialdir=models_root,
            title="Select file",
            filetypes=(
                ("gltf files", "*.gltf"),
                ("glb files", "*.glb"),
                ("all files", "*.*"),
            ),
        )
        if not scene_path:
            return
        scene_path = Path(scene_path)
        scene = GltfLoader().load(scene_path)

        Scheduler().schedule_once(lambda dt: self.show(scene))

    def show(self, scene: Scene3D):
        logger.debug("Showing scene")
        self.scene = scene
        self.create_view(scene)

        self.director = Director3D(scene)

        light = self.scene.lighting.lights[0]

        self.director.place_camera_and_light(self.camera, light)
        target = self.director.get_target_position()
        max_extent = self.director.get_max_extent()
        self.controller = ArcballCameraController(self, self.camera, target, max_extent)
        self.controller.activate()

        return self

    def _draw(self):
        self.draw_main_menu()
        self.draw_stats_dock()
        self.draw_scene_tree_dock()
        self.draw_lighting_dock()

        super()._draw()

    def draw_main_menu(self):
        if imgui.begin_main_menu_bar():
            # File
            if imgui.begin_menu("File", True):
                clicked_open, selected_open = imgui.menu_item(
                    "Open", "Ctrl+O", False, True
                )

                if clicked_open:
                    self.open()

                imgui.separator()

                clicked_exit, selected_exit = imgui.menu_item(
                    "Exit", "Ctrl+Q", False, True
                )
                if clicked_exit:
                    self.quit()

                imgui.end_menu()

            # View
            if imgui.begin_menu("View", True):
                clicked_stats, selected_stats = imgui.menu_item(
                    "Stats", "Ctrl+S", False, True
                )
                if clicked_stats:
                    self.stats_dock_visible = not self.stats_dock_visible
                clicked_scene, selected_scene = imgui.menu_item(
                    "Scene", "Ctrl+E", False, True
                )
                if clicked_scene:
                    self.scene_tree_dock_visible = not self.scene_tree_dock_visible
                clicked_lighting, selected_lighting = imgui.menu_item(
                    "Lighting", "Ctrl+L", False, True
                )
                if clicked_lighting:
                    self.lighting_dock_visible = not self.lighting_dock_visible
                imgui.end_menu()

            imgui.end_main_menu_bar()

    def _format_stat(self, key: str, ch) -> str:
        # ch is StatChannel
        if key.endswith("_s"):
            # seconds -> ms
            return f"{ch.ema * 1000.0:,.3f} ms"
        if key == "fps":
            return f"{ch.ema:,.1f}"
        # generic numeric
        return f"{ch.ema:,.3f}"

    def _format_stat_last(self, key: str, ch) -> str:
        if key.endswith("_s"):
            return f"{ch.last * 1000.0:,.3f} ms"
        if key == "fps":
            return f"{ch.last:,.1f}"
        return f"{ch.last:,.3f}"

    def draw_stats_dock(self):
        if not self.stats_dock_visible:
            return

        # If you want the window closable, pass p_open for the window here instead.
        imgui.begin("Stats")

        for group in self.stats.groups:
            if not imgui.collapsing_header(
                group.name,
                flags=imgui.TreeNodeFlags.DEFAULT_OPEN,
            ):
                continue

            channels = group.channels()
            if not channels:
                imgui.text_disabled("(no channels)")
                continue

            table_id = f"##stats_table_{group.name}"

            # Flags you likely want in a stats table
            flags = (
                imgui.TableFlags.BORDERS_INNER_V
                | imgui.TableFlags.ROW_BG
                | imgui.TableFlags.SIZING_STRETCH_PROP
            )

            if imgui.begin_table(table_id, 3, flags=flags):
                imgui.table_setup_column("Metric", imgui.TableColumnFlags.WIDTH_STRETCH)
                imgui.table_setup_column("Avg", imgui.TableColumnFlags.WIDTH_FIXED)
                imgui.table_setup_column("Last", imgui.TableColumnFlags.WIDTH_FIXED)
                imgui.table_headers_row()

                # Optional: stable order
                for key in sorted(channels.keys()):
                    ch = channels[key]

                    imgui.table_next_row()

                    imgui.table_set_column_index(0)
                    imgui.text_unformatted(key)

                    imgui.table_set_column_index(1)
                    imgui.text_unformatted(self._format_stat(key, ch))

                    imgui.table_set_column_index(2)
                    imgui.text_unformatted(self._format_stat_last(key, ch))

                imgui.end_table()

        imgui.end()

    def draw_scene_tree_dock(self):
        if not self.scene_tree_dock_visible:
            return
        self.scene_tree_dock.draw(self.scene)

    def draw_lighting_dock(self):
        if not self.lighting_dock_visible:
            return

        imgui.begin("Lighting")

        light = self.scene.lighting.lights[0]

        (
            light_position_speed,
            light_position_min,
            light_position_max,
        ) = self.director.get_light_position_limits()

        changed, position = imgui.drag_float3(
            "Diffuse Position",
            tuple(light.position),
            light_position_speed,
            light_position_min[0],
            light_position_max[0],
        )
        if changed:
            light.position = glm.vec3(position)

        changed, color = imgui.color_edit3("Diffuse Color", list(light.color))
        if changed:
            light.color = glm.vec3(color)

        light_energy_speed, light_energy_min, light_energy_max = (
            self.director.get_light_energy_limits()
        )
        # changed, energy = imgui.slider_float("Diffuse Energy", light.energy, 0.0, 100.0)
        # changed, energy = imgui.drag_float("Diffuse Energy", light.energy, light_energy_speed, light_energy_min, light_energy_max)
        changed, energy = imgui.slider_float(
            "Diffuse Energy", light.energy, light_energy_min, light_energy_max
        )
        if changed:
            light.energy = energy

        light_range_speed, light_range_min, light_range_max = (
            self.director.get_light_range_limits()
        )

        # changed, range = imgui.slider_float("Diffuse Range", light.range, 1.0, 20.0)
        changed, range = imgui.slider_float(
            "Diffuse Range", light.range, light_range_min, light_range_max
        )
        if changed:
            light.range = range

        imgui.end()

    def on_key(self, event: sdl.KeyboardEvent):
        key = event.key
        down = event.down
        if key == sdl.SDLK_ESCAPE and down:
            self.quit()
