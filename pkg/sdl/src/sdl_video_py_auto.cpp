#include <stdbool.h>
#include <limits>
#include <iostream>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <SDL3/SDL.h>
#include <SDL3/SDL_video.h>

#include <cxbind/cxbind.h>

#include <crunge/sdl/crunge-sdl.h>
#include <crunge/sdl/conversions.h>

namespace py = pybind11;

void init_sdl_video_py_auto(py::module &_sdl, Registry &registry) {
    py::enum_<SDL_SystemTheme>(_sdl, "SystemTheme", py::arithmetic())
        .value("SYSTEM_THEME_UNKNOWN", SDL_SystemTheme::SDL_SYSTEM_THEME_UNKNOWN)
        .value("SYSTEM_THEME_LIGHT", SDL_SystemTheme::SDL_SYSTEM_THEME_LIGHT)
        .value("SYSTEM_THEME_DARK", SDL_SystemTheme::SDL_SYSTEM_THEME_DARK)
        .export_values()
    ;
    py::class_<SDL_DisplayMode> _DisplayMode(_sdl, "DisplayMode");
    registry.on(_sdl, "DisplayMode", _DisplayMode);
        _DisplayMode
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
    py::enum_<SDL_ProgressState>(_sdl, "ProgressState", py::arithmetic())
        .value("PROGRESS_STATE_INVALID", SDL_ProgressState::SDL_PROGRESS_STATE_INVALID)
        .value("PROGRESS_STATE_NONE", SDL_ProgressState::SDL_PROGRESS_STATE_NONE)
        .value("PROGRESS_STATE_INDETERMINATE", SDL_ProgressState::SDL_PROGRESS_STATE_INDETERMINATE)
        .value("PROGRESS_STATE_NORMAL", SDL_ProgressState::SDL_PROGRESS_STATE_NORMAL)
        .value("PROGRESS_STATE_PAUSED", SDL_ProgressState::SDL_PROGRESS_STATE_PAUSED)
        .value("PROGRESS_STATE_ERROR", SDL_ProgressState::SDL_PROGRESS_STATE_ERROR)
        .export_values()
    ;
    py::enum_<SDL_GLAttr>(_sdl, "GLAttr", py::arithmetic())
        .value("GL_RED_SIZE", SDL_GLAttr::SDL_GL_RED_SIZE)
        .value("GL_GREEN_SIZE", SDL_GLAttr::SDL_GL_GREEN_SIZE)
        .value("GL_BLUE_SIZE", SDL_GLAttr::SDL_GL_BLUE_SIZE)
        .value("GL_ALPHA_SIZE", SDL_GLAttr::SDL_GL_ALPHA_SIZE)
        .value("GL_BUFFER_SIZE", SDL_GLAttr::SDL_GL_BUFFER_SIZE)
        .value("GL_DOUBLEBUFFER", SDL_GLAttr::SDL_GL_DOUBLEBUFFER)
        .value("GL_DEPTH_SIZE", SDL_GLAttr::SDL_GL_DEPTH_SIZE)
        .value("GL_STENCIL_SIZE", SDL_GLAttr::SDL_GL_STENCIL_SIZE)
        .value("GL_ACCUM_RED_SIZE", SDL_GLAttr::SDL_GL_ACCUM_RED_SIZE)
        .value("GL_ACCUM_GREEN_SIZE", SDL_GLAttr::SDL_GL_ACCUM_GREEN_SIZE)
        .value("GL_ACCUM_BLUE_SIZE", SDL_GLAttr::SDL_GL_ACCUM_BLUE_SIZE)
        .value("GL_ACCUM_ALPHA_SIZE", SDL_GLAttr::SDL_GL_ACCUM_ALPHA_SIZE)
        .value("GL_STEREO", SDL_GLAttr::SDL_GL_STEREO)
        .value("GL_MULTISAMPLEBUFFERS", SDL_GLAttr::SDL_GL_MULTISAMPLEBUFFERS)
        .value("GL_MULTISAMPLESAMPLES", SDL_GLAttr::SDL_GL_MULTISAMPLESAMPLES)
        .value("GL_ACCELERATED_VISUAL", SDL_GLAttr::SDL_GL_ACCELERATED_VISUAL)
        .value("GL_RETAINED_BACKING", SDL_GLAttr::SDL_GL_RETAINED_BACKING)
        .value("GL_CONTEXT_MAJOR_VERSION", SDL_GLAttr::SDL_GL_CONTEXT_MAJOR_VERSION)
        .value("GL_CONTEXT_MINOR_VERSION", SDL_GLAttr::SDL_GL_CONTEXT_MINOR_VERSION)
        .value("GL_CONTEXT_FLAGS", SDL_GLAttr::SDL_GL_CONTEXT_FLAGS)
        .value("GL_CONTEXT_PROFILE_MASK", SDL_GLAttr::SDL_GL_CONTEXT_PROFILE_MASK)
        .value("GL_SHARE_WITH_CURRENT_CONTEXT", SDL_GLAttr::SDL_GL_SHARE_WITH_CURRENT_CONTEXT)
        .value("GL_FRAMEBUFFER_SRGB_CAPABLE", SDL_GLAttr::SDL_GL_FRAMEBUFFER_SRGB_CAPABLE)
        .value("GL_CONTEXT_RELEASE_BEHAVIOR", SDL_GLAttr::SDL_GL_CONTEXT_RELEASE_BEHAVIOR)
        .value("GL_CONTEXT_RESET_NOTIFICATION", SDL_GLAttr::SDL_GL_CONTEXT_RESET_NOTIFICATION)
        .value("GL_CONTEXT_NO_ERROR", SDL_GLAttr::SDL_GL_CONTEXT_NO_ERROR)
        .value("GL_FLOATBUFFERS", SDL_GLAttr::SDL_GL_FLOATBUFFERS)
        .value("GL_EGL_PLATFORM", SDL_GLAttr::SDL_GL_EGL_PLATFORM)
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
            SDL_GetDisplays(count);
            return std::make_tuple(count);
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
        , py::arg("closest")
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
    .def("get_display_for_window", [](const SDLWindowWrapper& window)
        {
            return SDL_GetDisplayForWindow(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("get_window_pixel_density", [](const SDLWindowWrapper& window)
        {
            return SDL_GetWindowPixelDensity(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("get_window_display_scale", [](const SDLWindowWrapper& window)
        {
            return SDL_GetWindowDisplayScale(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("set_window_fullscreen_mode", [](const SDLWindowWrapper& window, const SDL_DisplayMode * mode)
        {
            return SDL_SetWindowFullscreenMode(window.get(), mode);
        }
        , py::arg("window")
        , py::arg("mode")
        , py::return_value_policy::automatic_reference)
    .def("get_window_fullscreen_mode", [](const SDLWindowWrapper& window)
        {
            return SDL_GetWindowFullscreenMode(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("get_window_icc_profile", [](const SDLWindowWrapper& window, size_t * size)
        {
            SDL_GetWindowICCProfile(window.get(), size);
            return std::make_tuple(size);
        }
        , py::arg("window")
        , py::arg("size")
        , py::return_value_policy::automatic_reference)
    .def("get_window_pixel_format", [](const SDLWindowWrapper& window)
        {
            return SDL_GetWindowPixelFormat(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("create_window", [](const char * title, int w, int h, SDL_WindowFlags flags)
        {
            return SDLWindowWrapper(SDL_CreateWindow(title, w, h, flags));
        }
        , py::arg("title")
        , py::arg("w")
        , py::arg("h")
        , py::arg("flags")
        , py::return_value_policy::automatic_reference)
    .def("create_popup_window", [](const SDLWindowWrapper& parent, int offset_x, int offset_y, int w, int h, SDL_WindowFlags flags)
        {
            return SDLWindowWrapper(SDL_CreatePopupWindow(parent.get(), offset_x, offset_y, w, h, flags));
        }
        , py::arg("parent")
        , py::arg("offset_x")
        , py::arg("offset_y")
        , py::arg("w")
        , py::arg("h")
        , py::arg("flags")
        , py::return_value_policy::automatic_reference)
    .def("create_window_with_properties", [](SDL_PropertiesID props)
        {
            return SDLWindowWrapper(SDL_CreateWindowWithProperties(props));
        }
        , py::arg("props")
        , py::return_value_policy::automatic_reference)
    .def("get_window_id", [](const SDLWindowWrapper& window)
        {
            return SDL_GetWindowID(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("get_window_from_id", [](SDL_WindowID id)
        {
            return SDLWindowWrapper(SDL_GetWindowFromID(id));
        }
        , py::arg("id")
        , py::return_value_policy::automatic_reference)
    .def("get_window_parent", [](const SDLWindowWrapper& window)
        {
            return SDLWindowWrapper(SDL_GetWindowParent(window.get()));
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("get_window_properties", [](const SDLWindowWrapper& window)
        {
            return SDL_GetWindowProperties(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("get_window_flags", [](const SDLWindowWrapper& window)
        {
            return SDL_GetWindowFlags(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("set_window_title", [](const SDLWindowWrapper& window, const char * title)
        {
            return SDL_SetWindowTitle(window.get(), title);
        }
        , py::arg("window")
        , py::arg("title")
        , py::return_value_policy::automatic_reference)
    .def("get_window_title", [](const SDLWindowWrapper& window)
        {
            return SDL_GetWindowTitle(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("set_window_icon", [](const SDLWindowWrapper& window, SDL_Surface * icon)
        {
            return SDL_SetWindowIcon(window.get(), icon);
        }
        , py::arg("window")
        , py::arg("icon")
        , py::return_value_policy::automatic_reference)
    .def("set_window_position", [](const SDLWindowWrapper& window, int x, int y)
        {
            return SDL_SetWindowPosition(window.get(), x, y);
        }
        , py::arg("window")
        , py::arg("x")
        , py::arg("y")
        , py::return_value_policy::automatic_reference)
    .def("get_window_position", [](const SDLWindowWrapper& window, int * x, int * y)
        {
            SDL_GetWindowPosition(window.get(), x, y);
            return std::make_tuple(x, y);
        }
        , py::arg("window")
        , py::arg("x")
        , py::arg("y")
        , py::return_value_policy::automatic_reference)
    .def("set_window_size", [](const SDLWindowWrapper& window, int w, int h)
        {
            return SDL_SetWindowSize(window.get(), w, h);
        }
        , py::arg("window")
        , py::arg("w")
        , py::arg("h")
        , py::return_value_policy::automatic_reference)
    .def("get_window_size", [](const SDLWindowWrapper& window, int * w, int * h)
        {
            SDL_GetWindowSize(window.get(), w, h);
            return std::make_tuple(w, h);
        }
        , py::arg("window")
        , py::arg("w") = 0
        , py::arg("h") = 0
        , py::return_value_policy::automatic_reference)
    .def("get_window_safe_area", [](const SDLWindowWrapper& window, SDL_Rect * rect)
        {
            return SDL_GetWindowSafeArea(window.get(), rect);
        }
        , py::arg("window")
        , py::arg("rect")
        , py::return_value_policy::automatic_reference)
    .def("set_window_aspect_ratio", [](const SDLWindowWrapper& window, float min_aspect, float max_aspect)
        {
            return SDL_SetWindowAspectRatio(window.get(), min_aspect, max_aspect);
        }
        , py::arg("window")
        , py::arg("min_aspect")
        , py::arg("max_aspect")
        , py::return_value_policy::automatic_reference)
    .def("get_window_aspect_ratio", [](const SDLWindowWrapper& window, float * min_aspect, float * max_aspect)
        {
            SDL_GetWindowAspectRatio(window.get(), min_aspect, max_aspect);
            return std::make_tuple(min_aspect, max_aspect);
        }
        , py::arg("window")
        , py::arg("min_aspect")
        , py::arg("max_aspect")
        , py::return_value_policy::automatic_reference)
    .def("get_window_borders_size", [](const SDLWindowWrapper& window, int * top, int * left, int * bottom, int * right)
        {
            SDL_GetWindowBordersSize(window.get(), top, left, bottom, right);
            return std::make_tuple(top, left, bottom, right);
        }
        , py::arg("window")
        , py::arg("top")
        , py::arg("left")
        , py::arg("bottom")
        , py::arg("right")
        , py::return_value_policy::automatic_reference)
    .def("get_window_size_in_pixels", [](const SDLWindowWrapper& window, int * w, int * h)
        {
            SDL_GetWindowSizeInPixels(window.get(), w, h);
            return std::make_tuple(w, h);
        }
        , py::arg("window")
        , py::arg("w") = 0
        , py::arg("h") = 0
        , py::return_value_policy::automatic_reference)
    .def("set_window_minimum_size", [](const SDLWindowWrapper& window, int min_w, int min_h)
        {
            return SDL_SetWindowMinimumSize(window.get(), min_w, min_h);
        }
        , py::arg("window")
        , py::arg("min_w")
        , py::arg("min_h")
        , py::return_value_policy::automatic_reference)
    .def("get_window_minimum_size", [](const SDLWindowWrapper& window, int * w, int * h)
        {
            SDL_GetWindowMinimumSize(window.get(), w, h);
            return std::make_tuple(w, h);
        }
        , py::arg("window")
        , py::arg("w")
        , py::arg("h")
        , py::return_value_policy::automatic_reference)
    .def("set_window_maximum_size", [](const SDLWindowWrapper& window, int max_w, int max_h)
        {
            return SDL_SetWindowMaximumSize(window.get(), max_w, max_h);
        }
        , py::arg("window")
        , py::arg("max_w")
        , py::arg("max_h")
        , py::return_value_policy::automatic_reference)
    .def("get_window_maximum_size", [](const SDLWindowWrapper& window, int * w, int * h)
        {
            SDL_GetWindowMaximumSize(window.get(), w, h);
            return std::make_tuple(w, h);
        }
        , py::arg("window")
        , py::arg("w")
        , py::arg("h")
        , py::return_value_policy::automatic_reference)
    .def("set_window_bordered", [](const SDLWindowWrapper& window, _Bool bordered)
        {
            return SDL_SetWindowBordered(window.get(), bordered);
        }
        , py::arg("window")
        , py::arg("bordered")
        , py::return_value_policy::automatic_reference)
    .def("set_window_resizable", [](const SDLWindowWrapper& window, _Bool resizable)
        {
            return SDL_SetWindowResizable(window.get(), resizable);
        }
        , py::arg("window")
        , py::arg("resizable")
        , py::return_value_policy::automatic_reference)
    .def("set_window_always_on_top", [](const SDLWindowWrapper& window, _Bool on_top)
        {
            return SDL_SetWindowAlwaysOnTop(window.get(), on_top);
        }
        , py::arg("window")
        , py::arg("on_top")
        , py::return_value_policy::automatic_reference)
    .def("set_window_fill_document", [](const SDLWindowWrapper& window, _Bool fill)
        {
            return SDL_SetWindowFillDocument(window.get(), fill);
        }
        , py::arg("window")
        , py::arg("fill")
        , py::return_value_policy::automatic_reference)
    .def("show_window", [](const SDLWindowWrapper& window)
        {
            return SDL_ShowWindow(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("hide_window", [](const SDLWindowWrapper& window)
        {
            return SDL_HideWindow(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("raise_window", [](const SDLWindowWrapper& window)
        {
            return SDL_RaiseWindow(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("maximize_window", [](const SDLWindowWrapper& window)
        {
            return SDL_MaximizeWindow(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("minimize_window", [](const SDLWindowWrapper& window)
        {
            return SDL_MinimizeWindow(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("restore_window", [](const SDLWindowWrapper& window)
        {
            return SDL_RestoreWindow(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("set_window_fullscreen", [](const SDLWindowWrapper& window, _Bool fullscreen)
        {
            return SDL_SetWindowFullscreen(window.get(), fullscreen);
        }
        , py::arg("window")
        , py::arg("fullscreen")
        , py::return_value_policy::automatic_reference)
    .def("sync_window", [](const SDLWindowWrapper& window)
        {
            return SDL_SyncWindow(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("window_has_surface", [](const SDLWindowWrapper& window)
        {
            return SDL_WindowHasSurface(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("get_window_surface", [](const SDLWindowWrapper& window)
        {
            return SDL_GetWindowSurface(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("set_window_surface_v_sync", [](const SDLWindowWrapper& window, int vsync)
        {
            return SDL_SetWindowSurfaceVSync(window.get(), vsync);
        }
        , py::arg("window")
        , py::arg("vsync")
        , py::return_value_policy::automatic_reference)
    .def("get_window_surface_v_sync", [](const SDLWindowWrapper& window, int * vsync)
        {
            SDL_GetWindowSurfaceVSync(window.get(), vsync);
            return std::make_tuple(vsync);
        }
        , py::arg("window")
        , py::arg("vsync")
        , py::return_value_policy::automatic_reference)
    .def("update_window_surface", [](const SDLWindowWrapper& window)
        {
            return SDL_UpdateWindowSurface(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("update_window_surface_rects", [](const SDLWindowWrapper& window, const SDL_Rect * rects, int numrects)
        {
            return SDL_UpdateWindowSurfaceRects(window.get(), rects, numrects);
        }
        , py::arg("window")
        , py::arg("rects")
        , py::arg("numrects")
        , py::return_value_policy::automatic_reference)
    .def("destroy_window_surface", [](const SDLWindowWrapper& window)
        {
            return SDL_DestroyWindowSurface(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("set_window_keyboard_grab", [](const SDLWindowWrapper& window, _Bool grabbed)
        {
            return SDL_SetWindowKeyboardGrab(window.get(), grabbed);
        }
        , py::arg("window")
        , py::arg("grabbed")
        , py::return_value_policy::automatic_reference)
    .def("set_window_mouse_grab", [](const SDLWindowWrapper& window, _Bool grabbed)
        {
            return SDL_SetWindowMouseGrab(window.get(), grabbed);
        }
        , py::arg("window")
        , py::arg("grabbed")
        , py::return_value_policy::automatic_reference)
    .def("get_window_keyboard_grab", [](const SDLWindowWrapper& window)
        {
            return SDL_GetWindowKeyboardGrab(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("get_window_mouse_grab", [](const SDLWindowWrapper& window)
        {
            return SDL_GetWindowMouseGrab(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("get_grabbed_window", []()
        {
            return SDLWindowWrapper(SDL_GetGrabbedWindow());
        }
        , py::return_value_policy::automatic_reference)
    .def("set_window_mouse_rect", [](const SDLWindowWrapper& window, const SDL_Rect * rect)
        {
            return SDL_SetWindowMouseRect(window.get(), rect);
        }
        , py::arg("window")
        , py::arg("rect")
        , py::return_value_policy::automatic_reference)
    .def("get_window_mouse_rect", [](const SDLWindowWrapper& window)
        {
            return SDL_GetWindowMouseRect(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("set_window_opacity", [](const SDLWindowWrapper& window, float opacity)
        {
            return SDL_SetWindowOpacity(window.get(), opacity);
        }
        , py::arg("window")
        , py::arg("opacity")
        , py::return_value_policy::automatic_reference)
    .def("get_window_opacity", [](const SDLWindowWrapper& window)
        {
            return SDL_GetWindowOpacity(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("set_window_parent", [](const SDLWindowWrapper& window, const SDLWindowWrapper& parent)
        {
            return SDL_SetWindowParent(window.get(), parent.get());
        }
        , py::arg("window")
        , py::arg("parent")
        , py::return_value_policy::automatic_reference)
    .def("set_window_modal", [](const SDLWindowWrapper& window, _Bool modal)
        {
            return SDL_SetWindowModal(window.get(), modal);
        }
        , py::arg("window")
        , py::arg("modal")
        , py::return_value_policy::automatic_reference)
    .def("set_window_focusable", [](const SDLWindowWrapper& window, _Bool focusable)
        {
            return SDL_SetWindowFocusable(window.get(), focusable);
        }
        , py::arg("window")
        , py::arg("focusable")
        , py::return_value_policy::automatic_reference)
    .def("show_window_system_menu", [](const SDLWindowWrapper& window, int x, int y)
        {
            return SDL_ShowWindowSystemMenu(window.get(), x, y);
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
    .def("set_window_shape", [](const SDLWindowWrapper& window, SDL_Surface * shape)
        {
            return SDL_SetWindowShape(window.get(), shape);
        }
        , py::arg("window")
        , py::arg("shape")
        , py::return_value_policy::automatic_reference)
    .def("flash_window", [](const SDLWindowWrapper& window, SDL_FlashOperation operation)
        {
            return SDL_FlashWindow(window.get(), operation);
        }
        , py::arg("window")
        , py::arg("operation")
        , py::return_value_policy::automatic_reference)
    .def("set_window_progress_state", [](const SDLWindowWrapper& window, SDL_ProgressState state)
        {
            return SDL_SetWindowProgressState(window.get(), state);
        }
        , py::arg("window")
        , py::arg("state")
        , py::return_value_policy::automatic_reference)
    .def("get_window_progress_state", [](const SDLWindowWrapper& window)
        {
            return SDL_GetWindowProgressState(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("set_window_progress_value", [](const SDLWindowWrapper& window, float value)
        {
            return SDL_SetWindowProgressValue(window.get(), value);
        }
        , py::arg("window")
        , py::arg("value")
        , py::return_value_policy::automatic_reference)
    .def("get_window_progress_value", [](const SDLWindowWrapper& window)
        {
            return SDL_GetWindowProgressValue(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("destroy_window", [](const SDLWindowWrapper& window)
        {
            return SDL_DestroyWindow(window.get());
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
    .def("gl_get_attribute", [](SDL_GLAttr attr, int * value)
        {
            SDL_GL_GetAttribute(attr, value);
            return std::make_tuple(value);
        }
        , py::arg("attr")
        , py::arg("value")
        , py::return_value_policy::automatic_reference)
    .def("gl_get_current_window", []()
        {
            return SDLWindowWrapper(SDL_GL_GetCurrentWindow());
        }
        , py::return_value_policy::automatic_reference)
    .def("egl_get_current_display", &SDL_EGL_GetCurrentDisplay
        , py::return_value_policy::automatic_reference)
    .def("egl_get_current_config", &SDL_EGL_GetCurrentConfig
        , py::return_value_policy::automatic_reference)
    .def("egl_get_window_surface", [](const SDLWindowWrapper& window)
        {
            return SDL_EGL_GetWindowSurface(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    .def("egl_set_attribute_callbacks", &SDL_EGL_SetAttributeCallbacks
        , py::arg("platform_attrib_callback")
        , py::arg("surface_attrib_callback")
        , py::arg("context_attrib_callback")
        , py::arg("userdata")
        , py::return_value_policy::automatic_reference)
    .def("gl_set_swap_interval", &SDL_GL_SetSwapInterval
        , py::arg("interval")
        , py::return_value_policy::automatic_reference)
    .def("gl_get_swap_interval", [](int * interval)
        {
            SDL_GL_GetSwapInterval(interval);
            return std::make_tuple(interval);
        }
        , py::arg("interval")
        , py::return_value_policy::automatic_reference)
    .def("gl_swap_window", [](const SDLWindowWrapper& window)
        {
            return SDL_GL_SwapWindow(window.get());
        }
        , py::arg("window")
        , py::return_value_policy::automatic_reference)
    ;


}