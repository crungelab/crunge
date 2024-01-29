#include <limits>
#include <filesystem>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#define BUILDING_DLL

#include <SDL.h>

#include <cxbind/cxbind.h>

#include <crunge/sdl/crunge-sdl.h>
#include <crunge/sdl/conversions.h>

namespace py = pybind11;

// SDLWindowWrapper::SDLWindowWrapper(SDL_Window *window) : window(window) {}

void init_main(py::module &_sdl, Registry &registry)
{
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
