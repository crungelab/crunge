"""System cursors.

The constants are SDL system-cursor ids, not cursor handles, so importing
this module is safe at any time. Handles are created on first use:
SDL_CreateSystemCursor fails before the video subsystem is initialized,
and a NULL handle passed to SDL_SetCursor means "redraw the current
cursor" -- the change silently does nothing. That's what happened once
engine code started importing this module ahead of sdl_init.

Always go through set_cursor() here, never sdl.set_cursor directly.
"""
from __future__ import annotations

from loguru import logger

from crunge import sdl

CURSOR_ARROW = sdl.SYSTEM_CURSOR_DEFAULT
CURSOR_TEXT = sdl.SYSTEM_CURSOR_TEXT
CURSOR_WAIT = sdl.SYSTEM_CURSOR_WAIT
CURSOR_PROGRESS = sdl.SYSTEM_CURSOR_PROGRESS
CURSOR_CROSSHAIR = sdl.SYSTEM_CURSOR_CROSSHAIR
CURSOR_HAND = sdl.SYSTEM_CURSOR_POINTER
CURSOR_MOVE = sdl.SYSTEM_CURSOR_MOVE
CURSOR_NOT_ALLOWED = sdl.SYSTEM_CURSOR_NOT_ALLOWED

# Two-way resizes
CURSOR_RESIZE_EW = sdl.SYSTEM_CURSOR_EW_RESIZE
CURSOR_RESIZE_NS = sdl.SYSTEM_CURSOR_NS_RESIZE
CURSOR_RESIZE_NWSE = sdl.SYSTEM_CURSOR_NWSE_RESIZE
CURSOR_RESIZE_NESW = sdl.SYSTEM_CURSOR_NESW_RESIZE

# Edge and corner resizes, for window-like frames
CURSOR_RESIZE_N = sdl.SYSTEM_CURSOR_N_RESIZE
CURSOR_RESIZE_NE = sdl.SYSTEM_CURSOR_NE_RESIZE
CURSOR_RESIZE_E = sdl.SYSTEM_CURSOR_E_RESIZE
CURSOR_RESIZE_SE = sdl.SYSTEM_CURSOR_SE_RESIZE
CURSOR_RESIZE_S = sdl.SYSTEM_CURSOR_S_RESIZE
CURSOR_RESIZE_SW = sdl.SYSTEM_CURSOR_SW_RESIZE
CURSOR_RESIZE_W = sdl.SYSTEM_CURSOR_W_RESIZE
CURSOR_RESIZE_NW = sdl.SYSTEM_CURSOR_NW_RESIZE

CURSOR_NAMES = {
    CURSOR_ARROW: "arrow",
    CURSOR_TEXT: "text",
    CURSOR_WAIT: "wait",
    CURSOR_PROGRESS: "progress",
    CURSOR_CROSSHAIR: "crosshair",
    CURSOR_HAND: "hand",
    CURSOR_MOVE: "move",
    CURSOR_NOT_ALLOWED: "not_allowed",
    CURSOR_RESIZE_EW: "resize_ew",
    CURSOR_RESIZE_NS: "resize_ns",
    CURSOR_RESIZE_NWSE: "resize_nwse",
    CURSOR_RESIZE_NESW: "resize_nesw",
    CURSOR_RESIZE_N: "resize_n",
    CURSOR_RESIZE_NE: "resize_ne",
    CURSOR_RESIZE_E: "resize_e",
    CURSOR_RESIZE_SE: "resize_se",
    CURSOR_RESIZE_S: "resize_s",
    CURSOR_RESIZE_SW: "resize_sw",
    CURSOR_RESIZE_W: "resize_w",
    CURSOR_RESIZE_NW: "resize_nw",
}

_handles: dict = {}


def get_cursor_name(cursor) -> str:
    if cursor is None:
        return "none"
    return CURSOR_NAMES.get(cursor, repr(cursor))


def set_cursor(cursor) -> bool:
    """Make `cursor` current, creating its handle on first use."""
    handle = _handles.get(cursor)
    if handle is None:
        handle = sdl.create_system_cursor(cursor)
        if handle is None:
            logger.error(
                f"create_system_cursor({get_cursor_name(cursor)}) failed -- "
                "is the SDL video subsystem initialized?"
            )
            return False
        _handles[cursor] = handle

    # SDL3 returns bool; compare to False in case the binding returns None.
    return sdl.set_cursor(handle) is not False


def destroy_cursors() -> None:
    """Free every handle created so far. Call from app teardown, before
    SDL_Quit. Safe to call more than once; handles are recreated on the
    next set_cursor."""
    if not _handles:
        return
    sdl.set_cursor(sdl.get_default_cursor())  # ASSUMPTION: bound; never destroy the active cursor
    for handle in _handles.values():
        sdl.destroy_cursor(handle)  # ASSUMPTION: bound
    _handles.clear()