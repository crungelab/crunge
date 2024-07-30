from enum import IntFlag

class WindowFlags(IntFlag):
    FULLSCREEN = 0x00000001  # window is in fullscreen mode
    OPENGL = 0x00000002  # window usable with OpenGL context
    OCCLUDED = 0x00000004  # window is occluded
    HIDDEN = 0x00000008  # window is neither mapped onto the desktop nor shown in the taskbar/dock/window list; SDL_ShowWindow() is required for it to become visible
    BORDERLESS = 0x00000010  # no window decoration
    RESIZABLE = 0x00000020  # window can be resized
    MINIMIZED = 0x00000040  # window is minimized
    MAXIMIZED = 0x00000080  # window is maximized
    MOUSE_GRABBED = 0x00000100  # window has grabbed mouse input
    INPUT_FOCUS = 0x00000200  # window has input focus
    MOUSE_FOCUS = 0x00000400  # window has mouse focus
    EXTERNAL = 0x00000800  # window not created by SDL
    HIGH_PIXEL_DENSITY = 0x00002000  # window uses high pixel density back buffer if possible
    MOUSE_CAPTURE = 0x00004000  # window has mouse captured (unrelated to MOUSE_GRABBED)
    ALWAYS_ON_TOP = 0x00008000  # window should always be above others
    UTILITY = 0x00020000  # window should be treated as a utility window, not showing in the task bar and window list
    TOOLTIP = 0x00040000  # window should be treated as a tooltip
    POPUP_MENU = 0x00080000  # window should be treated as a popup menu
    KEYBOARD_GRABBED = 0x00100000  # window has grabbed keyboard input
    VULKAN = 0x10000000  # window usable for Vulkan surface
    METAL = 0x20000000  # window usable for Metal view
    TRANSPARENT = 0x40000000  # window with transparent buffer
    NOT_FOCUSABLE = 0x80000000  # window should not be focusable
