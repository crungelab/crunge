import glfw
from imgui_bundle import imgui 

key_map = {
    glfw.KEY_TAB: imgui.Key.tab,
    glfw.KEY_LEFT: imgui.Key.left_arrow,
    glfw.KEY_RIGHT: imgui.Key.right_arrow,
    glfw.KEY_UP: imgui.Key.up_arrow,
    glfw.KEY_DOWN: imgui.Key.down_arrow,
    glfw.KEY_PAGE_UP: imgui.Key.page_up,
    glfw.KEY_PAGE_DOWN: imgui.Key.page_down,
    glfw.KEY_HOME: imgui.Key.home,
    glfw.KEY_END: imgui.Key.end,
    glfw.KEY_INSERT: imgui.Key.insert,
    glfw.KEY_DELETE: imgui.Key.delete,
    glfw.KEY_BACKSPACE: imgui.Key.backspace,
    glfw.KEY_SPACE: imgui.Key.space,
    glfw.KEY_ENTER: imgui.Key.enter,
    glfw.KEY_ESCAPE: imgui.Key.escape,
    glfw.KEY_APOSTROPHE: imgui.Key.apostrophe,
    glfw.KEY_COMMA: imgui.Key.comma,
    glfw.KEY_MINUS: imgui.Key.minus,
    glfw.KEY_PERIOD: imgui.Key.period,
    glfw.KEY_SLASH: imgui.Key.slash,
    glfw.KEY_SEMICOLON: imgui.Key.semicolon,
    glfw.KEY_EQUAL: imgui.Key.equal,
    glfw.KEY_LEFT_BRACKET: imgui.Key.left_bracket,
    glfw.KEY_BACKSLASH: imgui.Key.backslash,
    glfw.KEY_RIGHT_BRACKET: imgui.Key.right_bracket,
    glfw.KEY_GRAVE_ACCENT: imgui.Key.grave_accent,
    glfw.KEY_CAPS_LOCK: imgui.Key.caps_lock,
    glfw.KEY_SCROLL_LOCK: imgui.Key.scroll_lock,
    glfw.KEY_NUM_LOCK: imgui.Key.num_lock,
    glfw.KEY_PRINT_SCREEN: imgui.Key.print_screen,
    glfw.KEY_PAUSE: imgui.Key.pause,
    glfw.KEY_KP_0: imgui.Key.keypad0,
    glfw.KEY_KP_1: imgui.Key.keypad1,
    glfw.KEY_KP_2: imgui.Key.keypad2,
    glfw.KEY_KP_3: imgui.Key.keypad3,
    glfw.KEY_KP_4: imgui.Key.keypad4,
    glfw.KEY_KP_5: imgui.Key.keypad5,
    glfw.KEY_KP_6: imgui.Key.keypad6,
    glfw.KEY_KP_7: imgui.Key.keypad7,
    glfw.KEY_KP_8: imgui.Key.keypad8,
    glfw.KEY_KP_9: imgui.Key.keypad9,
    glfw.KEY_KP_DECIMAL: imgui.Key.keypad_decimal,
    glfw.KEY_KP_DIVIDE: imgui.Key.keypad_divide,
    glfw.KEY_KP_MULTIPLY: imgui.Key.keypad_multiply,
    glfw.KEY_KP_SUBTRACT: imgui.Key.keypad_subtract,
    glfw.KEY_KP_ADD: imgui.Key.keypad_add,
    glfw.KEY_KP_ENTER: imgui.Key.keypad_enter,
    glfw.KEY_KP_EQUAL: imgui.Key.keypad_equal,
    glfw.KEY_LEFT_SHIFT: imgui.Key.left_shift,
    glfw.KEY_LEFT_CONTROL: imgui.Key.left_ctrl,
    glfw.KEY_LEFT_ALT: imgui.Key.left_alt,
    glfw.KEY_LEFT_SUPER: imgui.Key.left_super,
    glfw.KEY_RIGHT_SHIFT: imgui.Key.right_shift,
    glfw.KEY_RIGHT_CONTROL: imgui.Key.right_ctrl,
    glfw.KEY_RIGHT_ALT: imgui.Key.right_alt,
    glfw.KEY_RIGHT_SUPER: imgui.Key.right_super,
    glfw.KEY_MENU: imgui.Key.menu,
}

# Add number keys
for i in range(10):
    key_map[getattr(glfw, f'KEY_{i}')] = getattr(imgui.Key, f"_{str(i)}")

# Add letter keys
for c in range(ord('A'), ord('Z') + 1):
    key_map[getattr(glfw, f'KEY_{chr(c)}')] = getattr(imgui.Key, chr(c).lower())

# Add function keys
for i in range(1, 13):
    key_map[getattr(glfw, f'KEY_F{i}')] = getattr(imgui.Key, f'f{i}')
