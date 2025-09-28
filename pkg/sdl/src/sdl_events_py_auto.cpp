#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

#include <SDL3/SDL.h>
#include <iostream>

#include <cxbind/cxbind.h>
#include <crunge/sdl/conversions.h>

namespace py = pybind11;

void init_sdl_events_py_auto(py::module &_sdl, Registry &registry) {
    py::enum_<SDL_EventType>(_sdl, "EventType", py::arithmetic())
        .value("FIRST", SDL_EventType::SDL_EVENT_FIRST)
        .value("QUIT", SDL_EventType::SDL_EVENT_QUIT)
        .value("TERMINATING", SDL_EventType::SDL_EVENT_TERMINATING)
        .value("LOW_MEMORY", SDL_EventType::SDL_EVENT_LOW_MEMORY)
        .value("WILL_ENTER_BACKGROUND", SDL_EventType::SDL_EVENT_WILL_ENTER_BACKGROUND)
        .value("DID_ENTER_BACKGROUND", SDL_EventType::SDL_EVENT_DID_ENTER_BACKGROUND)
        .value("WILL_ENTER_FOREGROUND", SDL_EventType::SDL_EVENT_WILL_ENTER_FOREGROUND)
        .value("DID_ENTER_FOREGROUND", SDL_EventType::SDL_EVENT_DID_ENTER_FOREGROUND)
        .value("LOCALE_CHANGED", SDL_EventType::SDL_EVENT_LOCALE_CHANGED)
        .value("SYSTEM_THEME_CHANGED", SDL_EventType::SDL_EVENT_SYSTEM_THEME_CHANGED)
        .value("DISPLAY_ORIENTATION", SDL_EventType::SDL_EVENT_DISPLAY_ORIENTATION)
        .value("DISPLAY_ADDED", SDL_EventType::SDL_EVENT_DISPLAY_ADDED)
        .value("DISPLAY_REMOVED", SDL_EventType::SDL_EVENT_DISPLAY_REMOVED)
        .value("DISPLAY_MOVED", SDL_EventType::SDL_EVENT_DISPLAY_MOVED)
        .value("DISPLAY_DESKTOP_MODE_CHANGED", SDL_EventType::SDL_EVENT_DISPLAY_DESKTOP_MODE_CHANGED)
        .value("DISPLAY_CURRENT_MODE_CHANGED", SDL_EventType::SDL_EVENT_DISPLAY_CURRENT_MODE_CHANGED)
        .value("DISPLAY_CONTENT_SCALE_CHANGED", SDL_EventType::SDL_EVENT_DISPLAY_CONTENT_SCALE_CHANGED)
        .value("DISPLAY_FIRST", SDL_EventType::SDL_EVENT_DISPLAY_FIRST)
        .value("DISPLAY_LAST", SDL_EventType::SDL_EVENT_DISPLAY_LAST)
        .value("WINDOW_SHOWN", SDL_EventType::SDL_EVENT_WINDOW_SHOWN)
        .value("WINDOW_HIDDEN", SDL_EventType::SDL_EVENT_WINDOW_HIDDEN)
        .value("WINDOW_EXPOSED", SDL_EventType::SDL_EVENT_WINDOW_EXPOSED)
        .value("WINDOW_MOVED", SDL_EventType::SDL_EVENT_WINDOW_MOVED)
        .value("WINDOW_RESIZED", SDL_EventType::SDL_EVENT_WINDOW_RESIZED)
        .value("WINDOW_PIXEL_SIZE_CHANGED", SDL_EventType::SDL_EVENT_WINDOW_PIXEL_SIZE_CHANGED)
        .value("WINDOW_METAL_VIEW_RESIZED", SDL_EventType::SDL_EVENT_WINDOW_METAL_VIEW_RESIZED)
        .value("WINDOW_MINIMIZED", SDL_EventType::SDL_EVENT_WINDOW_MINIMIZED)
        .value("WINDOW_MAXIMIZED", SDL_EventType::SDL_EVENT_WINDOW_MAXIMIZED)
        .value("WINDOW_RESTORED", SDL_EventType::SDL_EVENT_WINDOW_RESTORED)
        .value("WINDOW_MOUSE_ENTER", SDL_EventType::SDL_EVENT_WINDOW_MOUSE_ENTER)
        .value("WINDOW_MOUSE_LEAVE", SDL_EventType::SDL_EVENT_WINDOW_MOUSE_LEAVE)
        .value("WINDOW_FOCUS_GAINED", SDL_EventType::SDL_EVENT_WINDOW_FOCUS_GAINED)
        .value("WINDOW_FOCUS_LOST", SDL_EventType::SDL_EVENT_WINDOW_FOCUS_LOST)
        .value("WINDOW_CLOSE_REQUESTED", SDL_EventType::SDL_EVENT_WINDOW_CLOSE_REQUESTED)
        .value("WINDOW_HIT_TEST", SDL_EventType::SDL_EVENT_WINDOW_HIT_TEST)
        .value("WINDOW_ICCPROF_CHANGED", SDL_EventType::SDL_EVENT_WINDOW_ICCPROF_CHANGED)
        .value("WINDOW_DISPLAY_CHANGED", SDL_EventType::SDL_EVENT_WINDOW_DISPLAY_CHANGED)
        .value("WINDOW_DISPLAY_SCALE_CHANGED", SDL_EventType::SDL_EVENT_WINDOW_DISPLAY_SCALE_CHANGED)
        .value("WINDOW_SAFE_AREA_CHANGED", SDL_EventType::SDL_EVENT_WINDOW_SAFE_AREA_CHANGED)
        .value("WINDOW_OCCLUDED", SDL_EventType::SDL_EVENT_WINDOW_OCCLUDED)
        .value("WINDOW_ENTER_FULLSCREEN", SDL_EventType::SDL_EVENT_WINDOW_ENTER_FULLSCREEN)
        .value("WINDOW_LEAVE_FULLSCREEN", SDL_EventType::SDL_EVENT_WINDOW_LEAVE_FULLSCREEN)
        .value("WINDOW_DESTROYED", SDL_EventType::SDL_EVENT_WINDOW_DESTROYED)
        .value("WINDOW_HDR_STATE_CHANGED", SDL_EventType::SDL_EVENT_WINDOW_HDR_STATE_CHANGED)
        .value("WINDOW_FIRST", SDL_EventType::SDL_EVENT_WINDOW_FIRST)
        .value("WINDOW_LAST", SDL_EventType::SDL_EVENT_WINDOW_LAST)
        .value("KEY_DOWN", SDL_EventType::SDL_EVENT_KEY_DOWN)
        .value("KEY_UP", SDL_EventType::SDL_EVENT_KEY_UP)
        .value("TEXT_EDITING", SDL_EventType::SDL_EVENT_TEXT_EDITING)
        .value("TEXT_INPUT", SDL_EventType::SDL_EVENT_TEXT_INPUT)
        .value("KEYMAP_CHANGED", SDL_EventType::SDL_EVENT_KEYMAP_CHANGED)
        .value("KEYBOARD_ADDED", SDL_EventType::SDL_EVENT_KEYBOARD_ADDED)
        .value("KEYBOARD_REMOVED", SDL_EventType::SDL_EVENT_KEYBOARD_REMOVED)
        .value("TEXT_EDITING_CANDIDATES", SDL_EventType::SDL_EVENT_TEXT_EDITING_CANDIDATES)
        .value("MOUSE_MOTION", SDL_EventType::SDL_EVENT_MOUSE_MOTION)
        .value("MOUSE_BUTTON_DOWN", SDL_EventType::SDL_EVENT_MOUSE_BUTTON_DOWN)
        .value("MOUSE_BUTTON_UP", SDL_EventType::SDL_EVENT_MOUSE_BUTTON_UP)
        .value("MOUSE_WHEEL", SDL_EventType::SDL_EVENT_MOUSE_WHEEL)
        .value("MOUSE_ADDED", SDL_EventType::SDL_EVENT_MOUSE_ADDED)
        .value("MOUSE_REMOVED", SDL_EventType::SDL_EVENT_MOUSE_REMOVED)
        .value("JOYSTICK_AXIS_MOTION", SDL_EventType::SDL_EVENT_JOYSTICK_AXIS_MOTION)
        .value("JOYSTICK_BALL_MOTION", SDL_EventType::SDL_EVENT_JOYSTICK_BALL_MOTION)
        .value("JOYSTICK_HAT_MOTION", SDL_EventType::SDL_EVENT_JOYSTICK_HAT_MOTION)
        .value("JOYSTICK_BUTTON_DOWN", SDL_EventType::SDL_EVENT_JOYSTICK_BUTTON_DOWN)
        .value("JOYSTICK_BUTTON_UP", SDL_EventType::SDL_EVENT_JOYSTICK_BUTTON_UP)
        .value("JOYSTICK_ADDED", SDL_EventType::SDL_EVENT_JOYSTICK_ADDED)
        .value("JOYSTICK_REMOVED", SDL_EventType::SDL_EVENT_JOYSTICK_REMOVED)
        .value("JOYSTICK_BATTERY_UPDATED", SDL_EventType::SDL_EVENT_JOYSTICK_BATTERY_UPDATED)
        .value("JOYSTICK_UPDATE_COMPLETE", SDL_EventType::SDL_EVENT_JOYSTICK_UPDATE_COMPLETE)
        .value("GAMEPAD_AXIS_MOTION", SDL_EventType::SDL_EVENT_GAMEPAD_AXIS_MOTION)
        .value("GAMEPAD_BUTTON_DOWN", SDL_EventType::SDL_EVENT_GAMEPAD_BUTTON_DOWN)
        .value("GAMEPAD_BUTTON_UP", SDL_EventType::SDL_EVENT_GAMEPAD_BUTTON_UP)
        .value("GAMEPAD_ADDED", SDL_EventType::SDL_EVENT_GAMEPAD_ADDED)
        .value("GAMEPAD_REMOVED", SDL_EventType::SDL_EVENT_GAMEPAD_REMOVED)
        .value("GAMEPAD_REMAPPED", SDL_EventType::SDL_EVENT_GAMEPAD_REMAPPED)
        .value("GAMEPAD_TOUCHPAD_DOWN", SDL_EventType::SDL_EVENT_GAMEPAD_TOUCHPAD_DOWN)
        .value("GAMEPAD_TOUCHPAD_MOTION", SDL_EventType::SDL_EVENT_GAMEPAD_TOUCHPAD_MOTION)
        .value("GAMEPAD_TOUCHPAD_UP", SDL_EventType::SDL_EVENT_GAMEPAD_TOUCHPAD_UP)
        .value("GAMEPAD_SENSOR_UPDATE", SDL_EventType::SDL_EVENT_GAMEPAD_SENSOR_UPDATE)
        .value("GAMEPAD_UPDATE_COMPLETE", SDL_EventType::SDL_EVENT_GAMEPAD_UPDATE_COMPLETE)
        .value("GAMEPAD_STEAM_HANDLE_UPDATED", SDL_EventType::SDL_EVENT_GAMEPAD_STEAM_HANDLE_UPDATED)
        .value("FINGER_DOWN", SDL_EventType::SDL_EVENT_FINGER_DOWN)
        .value("FINGER_UP", SDL_EventType::SDL_EVENT_FINGER_UP)
        .value("FINGER_MOTION", SDL_EventType::SDL_EVENT_FINGER_MOTION)
        .value("FINGER_CANCELED", SDL_EventType::SDL_EVENT_FINGER_CANCELED)
        .value("CLIPBOARD_UPDATE", SDL_EventType::SDL_EVENT_CLIPBOARD_UPDATE)
        .value("DROP_FILE", SDL_EventType::SDL_EVENT_DROP_FILE)
        .value("DROP_TEXT", SDL_EventType::SDL_EVENT_DROP_TEXT)
        .value("DROP_BEGIN", SDL_EventType::SDL_EVENT_DROP_BEGIN)
        .value("DROP_COMPLETE", SDL_EventType::SDL_EVENT_DROP_COMPLETE)
        .value("DROP_POSITION", SDL_EventType::SDL_EVENT_DROP_POSITION)
        .value("AUDIO_DEVICE_ADDED", SDL_EventType::SDL_EVENT_AUDIO_DEVICE_ADDED)
        .value("AUDIO_DEVICE_REMOVED", SDL_EventType::SDL_EVENT_AUDIO_DEVICE_REMOVED)
        .value("AUDIO_DEVICE_FORMAT_CHANGED", SDL_EventType::SDL_EVENT_AUDIO_DEVICE_FORMAT_CHANGED)
        .value("SENSOR_UPDATE", SDL_EventType::SDL_EVENT_SENSOR_UPDATE)
        .value("PEN_PROXIMITY_IN", SDL_EventType::SDL_EVENT_PEN_PROXIMITY_IN)
        .value("PEN_PROXIMITY_OUT", SDL_EventType::SDL_EVENT_PEN_PROXIMITY_OUT)
        .value("PEN_DOWN", SDL_EventType::SDL_EVENT_PEN_DOWN)
        .value("PEN_UP", SDL_EventType::SDL_EVENT_PEN_UP)
        .value("PEN_BUTTON_DOWN", SDL_EventType::SDL_EVENT_PEN_BUTTON_DOWN)
        .value("PEN_BUTTON_UP", SDL_EventType::SDL_EVENT_PEN_BUTTON_UP)
        .value("PEN_MOTION", SDL_EventType::SDL_EVENT_PEN_MOTION)
        .value("PEN_AXIS", SDL_EventType::SDL_EVENT_PEN_AXIS)
        .value("CAMERA_DEVICE_ADDED", SDL_EventType::SDL_EVENT_CAMERA_DEVICE_ADDED)
        .value("CAMERA_DEVICE_REMOVED", SDL_EventType::SDL_EVENT_CAMERA_DEVICE_REMOVED)
        .value("CAMERA_DEVICE_APPROVED", SDL_EventType::SDL_EVENT_CAMERA_DEVICE_APPROVED)
        .value("CAMERA_DEVICE_DENIED", SDL_EventType::SDL_EVENT_CAMERA_DEVICE_DENIED)
        .value("RENDER_TARGETS_RESET", SDL_EventType::SDL_EVENT_RENDER_TARGETS_RESET)
        .value("RENDER_DEVICE_RESET", SDL_EventType::SDL_EVENT_RENDER_DEVICE_RESET)
        .value("RENDER_DEVICE_LOST", SDL_EventType::SDL_EVENT_RENDER_DEVICE_LOST)
        .value("PRIVATE0", SDL_EventType::SDL_EVENT_PRIVATE0)
        .value("PRIVATE1", SDL_EventType::SDL_EVENT_PRIVATE1)
        .value("PRIVATE2", SDL_EventType::SDL_EVENT_PRIVATE2)
        .value("PRIVATE3", SDL_EventType::SDL_EVENT_PRIVATE3)
        .value("POLL_SENTINEL", SDL_EventType::SDL_EVENT_POLL_SENTINEL)
        .value("USER", SDL_EventType::SDL_EVENT_USER)
        .value("LAST", SDL_EventType::SDL_EVENT_LAST)
        .value("ENUM_PADDING", SDL_EventType::SDL_EVENT_ENUM_PADDING)
        .export_values()
    ;
    py::class_<SDL_CommonEvent> _CommonEvent(_sdl, "CommonEvent");
    registry.on(_sdl, "CommonEvent", _CommonEvent);
        _CommonEvent
        .def_readwrite("type", &SDL_CommonEvent::type)
        .def_readwrite("reserved", &SDL_CommonEvent::reserved)
        .def_readwrite("timestamp", &SDL_CommonEvent::timestamp)
    ;

    py::class_<SDL_DisplayEvent> _DisplayEvent(_sdl, "DisplayEvent");
    registry.on(_sdl, "DisplayEvent", _DisplayEvent);
        _DisplayEvent
        .def_readwrite("type", &SDL_DisplayEvent::type)
        .def_readwrite("reserved", &SDL_DisplayEvent::reserved)
        .def_readwrite("timestamp", &SDL_DisplayEvent::timestamp)
        .def_readwrite("display_id", &SDL_DisplayEvent::displayID)
        .def_readwrite("data1", &SDL_DisplayEvent::data1)
        .def_readwrite("data2", &SDL_DisplayEvent::data2)
    ;

    py::class_<SDL_WindowEvent> _WindowEvent(_sdl, "WindowEvent");
    registry.on(_sdl, "WindowEvent", _WindowEvent);
        _WindowEvent
        .def_readwrite("type", &SDL_WindowEvent::type)
        .def_readwrite("reserved", &SDL_WindowEvent::reserved)
        .def_readwrite("timestamp", &SDL_WindowEvent::timestamp)
        .def_readwrite("window_id", &SDL_WindowEvent::windowID)
        .def_readwrite("data1", &SDL_WindowEvent::data1)
        .def_readwrite("data2", &SDL_WindowEvent::data2)
    ;

    py::class_<SDL_KeyboardDeviceEvent> _KeyboardDeviceEvent(_sdl, "KeyboardDeviceEvent");
    registry.on(_sdl, "KeyboardDeviceEvent", _KeyboardDeviceEvent);
        _KeyboardDeviceEvent
        .def_readwrite("type", &SDL_KeyboardDeviceEvent::type)
        .def_readwrite("reserved", &SDL_KeyboardDeviceEvent::reserved)
        .def_readwrite("timestamp", &SDL_KeyboardDeviceEvent::timestamp)
        .def_readwrite("which", &SDL_KeyboardDeviceEvent::which)
    ;

    py::class_<SDL_KeyboardEvent> _KeyboardEvent(_sdl, "KeyboardEvent");
    registry.on(_sdl, "KeyboardEvent", _KeyboardEvent);
        _KeyboardEvent
        .def_readwrite("type", &SDL_KeyboardEvent::type)
        .def_readwrite("reserved", &SDL_KeyboardEvent::reserved)
        .def_readwrite("timestamp", &SDL_KeyboardEvent::timestamp)
        .def_readwrite("window_id", &SDL_KeyboardEvent::windowID)
        .def_readwrite("which", &SDL_KeyboardEvent::which)
        .def_readwrite("scancode", &SDL_KeyboardEvent::scancode)
        .def_readwrite("key", &SDL_KeyboardEvent::key)
        .def_readwrite("mod", &SDL_KeyboardEvent::mod)
        .def_readwrite("raw", &SDL_KeyboardEvent::raw)
        .def_readwrite("down", &SDL_KeyboardEvent::down)
        .def_readwrite("repeat", &SDL_KeyboardEvent::repeat)
    ;

    py::class_<SDL_TextEditingEvent> _TextEditingEvent(_sdl, "TextEditingEvent");
    registry.on(_sdl, "TextEditingEvent", _TextEditingEvent);
        _TextEditingEvent
        .def_readwrite("type", &SDL_TextEditingEvent::type)
        .def_readwrite("reserved", &SDL_TextEditingEvent::reserved)
        .def_readwrite("timestamp", &SDL_TextEditingEvent::timestamp)
        .def_readwrite("window_id", &SDL_TextEditingEvent::windowID)
        .def_property("text",
            [](const SDL_TextEditingEvent& self){ return self.text; },
            [](SDL_TextEditingEvent& self, const char* source){ self.text = strdup(source); }
        )
        .def_readwrite("start", &SDL_TextEditingEvent::start)
        .def_readwrite("length", &SDL_TextEditingEvent::length)
    ;

    py::class_<SDL_TextEditingCandidatesEvent> _TextEditingCandidatesEvent(_sdl, "TextEditingCandidatesEvent");
    registry.on(_sdl, "TextEditingCandidatesEvent", _TextEditingCandidatesEvent);
        _TextEditingCandidatesEvent
        .def_readwrite("type", &SDL_TextEditingCandidatesEvent::type)
        .def_readwrite("reserved", &SDL_TextEditingCandidatesEvent::reserved)
        .def_readwrite("timestamp", &SDL_TextEditingCandidatesEvent::timestamp)
        .def_readwrite("window_id", &SDL_TextEditingCandidatesEvent::windowID)
        .def_readwrite("num_candidates", &SDL_TextEditingCandidatesEvent::num_candidates)
        .def_readwrite("selected_candidate", &SDL_TextEditingCandidatesEvent::selected_candidate)
        .def_readwrite("horizontal", &SDL_TextEditingCandidatesEvent::horizontal)
        .def_readwrite("padding1", &SDL_TextEditingCandidatesEvent::padding1)
        .def_readwrite("padding2", &SDL_TextEditingCandidatesEvent::padding2)
        .def_readwrite("padding3", &SDL_TextEditingCandidatesEvent::padding3)
    ;

    py::class_<SDL_TextInputEvent> _TextInputEvent(_sdl, "TextInputEvent");
    registry.on(_sdl, "TextInputEvent", _TextInputEvent);
        _TextInputEvent
        .def_readwrite("type", &SDL_TextInputEvent::type)
        .def_readwrite("reserved", &SDL_TextInputEvent::reserved)
        .def_readwrite("timestamp", &SDL_TextInputEvent::timestamp)
        .def_readwrite("window_id", &SDL_TextInputEvent::windowID)
        .def_property("text",
            [](const SDL_TextInputEvent& self){ return self.text; },
            [](SDL_TextInputEvent& self, const char* source){ self.text = strdup(source); }
        )
    ;

    py::class_<SDL_MouseDeviceEvent> _MouseDeviceEvent(_sdl, "MouseDeviceEvent");
    registry.on(_sdl, "MouseDeviceEvent", _MouseDeviceEvent);
        _MouseDeviceEvent
        .def_readwrite("type", &SDL_MouseDeviceEvent::type)
        .def_readwrite("reserved", &SDL_MouseDeviceEvent::reserved)
        .def_readwrite("timestamp", &SDL_MouseDeviceEvent::timestamp)
        .def_readwrite("which", &SDL_MouseDeviceEvent::which)
    ;

    py::class_<SDL_MouseMotionEvent> _MouseMotionEvent(_sdl, "MouseMotionEvent");
    registry.on(_sdl, "MouseMotionEvent", _MouseMotionEvent);
        _MouseMotionEvent
        .def_readwrite("type", &SDL_MouseMotionEvent::type)
        .def_readwrite("reserved", &SDL_MouseMotionEvent::reserved)
        .def_readwrite("timestamp", &SDL_MouseMotionEvent::timestamp)
        .def_readwrite("window_id", &SDL_MouseMotionEvent::windowID)
        .def_readwrite("which", &SDL_MouseMotionEvent::which)
        .def_readwrite("state", &SDL_MouseMotionEvent::state)
        .def_readwrite("x", &SDL_MouseMotionEvent::x)
        .def_readwrite("y", &SDL_MouseMotionEvent::y)
        .def_readwrite("xrel", &SDL_MouseMotionEvent::xrel)
        .def_readwrite("yrel", &SDL_MouseMotionEvent::yrel)
    ;

    py::class_<SDL_MouseButtonEvent> _MouseButtonEvent(_sdl, "MouseButtonEvent");
    registry.on(_sdl, "MouseButtonEvent", _MouseButtonEvent);
        _MouseButtonEvent
        .def_readwrite("type", &SDL_MouseButtonEvent::type)
        .def_readwrite("reserved", &SDL_MouseButtonEvent::reserved)
        .def_readwrite("timestamp", &SDL_MouseButtonEvent::timestamp)
        .def_readwrite("window_id", &SDL_MouseButtonEvent::windowID)
        .def_readwrite("which", &SDL_MouseButtonEvent::which)
        .def_readwrite("button", &SDL_MouseButtonEvent::button)
        .def_readwrite("down", &SDL_MouseButtonEvent::down)
        .def_readwrite("clicks", &SDL_MouseButtonEvent::clicks)
        .def_readwrite("padding", &SDL_MouseButtonEvent::padding)
        .def_readwrite("x", &SDL_MouseButtonEvent::x)
        .def_readwrite("y", &SDL_MouseButtonEvent::y)
    ;

    py::class_<SDL_MouseWheelEvent> _MouseWheelEvent(_sdl, "MouseWheelEvent");
    registry.on(_sdl, "MouseWheelEvent", _MouseWheelEvent);
        _MouseWheelEvent
        .def_readwrite("type", &SDL_MouseWheelEvent::type)
        .def_readwrite("reserved", &SDL_MouseWheelEvent::reserved)
        .def_readwrite("timestamp", &SDL_MouseWheelEvent::timestamp)
        .def_readwrite("window_id", &SDL_MouseWheelEvent::windowID)
        .def_readwrite("which", &SDL_MouseWheelEvent::which)
        .def_readwrite("x", &SDL_MouseWheelEvent::x)
        .def_readwrite("y", &SDL_MouseWheelEvent::y)
        .def_readwrite("direction", &SDL_MouseWheelEvent::direction)
        .def_readwrite("mouse_x", &SDL_MouseWheelEvent::mouse_x)
        .def_readwrite("mouse_y", &SDL_MouseWheelEvent::mouse_y)
        .def_readwrite("integer_x", &SDL_MouseWheelEvent::integer_x)
        .def_readwrite("integer_y", &SDL_MouseWheelEvent::integer_y)
    ;

    py::class_<SDL_JoyAxisEvent> _JoyAxisEvent(_sdl, "JoyAxisEvent");
    registry.on(_sdl, "JoyAxisEvent", _JoyAxisEvent);
        _JoyAxisEvent
        .def_readwrite("type", &SDL_JoyAxisEvent::type)
        .def_readwrite("reserved", &SDL_JoyAxisEvent::reserved)
        .def_readwrite("timestamp", &SDL_JoyAxisEvent::timestamp)
        .def_readwrite("which", &SDL_JoyAxisEvent::which)
        .def_readwrite("axis", &SDL_JoyAxisEvent::axis)
        .def_readwrite("padding1", &SDL_JoyAxisEvent::padding1)
        .def_readwrite("padding2", &SDL_JoyAxisEvent::padding2)
        .def_readwrite("padding3", &SDL_JoyAxisEvent::padding3)
        .def_readwrite("value", &SDL_JoyAxisEvent::value)
        .def_readwrite("padding4", &SDL_JoyAxisEvent::padding4)
    ;

    py::class_<SDL_JoyBallEvent> _JoyBallEvent(_sdl, "JoyBallEvent");
    registry.on(_sdl, "JoyBallEvent", _JoyBallEvent);
        _JoyBallEvent
        .def_readwrite("type", &SDL_JoyBallEvent::type)
        .def_readwrite("reserved", &SDL_JoyBallEvent::reserved)
        .def_readwrite("timestamp", &SDL_JoyBallEvent::timestamp)
        .def_readwrite("which", &SDL_JoyBallEvent::which)
        .def_readwrite("ball", &SDL_JoyBallEvent::ball)
        .def_readwrite("padding1", &SDL_JoyBallEvent::padding1)
        .def_readwrite("padding2", &SDL_JoyBallEvent::padding2)
        .def_readwrite("padding3", &SDL_JoyBallEvent::padding3)
        .def_readwrite("xrel", &SDL_JoyBallEvent::xrel)
        .def_readwrite("yrel", &SDL_JoyBallEvent::yrel)
    ;

    py::class_<SDL_JoyHatEvent> _JoyHatEvent(_sdl, "JoyHatEvent");
    registry.on(_sdl, "JoyHatEvent", _JoyHatEvent);
        _JoyHatEvent
        .def_readwrite("type", &SDL_JoyHatEvent::type)
        .def_readwrite("reserved", &SDL_JoyHatEvent::reserved)
        .def_readwrite("timestamp", &SDL_JoyHatEvent::timestamp)
        .def_readwrite("which", &SDL_JoyHatEvent::which)
        .def_readwrite("hat", &SDL_JoyHatEvent::hat)
        .def_readwrite("value", &SDL_JoyHatEvent::value)
        .def_readwrite("padding1", &SDL_JoyHatEvent::padding1)
        .def_readwrite("padding2", &SDL_JoyHatEvent::padding2)
    ;

    py::class_<SDL_JoyButtonEvent> _JoyButtonEvent(_sdl, "JoyButtonEvent");
    registry.on(_sdl, "JoyButtonEvent", _JoyButtonEvent);
        _JoyButtonEvent
        .def_readwrite("type", &SDL_JoyButtonEvent::type)
        .def_readwrite("reserved", &SDL_JoyButtonEvent::reserved)
        .def_readwrite("timestamp", &SDL_JoyButtonEvent::timestamp)
        .def_readwrite("which", &SDL_JoyButtonEvent::which)
        .def_readwrite("button", &SDL_JoyButtonEvent::button)
        .def_readwrite("down", &SDL_JoyButtonEvent::down)
        .def_readwrite("padding1", &SDL_JoyButtonEvent::padding1)
        .def_readwrite("padding2", &SDL_JoyButtonEvent::padding2)
    ;

    py::class_<SDL_JoyDeviceEvent> _JoyDeviceEvent(_sdl, "JoyDeviceEvent");
    registry.on(_sdl, "JoyDeviceEvent", _JoyDeviceEvent);
        _JoyDeviceEvent
        .def_readwrite("type", &SDL_JoyDeviceEvent::type)
        .def_readwrite("reserved", &SDL_JoyDeviceEvent::reserved)
        .def_readwrite("timestamp", &SDL_JoyDeviceEvent::timestamp)
        .def_readwrite("which", &SDL_JoyDeviceEvent::which)
    ;

    py::class_<SDL_JoyBatteryEvent> _JoyBatteryEvent(_sdl, "JoyBatteryEvent");
    registry.on(_sdl, "JoyBatteryEvent", _JoyBatteryEvent);
        _JoyBatteryEvent
        .def_readwrite("type", &SDL_JoyBatteryEvent::type)
        .def_readwrite("reserved", &SDL_JoyBatteryEvent::reserved)
        .def_readwrite("timestamp", &SDL_JoyBatteryEvent::timestamp)
        .def_readwrite("which", &SDL_JoyBatteryEvent::which)
        .def_readwrite("state", &SDL_JoyBatteryEvent::state)
        .def_readwrite("percent", &SDL_JoyBatteryEvent::percent)
    ;

    py::class_<SDL_GamepadAxisEvent> _GamepadAxisEvent(_sdl, "GamepadAxisEvent");
    registry.on(_sdl, "GamepadAxisEvent", _GamepadAxisEvent);
        _GamepadAxisEvent
        .def_readwrite("type", &SDL_GamepadAxisEvent::type)
        .def_readwrite("reserved", &SDL_GamepadAxisEvent::reserved)
        .def_readwrite("timestamp", &SDL_GamepadAxisEvent::timestamp)
        .def_readwrite("which", &SDL_GamepadAxisEvent::which)
        .def_readwrite("axis", &SDL_GamepadAxisEvent::axis)
        .def_readwrite("padding1", &SDL_GamepadAxisEvent::padding1)
        .def_readwrite("padding2", &SDL_GamepadAxisEvent::padding2)
        .def_readwrite("padding3", &SDL_GamepadAxisEvent::padding3)
        .def_readwrite("value", &SDL_GamepadAxisEvent::value)
        .def_readwrite("padding4", &SDL_GamepadAxisEvent::padding4)
    ;

    py::class_<SDL_GamepadButtonEvent> _GamepadButtonEvent(_sdl, "GamepadButtonEvent");
    registry.on(_sdl, "GamepadButtonEvent", _GamepadButtonEvent);
        _GamepadButtonEvent
        .def_readwrite("type", &SDL_GamepadButtonEvent::type)
        .def_readwrite("reserved", &SDL_GamepadButtonEvent::reserved)
        .def_readwrite("timestamp", &SDL_GamepadButtonEvent::timestamp)
        .def_readwrite("which", &SDL_GamepadButtonEvent::which)
        .def_readwrite("button", &SDL_GamepadButtonEvent::button)
        .def_readwrite("down", &SDL_GamepadButtonEvent::down)
        .def_readwrite("padding1", &SDL_GamepadButtonEvent::padding1)
        .def_readwrite("padding2", &SDL_GamepadButtonEvent::padding2)
    ;

    py::class_<SDL_GamepadDeviceEvent> _GamepadDeviceEvent(_sdl, "GamepadDeviceEvent");
    registry.on(_sdl, "GamepadDeviceEvent", _GamepadDeviceEvent);
        _GamepadDeviceEvent
        .def_readwrite("type", &SDL_GamepadDeviceEvent::type)
        .def_readwrite("reserved", &SDL_GamepadDeviceEvent::reserved)
        .def_readwrite("timestamp", &SDL_GamepadDeviceEvent::timestamp)
        .def_readwrite("which", &SDL_GamepadDeviceEvent::which)
    ;

    py::class_<SDL_GamepadTouchpadEvent> _GamepadTouchpadEvent(_sdl, "GamepadTouchpadEvent");
    registry.on(_sdl, "GamepadTouchpadEvent", _GamepadTouchpadEvent);
        _GamepadTouchpadEvent
        .def_readwrite("type", &SDL_GamepadTouchpadEvent::type)
        .def_readwrite("reserved", &SDL_GamepadTouchpadEvent::reserved)
        .def_readwrite("timestamp", &SDL_GamepadTouchpadEvent::timestamp)
        .def_readwrite("which", &SDL_GamepadTouchpadEvent::which)
        .def_readwrite("touchpad", &SDL_GamepadTouchpadEvent::touchpad)
        .def_readwrite("finger", &SDL_GamepadTouchpadEvent::finger)
        .def_readwrite("x", &SDL_GamepadTouchpadEvent::x)
        .def_readwrite("y", &SDL_GamepadTouchpadEvent::y)
        .def_readwrite("pressure", &SDL_GamepadTouchpadEvent::pressure)
    ;

    py::class_<SDL_GamepadSensorEvent> _GamepadSensorEvent(_sdl, "GamepadSensorEvent");
    registry.on(_sdl, "GamepadSensorEvent", _GamepadSensorEvent);
        _GamepadSensorEvent
        .def_readwrite("type", &SDL_GamepadSensorEvent::type)
        .def_readwrite("reserved", &SDL_GamepadSensorEvent::reserved)
        .def_readwrite("timestamp", &SDL_GamepadSensorEvent::timestamp)
        .def_readwrite("which", &SDL_GamepadSensorEvent::which)
        .def_readwrite("sensor", &SDL_GamepadSensorEvent::sensor)
        .def_readonly("data", &SDL_GamepadSensorEvent::data)
        .def_readwrite("sensor_timestamp", &SDL_GamepadSensorEvent::sensor_timestamp)
    ;

    py::class_<SDL_AudioDeviceEvent> _AudioDeviceEvent(_sdl, "AudioDeviceEvent");
    registry.on(_sdl, "AudioDeviceEvent", _AudioDeviceEvent);
        _AudioDeviceEvent
        .def_readwrite("type", &SDL_AudioDeviceEvent::type)
        .def_readwrite("reserved", &SDL_AudioDeviceEvent::reserved)
        .def_readwrite("timestamp", &SDL_AudioDeviceEvent::timestamp)
        .def_readwrite("which", &SDL_AudioDeviceEvent::which)
        .def_readwrite("recording", &SDL_AudioDeviceEvent::recording)
        .def_readwrite("padding1", &SDL_AudioDeviceEvent::padding1)
        .def_readwrite("padding2", &SDL_AudioDeviceEvent::padding2)
        .def_readwrite("padding3", &SDL_AudioDeviceEvent::padding3)
    ;

    py::class_<SDL_CameraDeviceEvent> _CameraDeviceEvent(_sdl, "CameraDeviceEvent");
    registry.on(_sdl, "CameraDeviceEvent", _CameraDeviceEvent);
        _CameraDeviceEvent
        .def_readwrite("type", &SDL_CameraDeviceEvent::type)
        .def_readwrite("reserved", &SDL_CameraDeviceEvent::reserved)
        .def_readwrite("timestamp", &SDL_CameraDeviceEvent::timestamp)
        .def_readwrite("which", &SDL_CameraDeviceEvent::which)
    ;

    py::class_<SDL_RenderEvent> _RenderEvent(_sdl, "RenderEvent");
    registry.on(_sdl, "RenderEvent", _RenderEvent);
        _RenderEvent
        .def_readwrite("type", &SDL_RenderEvent::type)
        .def_readwrite("reserved", &SDL_RenderEvent::reserved)
        .def_readwrite("timestamp", &SDL_RenderEvent::timestamp)
        .def_readwrite("window_id", &SDL_RenderEvent::windowID)
    ;

    py::class_<SDL_TouchFingerEvent> _TouchFingerEvent(_sdl, "TouchFingerEvent");
    registry.on(_sdl, "TouchFingerEvent", _TouchFingerEvent);
        _TouchFingerEvent
        .def_readwrite("type", &SDL_TouchFingerEvent::type)
        .def_readwrite("reserved", &SDL_TouchFingerEvent::reserved)
        .def_readwrite("timestamp", &SDL_TouchFingerEvent::timestamp)
        .def_readwrite("touch_id", &SDL_TouchFingerEvent::touchID)
        .def_readwrite("finger_id", &SDL_TouchFingerEvent::fingerID)
        .def_readwrite("x", &SDL_TouchFingerEvent::x)
        .def_readwrite("y", &SDL_TouchFingerEvent::y)
        .def_readwrite("dx", &SDL_TouchFingerEvent::dx)
        .def_readwrite("dy", &SDL_TouchFingerEvent::dy)
        .def_readwrite("pressure", &SDL_TouchFingerEvent::pressure)
        .def_readwrite("window_id", &SDL_TouchFingerEvent::windowID)
    ;

    py::class_<SDL_PenProximityEvent> _PenProximityEvent(_sdl, "PenProximityEvent");
    registry.on(_sdl, "PenProximityEvent", _PenProximityEvent);
        _PenProximityEvent
        .def_readwrite("type", &SDL_PenProximityEvent::type)
        .def_readwrite("reserved", &SDL_PenProximityEvent::reserved)
        .def_readwrite("timestamp", &SDL_PenProximityEvent::timestamp)
        .def_readwrite("window_id", &SDL_PenProximityEvent::windowID)
        .def_readwrite("which", &SDL_PenProximityEvent::which)
    ;

    py::class_<SDL_PenMotionEvent> _PenMotionEvent(_sdl, "PenMotionEvent");
    registry.on(_sdl, "PenMotionEvent", _PenMotionEvent);
        _PenMotionEvent
        .def_readwrite("type", &SDL_PenMotionEvent::type)
        .def_readwrite("reserved", &SDL_PenMotionEvent::reserved)
        .def_readwrite("timestamp", &SDL_PenMotionEvent::timestamp)
        .def_readwrite("window_id", &SDL_PenMotionEvent::windowID)
        .def_readwrite("which", &SDL_PenMotionEvent::which)
        .def_readwrite("pen_state", &SDL_PenMotionEvent::pen_state)
        .def_readwrite("x", &SDL_PenMotionEvent::x)
        .def_readwrite("y", &SDL_PenMotionEvent::y)
    ;

    py::class_<SDL_PenTouchEvent> _PenTouchEvent(_sdl, "PenTouchEvent");
    registry.on(_sdl, "PenTouchEvent", _PenTouchEvent);
        _PenTouchEvent
        .def_readwrite("type", &SDL_PenTouchEvent::type)
        .def_readwrite("reserved", &SDL_PenTouchEvent::reserved)
        .def_readwrite("timestamp", &SDL_PenTouchEvent::timestamp)
        .def_readwrite("window_id", &SDL_PenTouchEvent::windowID)
        .def_readwrite("which", &SDL_PenTouchEvent::which)
        .def_readwrite("pen_state", &SDL_PenTouchEvent::pen_state)
        .def_readwrite("x", &SDL_PenTouchEvent::x)
        .def_readwrite("y", &SDL_PenTouchEvent::y)
        .def_readwrite("eraser", &SDL_PenTouchEvent::eraser)
        .def_readwrite("down", &SDL_PenTouchEvent::down)
    ;

    py::class_<SDL_PenButtonEvent> _PenButtonEvent(_sdl, "PenButtonEvent");
    registry.on(_sdl, "PenButtonEvent", _PenButtonEvent);
        _PenButtonEvent
        .def_readwrite("type", &SDL_PenButtonEvent::type)
        .def_readwrite("reserved", &SDL_PenButtonEvent::reserved)
        .def_readwrite("timestamp", &SDL_PenButtonEvent::timestamp)
        .def_readwrite("window_id", &SDL_PenButtonEvent::windowID)
        .def_readwrite("which", &SDL_PenButtonEvent::which)
        .def_readwrite("pen_state", &SDL_PenButtonEvent::pen_state)
        .def_readwrite("x", &SDL_PenButtonEvent::x)
        .def_readwrite("y", &SDL_PenButtonEvent::y)
        .def_readwrite("button", &SDL_PenButtonEvent::button)
        .def_readwrite("down", &SDL_PenButtonEvent::down)
    ;

    py::class_<SDL_PenAxisEvent> _PenAxisEvent(_sdl, "PenAxisEvent");
    registry.on(_sdl, "PenAxisEvent", _PenAxisEvent);
        _PenAxisEvent
        .def_readwrite("type", &SDL_PenAxisEvent::type)
        .def_readwrite("reserved", &SDL_PenAxisEvent::reserved)
        .def_readwrite("timestamp", &SDL_PenAxisEvent::timestamp)
        .def_readwrite("window_id", &SDL_PenAxisEvent::windowID)
        .def_readwrite("which", &SDL_PenAxisEvent::which)
        .def_readwrite("pen_state", &SDL_PenAxisEvent::pen_state)
        .def_readwrite("x", &SDL_PenAxisEvent::x)
        .def_readwrite("y", &SDL_PenAxisEvent::y)
        .def_readwrite("axis", &SDL_PenAxisEvent::axis)
        .def_readwrite("value", &SDL_PenAxisEvent::value)
    ;

    py::class_<SDL_DropEvent> _DropEvent(_sdl, "DropEvent");
    registry.on(_sdl, "DropEvent", _DropEvent);
        _DropEvent
        .def_readwrite("type", &SDL_DropEvent::type)
        .def_readwrite("reserved", &SDL_DropEvent::reserved)
        .def_readwrite("timestamp", &SDL_DropEvent::timestamp)
        .def_readwrite("window_id", &SDL_DropEvent::windowID)
        .def_readwrite("x", &SDL_DropEvent::x)
        .def_readwrite("y", &SDL_DropEvent::y)
        .def_property("source",
            [](const SDL_DropEvent& self){ return self.source; },
            [](SDL_DropEvent& self, const char* source){ self.source = strdup(source); }
        )
        .def_property("data",
            [](const SDL_DropEvent& self){ return self.data; },
            [](SDL_DropEvent& self, const char* source){ self.data = strdup(source); }
        )
    ;

    py::class_<SDL_ClipboardEvent> _ClipboardEvent(_sdl, "ClipboardEvent");
    registry.on(_sdl, "ClipboardEvent", _ClipboardEvent);
        _ClipboardEvent
        .def_readwrite("type", &SDL_ClipboardEvent::type)
        .def_readwrite("reserved", &SDL_ClipboardEvent::reserved)
        .def_readwrite("timestamp", &SDL_ClipboardEvent::timestamp)
        .def_readwrite("owner", &SDL_ClipboardEvent::owner)
        .def_readwrite("num_mime_types", &SDL_ClipboardEvent::num_mime_types)
    ;

    py::class_<SDL_SensorEvent> _SensorEvent(_sdl, "SensorEvent");
    registry.on(_sdl, "SensorEvent", _SensorEvent);
        _SensorEvent
        .def_readwrite("type", &SDL_SensorEvent::type)
        .def_readwrite("reserved", &SDL_SensorEvent::reserved)
        .def_readwrite("timestamp", &SDL_SensorEvent::timestamp)
        .def_readwrite("which", &SDL_SensorEvent::which)
        .def_readonly("data", &SDL_SensorEvent::data)
        .def_readwrite("sensor_timestamp", &SDL_SensorEvent::sensor_timestamp)
    ;

    py::class_<SDL_QuitEvent> _QuitEvent(_sdl, "QuitEvent");
    registry.on(_sdl, "QuitEvent", _QuitEvent);
        _QuitEvent
        .def_readwrite("type", &SDL_QuitEvent::type)
        .def_readwrite("reserved", &SDL_QuitEvent::reserved)
        .def_readwrite("timestamp", &SDL_QuitEvent::timestamp)
    ;

    py::class_<SDL_UserEvent> _UserEvent(_sdl, "UserEvent");
    registry.on(_sdl, "UserEvent", _UserEvent);
        _UserEvent
        .def_readwrite("type", &SDL_UserEvent::type)
        .def_readwrite("reserved", &SDL_UserEvent::reserved)
        .def_readwrite("timestamp", &SDL_UserEvent::timestamp)
        .def_readwrite("window_id", &SDL_UserEvent::windowID)
        .def_readwrite("code", &SDL_UserEvent::code)
        .def_readwrite("data1", &SDL_UserEvent::data1)
        .def_readwrite("data2", &SDL_UserEvent::data2)
    ;

    _sdl
    .def("pump_events", &SDL_PumpEvents
        , py::return_value_policy::automatic_reference)
    ;

    py::enum_<SDL_EventAction>(_sdl, "EventAction", py::arithmetic())
        .value("ADDEVENT", SDL_EventAction::SDL_ADDEVENT)
        .value("PEEKEVENT", SDL_EventAction::SDL_PEEKEVENT)
        .value("GETEVENT", SDL_EventAction::SDL_GETEVENT)
        .export_values()
    ;
    _sdl
    .def("peep_events", &SDL_PeepEvents
        , py::arg("events")
        , py::arg("numevents")
        , py::arg("action")
        , py::arg("min_type")
        , py::arg("max_type")
        , py::return_value_policy::automatic_reference)
    .def("has_event", &SDL_HasEvent
        , py::arg("type")
        , py::return_value_policy::automatic_reference)
    .def("has_events", &SDL_HasEvents
        , py::arg("min_type")
        , py::arg("max_type")
        , py::return_value_policy::automatic_reference)
    .def("flush_event", &SDL_FlushEvent
        , py::arg("type")
        , py::return_value_policy::automatic_reference)
    .def("flush_events", &SDL_FlushEvents
        , py::arg("min_type")
        , py::arg("max_type")
        , py::return_value_policy::automatic_reference)
    .def("wait_event", &SDL_WaitEvent
        , py::arg("event")
        , py::return_value_policy::automatic_reference)
    .def("wait_event_timeout", &SDL_WaitEventTimeout
        , py::arg("event")
        , py::arg("timeout_ms")
        , py::return_value_policy::automatic_reference)
    .def("push_event", &SDL_PushEvent
        , py::arg("event")
        , py::return_value_policy::automatic_reference)
    .def("set_event_filter", &SDL_SetEventFilter
        , py::arg("filter")
        , py::arg("userdata")
        , py::return_value_policy::automatic_reference)
    .def("add_event_watch", &SDL_AddEventWatch
        , py::arg("filter")
        , py::arg("userdata")
        , py::return_value_policy::automatic_reference)
    .def("remove_event_watch", &SDL_RemoveEventWatch
        , py::arg("filter")
        , py::arg("userdata")
        , py::return_value_policy::automatic_reference)
    .def("filter_events", &SDL_FilterEvents
        , py::arg("filter")
        , py::arg("userdata")
        , py::return_value_policy::automatic_reference)
    .def("set_event_enabled", &SDL_SetEventEnabled
        , py::arg("type")
        , py::arg("enabled")
        , py::return_value_policy::automatic_reference)
    .def("event_enabled", &SDL_EventEnabled
        , py::arg("type")
        , py::return_value_policy::automatic_reference)
    .def("register_events", &SDL_RegisterEvents
        , py::arg("numevents")
        , py::return_value_policy::automatic_reference)
    .def("get_event_description", &SDL_GetEventDescription
        , py::arg("event")
        , py::arg("buf")
        , py::arg("buflen")
        , py::return_value_policy::automatic_reference)
    ;


}