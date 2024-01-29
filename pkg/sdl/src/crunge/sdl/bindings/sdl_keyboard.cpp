#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

#include <SDL3/SDL.h>
#include <iostream>

#include <cxbind/cxbind.h>
#include <crunge/sdl/conversions.h>
#include <crunge/sdl/crunge-sdl.h>

namespace py = pybind11;

void init_sdl_keyboard(py::module &_sdl, Registry &registry) {
    PYCLASS_BEGIN(_sdl, SDL_Keysym, Keysym)
        Keysym.def_readwrite("scancode", &SDL_Keysym::scancode);
        Keysym.def_readwrite("sym", &SDL_Keysym::sym);
        Keysym.def_readwrite("mod", &SDL_Keysym::mod);
        Keysym.def_readwrite("unused", &SDL_Keysym::unused);
    PYCLASS_END(_sdl, SDL_Keysym, Keysym)

    _sdl.def("get_keyboard_focus", []()
    {
        auto ret = new SDLWindowWrapper(SDL_GetKeyboardFocus());
        return ret;
    }
    , py::return_value_policy::automatic_reference);

    _sdl.def("get_keyboard_state", [](int * numkeys)
    {
        auto ret = SDL_GetKeyboardState(numkeys);
        return std::make_tuple(ret, numkeys);
    }
    , py::arg("numkeys")
    , py::return_value_policy::automatic_reference);

    _sdl.def("reset_keyboard", &SDL_ResetKeyboard
    , py::return_value_policy::automatic_reference);

    _sdl.def("get_mod_state", &SDL_GetModState
    , py::return_value_policy::automatic_reference);

    _sdl.def("set_mod_state", &SDL_SetModState
    , py::arg("modstate")
    , py::return_value_policy::automatic_reference);

    _sdl.def("get_key_from_scancode", &SDL_GetKeyFromScancode
    , py::arg("scancode")
    , py::return_value_policy::automatic_reference);

    _sdl.def("get_scancode_from_key", &SDL_GetScancodeFromKey
    , py::arg("key")
    , py::return_value_policy::automatic_reference);

    _sdl.def("get_scancode_name", &SDL_GetScancodeName
    , py::arg("scancode")
    , py::return_value_policy::automatic_reference);

    _sdl.def("get_scancode_from_name", &SDL_GetScancodeFromName
    , py::arg("name")
    , py::return_value_policy::automatic_reference);

    _sdl.def("get_key_name", &SDL_GetKeyName
    , py::arg("key")
    , py::return_value_policy::automatic_reference);

    _sdl.def("get_key_from_name", &SDL_GetKeyFromName
    , py::arg("name")
    , py::return_value_policy::automatic_reference);

    _sdl.def("start_text_input", &SDL_StartTextInput
    , py::return_value_policy::automatic_reference);

    _sdl.def("text_input_active", &SDL_TextInputActive
    , py::return_value_policy::automatic_reference);

    _sdl.def("stop_text_input", &SDL_StopTextInput
    , py::return_value_policy::automatic_reference);

    _sdl.def("clear_composition", &SDL_ClearComposition
    , py::return_value_policy::automatic_reference);

    _sdl.def("text_input_shown", &SDL_TextInputShown
    , py::return_value_policy::automatic_reference);

    _sdl.def("set_text_input_rect", &SDL_SetTextInputRect
    , py::arg("rect")
    , py::return_value_policy::automatic_reference);

    _sdl.def("has_screen_keyboard_support", &SDL_HasScreenKeyboardSupport
    , py::return_value_policy::automatic_reference);

    _sdl.def("screen_keyboard_shown", [](SDLWindowWrapper * window)
    {
        auto ret = SDL_ScreenKeyboardShown(window->get());
        return ret;
    }
    , py::arg("window")
    , py::return_value_policy::automatic_reference);


}