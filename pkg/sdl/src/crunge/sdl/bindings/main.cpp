#include <limits>
#include <filesystem>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#define BUILDING_DLL

#include <SDL3/SDL.h>

#include <cxbind/cxbind.h>

#include <crunge/sdl/crunge-sdl.h>
#include <crunge/sdl/conversions.h>

namespace py = pybind11;

// Define an enum that mimics the old SDL initialization flags
enum class InitFlags : SDL_InitFlags {
    INIT_TIMER      = SDL_INIT_TIMER,
    INIT_AUDIO      = SDL_INIT_AUDIO,
    INIT_VIDEO      = SDL_INIT_VIDEO,
    INIT_JOYSTICK   = SDL_INIT_JOYSTICK,
    INIT_HAPTIC     = SDL_INIT_HAPTIC,
    INIT_GAMEPAD    = SDL_INIT_GAMEPAD,
    INIT_EVENTS     = SDL_INIT_EVENTS,
    INIT_SENSOR     = SDL_INIT_SENSOR,
    INIT_CAMERA     = SDL_INIT_CAMERA
};

void init_main(py::module &_sdl, Registry &registry)
{

    py::enum_<InitFlags>(_sdl, "InitFlags", py::arithmetic())
        .value("INIT_TIMER", InitFlags::INIT_TIMER)
        .value("INIT_AUDIO", InitFlags::INIT_AUDIO)
        .value("INIT_VIDEO", InitFlags::INIT_VIDEO)
        .value("INIT_JOYSTICK", InitFlags::INIT_JOYSTICK)
        .value("INIT_HAPTIC", InitFlags::INIT_HAPTIC)
        .value("INIT_GAMEPAD", InitFlags::INIT_GAMEPAD)
        .value("INIT_EVENTS", InitFlags::INIT_EVENTS)
        .value("INIT_SENSOR", InitFlags::INIT_SENSOR)
        .value("INIT_CAMERA", InitFlags::INIT_CAMERA)
        .export_values();

    PYCLASS_BEGIN(_sdl, SDLWindowWrapper, Window)
    PYCLASS_END(_sdl, SDLWindowWrapper, Window)

    _sdl.def(
        "poll_event", []()
        {
        SDL_Event event;
        if(!SDL_PollEvent(&event))
            return py::cast<py::object>(Py_None);
        if (event.type >= SDL_EVENT_WINDOW_FIRST && event.type <= SDL_EVENT_WINDOW_LAST) {
            SDL_WindowEvent windowEvent = event.window;
            return py::cast(windowEvent);
        }
        switch (event.type)
        {
            case SDL_EVENT_QUIT:
            {
                SDL_QuitEvent quitEvent = event.quit;
                return py::cast(quitEvent);
            }
            case SDL_EVENT_KEY_DOWN:
            case SDL_EVENT_KEY_UP:
            {
                SDL_KeyboardEvent keyEvent = event.key;
                return py::cast(keyEvent);
            }
            case SDL_EVENT_MOUSE_MOTION:
            {
                SDL_MouseMotionEvent mouseMotionEvent = event.motion;
                return py::cast(mouseMotionEvent);
            }
            case SDL_EVENT_MOUSE_BUTTON_DOWN:
            case SDL_EVENT_MOUSE_BUTTON_UP:
            {
                SDL_MouseButtonEvent mouseButtonEvent = event.button;
                return py::cast(mouseButtonEvent);
            }
            case SDL_EVENT_MOUSE_WHEEL:
            {
                SDL_MouseWheelEvent mouseWheelEvent = event.wheel;
                return py::cast(mouseWheelEvent);
            }
        }
        return py::cast<py::object>(Py_None); },
        py::return_value_policy::automatic_reference);
}
