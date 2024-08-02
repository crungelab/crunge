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
    _sdl.def("has_keyboard", &SDL_HasKeyboard
    , py::return_value_policy::automatic_reference);

    _sdl.def("get_keyboards", [](int * count)
    {
        auto ret = SDL_GetKeyboards(count);
        return std::make_tuple(ret, count);
    }
    , py::arg("count")
    , py::return_value_policy::automatic_reference);

    _sdl.def("get_keyboard_name_for_id", &SDL_GetKeyboardNameForID
    , py::arg("instance_id")
    , py::return_value_policy::automatic_reference);

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

    _sdl.def("get_default_key_from_scancode", &SDL_GetDefaultKeyFromScancode
    , py::arg("scancode")
    , py::arg("modstate")
    , py::return_value_policy::automatic_reference);

    _sdl.def("get_key_from_scancode", &SDL_GetKeyFromScancode
    , py::arg("scancode")
    , py::arg("modstate")
    , py::return_value_policy::automatic_reference);

    _sdl.def("get_default_scancode_from_key", [](unsigned int key, unsigned short * modstate)
    {
        auto ret = SDL_GetDefaultScancodeFromKey(key, modstate);
        return std::make_tuple(ret, modstate);
    }
    , py::arg("key")
    , py::arg("modstate")
    , py::return_value_policy::automatic_reference);

    _sdl.def("get_scancode_from_key", [](unsigned int key, unsigned short * modstate)
    {
        auto ret = SDL_GetScancodeFromKey(key, modstate);
        return std::make_tuple(ret, modstate);
    }
    , py::arg("key")
    , py::arg("modstate")
    , py::return_value_policy::automatic_reference);

    _sdl.def("set_scancode_name", &SDL_SetScancodeName
    , py::arg("scancode")
    , py::arg("name")
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

    _sdl.def("start_text_input", [](SDLWindowWrapper * window)
    {
        auto ret = SDL_StartTextInput(window->get());
        return ret;
    }
    , py::arg("window")
    , py::return_value_policy::automatic_reference);

    _sdl.def("text_input_active", [](SDLWindowWrapper * window)
    {
        auto ret = SDL_TextInputActive(window->get());
        return ret;
    }
    , py::arg("window")
    , py::return_value_policy::automatic_reference);

    _sdl.def("stop_text_input", [](SDLWindowWrapper * window)
    {
        auto ret = SDL_StopTextInput(window->get());
        return ret;
    }
    , py::arg("window")
    , py::return_value_policy::automatic_reference);

    _sdl.def("clear_composition", [](SDLWindowWrapper * window)
    {
        auto ret = SDL_ClearComposition(window->get());
        return ret;
    }
    , py::arg("window")
    , py::return_value_policy::automatic_reference);

    _sdl.def("set_text_input_area", [](SDLWindowWrapper * window, const SDL_Rect * rect, int cursor)
    {
        auto ret = SDL_SetTextInputArea(window->get(), rect, cursor);
        return ret;
    }
    , py::arg("window")
    , py::arg("rect")
    , py::arg("cursor")
    , py::return_value_policy::automatic_reference);

    _sdl.def("get_text_input_area", [](SDLWindowWrapper * window, SDL_Rect * rect, int * cursor)
    {
        auto ret = SDL_GetTextInputArea(window->get(), rect, cursor);
        return std::make_tuple(ret, cursor);
    }
    , py::arg("window")
    , py::arg("rect")
    , py::arg("cursor")
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