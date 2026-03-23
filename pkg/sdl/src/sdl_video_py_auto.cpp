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
        )
    .def("get_video_driver", &SDL_GetVideoDriver
        , py::arg("index")
        )
    .def("get_current_video_driver", &SDL_GetCurrentVideoDriver
        )
    .def("get_system_theme", &SDL_GetSystemTheme
        )
    .def("get_displays", [](int * count)
        {
            auto _ret = SDL_GetDisplays(count);
            return std::make_tuple(_ret, count);
        }
        , py::arg("count")
        )
    .def("get_primary_display", &SDL_GetPrimaryDisplay
        )
    .def("get_display_properties", &SDL_GetDisplayProperties
        , py::arg("display_id")
        )
    .def("get_display_name", &SDL_GetDisplayName
        , py::arg("display_id")
        )
    .def("get_display_bounds", &SDL_GetDisplayBounds
        , py::arg("display_id")
        , py::arg("rect")
        )
    .def("get_display_usable_bounds", &SDL_GetDisplayUsableBounds
        , py::arg("display_id")
        , py::arg("rect")
        )
    .def("get_natural_display_orientation", &SDL_GetNaturalDisplayOrientation
        , py::arg("display_id")
        )
    .def("get_current_display_orientation", &SDL_GetCurrentDisplayOrientation
        , py::arg("display_id")
        )
    .def("get_display_content_scale", &SDL_GetDisplayContentScale
        , py::arg("display_id")
        )
    .def("get_closest_fullscreen_display_mode", &SDL_GetClosestFullscreenDisplayMode
        , py::arg("display_id")
        , py::arg("w")
        , py::arg("h")
        , py::arg("refresh_rate")
        , py::arg("include_high_density_modes")
        , py::arg("closest")
        )
    .def("get_desktop_display_mode", &SDL_GetDesktopDisplayMode
        , py::arg("display_id")
        )
    .def("get_current_display_mode", &SDL_GetCurrentDisplayMode
        , py::arg("display_id")
        )
    .def("get_display_for_point", &SDL_GetDisplayForPoint
        , py::arg("point")
        )
    .def("get_display_for_rect", &SDL_GetDisplayForRect
        , py::arg("rect")
        )
    .def("get_display_for_window", [](SDLWindowWrapper window)
        {
            return SDL_GetDisplayForWindow(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("get_window_pixel_density", [](SDLWindowWrapper window)
        {
            return SDL_GetWindowPixelDensity(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("get_window_display_scale", [](SDLWindowWrapper window)
        {
            return SDL_GetWindowDisplayScale(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("set_window_fullscreen_mode", [](SDLWindowWrapper window, const SDL_DisplayMode * mode)
        {
            return SDL_SetWindowFullscreenMode(static_cast<SDL_Window *>(window.get()), mode);
        }
        , py::arg("window")
        , py::arg("mode")
        )
    .def("get_window_fullscreen_mode", [](SDLWindowWrapper window)
        {
            return SDL_GetWindowFullscreenMode(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("get_window_icc_profile", [](SDLWindowWrapper window, size_t * size)
        {
            auto _ret = SDL_GetWindowICCProfile(static_cast<SDL_Window *>(window.get()), size);
            return std::make_tuple(_ret, size);
        }
        , py::arg("window")
        , py::arg("size")
        )
    .def("get_window_pixel_format", [](SDLWindowWrapper window)
        {
            return SDL_GetWindowPixelFormat(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("create_window", [](const char * title, int w, int h, SDL_WindowFlags flags)
        {
            return SDLWindowWrapper(SDL_CreateWindow(title, w, h, flags));
        }
        , py::arg("title")
        , py::arg("w")
        , py::arg("h")
        , py::arg("flags")
        )
    .def("create_popup_window", [](SDLWindowWrapper parent, int offset_x, int offset_y, int w, int h, SDL_WindowFlags flags)
        {
            return SDLWindowWrapper(SDL_CreatePopupWindow(static_cast<SDL_Window *>(parent.get()), offset_x, offset_y, w, h, flags));
        }
        , py::arg("parent")
        , py::arg("offset_x")
        , py::arg("offset_y")
        , py::arg("w")
        , py::arg("h")
        , py::arg("flags")
        )
    .def("create_window_with_properties", [](SDL_PropertiesID props)
        {
            return SDLWindowWrapper(SDL_CreateWindowWithProperties(props));
        }
        , py::arg("props")
        )
    .def("get_window_id", [](SDLWindowWrapper window)
        {
            return SDL_GetWindowID(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("get_window_from_id", [](SDL_WindowID id)
        {
            return SDLWindowWrapper(SDL_GetWindowFromID(id));
        }
        , py::arg("id")
        )
    .def("get_window_parent", [](SDLWindowWrapper window)
        {
            return SDLWindowWrapper(SDL_GetWindowParent(static_cast<SDL_Window *>(window.get())));
        }
        , py::arg("window")
        )
    .def("get_window_properties", [](SDLWindowWrapper window)
        {
            return SDL_GetWindowProperties(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("get_window_flags", [](SDLWindowWrapper window)
        {
            return SDL_GetWindowFlags(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("set_window_title", [](SDLWindowWrapper window, const char * title)
        {
            return SDL_SetWindowTitle(static_cast<SDL_Window *>(window.get()), title);
        }
        , py::arg("window")
        , py::arg("title")
        )
    .def("get_window_title", [](SDLWindowWrapper window)
        {
            return SDL_GetWindowTitle(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("set_window_icon", [](SDLWindowWrapper window, SDL_Surface * icon)
        {
            return SDL_SetWindowIcon(static_cast<SDL_Window *>(window.get()), icon);
        }
        , py::arg("window")
        , py::arg("icon")
        )
    .def("set_window_position", [](SDLWindowWrapper window, int x, int y)
        {
            return SDL_SetWindowPosition(static_cast<SDL_Window *>(window.get()), x, y);
        }
        , py::arg("window")
        , py::arg("x")
        , py::arg("y")
        )
    .def("get_window_position", [](SDLWindowWrapper window, int * x, int * y)
        {
            auto _ret = SDL_GetWindowPosition(static_cast<SDL_Window *>(window.get()), x, y);
            return std::make_tuple(_ret, x, y);
        }
        , py::arg("window")
        , py::arg("x")
        , py::arg("y")
        )
    .def("set_window_size", [](SDLWindowWrapper window, int w, int h)
        {
            return SDL_SetWindowSize(static_cast<SDL_Window *>(window.get()), w, h);
        }
        , py::arg("window")
        , py::arg("w")
        , py::arg("h")
        )
    .def("get_window_size", [](SDLWindowWrapper window, int * w, int * h)
        {
            SDL_GetWindowSize(static_cast<SDL_Window *>(window.get()), w, h);
            return std::make_tuple(w, h);
        }
        , py::arg("window")
        , py::arg("w") = 0
        , py::arg("h") = 0
        )
    .def("get_window_safe_area", [](SDLWindowWrapper window, SDL_Rect * rect)
        {
            return SDL_GetWindowSafeArea(static_cast<SDL_Window *>(window.get()), rect);
        }
        , py::arg("window")
        , py::arg("rect")
        )
    .def("set_window_aspect_ratio", [](SDLWindowWrapper window, float min_aspect, float max_aspect)
        {
            return SDL_SetWindowAspectRatio(static_cast<SDL_Window *>(window.get()), min_aspect, max_aspect);
        }
        , py::arg("window")
        , py::arg("min_aspect")
        , py::arg("max_aspect")
        )
    .def("get_window_aspect_ratio", [](SDLWindowWrapper window, float * min_aspect, float * max_aspect)
        {
            auto _ret = SDL_GetWindowAspectRatio(static_cast<SDL_Window *>(window.get()), min_aspect, max_aspect);
            return std::make_tuple(_ret, min_aspect, max_aspect);
        }
        , py::arg("window")
        , py::arg("min_aspect")
        , py::arg("max_aspect")
        )
    .def("get_window_borders_size", [](SDLWindowWrapper window, int * top, int * left, int * bottom, int * right)
        {
            auto _ret = SDL_GetWindowBordersSize(static_cast<SDL_Window *>(window.get()), top, left, bottom, right);
            return std::make_tuple(_ret, top, left, bottom, right);
        }
        , py::arg("window")
        , py::arg("top")
        , py::arg("left")
        , py::arg("bottom")
        , py::arg("right")
        )
    .def("get_window_size_in_pixels", [](SDLWindowWrapper window, int * w, int * h)
        {
            SDL_GetWindowSizeInPixels(static_cast<SDL_Window *>(window.get()), w, h);
            return std::make_tuple(w, h);
        }
        , py::arg("window")
        , py::arg("w") = 0
        , py::arg("h") = 0
        )
    .def("set_window_minimum_size", [](SDLWindowWrapper window, int min_w, int min_h)
        {
            return SDL_SetWindowMinimumSize(static_cast<SDL_Window *>(window.get()), min_w, min_h);
        }
        , py::arg("window")
        , py::arg("min_w")
        , py::arg("min_h")
        )
    .def("get_window_minimum_size", [](SDLWindowWrapper window, int * w, int * h)
        {
            auto _ret = SDL_GetWindowMinimumSize(static_cast<SDL_Window *>(window.get()), w, h);
            return std::make_tuple(_ret, w, h);
        }
        , py::arg("window")
        , py::arg("w")
        , py::arg("h")
        )
    .def("set_window_maximum_size", [](SDLWindowWrapper window, int max_w, int max_h)
        {
            return SDL_SetWindowMaximumSize(static_cast<SDL_Window *>(window.get()), max_w, max_h);
        }
        , py::arg("window")
        , py::arg("max_w")
        , py::arg("max_h")
        )
    .def("get_window_maximum_size", [](SDLWindowWrapper window, int * w, int * h)
        {
            auto _ret = SDL_GetWindowMaximumSize(static_cast<SDL_Window *>(window.get()), w, h);
            return std::make_tuple(_ret, w, h);
        }
        , py::arg("window")
        , py::arg("w")
        , py::arg("h")
        )
    .def("set_window_bordered", [](SDLWindowWrapper window, _Bool bordered)
        {
            return SDL_SetWindowBordered(static_cast<SDL_Window *>(window.get()), bordered);
        }
        , py::arg("window")
        , py::arg("bordered")
        )
    .def("set_window_resizable", [](SDLWindowWrapper window, _Bool resizable)
        {
            return SDL_SetWindowResizable(static_cast<SDL_Window *>(window.get()), resizable);
        }
        , py::arg("window")
        , py::arg("resizable")
        )
    .def("set_window_always_on_top", [](SDLWindowWrapper window, _Bool on_top)
        {
            return SDL_SetWindowAlwaysOnTop(static_cast<SDL_Window *>(window.get()), on_top);
        }
        , py::arg("window")
        , py::arg("on_top")
        )
    .def("set_window_fill_document", [](SDLWindowWrapper window, _Bool fill)
        {
            return SDL_SetWindowFillDocument(static_cast<SDL_Window *>(window.get()), fill);
        }
        , py::arg("window")
        , py::arg("fill")
        )
    .def("show_window", [](SDLWindowWrapper window)
        {
            return SDL_ShowWindow(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("hide_window", [](SDLWindowWrapper window)
        {
            return SDL_HideWindow(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("raise_window", [](SDLWindowWrapper window)
        {
            return SDL_RaiseWindow(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("maximize_window", [](SDLWindowWrapper window)
        {
            return SDL_MaximizeWindow(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("minimize_window", [](SDLWindowWrapper window)
        {
            return SDL_MinimizeWindow(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("restore_window", [](SDLWindowWrapper window)
        {
            return SDL_RestoreWindow(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("set_window_fullscreen", [](SDLWindowWrapper window, _Bool fullscreen)
        {
            return SDL_SetWindowFullscreen(static_cast<SDL_Window *>(window.get()), fullscreen);
        }
        , py::arg("window")
        , py::arg("fullscreen")
        )
    .def("sync_window", [](SDLWindowWrapper window)
        {
            return SDL_SyncWindow(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("window_has_surface", [](SDLWindowWrapper window)
        {
            return SDL_WindowHasSurface(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("get_window_surface", [](SDLWindowWrapper window)
        {
            return SDL_GetWindowSurface(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("set_window_surface_v_sync", [](SDLWindowWrapper window, int vsync)
        {
            return SDL_SetWindowSurfaceVSync(static_cast<SDL_Window *>(window.get()), vsync);
        }
        , py::arg("window")
        , py::arg("vsync")
        )
    .def("get_window_surface_v_sync", [](SDLWindowWrapper window, int * vsync)
        {
            auto _ret = SDL_GetWindowSurfaceVSync(static_cast<SDL_Window *>(window.get()), vsync);
            return std::make_tuple(_ret, vsync);
        }
        , py::arg("window")
        , py::arg("vsync")
        )
    .def("update_window_surface", [](SDLWindowWrapper window)
        {
            return SDL_UpdateWindowSurface(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("update_window_surface_rects", [](SDLWindowWrapper window, const SDL_Rect * rects, int numrects)
        {
            return SDL_UpdateWindowSurfaceRects(static_cast<SDL_Window *>(window.get()), rects, numrects);
        }
        , py::arg("window")
        , py::arg("rects")
        , py::arg("numrects")
        )
    .def("destroy_window_surface", [](SDLWindowWrapper window)
        {
            return SDL_DestroyWindowSurface(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("set_window_keyboard_grab", [](SDLWindowWrapper window, _Bool grabbed)
        {
            return SDL_SetWindowKeyboardGrab(static_cast<SDL_Window *>(window.get()), grabbed);
        }
        , py::arg("window")
        , py::arg("grabbed")
        )
    .def("set_window_mouse_grab", [](SDLWindowWrapper window, _Bool grabbed)
        {
            return SDL_SetWindowMouseGrab(static_cast<SDL_Window *>(window.get()), grabbed);
        }
        , py::arg("window")
        , py::arg("grabbed")
        )
    .def("get_window_keyboard_grab", [](SDLWindowWrapper window)
        {
            return SDL_GetWindowKeyboardGrab(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("get_window_mouse_grab", [](SDLWindowWrapper window)
        {
            return SDL_GetWindowMouseGrab(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("get_grabbed_window", []()
        {
            return SDLWindowWrapper(SDL_GetGrabbedWindow());
        }
        )
    .def("set_window_mouse_rect", [](SDLWindowWrapper window, const SDL_Rect * rect)
        {
            return SDL_SetWindowMouseRect(static_cast<SDL_Window *>(window.get()), rect);
        }
        , py::arg("window")
        , py::arg("rect")
        )
    .def("get_window_mouse_rect", [](SDLWindowWrapper window)
        {
            return SDL_GetWindowMouseRect(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("set_window_opacity", [](SDLWindowWrapper window, float opacity)
        {
            return SDL_SetWindowOpacity(static_cast<SDL_Window *>(window.get()), opacity);
        }
        , py::arg("window")
        , py::arg("opacity")
        )
    .def("get_window_opacity", [](SDLWindowWrapper window)
        {
            return SDL_GetWindowOpacity(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("set_window_parent", [](SDLWindowWrapper window, SDLWindowWrapper parent)
        {
            return SDL_SetWindowParent(static_cast<SDL_Window *>(window.get()), static_cast<SDL_Window *>(parent.get()));
        }
        , py::arg("window")
        , py::arg("parent")
        )
    .def("set_window_modal", [](SDLWindowWrapper window, _Bool modal)
        {
            return SDL_SetWindowModal(static_cast<SDL_Window *>(window.get()), modal);
        }
        , py::arg("window")
        , py::arg("modal")
        )
    .def("set_window_focusable", [](SDLWindowWrapper window, _Bool focusable)
        {
            return SDL_SetWindowFocusable(static_cast<SDL_Window *>(window.get()), focusable);
        }
        , py::arg("window")
        , py::arg("focusable")
        )
    .def("show_window_system_menu", [](SDLWindowWrapper window, int x, int y)
        {
            return SDL_ShowWindowSystemMenu(static_cast<SDL_Window *>(window.get()), x, y);
        }
        , py::arg("window")
        , py::arg("x")
        , py::arg("y")
        )
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
    .def("set_window_shape", [](SDLWindowWrapper window, SDL_Surface * shape)
        {
            return SDL_SetWindowShape(static_cast<SDL_Window *>(window.get()), shape);
        }
        , py::arg("window")
        , py::arg("shape")
        )
    .def("flash_window", [](SDLWindowWrapper window, SDL_FlashOperation operation)
        {
            return SDL_FlashWindow(static_cast<SDL_Window *>(window.get()), operation);
        }
        , py::arg("window")
        , py::arg("operation")
        )
    .def("set_window_progress_state", [](SDLWindowWrapper window, SDL_ProgressState state)
        {
            return SDL_SetWindowProgressState(static_cast<SDL_Window *>(window.get()), state);
        }
        , py::arg("window")
        , py::arg("state")
        )
    .def("get_window_progress_state", [](SDLWindowWrapper window)
        {
            return SDL_GetWindowProgressState(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("set_window_progress_value", [](SDLWindowWrapper window, float value)
        {
            return SDL_SetWindowProgressValue(static_cast<SDL_Window *>(window.get()), value);
        }
        , py::arg("window")
        , py::arg("value")
        )
    .def("get_window_progress_value", [](SDLWindowWrapper window)
        {
            return SDL_GetWindowProgressValue(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("destroy_window", [](SDLWindowWrapper window)
        {
            return SDL_DestroyWindow(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("screen_saver_enabled", &SDL_ScreenSaverEnabled
        )
    .def("enable_screen_saver", &SDL_EnableScreenSaver
        )
    .def("disable_screen_saver", &SDL_DisableScreenSaver
        )
    .def("gl_load_library", &SDL_GL_LoadLibrary
        , py::arg("path")
        )
    .def("gl_unload_library", &SDL_GL_UnloadLibrary
        )
    .def("gl_extension_supported", &SDL_GL_ExtensionSupported
        , py::arg("extension")
        )
    .def("gl_reset_attributes", &SDL_GL_ResetAttributes
        )
    .def("gl_set_attribute", &SDL_GL_SetAttribute
        , py::arg("attr")
        , py::arg("value")
        )
    .def("gl_get_attribute", [](SDL_GLAttr attr, int * value)
        {
            auto _ret = SDL_GL_GetAttribute(attr, value);
            return std::make_tuple(_ret, value);
        }
        , py::arg("attr")
        , py::arg("value")
        )
    .def("gl_get_current_window", []()
        {
            return SDLWindowWrapper(SDL_GL_GetCurrentWindow());
        }
        )
    .def("egl_get_current_display", &SDL_EGL_GetCurrentDisplay
        )
    .def("egl_get_current_config", &SDL_EGL_GetCurrentConfig
        )
    .def("egl_get_window_surface", [](SDLWindowWrapper window)
        {
            return SDL_EGL_GetWindowSurface(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("egl_set_attribute_callbacks", &SDL_EGL_SetAttributeCallbacks
        , py::arg("platform_attrib_callback")
        , py::arg("surface_attrib_callback")
        , py::arg("context_attrib_callback")
        , py::arg("userdata")
        )
    .def("gl_set_swap_interval", &SDL_GL_SetSwapInterval
        , py::arg("interval")
        )
    .def("gl_get_swap_interval", [](int * interval)
        {
            auto _ret = SDL_GL_GetSwapInterval(interval);
            return std::make_tuple(_ret, interval);
        }
        , py::arg("interval")
        )
    .def("gl_swap_window", [](SDLWindowWrapper window)
        {
            return SDL_GL_SwapWindow(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    ;


}