#include <stdbool.h>
#include <limits>
#include <iostream>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <SDL3/SDL.h>

#include <cxbind/cxbind.h>
#include <crunge/sdl/conversions.h>
#include <crunge/sdl/crunge-sdl.h>

namespace py = pybind11;

void init_sdl_keyboard_py_auto(py::module &_sdl, Registry &registry) {
    _sdl
    .def("has_keyboard", &SDL_HasKeyboard
        )
    .def("get_keyboards", [](int * count)
        {
            auto _ret = SDL_GetKeyboards(count);
            return std::make_tuple(_ret, count);
        }
        , py::arg("count")
        )
    .def("get_keyboard_name_for_id", &SDL_GetKeyboardNameForID
        , py::arg("instance_id")
        )
    .def("get_keyboard_focus", []()
        {
            return SDLWindowWrapper(SDL_GetKeyboardFocus());
        }
        )
    .def("get_keyboard_state", [](int * numkeys)
        {
            auto _ret = SDL_GetKeyboardState(numkeys);
            return std::make_tuple(_ret, numkeys);
        }
        , py::arg("numkeys")
        )
    .def("reset_keyboard", &SDL_ResetKeyboard
        )
    .def("get_mod_state", &SDL_GetModState
        )
    .def("set_mod_state", &SDL_SetModState
        , py::arg("modstate")
        )
    .def("get_key_from_scancode", &SDL_GetKeyFromScancode
        , py::arg("scancode")
        , py::arg("modstate")
        , py::arg("key_event")
        )
    .def("get_scancode_from_key", [](SDL_Keycode key, SDL_Keymod * modstate)
        {
            auto _ret = SDL_GetScancodeFromKey(key, modstate);
            return std::make_tuple(_ret, modstate);
        }
        , py::arg("key")
        , py::arg("modstate")
        )
    .def("set_scancode_name", &SDL_SetScancodeName
        , py::arg("scancode")
        , py::arg("name")
        )
    .def("get_scancode_name", &SDL_GetScancodeName
        , py::arg("scancode")
        )
    .def("get_scancode_from_name", &SDL_GetScancodeFromName
        , py::arg("name")
        )
    .def("get_key_name", &SDL_GetKeyName
        , py::arg("key")
        )
    .def("get_key_from_name", &SDL_GetKeyFromName
        , py::arg("name")
        )
    .def("start_text_input", [](SDLWindowWrapper window)
        {
            return SDL_StartTextInput(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    ;

    py::enum_<SDL_TextInputType>(_sdl, "TextInputType", py::arithmetic())
        .value("TEXTINPUT_TYPE_TEXT", SDL_TextInputType::SDL_TEXTINPUT_TYPE_TEXT)
        .value("TEXTINPUT_TYPE_TEXT_NAME", SDL_TextInputType::SDL_TEXTINPUT_TYPE_TEXT_NAME)
        .value("TEXTINPUT_TYPE_TEXT_EMAIL", SDL_TextInputType::SDL_TEXTINPUT_TYPE_TEXT_EMAIL)
        .value("TEXTINPUT_TYPE_TEXT_USERNAME", SDL_TextInputType::SDL_TEXTINPUT_TYPE_TEXT_USERNAME)
        .value("TEXTINPUT_TYPE_TEXT_PASSWORD_HIDDEN", SDL_TextInputType::SDL_TEXTINPUT_TYPE_TEXT_PASSWORD_HIDDEN)
        .value("TEXTINPUT_TYPE_TEXT_PASSWORD_VISIBLE", SDL_TextInputType::SDL_TEXTINPUT_TYPE_TEXT_PASSWORD_VISIBLE)
        .value("TEXTINPUT_TYPE_NUMBER", SDL_TextInputType::SDL_TEXTINPUT_TYPE_NUMBER)
        .value("TEXTINPUT_TYPE_NUMBER_PASSWORD_HIDDEN", SDL_TextInputType::SDL_TEXTINPUT_TYPE_NUMBER_PASSWORD_HIDDEN)
        .value("TEXTINPUT_TYPE_NUMBER_PASSWORD_VISIBLE", SDL_TextInputType::SDL_TEXTINPUT_TYPE_NUMBER_PASSWORD_VISIBLE)
        .export_values()
    ;
    py::enum_<SDL_Capitalization>(_sdl, "Capitalization", py::arithmetic())
        .value("CAPITALIZE_NONE", SDL_Capitalization::SDL_CAPITALIZE_NONE)
        .value("CAPITALIZE_SENTENCES", SDL_Capitalization::SDL_CAPITALIZE_SENTENCES)
        .value("CAPITALIZE_WORDS", SDL_Capitalization::SDL_CAPITALIZE_WORDS)
        .value("CAPITALIZE_LETTERS", SDL_Capitalization::SDL_CAPITALIZE_LETTERS)
        .export_values()
    ;
    _sdl
    .def("start_text_input_with_properties", [](SDLWindowWrapper window, SDL_PropertiesID props)
        {
            return SDL_StartTextInputWithProperties(static_cast<SDL_Window *>(window.get()), props);
        }
        , py::arg("window")
        , py::arg("props")
        )
    .def("text_input_active", [](SDLWindowWrapper window)
        {
            return SDL_TextInputActive(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("stop_text_input", [](SDLWindowWrapper window)
        {
            return SDL_StopTextInput(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("clear_composition", [](SDLWindowWrapper window)
        {
            return SDL_ClearComposition(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    .def("set_text_input_area", [](SDLWindowWrapper window, const SDL_Rect * rect, int cursor)
        {
            return SDL_SetTextInputArea(static_cast<SDL_Window *>(window.get()), rect, cursor);
        }
        , py::arg("window")
        , py::arg("rect")
        , py::arg("cursor")
        )
    .def("get_text_input_area", [](SDLWindowWrapper window, SDL_Rect * rect, int * cursor)
        {
            auto _ret = SDL_GetTextInputArea(static_cast<SDL_Window *>(window.get()), rect, cursor);
            return std::make_tuple(_ret, cursor);
        }
        , py::arg("window")
        , py::arg("rect")
        , py::arg("cursor")
        )
    .def("has_screen_keyboard_support", &SDL_HasScreenKeyboardSupport
        )
    .def("screen_keyboard_shown", [](SDLWindowWrapper window)
        {
            return SDL_ScreenKeyboardShown(static_cast<SDL_Window *>(window.get()));
        }
        , py::arg("window")
        )
    ;


}