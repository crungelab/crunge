from typing import TYPE_CHECKING, Type, Dict, List, Any, Callable

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
