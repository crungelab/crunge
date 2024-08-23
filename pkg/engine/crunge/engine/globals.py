from typing import TYPE_CHECKING, Type, Dict, List, Any, Callable

if TYPE_CHECKING:
    from .window import Window

from crunge import wgpu

from .gfx import Gfx

gfx: Gfx = None

instance: wgpu.Instance = None
device: wgpu.Device = None
queue: wgpu.Queue = None

def set_gfx(g: Gfx):
    global gfx
    gfx = g
    global instance
    instance = g.instance
    global device
    device = g.device
    global queue
    queue = g.queue

current_window: "Window" = None

def set_current_window(w: "Window"):
    global current_window
    current_window = w

def get_current_window() -> "Window":
    return current_window

