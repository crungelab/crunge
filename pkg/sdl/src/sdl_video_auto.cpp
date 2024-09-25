#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

#include <SDL3/SDL.h>
#include <SDL3/SDL_video.h>
#include <iostream>

#include <cxbind/cxbind.h>

#include <crunge/sdl/crunge-sdl.h>
#include <crunge/sdl/conversions.h>

namespace py = pybind11;

void init_sdl_video_auto(py::module &_sdl, Registry &registry) {
    py::enum_<SDL_SystemTheme>(_sdl, "SystemTheme", py::arithmetic())
        .value("SYSTEM_THEME_UNKNOWN", SDL_SystemTheme::SDL_SYSTEM_THEME_UNKNOWN)
        .value("SYSTEM_THEME_LIGHT", SDL_SystemTheme::SDL_SYSTEM_THEME_LIGHT)
        .value("SYSTEM_THEME_DARK", SDL_SystemTheme::SDL_SYSTEM_THEME_DARK)
        .export_values()
    ;

    PYCLASS(_sdl, SDL_DisplayMode, DisplayMode)
        .def_readwrite("display_id", &SDL_DisplayMode::displayID)

        .def_readwrite("format", &SDL_DisplayMode::format)

        .def_readwrite("w", &SDL_DisplayMode::w)

        .def_readwrite("h", &SDL_DisplayMode::h)

        .def_readwrite("pixel_density", &SDL_DisplayMode::pixel_density)

        .def_readwrite("refresh_rate", &SDL_DisplayMode::refresh_rate)

        .def_readwrite("refresh_rate_numerator", &SDL_DisplayMode::refresh_rate_numerator)

        .def_readwrite("refresh_rate_denominator", &SDL_DisplayMode::refresh_rate_denominator)

    ;

    py::enum_<SDL_DisplayOrientation>(_sdl, "DisplayOrientation", py::arithmetic())
        .value("ORIENTATION_UNKNOWN", SDL_DisplayOrientation::SDL_ORIENTATION_UNKNOWN)
        .value("ORIENTATION_LANDSCAPE", SDL_DisplayOrientation::SDL_ORIENTATION_LANDSCAPE)
        .value("ORIENTATION_LANDSCAPE_FLIPPED", SDL_DisplayOrientation::SDL_ORIENTATION_LANDSCAPE_FLIPPED)
        .value("ORIENTATION_PORTRAIT", SDL_DisplayOrientation::SDL_ORIENTATION_PORTRAIT)
        .value("ORIENTATION_PORTRAIT_FLIPPED", SDL_DisplayOrientation::SDL_ORIENTATION_PORTRAIT_FLIPPED)
        .export_values()
    ;

    py::enum_<SDL_FlashOperation>(_sdl, "FlashOperation", py::arithmetic())
        .value("FLASH_CANCEL", SDL_FlashOperation::SDL_FLASH_CANCEL)
        .value("FLASH_BRIEFLY", SDL_FlashOperation::SDL_FLASH_BRIEFLY)
        .value("FLASH_UNTIL_FOCUSED", SDL_FlashOperation::SDL_FLASH_UNTIL_FOCUSED)
        .export_values()
    ;

    py::enum_<SDL_GLattr>(_sdl, "GLattr", py::arithmetic())
        .value("GL_RED_SIZE", SDL_GLattr::SDL_GL_RED_SIZE)
        .value("GL_GREEN_SIZE", SDL_GLattr::SDL_GL_GREEN_SIZE)
        .value("GL_BLUE_SIZE", SDL_GLattr::SDL_GL_BLUE_SIZE)
        .value("GL_ALPHA_SIZE", SDL_GLattr::SDL_GL_ALPHA_SIZE)
        .value("GL_BUFFER_SIZE", SDL_GLattr::SDL_GL_BUFFER_SIZE)
        .value("GL_DOUBLEBUFFER", SDL_GLattr::SDL_GL_DOUBLEBUFFER)
        .value("GL_DEPTH_SIZE", SDL_GLattr::SDL_GL_DEPTH_SIZE)
        .value("GL_STENCIL_SIZE", SDL_GLattr::SDL_GL_STENCIL_SIZE)
        .value("GL_ACCUM_RED_SIZE", SDL_GLattr::SDL_GL_ACCUM_RED_SIZE)
        .value("GL_ACCUM_GREEN_SIZE", SDL_GLattr::SDL_GL_ACCUM_GREEN_SIZE)
        .value("GL_ACCUM_BLUE_SIZE", SDL_GLattr::SDL_GL_ACCUM_BLUE_SIZE)
        .value("GL_ACCUM_ALPHA_SIZE", SDL_GLattr::SDL_GL_ACCUM_ALPHA_SIZE)
        .value("GL_STEREO", SDL_GLattr::SDL_GL_STEREO)
        .value("GL_MULTISAMPLEBUFFERS", SDL_GLattr::SDL_GL_MULTISAMPLEBUFFERS)
        .value("GL_MULTISAMPLESAMPLES", SDL_GLattr::SDL_GL_MULTISAMPLESAMPLES)
        .value("GL_ACCELERATED_VISUAL", SDL_GLattr::SDL_GL_ACCELERATED_VISUAL)
        .value("GL_RETAINED_BACKING", SDL_GLattr::SDL_GL_RETAINED_BACKING)
        .value("GL_CONTEXT_MAJOR_VERSION", SDL_GLattr::SDL_GL_CONTEXT_MAJOR_VERSION)
        .value("GL_CONTEXT_MINOR_VERSION", SDL_GLattr::SDL_GL_CONTEXT_MINOR_VERSION)
        .value("GL_CONTEXT_FLAGS", SDL_GLattr::SDL_GL_CONTEXT_FLAGS)
        .value("GL_CONTEXT_PROFILE_MASK", SDL_GLattr::SDL_GL_CONTEXT_PROFILE_MASK)
        .value("GL_SHARE_WITH_CURRENT_CONTEXT", SDL_GLattr::SDL_GL_SHARE_WITH_CURRENT_CONTEXT)
        .value("GL_FRAMEBUFFER_SRGB_CAPABLE", SDL_GLattr::SDL_GL_FRAMEBUFFER_SRGB_CAPABLE)
        .value("GL_CONTEXT_RELEASE_BEHAVIOR", SDL_GLattr::SDL_GL_CONTEXT_RELEASE_BEHAVIOR)
        .value("GL_CONTEXT_RESET_NOTIFICATION", SDL_GLattr::SDL_GL_CONTEXT_RESET_NOTIFICATION)
        .value("GL_CONTEXT_NO_ERROR", SDL_GLattr::SDL_GL_CONTEXT_NO_ERROR)
        .value("GL_FLOATBUFFERS", SDL_GLattr::SDL_GL_FLOATBUFFERS)
        .value("GL_EGL_PLATFORM", SDL_GLattr::SDL_GL_EGL_PLATFORM)
        .export_values()
    ;

    py::enum_<SDL_GLprofile>(_sdl, "GLprofile", py::arithmetic())
        .value("GL_CONTEXT_PROFILE_CORE", SDL_GLprofile::SDL_GL_CONTEXT_PROFILE_CORE)
        .value("GL_CONTEXT_PROFILE_COMPATIBILITY", SDL_GLprofile::SDL_GL_CONTEXT_PROFILE_COMPATIBILITY)
        .value("GL_CONTEXT_PROFILE_ES", SDL_GLprofile::SDL_GL_CONTEXT_PROFILE_ES)
        .export_values()
    ;

    py::enum_<SDL_GLcontextFlag>(_sdl, "GLcontextFlag", py::arithmetic())
        .value("GL_CONTEXT_DEBUG_FLAG", SDL_GLcontextFlag::SDL_GL_CONTEXT_DEBUG_FLAG)
        .value("GL_CONTEXT_FORWARD_COMPATIBLE_FLAG", SDL_GLcontextFlag::SDL_GL_CONTEXT_FORWARD_COMPATIBLE_FLAG)
        .value("GL_CONTEXT_ROBUST_ACCESS_FLAG", SDL_GLcontextFlag::SDL_GL_CONTEXT_ROBUST_ACCESS_FLAG)
        .value("GL_CONTEXT_RESET_ISOLATION_FLAG", SDL_GLcontextFlag::SDL_GL_CONTEXT_RESET_ISOLATION_FLAG)
        .export_values()
    ;

    py::enum_<SDL_GLcontextReleaseFlag>(_sdl, "GLcontextReleaseFlag", py::arithmetic())
        .value("GL_CONTEXT_RELEASE_BEHAVIOR_NONE", SDL_GLcontextReleaseFlag::SDL_GL_CONTEXT_RELEASE_BEHAVIOR_NONE)
        .value("GL_CONTEXT_RELEASE_BEHAVIOR_FLUSH", SDL_GLcontextReleaseFlag::SDL_GL_CONTEXT_RELEASE_BEHAVIOR_FLUSH)
        .export_values()
    ;

    py::enum_<SDL_GLContextResetNotification>(_sdl, "GLContextResetNotification", py::arithmetic())
        .value("GL_CONTEXT_RESET_NO_NOTIFICATION", SDL_GLContextResetNotification::SDL_GL_CONTEXT_RESET_NO_NOTIFICATION)
        .value("GL_CONTEXT_RESET_LOSE_CONTEXT", SDL_GLContextResetNotification::SDL_GL_CONTEXT_RESET_LOSE_CONTEXT)
        .export_values()
    ;

    _sdl
    .def("get_num_video_drivers", &SDL_GetNumVideoDrivers
        , py::return_value_policy::automatic_reference)

    .def("get_video_driver", &SDL_GetVideoDriver
        , py::arg("index")
        , py::return_value_policy::automatic_reference)

    .def("get_current_video_driver", &SDL_GetCurrentVideoDriver
        , py::return_value_policy::automatic_reference)

    .def("get_system_theme", &SDL_GetSystemTheme
        , py::return_value_policy::automatic_reference)

    .def("get_displays", [](int * count)
        {
            auto ret = SDL_GetDisplays(count);
            return std::make_tuple(ret, count);
        }
        , py::arg("count")
        , py::return_value_policy::automatic_reference)

    .def("get_primary_display", &SDL_GetPrimaryDisplay
        , py::return_value_policy::automatic_reference)

    .def("get_display_properties", &SDL_GetDisplayProperties
        , py::arg("display_id")
        , py::return_value_policy::automatic_reference)

    .def("get_display_name", &SDL_GetDisplayName
        , py::arg("display_id")
        , py::return_value_policy::automatic_reference)

    .def("get_display_bounds", &SDL_GetDisplayBounds
        , py::arg("display_id")
        , py::arg("rect")
        , py::return_value_policy::automatic_reference)

    .def("get_display_usable_bounds", &SDL_GetDisplayUsableBounds
        , py::arg("display_id")
        , py::arg("rect")
        , py::return_value_policy::automatic_reference)

    .def("get_natural_display_orientation", &SDL_GetNaturalDisplayOrientation
        , py::arg("display_id")
        , py::return_value_policy::automatic_reference)

    .def("get_current_display_orientation", &SDL_GetCurrentDisplayOrientation
        , py::arg("display_id")
        , py::return_value_policy::automatic_reference)

    .def("get_display_content_scale", &SDL_GetDisplayContentScale
        , py::arg("display_id")
        , py::return_value_policy::automatic_reference)

    .def("get_closest_fullscreen_display_mode", &SDL_GetClosestFullscreenDisplayMode
        , py::arg("display_id")
        , py::arg("w")
        , py::arg("h")
        , py::arg("refresh_rate")
        , py::arg("include_high_density_modes")
        , py::arg("mode")
        , py::return_value_policy::automatic_reference)

    .def("get_desktop_display_mode", &SDL_GetDesktopDisplayMode
        , py::arg("display_id")
        , py::return_value_policy::automatic_reference)

    .def("get_current_display_mode", &SDL_GetCurrentDisplayMode
        , py::arg("display_id")
        , py::return_value_policy::automatic_reference)

    .def("get_display_for_point", &SDL_GetDisplayForPoint
        , py::arg("point")
        , py::return_value_policy::automatic_reference)

    .def("get_display_for_rect", &SDL_GetDisplayForRect
        , py::arg("rect")
        , py::return_value_policy::automatic_reference)

    .def("get_display_for_window", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_GetDisplayForWindow(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("get_window_pixel_density", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_GetWindowPixelDensity(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("get_window_display_scale", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_GetWindowDisplayScale(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("set_window_fullscreen_mode", [](SDLWindowWrapper * window, const SDL_DisplayMode * mode)
        {
            auto ret = SDL_SetWindowFullscreenMode(window->get(), mode);
            return ret;
        }
        , py::arg("window")
        , py::arg("mode")
        , py::return_value_policy::automatic_reference)

    .def("get_window_fullscreen_mode", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_GetWindowFullscreenMode(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("get_window_icc_profile", [](SDLWindowWrapper * window, unsigned long * size)
        {
            auto ret = SDL_GetWindowICCProfile(window->get(), size);
            return std::make_tuple(ret, size);
        }
        , py::arg("window")
        , py::arg("size")
        , py::return_value_policy::automatic_reference)

    .def("get_window_pixel_format", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_GetWindowPixelFormat(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("create_window", [](const char * title, int w, int h, unsigned long flags)
        {
            auto ret = new SDLWindowWrapper(SDL_CreateWindow(title, w, h, flags));
            return ret;
        }
        , py::arg("title")
        , py::arg("w")
        , py::arg("h")
        , py::arg("flags")
        , py::return_value_policy::automatic_reference)

    .def("create_popup_window", [](SDLWindowWrapper * parent, int offset_x, int offset_y, int w, int h, unsigned long flags)
        {
            auto ret = new SDLWindowWrapper(SDL_CreatePopupWindow(parent->get(), offset_x, offset_y, w, h, flags));
            return ret;
        }
        , py::arg("parent")
        , py::arg("offset_x")
        , py::arg("offset_y")
        , py::arg("w")
        , py::arg("h")
        , py::arg("flags")
        , py::return_value_policy::automatic_reference)

    .def("create_window_with_properties", [](unsigned int props)
        {
            auto ret = new SDLWindowWrapper(SDL_CreateWindowWithProperties(props));
            return ret;
        }
        , py::arg("props")
        , py::return_value_policy::automatic_reference)

    .def("get_window_id", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_GetWindowID(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("get_window_from_id", [](unsigned int id)
        {
            auto ret = new SDLWindowWrapper(SDL_GetWindowFromID(id));
            return ret;
        }
        , py::arg("id")
        , py::return_value_policy::automatic_reference)

    .def("get_window_parent", [](SDLWindowWrapper * window)
        {
            auto ret = new SDLWindowWrapper(SDL_GetWindowParent(window->get()));
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("get_window_properties", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_GetWindowProperties(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("get_window_flags", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_GetWindowFlags(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("set_window_title", [](SDLWindowWrapper * window, const char * title)
        {
            auto ret = SDL_SetWindowTitle(window->get(), title);
            return ret;
        }
        , py::arg("window")
        , py::arg("title")
        , py::return_value_policy::automatic_reference)

    .def("get_window_title", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_GetWindowTitle(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("set_window_icon", [](SDLWindowWrapper * window, SDL_Surface * icon)
        {
            auto ret = SDL_SetWindowIcon(window->get(), icon);
            return ret;
        }
        , py::arg("window")
        , py::arg("icon")
        , py::return_value_policy::automatic_reference)

    .def("set_window_position", [](SDLWindowWrapper * window, int x, int y)
        {
            auto ret = SDL_SetWindowPosition(window->get(), x, y);
            return ret;
        }
        , py::arg("window")
        , py::arg("x")
        , py::arg("y")
        , py::return_value_policy::automatic_reference)

    .def("get_window_position", [](SDLWindowWrapper * window, int * x, int * y)
        {
            auto ret = SDL_GetWindowPosition(window->get(), x, y);
            return std::make_tuple(ret, x, y);
        }
        , py::arg("window")
        , py::arg("x")
        , py::arg("y")
        , py::return_value_policy::automatic_reference)

    .def("set_window_size", [](SDLWindowWrapper * window, int w, int h)
        {
            auto ret = SDL_SetWindowSize(window->get(), w, h);
            return ret;
        }
        , py::arg("window")
        , py::arg("w")
        , py::arg("h")
        , py::return_value_policy::automatic_reference)

    .def("get_window_size", [](SDLWindowWrapper * window, int * w, int * h)
        {
            auto ret = SDL_GetWindowSize(window->get(), w, h);
            return std::make_tuple(w, h);
        }
        , py::arg("window")
        , py::arg("w") = 0
        , py::arg("h") = 0
        , py::return_value_policy::automatic_reference)

    .def("get_window_safe_area", [](SDLWindowWrapper * window, SDL_Rect * rect)
        {
            auto ret = SDL_GetWindowSafeArea(window->get(), rect);
            return ret;
        }
        , py::arg("window")
        , py::arg("rect")
        , py::return_value_policy::automatic_reference)

    .def("set_window_aspect_ratio", [](SDLWindowWrapper * window, float min_aspect, float max_aspect)
        {
            auto ret = SDL_SetWindowAspectRatio(window->get(), min_aspect, max_aspect);
            return ret;
        }
        , py::arg("window")
        , py::arg("min_aspect")
        , py::arg("max_aspect")
        , py::return_value_policy::automatic_reference)

    .def("get_window_aspect_ratio", [](SDLWindowWrapper * window, float * min_aspect, float * max_aspect)
        {
            auto ret = SDL_GetWindowAspectRatio(window->get(), min_aspect, max_aspect);
            return std::make_tuple(ret, min_aspect, max_aspect);
        }
        , py::arg("window")
        , py::arg("min_aspect")
        , py::arg("max_aspect")
        , py::return_value_policy::automatic_reference)

    .def("get_window_borders_size", [](SDLWindowWrapper * window, int * top, int * left, int * bottom, int * right)
        {
            auto ret = SDL_GetWindowBordersSize(window->get(), top, left, bottom, right);
            return std::make_tuple(ret, top, left, bottom, right);
        }
        , py::arg("window")
        , py::arg("top")
        , py::arg("left")
        , py::arg("bottom")
        , py::arg("right")
        , py::return_value_policy::automatic_reference)

    .def("get_window_size_in_pixels", [](SDLWindowWrapper * window, int * w, int * h)
        {
            auto ret = SDL_GetWindowSizeInPixels(window->get(), w, h);
            return std::make_tuple(w, h);
        }
        , py::arg("window")
        , py::arg("w") = 0
        , py::arg("h") = 0
        , py::return_value_policy::automatic_reference)

    .def("set_window_minimum_size", [](SDLWindowWrapper * window, int min_w, int min_h)
        {
            auto ret = SDL_SetWindowMinimumSize(window->get(), min_w, min_h);
            return ret;
        }
        , py::arg("window")
        , py::arg("min_w")
        , py::arg("min_h")
        , py::return_value_policy::automatic_reference)

    .def("get_window_minimum_size", [](SDLWindowWrapper * window, int * w, int * h)
        {
            auto ret = SDL_GetWindowMinimumSize(window->get(), w, h);
            return std::make_tuple(ret, w, h);
        }
        , py::arg("window")
        , py::arg("w")
        , py::arg("h")
        , py::return_value_policy::automatic_reference)

    .def("set_window_maximum_size", [](SDLWindowWrapper * window, int max_w, int max_h)
        {
            auto ret = SDL_SetWindowMaximumSize(window->get(), max_w, max_h);
            return ret;
        }
        , py::arg("window")
        , py::arg("max_w")
        , py::arg("max_h")
        , py::return_value_policy::automatic_reference)

    .def("get_window_maximum_size", [](SDLWindowWrapper * window, int * w, int * h)
        {
            auto ret = SDL_GetWindowMaximumSize(window->get(), w, h);
            return std::make_tuple(ret, w, h);
        }
        , py::arg("window")
        , py::arg("w")
        , py::arg("h")
        , py::return_value_policy::automatic_reference)

    .def("set_window_bordered", [](SDLWindowWrapper * window, bool bordered)
        {
            auto ret = SDL_SetWindowBordered(window->get(), bordered);
            return ret;
        }
        , py::arg("window")
        , py::arg("bordered")
        , py::return_value_policy::automatic_reference)

    .def("set_window_resizable", [](SDLWindowWrapper * window, bool resizable)
        {
            auto ret = SDL_SetWindowResizable(window->get(), resizable);
            return ret;
        }
        , py::arg("window")
        , py::arg("resizable")
        , py::return_value_policy::automatic_reference)

    .def("set_window_always_on_top", [](SDLWindowWrapper * window, bool on_top)
        {
            auto ret = SDL_SetWindowAlwaysOnTop(window->get(), on_top);
            return ret;
        }
        , py::arg("window")
        , py::arg("on_top")
        , py::return_value_policy::automatic_reference)

    .def("show_window", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_ShowWindow(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("hide_window", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_HideWindow(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("raise_window", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_RaiseWindow(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("maximize_window", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_MaximizeWindow(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("minimize_window", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_MinimizeWindow(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("restore_window", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_RestoreWindow(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("set_window_fullscreen", [](SDLWindowWrapper * window, bool fullscreen)
        {
            auto ret = SDL_SetWindowFullscreen(window->get(), fullscreen);
            return ret;
        }
        , py::arg("window")
        , py::arg("fullscreen")
        , py::return_value_policy::automatic_reference)

    .def("sync_window", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_SyncWindow(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("window_has_surface", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_WindowHasSurface(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("get_window_surface", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_GetWindowSurface(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("set_window_surface_v_sync", [](SDLWindowWrapper * window, int vsync)
        {
            auto ret = SDL_SetWindowSurfaceVSync(window->get(), vsync);
            return ret;
        }
        , py::arg("window")
        , py::arg("vsync")
        , py::return_value_policy::automatic_reference)

    .def("get_window_surface_v_sync", [](SDLWindowWrapper * window, int * vsync)
        {
            auto ret = SDL_GetWindowSurfaceVSync(window->get(), vsync);
            return std::make_tuple(ret, vsync);
        }
        , py::arg("window")
        , py::arg("vsync")
        , py::return_value_policy::automatic_reference)

    .def("update_window_surface", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_UpdateWindowSurface(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("update_window_surface_rects", [](SDLWindowWrapper * window, const SDL_Rect * rects, int numrects)
        {
            auto ret = SDL_UpdateWindowSurfaceRects(window->get(), rects, numrects);
            return ret;
        }
        , py::arg("window")
        , py::arg("rects")
        , py::arg("numrects")
        , py::return_value_policy::automatic_reference)

    .def("destroy_window_surface", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_DestroyWindowSurface(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("set_window_keyboard_grab", [](SDLWindowWrapper * window, bool grabbed)
        {
            auto ret = SDL_SetWindowKeyboardGrab(window->get(), grabbed);
            return ret;
        }
        , py::arg("window")
        , py::arg("grabbed")
        , py::return_value_policy::automatic_reference)

    .def("set_window_mouse_grab", [](SDLWindowWrapper * window, bool grabbed)
        {
            auto ret = SDL_SetWindowMouseGrab(window->get(), grabbed);
            return ret;
        }
        , py::arg("window")
        , py::arg("grabbed")
        , py::return_value_policy::automatic_reference)

    .def("get_window_keyboard_grab", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_GetWindowKeyboardGrab(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("get_window_mouse_grab", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_GetWindowMouseGrab(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("get_grabbed_window", []()
        {
            auto ret = new SDLWindowWrapper(SDL_GetGrabbedWindow());
            return ret;
        }
        , py::return_value_policy::automatic_reference)

    .def("set_window_mouse_rect", [](SDLWindowWrapper * window, const SDL_Rect * rect)
        {
            auto ret = SDL_SetWindowMouseRect(window->get(), rect);
            return ret;
        }
        , py::arg("window")
        , py::arg("rect")
        , py::return_value_policy::automatic_reference)

    .def("get_window_mouse_rect", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_GetWindowMouseRect(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("set_window_opacity", [](SDLWindowWrapper * window, float opacity)
        {
            auto ret = SDL_SetWindowOpacity(window->get(), opacity);
            return ret;
        }
        , py::arg("window")
        , py::arg("opacity")
        , py::return_value_policy::automatic_reference)

    .def("get_window_opacity", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_GetWindowOpacity(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("set_window_parent", [](SDLWindowWrapper * window, SDLWindowWrapper * parent)
        {
            auto ret = SDL_SetWindowParent(window->get(), parent->get());
            return ret;
        }
        , py::arg("window")
        , py::arg("parent")
        , py::return_value_policy::automatic_reference)

    .def("set_window_modal", [](SDLWindowWrapper * window, bool modal)
        {
            auto ret = SDL_SetWindowModal(window->get(), modal);
            return ret;
        }
        , py::arg("window")
        , py::arg("modal")
        , py::return_value_policy::automatic_reference)

    .def("set_window_focusable", [](SDLWindowWrapper * window, bool focusable)
        {
            auto ret = SDL_SetWindowFocusable(window->get(), focusable);
            return ret;
        }
        , py::arg("window")
        , py::arg("focusable")
        , py::return_value_policy::automatic_reference)

    .def("show_window_system_menu", [](SDLWindowWrapper * window, int x, int y)
        {
            auto ret = SDL_ShowWindowSystemMenu(window->get(), x, y);
            return ret;
        }
        , py::arg("window")
        , py::arg("x")
        , py::arg("y")
        , py::return_value_policy::automatic_reference)

    ;
    py::enum_<SDL_HitTestResult>(_sdl, "HitTestResult", py::arithmetic())
        .value("HITTEST_NORMAL", SDL_HitTestResult::SDL_HITTEST_NORMAL)
        .value("HITTEST_DRAGGABLE", SDL_HitTestResult::SDL_HITTEST_DRAGGABLE)
        .value("HITTEST_RESIZE_TOPLEFT", SDL_HitTestResult::SDL_HITTEST_RESIZE_TOPLEFT)
        .value("HITTEST_RESIZE_TOP", SDL_HitTestResult::SDL_HITTEST_RESIZE_TOP)
        .value("HITTEST_RESIZE_TOPRIGHT", SDL_HitTestResult::SDL_HITTEST_RESIZE_TOPRIGHT)
        .value("HITTEST_RESIZE_RIGHT", SDL_HitTestResult::SDL_HITTEST_RESIZE_RIGHT)
        .value("HITTEST_RESIZE_BOTTOMRIGHT", SDL_HitTestResult::SDL_HITTEST_RESIZE_BOTTOMRIGHT)
        .value("HITTEST_RESIZE_BOTTOM", SDL_HitTestResult::SDL_HITTEST_RESIZE_BOTTOM)
        .value("HITTEST_RESIZE_BOTTOMLEFT", SDL_HitTestResult::SDL_HITTEST_RESIZE_BOTTOMLEFT)
        .value("HITTEST_RESIZE_LEFT", SDL_HitTestResult::SDL_HITTEST_RESIZE_LEFT)
        .export_values()
    ;

    _sdl
    .def("set_window_shape", [](SDLWindowWrapper * window, SDL_Surface * shape)
        {
            auto ret = SDL_SetWindowShape(window->get(), shape);
            return ret;
        }
        , py::arg("window")
        , py::arg("shape")
        , py::return_value_policy::automatic_reference)

    .def("flash_window", [](SDLWindowWrapper * window, SDL_FlashOperation operation)
        {
            auto ret = SDL_FlashWindow(window->get(), operation);
            return ret;
        }
        , py::arg("window")
        , py::arg("operation")
        , py::return_value_policy::automatic_reference)

    .def("destroy_window", [](SDLWindowWrapper * window)
        {
            SDL_DestroyWindow(window->get());
            return ;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("screen_saver_enabled", &SDL_ScreenSaverEnabled
        , py::return_value_policy::automatic_reference)

    .def("enable_screen_saver", &SDL_EnableScreenSaver
        , py::return_value_policy::automatic_reference)

    .def("disable_screen_saver", &SDL_DisableScreenSaver
        , py::return_value_policy::automatic_reference)

    .def("gl_load_library", &SDL_GL_LoadLibrary
        , py::arg("path")
        , py::return_value_policy::automatic_reference)

    .def("gl_unload_library", &SDL_GL_UnloadLibrary
        , py::return_value_policy::automatic_reference)

    .def("gl_extension_supported", &SDL_GL_ExtensionSupported
        , py::arg("extension")
        , py::return_value_policy::automatic_reference)

    .def("gl_reset_attributes", &SDL_GL_ResetAttributes
        , py::return_value_policy::automatic_reference)

    .def("gl_set_attribute", &SDL_GL_SetAttribute
        , py::arg("attr")
        , py::arg("value")
        , py::return_value_policy::automatic_reference)

    .def("gl_get_attribute", [](SDL_GLattr attr, int * value)
        {
            auto ret = SDL_GL_GetAttribute(attr, value);
            return std::make_tuple(ret, value);
        }
        , py::arg("attr")
        , py::arg("value")
        , py::return_value_policy::automatic_reference)

    .def("gl_get_current_window", []()
        {
            auto ret = new SDLWindowWrapper(SDL_GL_GetCurrentWindow());
            return ret;
        }
        , py::return_value_policy::automatic_reference)

    .def("egl_get_current_display", &SDL_EGL_GetCurrentDisplay
        , py::return_value_policy::automatic_reference)

    .def("egl_get_current_config", &SDL_EGL_GetCurrentConfig
        , py::return_value_policy::automatic_reference)

    .def("egl_get_window_surface", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_EGL_GetWindowSurface(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    .def("egl_set_attribute_callbacks", &SDL_EGL_SetAttributeCallbacks
        , py::arg("platform_attrib_callback")
        , py::arg("surface_attrib_callback")
        , py::arg("context_attrib_callback")
        , py::return_value_policy::automatic_reference)

    .def("gl_set_swap_interval", &SDL_GL_SetSwapInterval
        , py::arg("interval")
        , py::return_value_policy::automatic_reference)

    .def("gl_get_swap_interval", [](int * interval)
        {
            auto ret = SDL_GL_GetSwapInterval(interval);
            return std::make_tuple(ret, interval);
        }
        , py::arg("interval")
        , py::return_value_policy::automatic_reference)

    .def("gl_swap_window", [](SDLWindowWrapper * window)
        {
            auto ret = SDL_GL_SwapWindow(window->get());
            return ret;
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)

    ;

}