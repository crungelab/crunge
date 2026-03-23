#include <stdbool.h>
#include <limits>
#include <iostream>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <SDL3/SDL.h>

#include <cxbind/cxbind.h>

#include <crunge/sdl/crunge-sdl.h>
#include <crunge/sdl/conversions.h>

namespace py = pybind11;

void init_sdl_mouse_py_auto(py::module &_sdl, Registry &registry) {
    py::enum_<SDL_SystemCursor>(_sdl, "SystemCursor", py::arithmetic())
        .value("SYSTEM_CURSOR_DEFAULT", SDL_SystemCursor::SDL_SYSTEM_CURSOR_DEFAULT)
        .value("SYSTEM_CURSOR_TEXT", SDL_SystemCursor::SDL_SYSTEM_CURSOR_TEXT)
        .value("SYSTEM_CURSOR_WAIT", SDL_SystemCursor::SDL_SYSTEM_CURSOR_WAIT)
        .value("SYSTEM_CURSOR_CROSSHAIR", SDL_SystemCursor::SDL_SYSTEM_CURSOR_CROSSHAIR)
        .value("SYSTEM_CURSOR_PROGRESS", SDL_SystemCursor::SDL_SYSTEM_CURSOR_PROGRESS)
        .value("SYSTEM_CURSOR_NWSE_RESIZE", SDL_SystemCursor::SDL_SYSTEM_CURSOR_NWSE_RESIZE)
        .value("SYSTEM_CURSOR_NESW_RESIZE", SDL_SystemCursor::SDL_SYSTEM_CURSOR_NESW_RESIZE)
        .value("SYSTEM_CURSOR_EW_RESIZE", SDL_SystemCursor::SDL_SYSTEM_CURSOR_EW_RESIZE)
        .value("SYSTEM_CURSOR_NS_RESIZE", SDL_SystemCursor::SDL_SYSTEM_CURSOR_NS_RESIZE)
        .value("SYSTEM_CURSOR_MOVE", SDL_SystemCursor::SDL_SYSTEM_CURSOR_MOVE)
        .value("SYSTEM_CURSOR_NOT_ALLOWED", SDL_SystemCursor::SDL_SYSTEM_CURSOR_NOT_ALLOWED)
        .value("SYSTEM_CURSOR_POINTER", SDL_SystemCursor::SDL_SYSTEM_CURSOR_POINTER)
        .value("SYSTEM_CURSOR_NW_RESIZE", SDL_SystemCursor::SDL_SYSTEM_CURSOR_NW_RESIZE)
        .value("SYSTEM_CURSOR_N_RESIZE", SDL_SystemCursor::SDL_SYSTEM_CURSOR_N_RESIZE)
        .value("SYSTEM_CURSOR_NE_RESIZE", SDL_SystemCursor::SDL_SYSTEM_CURSOR_NE_RESIZE)
        .value("SYSTEM_CURSOR_E_RESIZE", SDL_SystemCursor::SDL_SYSTEM_CURSOR_E_RESIZE)
        .value("SYSTEM_CURSOR_SE_RESIZE", SDL_SystemCursor::SDL_SYSTEM_CURSOR_SE_RESIZE)
        .value("SYSTEM_CURSOR_S_RESIZE", SDL_SystemCursor::SDL_SYSTEM_CURSOR_S_RESIZE)
        .value("SYSTEM_CURSOR_SW_RESIZE", SDL_SystemCursor::SDL_SYSTEM_CURSOR_SW_RESIZE)
        .value("SYSTEM_CURSOR_W_RESIZE", SDL_SystemCursor::SDL_SYSTEM_CURSOR_W_RESIZE)
        .value("SYSTEM_CURSOR_COUNT", SDL_SystemCursor::SDL_SYSTEM_CURSOR_COUNT)
        .export_values()
    ;
    py::enum_<SDL_MouseWheelDirection>(_sdl, "MouseWheelDirection", py::arithmetic())
        .value("MOUSEWHEEL_NORMAL", SDL_MouseWheelDirection::SDL_MOUSEWHEEL_NORMAL)
        .value("MOUSEWHEEL_FLIPPED", SDL_MouseWheelDirection::SDL_MOUSEWHEEL_FLIPPED)
        .export_values()
    ;
    py::class_<SDL_CursorFrameInfo> _CursorFrameInfo(_sdl, "CursorFrameInfo");
    registry.on(_sdl, "CursorFrameInfo", _CursorFrameInfo);
        _CursorFrameInfo
        .def_readwrite("surface", &SDL_CursorFrameInfo::surface)
        .def_readwrite("duration", &SDL_CursorFrameInfo::duration)
    ;

    _sdl
    .def("has_mouse", &SDL_HasMouse
        )
    .def("get_mice", [](int * count)
        {
            auto _ret = SDL_GetMice(count);
            return std::make_tuple(_ret, count);
        }
        , py::arg("count")
        )
    .def("get_mouse_name_for_id", &SDL_GetMouseNameForID
        , py::arg("instance_id")
        )
    .def("get_mouse_focus", []()
        {
            return SDLWindowWrapper(SDL_GetMouseFocus());
        }
        )
    .def("get_mouse_state", [](float * x, float * y)
        {
            auto _ret = SDL_GetMouseState(x, y);
            return std::make_tuple(_ret, x, y);
        }
        , py::arg("x")
        , py::arg("y")
        )
    .def("get_global_mouse_state", [](float * x, float * y)
        {
            auto _ret = SDL_GetGlobalMouseState(x, y);
            return std::make_tuple(_ret, x, y);
        }
        , py::arg("x")
        , py::arg("y")
        )
    .def("get_relative_mouse_state", [](float * x, float * y)
        {
            auto _ret = SDL_GetRelativeMouseState(x, y);
            return std::make_tuple(_ret, x, y);
        }
        , py::arg("x")
        , py::arg("y")
        )
    .def("warp_mouse_in_window", [](SDLWindowWrapper window, float x, float y)
        {
            return SDL_WarpMouseInWindow(static_cast<SDL_Window *>(window.get()), x, y);
        }
        , py::arg("window")
        , py::arg("x")
        , py::arg("y")
        )
    .def("warp_mouse_global", &SDL_WarpMouseGlobal
        , py::arg("x")
        , py::arg("y")
        )
    .def("set_relative_mouse_transform", &SDL_SetRelativeMouseTransform
        , py::arg("callback")
        , py::arg("userdata")
        )
    .def("set_window_relative_mouse_mode", [](SDLWindowWrapper window, _Bool enabled)
        {
            return SDL_SetWindowRelativeMouseMode(static_cast<SDL_Window *>(window.get()), enabled);
        }
        , py::arg("window")
        , py::arg("enabled")
        )
    .def("get_window_relative_mouse_mode", [](SDLWindowWrapper window)
        {
            return SDL_GetWindowRelativeMouseMode(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("capture_mouse", &SDL_CaptureMouse
        , py::arg("enabled")
        )
    .def("create_cursor", [](const Uint8 * data, const Uint8 * mask, int w, int h, int hot_x, int hot_y)
        {
            return SDLCursorWrapper(SDL_CreateCursor(data, mask, w, h, hot_x, hot_y));
        }
        , py::arg("data")
        , py::arg("mask")
        , py::arg("w")
        , py::arg("h")
        , py::arg("hot_x")
        , py::arg("hot_y")
        )
    .def("create_color_cursor", [](SDL_Surface * surface, int hot_x, int hot_y)
        {
            return SDLCursorWrapper(SDL_CreateColorCursor(surface, hot_x, hot_y));
        }
        , py::arg("surface")
        , py::arg("hot_x")
        , py::arg("hot_y")
        )
    .def("create_animated_cursor", [](SDL_CursorFrameInfo * frames, int frame_count, int hot_x, int hot_y)
        {
            return SDLCursorWrapper(SDL_CreateAnimatedCursor(frames, frame_count, hot_x, hot_y));
        }
        , py::arg("frames")
        , py::arg("frame_count")
        , py::arg("hot_x")
        , py::arg("hot_y")
        )
    .def("create_system_cursor", [](SDL_SystemCursor id)
        {
            return SDLCursorWrapper(SDL_CreateSystemCursor(id));
        }
        , py::arg("id")
        )
    .def("set_cursor", [](SDLCursorWrapper cursor)
        {
            return SDL_SetCursor(static_cast<SDL_Cursor *>(cursor.get()));
        }
        , py::arg("cursor")
        )
    .def("get_cursor", []()
        {
            return SDLCursorWrapper(SDL_GetCursor());
        }
        )
    .def("get_default_cursor", []()
        {
            return SDLCursorWrapper(SDL_GetDefaultCursor());
        }
        )
    .def("destroy_cursor", [](SDLCursorWrapper cursor)
        {
            return SDL_DestroyCursor(static_cast<SDL_Cursor *>(cursor.get()));
        }
        , py::arg("cursor")
        )
    .def("show_cursor", &SDL_ShowCursor
        )
    .def("hide_cursor", &SDL_HideCursor
        )
    .def("cursor_visible", &SDL_CursorVisible
        )
    ;


}