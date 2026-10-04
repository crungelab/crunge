"""List the crunge.skia and crunge.imgui names miascope's UI assumes, and which are missing.

    python -m crunge.miascope.check_bindings
"""

from crunge import imgui, skia

SKIA = {
    "Font": ["set_size", "measure_text"],
    "Paint": ["set_anti_alias", "set_color4f", "set_stroke", "set_stroke_width"],
    "Canvas": ["save", "restore", "scale", "translate", "draw_line", "draw_round_rect", "draw_string"],
    "Color4f": [],
    "Rect": ["make_ltrb"],
}

IMGUI = [
    "begin", "end", "text", "text_colored", "button", "same_line", "separator",
    "input_text", "slider_int", "slider_float", "collapsing_header", "get_io",
    "is_mouse_dragging", "is_mouse_released",
]

IO_FIELDS = ["want_capture_mouse", "mouse_pos", "mouse_delta", "mouse_wheel", "display_size", "delta_time"]


def main():
    missing = []
    for cls, methods in SKIA.items():
        owner = getattr(skia, cls, None)
        if owner is None:
            missing.append(f"skia.{cls}")
            continue
        missing += [f"skia.{cls}.{m}" for m in methods if not hasattr(owner, m)]
    missing += [f"imgui.{name}" for name in IMGUI if not hasattr(imgui, name)]
    io_type = getattr(imgui, "IO", None)
    if io_type is not None:
        missing += [f"imgui.IO.{f}" for f in IO_FIELDS if not hasattr(io_type, f)]
    else:
        print("imgui.IO type not found; check io fields at runtime:", ", ".join(IO_FIELDS))
    print("\n".join(missing) if missing else "all assumed names are present")


if __name__ == "__main__":
    main()