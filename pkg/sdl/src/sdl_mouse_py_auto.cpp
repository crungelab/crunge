#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

#include <SDL3/SDL.h>
#include <iostream>

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

    _sdl
    .def("has_mouse", &SDL_HasMouse
        , py::return_value_policy::automatic_reference)

    .def("get_mice", [](int * count)
        {
            auto ret = SDL_GetMice(count);
            return std::make_tuple(ret, count);
        }
        , py::arg("count")
        , py::return_value_policy::automatic_reference)

    .def("get_mouse_name_for_id", &SDL_GetMouseNameForID
        , py::arg("instance_id")
        , py::return_value_policy::automatic_reference)

    .def("get_mouse_focus", []()
        {
            auto ret = SDLWindowWrapper(SDL_GetMouseFocus());
            return ret;
        }
        , py::return_value_policy::automatic_reference)

    .def("get_mouse_state", [](float * x, float * y)
        {
            auto ret = SDL_GetMouseState(x, y);
            return std::make_tuple(ret, x, y);
        }
        , py::arg("x")
        , py::arg("y")
        , py::return_value_policy::automatic_reference)

    .def("get_global_mouse_state", [](float * x, float * y)
        {
            auto ret = SDL_GetGlobalMouseState(x, y);
            return std::make_tuple(ret, x, y);
        }
        , py::arg("x")
        , py::arg("y")
        , py::return_value_policy::automatic_reference)

    .def("get_relative_mouse_state", [](float * x, float * y)
        {
            auto ret = SDL_GetRelativeMouseState(x, y);
            return std::make_tuple(ret, x, y);
        }
        , py::arg("x")
        , py::arg("y")
        , py::return_value_policy::automatic_reference)

    .def("warp_mouse_in_window", [](const SDLWindowWrapper& window, float x, float y)
        {
            SDL_WarpMouseInWindow(window, x, y);
            return ;
        }
        , py::arg("window")
        , py::arg("x")
        , py::arg("y")
        , py::return_value_policy::automatic_reference)

    .def("warp_mouse_global", &SDL_WarpMouseGlobal
        , py::arg("x")
        , py::arg("y")
        , py::return_value_policy::automatic_reference)

    .def("set_window_relative_mouse_mode", [](const SDLWindowWrapper& window, bool enabled)
        {
            auto ret = SDL_SetWindowRelativeMouseMode(window, enabled);
            return ret;
        }
        , py::arg("window")
        , py::arg("enabled")
        , py::return_value_policy::automatic_reference)

    .def("get_window_relative_mouse_mode", [](const SDLWindowWrapper& window)
        {
            auto ret = SDL_GetWindowRelativeMouseMode(window);
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("capture_mouse", &SDL_CaptureMouse
        , py::arg("enabled")
        , py::return_value_policy::automatic_reference)

    .def("create_cursor", [](const unsigned char * data, const unsigned char * mask, int w, int h, int hot_x, int hot_y)
        {
            auto ret = SDLCursorWrapper(SDL_CreateCursor(data, mask, w, h, hot_x, hot_y));
            return ret;
        }
        , py::arg("data")
        , py::arg("mask")
        , py::arg("w")
        , py::arg("h")
        , py::arg("hot_x")
        , py::arg("hot_y")
        , py::return_value_policy::automatic_reference)

    .def("create_color_cursor", [](SDL_Surface * surface, int hot_x, int hot_y)
        {
            auto ret = SDLCursorWrapper(SDL_CreateColorCursor(surface, hot_x, hot_y));
            return ret;
        }
        , py::arg("surface")
        , py::arg("hot_x")
        , py::arg("hot_y")
        , py::return_value_policy::automatic_reference)

    .def("create_system_cursor", [](SDL_SystemCursor id)
        {
            auto ret = SDLCursorWrapper(SDL_CreateSystemCursor(id));
            return ret;
        }
        , py::arg("id")
        , py::return_value_policy::automatic_reference)

    .def("set_cursor", [](const SDLCursorWrapper& cursor)
        {
            auto ret = SDL_SetCursor(cursor);
            return ret;
        }
        , py::arg("cursor")
        , py::return_value_policy::automatic_reference)

    .def("get_cursor", []()
        {
            auto ret = SDLCursorWrapper(SDL_GetCursor());
            return ret;
        }
        , py::return_value_policy::automatic_reference)

    .def("get_default_cursor", []()
        {
            auto ret = SDLCursorWrapper(SDL_GetDefaultCursor());
            return ret;
        }
        , py::return_value_policy::automatic_reference)

    .def("destroy_cursor", [](const SDLCursorWrapper& cursor)
        {
            SDL_DestroyCursor(cursor);
            return ;
        }
        , py::arg("cursor")
        , py::return_value_policy::automatic_reference)

    .def("show_cursor", &SDL_ShowCursor
        , py::return_value_policy::automatic_reference)

    .def("hide_cursor", &SDL_HideCursor
        , py::return_value_policy::automatic_reference)

    .def("cursor_visible", &SDL_CursorVisible
        , py::return_value_policy::automatic_reference)

    ;

}