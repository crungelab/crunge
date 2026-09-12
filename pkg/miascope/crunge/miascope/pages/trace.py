"""The miascope page: tree canvas, timeline, and inspector for one trace.

Modeled on canvasdemo's pages. `..page.Page` is the template's Page, which
submits the Skia canvas in `_draw`.
"""

from __future__ import annotations

import sys
import tkinter
import tkinter.filedialog
from pathlib import Path

from loguru import logger

from crunge import imgui
from crunge.demo import PageChannel
from crunge.engine import App, Renderer

from ..page import Page
from ..camera import Camera
from ..inspector import report
from ..model import Trace
from ..painter import Painter
from ..scene import Scene
from ..sources import DEFAULT_SAMPLE, load, sample_names
from ..style import CHANGE_TEXT, ERROR_TEXT, FONT_SIZE, GAP, LEVEL, PADDING

TEXT_BUFFER = 256  # crunge.imgui.input_text needs an explicit buffer size
from ..timeline import Timeline, describe


def ask_trace_path(initial_dir: str) -> str | None:
    """Show a native file dialog; return the chosen path, or None if cancelled."""
    root = tkinter.Tk()
    root.withdraw()                    # no empty Tk window next to the dialog
    root.attributes("-topmost", True)  # keep the dialog above the crunge window
    try:
        path = tkinter.filedialog.askopenfilename(
            parent=root,
            initialdir=initial_dir,
            title="Open trace",
            filetypes=(("Mia traces", "*.miatrace"), ("all files", "*.*")),
        )
    finally:
        root.destroy()
    return path or None  # "" or () when cancelled, depending on platform


def _xy(value) -> tuple[float, float]:
    """ImGui vectors may come back as tuples or as objects with x and y."""
    if hasattr(value, "x"):
        return float(value.x), float(value.y)
    return float(value[0]), float(value[1])


class TracePage(Page):
    def setup(self):
        super().setup()
        self.scale = 1.0
        self.painter = Painter(FONT_SIZE)
        self.camera = Camera()
        self.trace: Trace | None = None
        self.scene: Scene | None = None
        self.timeline: Timeline | None = None
        self.selected = None
        self.source: str | None = None  # a sample name or a path
        self.loaded = None              # the Source: trace, and the plan when it can be replayed
        self.samples = sample_names()
        self.error: str | None = None
        self.filter = ""
        self.dragging = False
        self.needs_fit = False
        self.open_requested = False
        self.load(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SAMPLE)

    def open(self):
        """Ask for a trace file and load it."""
        is_file = self.source is not None and Path(self.source).parent != Path(".")
        initial_dir = str(Path(self.source).parent) if is_file else str(Path.cwd())
        path = ask_trace_path(initial_dir)
        if path is not None:
            self.load(path)

    def load(self, source: str):
        """Load a sample by name (`blox.mia` records it fresh) or a file by path."""
        logger.debug(f"Loading trace from {source}")
        try:
            loaded = load(source)
        except Exception as e:  # show compile, runtime, and file errors in the panel
            logger.exception(f"Could not load {source}")
            self.error = f"{type(e).__name__}: {e}"
            return
        self.source, self.loaded, self.trace, self.error = source, loaded, loaded.trace, None
        self.scene = self.build_scene()
        self.timeline = Timeline(len(self.trace.events))
        self.selected = None
        self.needs_fit = True

    def build_scene(self) -> Scene:
        return Scene(
            self.trace,
            self.painter.measure,
            font_size=FONT_SIZE * self.scale,
            padding=PADDING * self.scale,
            gap=GAP * self.scale,
            level=LEVEL * self.scale,
        )

    def set_scale(self, scale: float):
        """Resize nodes, keeping the same part of the tree in view."""
        ratio = scale / self.scale
        self.scale = scale
        self.painter = Painter(FONT_SIZE * scale)
        self.scene = self.build_scene()
        self.camera.x *= ratio
        self.camera.y *= ratio

    def _draw(self):
        if self.open_requested:
            # Open the dialog between frames rather than while ImGui windows are half built.
            self.open_requested = False
            self.open()
        io = imgui.get_io()
        self.draw_file_panel()
        if self.trace is not None:
            width, height = _xy(io.display_size)
            if self.needs_fit:
                self.camera.fit(*self.scene.bounds, width, height)
                self.needs_fit = False
            self.timeline.update(io.delta_time)
            self.draw_timeline_panel()
            self.draw_inspector_panel()
            self.draw_plan_panel()
            self.handle_mouse(io)
            canvas = Renderer.get_current().canvas
            # ASSUMPTION: canvas pixels match ImGui display coordinates. On a
            # HiDPI display, multiply mouse and display size by
            # io.display_framebuffer_scale.
            self.painter.paint(canvas, self.scene, self.camera, self.timeline.t, self.selected, width, height)
        super()._draw()

    # ------------------------------------------------------------ panels

    def draw_file_panel(self):
        imgui.begin("Trace")
        if imgui.button("Open..."):
            self.open_requested = True
        if self.trace is not None:
            imgui.same_line()
            if imgui.button("Reload"):
                self.load(self.source)
            imgui.same_line()
            if imgui.button("Fit"):
                self.needs_fit = True
            changed, scale = imgui.slider_float("Node size", self.scale, 0.5, 2.0)   # ASSUMPTION: returns (changed, value)
            if changed:
                self.set_scale(scale)
            t = self.trace
            imgui.text(Path(self.source).name)
            imgui.text(f"{t.top.expert}: {len(t.nodes)} states, {len(t.spaces)} spaces, {len(t.events)} events")
        if self.error:
            imgui.text_colored(ERROR_TEXT, self.error)       # ASSUMPTION: text_colored(color, text)
        if self.samples and imgui.collapsing_header("Samples"):
            for name in self.samples:
                if imgui.button(name):
                    self.load(name)
        imgui.end()

    def draw_timeline_panel(self):
        tl = self.timeline
        imgui.begin("Timeline")
        if imgui.button("|<"):
            tl.seek(0)
        imgui.same_line()
        if imgui.button("<"):
            tl.step(-1)
        imgui.same_line()
        if imgui.button("Pause" if tl.playing else "Play"):
            tl.toggle()
        imgui.same_line()
        if imgui.button(">"):
            tl.step(1)
        imgui.same_line()
        if imgui.button(">|"):
            tl.seek(tl.last)
        changed, value = imgui.slider_int("Event", tl.t, 0, tl.last)   # ASSUMPTION: returns (changed, value)
        if changed:
            tl.seek(value)
            tl.playing = False
        imgui.text(describe(self.trace.events[tl.t]))
        imgui.end()

    def draw_plan_panel(self):
        """The actions of the solution: what the expert would actually do."""
        imgui.begin("Plan")
        node = self.selected if self.selected is not None else self.solution_node()
        if node is None:
            imgui.text("No solution in this trace.")
            imgui.end()
            return
        actions = self.trace.plan(node)
        imgui.text(f"state {node.id}: {len(actions)} actions")
        if self.loaded.runnable and node is self.solution_node():
            imgui.same_line()
            # Replaying performs real side effects, so only offer it for a
            # program miascope ran itself, where the functions still exist.
            if imgui.button("Run"):
                logger.info(f"Running plan for {self.source}")
                self.loaded.plan.run()
        for index, text in enumerate(actions, 1):
            imgui.text(f"{index}. {text}")
        imgui.end()

    def solution_node(self):
        """The top-level space's solution."""
        return self.trace.top.solution

    def draw_inspector_panel(self):
        imgui.begin("Inspector")
        if self.selected is None:
            imgui.text("Click a state to inspect it.")
            imgui.end()
            return
        r = report(self.trace, self.selected, self.timeline.t)
        for name, value in r.fields:
            imgui.text(f"{name}: {value}")
        if r.proposals and imgui.collapsing_header(f"Proposals ({len(r.proposals)})"):   # ASSUMPTION: returns bool
            for p in r.proposals:
                imgui.text(p["message"] + (f"  [{p['plan']}]" if p["plan"] else ""))
        if r.suspended and imgui.collapsing_header(f"Suspended tasks ({len(r.suspended)})"):
            for task in r.suspended:
                variables = ", ".join(f"${k} = {v}" for k, v in task["vars"].items())
                imgui.text(f"{task['task']}  pc {task['pc']}  {variables}")
        if r.context and imgui.collapsing_header(f"Context ({len(r.context)})"):
            _, self.filter = imgui.input_text("Filter", self.filter, TEXT_BUFFER)
            marks = {"added": "+ ", "removed": "- ", "kept": "  "}
            for row in r.context:
                if row.matches(self.filter):
                    imgui.text_colored(CHANGE_TEXT[row.change], marks[row.change] + row.clause)
        imgui.end()

    # ------------------------------------------------------------ input

    def handle_mouse(self, io):
        if io.want_capture_mouse:
            self.dragging = False
            return
        mx, my = _xy(io.mouse_pos)
        if io.mouse_wheel:
            self.camera.zoom_at(mx, my, 1.1 ** io.mouse_wheel)
        if imgui.is_mouse_dragging(0):             # ASSUMPTION: ImGuiMouseButton as int
            dx, dy = _xy(io.mouse_delta)
            self.camera.pan(dx, dy)
            self.dragging = True
        if imgui.is_mouse_released(0):
            if not self.dragging:
                self.selected = self.scene.hit(*self.camera.to_world(mx, my), self.timeline.t)
            self.dragging = False


def install(app: App):
    app.add_channel(PageChannel(TracePage, "trace", "Trace"))
