#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

#include <SDL3/SDL.h>
#include <iostream>

#include <cxbind/cxbind.h>
#include <crunge/sdl/conversions.h>

namespace py = pybind11;

void init_sdl_events(py::module &_sdl, Registry &registry) {
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
        .value("WINDOW_PEN_ENTER", SDL_EventType::SDL_EVENT_WINDOW_PEN_ENTER)
        .value("WINDOW_PEN_LEAVE", SDL_EventType::SDL_EVENT_WINDOW_PEN_LEAVE)
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
        .value("PEN_DOWN", SDL_EventType::SDL_EVENT_PEN_DOWN)
        .value("PEN_UP", SDL_EventType::SDL_EVENT_PEN_UP)
        .value("PEN_MOTION", SDL_EventType::SDL_EVENT_PEN_MOTION)
        .value("PEN_BUTTON_DOWN", SDL_EventType::SDL_EVENT_PEN_BUTTON_DOWN)
        .value("PEN_BUTTON_UP", SDL_EventType::SDL_EVENT_PEN_BUTTON_UP)
        .value("CAMERA_DEVICE_ADDED", SDL_EventType::SDL_EVENT_CAMERA_DEVICE_ADDED)
        .value("CAMERA_DEVICE_REMOVED", SDL_EventType::SDL_EVENT_CAMERA_DEVICE_REMOVED)
        .value("CAMERA_DEVICE_APPROVED", SDL_EventType::SDL_EVENT_CAMERA_DEVICE_APPROVED)
        .value("CAMERA_DEVICE_DENIED", SDL_EventType::SDL_EVENT_CAMERA_DEVICE_DENIED)
        .value("RENDER_TARGETS_RESET", SDL_EventType::SDL_EVENT_RENDER_TARGETS_RESET)
        .value("RENDER_DEVICE_RESET", SDL_EventType::SDL_EVENT_RENDER_DEVICE_RESET)
        .value("POLL_SENTINEL", SDL_EventType::SDL_EVENT_POLL_SENTINEL)
        .value("USER", SDL_EventType::SDL_EVENT_USER)
        .value("LAST", SDL_EventType::SDL_EVENT_LAST)
        .value("ENUM_PADDING", SDL_EventType::SDL_EVENT_ENUM_PADDING)
        .export_values();

    PYCLASS_BEGIN(_sdl, SDL_CommonEvent, CommonEvent)
        CommonEvent.def_readwrite("type", &SDL_CommonEvent::type);
        CommonEvent.def_readwrite("reserved", &SDL_CommonEvent::reserved);
        CommonEvent.def_readwrite("timestamp", &SDL_CommonEvent::timestamp);
    PYCLASS_END(_sdl, SDL_CommonEvent, CommonEvent)

    PYCLASS_BEGIN(_sdl, SDL_DisplayEvent, DisplayEvent)
        DisplayEvent.def_readwrite("type", &SDL_DisplayEvent::type);
        DisplayEvent.def_readwrite("reserved", &SDL_DisplayEvent::reserved);
        DisplayEvent.def_readwrite("timestamp", &SDL_DisplayEvent::timestamp);
        DisplayEvent.def_readwrite("display_id", &SDL_DisplayEvent::displayID);
        DisplayEvent.def_readwrite("data1", &SDL_DisplayEvent::data1);
        DisplayEvent.def_readwrite("data2", &SDL_DisplayEvent::data2);
    PYCLASS_END(_sdl, SDL_DisplayEvent, DisplayEvent)

    PYCLASS_BEGIN(_sdl, SDL_WindowEvent, WindowEvent)
        WindowEvent.def_readwrite("type", &SDL_WindowEvent::type);
        WindowEvent.def_readwrite("reserved", &SDL_WindowEvent::reserved);
        WindowEvent.def_readwrite("timestamp", &SDL_WindowEvent::timestamp);
        WindowEvent.def_readwrite("window_id", &SDL_WindowEvent::windowID);
        WindowEvent.def_readwrite("data1", &SDL_WindowEvent::data1);
        WindowEvent.def_readwrite("data2", &SDL_WindowEvent::data2);
    PYCLASS_END(_sdl, SDL_WindowEvent, WindowEvent)

    PYCLASS_BEGIN(_sdl, SDL_KeyboardDeviceEvent, KeyboardDeviceEvent)
        KeyboardDeviceEvent.def_readwrite("type", &SDL_KeyboardDeviceEvent::type);
        KeyboardDeviceEvent.def_readwrite("reserved", &SDL_KeyboardDeviceEvent::reserved);
        KeyboardDeviceEvent.def_readwrite("timestamp", &SDL_KeyboardDeviceEvent::timestamp);
        KeyboardDeviceEvent.def_readwrite("which", &SDL_KeyboardDeviceEvent::which);
    PYCLASS_END(_sdl, SDL_KeyboardDeviceEvent, KeyboardDeviceEvent)

    PYCLASS_BEGIN(_sdl, SDL_KeyboardEvent, KeyboardEvent)
        KeyboardEvent.def_readwrite("type", &SDL_KeyboardEvent::type);
        KeyboardEvent.def_readwrite("reserved", &SDL_KeyboardEvent::reserved);
        KeyboardEvent.def_readwrite("timestamp", &SDL_KeyboardEvent::timestamp);
        KeyboardEvent.def_readwrite("window_id", &SDL_KeyboardEvent::windowID);
        KeyboardEvent.def_readwrite("which", &SDL_KeyboardEvent::which);
        KeyboardEvent.def_readwrite("scancode", &SDL_KeyboardEvent::scancode);
        KeyboardEvent.def_readwrite("key", &SDL_KeyboardEvent::key);
        KeyboardEvent.def_readwrite("mod", &SDL_KeyboardEvent::mod);
        KeyboardEvent.def_readwrite("raw", &SDL_KeyboardEvent::raw);
        KeyboardEvent.def_readwrite("state", &SDL_KeyboardEvent::state);
        KeyboardEvent.def_readwrite("repeat", &SDL_KeyboardEvent::repeat);
    PYCLASS_END(_sdl, SDL_KeyboardEvent, KeyboardEvent)

    PYCLASS_BEGIN(_sdl, SDL_TextEditingEvent, TextEditingEvent)
        TextEditingEvent.def_readwrite("type", &SDL_TextEditingEvent::type);
        TextEditingEvent.def_readwrite("reserved", &SDL_TextEditingEvent::reserved);
        TextEditingEvent.def_readwrite("timestamp", &SDL_TextEditingEvent::timestamp);
        TextEditingEvent.def_readwrite("window_id", &SDL_TextEditingEvent::windowID);
        TextEditingEvent.def_property("text",
            [](const SDL_TextEditingEvent& self){ return self.text; },
            [](SDL_TextEditingEvent& self, const char* source){ self.text = strdup(source); }
        );
        TextEditingEvent.def_readwrite("start", &SDL_TextEditingEvent::start);
        TextEditingEvent.def_readwrite("length", &SDL_TextEditingEvent::length);
    PYCLASS_END(_sdl, SDL_TextEditingEvent, TextEditingEvent)

    PYCLASS_BEGIN(_sdl, SDL_TextEditingCandidatesEvent, TextEditingCandidatesEvent)
        TextEditingCandidatesEvent.def_readwrite("type", &SDL_TextEditingCandidatesEvent::type);
        TextEditingCandidatesEvent.def_readwrite("reserved", &SDL_TextEditingCandidatesEvent::reserved);
        TextEditingCandidatesEvent.def_readwrite("timestamp", &SDL_TextEditingCandidatesEvent::timestamp);
        TextEditingCandidatesEvent.def_readwrite("window_id", &SDL_TextEditingCandidatesEvent::windowID);
        TextEditingCandidatesEvent.def_readwrite("num_candidates", &SDL_TextEditingCandidatesEvent::num_candidates);
        TextEditingCandidatesEvent.def_readwrite("selected_candidate", &SDL_TextEditingCandidatesEvent::selected_candidate);
        TextEditingCandidatesEvent.def_readwrite("horizontal", &SDL_TextEditingCandidatesEvent::horizontal);
    PYCLASS_END(_sdl, SDL_TextEditingCandidatesEvent, TextEditingCandidatesEvent)

    PYCLASS_BEGIN(_sdl, SDL_TextInputEvent, TextInputEvent)
        TextInputEvent.def_readwrite("type", &SDL_TextInputEvent::type);
        TextInputEvent.def_readwrite("reserved", &SDL_TextInputEvent::reserved);
        TextInputEvent.def_readwrite("timestamp", &SDL_TextInputEvent::timestamp);
        TextInputEvent.def_readwrite("window_id", &SDL_TextInputEvent::windowID);
        TextInputEvent.def_property("text",
            [](const SDL_TextInputEvent& self){ return self.text; },
            [](SDL_TextInputEvent& self, const char* source){ self.text = strdup(source); }
        );
    PYCLASS_END(_sdl, SDL_TextInputEvent, TextInputEvent)

    PYCLASS_BEGIN(_sdl, SDL_MouseDeviceEvent, MouseDeviceEvent)
        MouseDeviceEvent.def_readwrite("type", &SDL_MouseDeviceEvent::type);
        MouseDeviceEvent.def_readwrite("reserved", &SDL_MouseDeviceEvent::reserved);
        MouseDeviceEvent.def_readwrite("timestamp", &SDL_MouseDeviceEvent::timestamp);
        MouseDeviceEvent.def_readwrite("which", &SDL_MouseDeviceEvent::which);
    PYCLASS_END(_sdl, SDL_MouseDeviceEvent, MouseDeviceEvent)

    PYCLASS_BEGIN(_sdl, SDL_MouseMotionEvent, MouseMotionEvent)
        MouseMotionEvent.def_readwrite("type", &SDL_MouseMotionEvent::type);
        MouseMotionEvent.def_readwrite("reserved", &SDL_MouseMotionEvent::reserved);
        MouseMotionEvent.def_readwrite("timestamp", &SDL_MouseMotionEvent::timestamp);
        MouseMotionEvent.def_readwrite("window_id", &SDL_MouseMotionEvent::windowID);
        MouseMotionEvent.def_readwrite("which", &SDL_MouseMotionEvent::which);
        MouseMotionEvent.def_readwrite("state", &SDL_MouseMotionEvent::state);
        MouseMotionEvent.def_readwrite("x", &SDL_MouseMotionEvent::x);
        MouseMotionEvent.def_readwrite("y", &SDL_MouseMotionEvent::y);
        MouseMotionEvent.def_readwrite("xrel", &SDL_MouseMotionEvent::xrel);
        MouseMotionEvent.def_readwrite("yrel", &SDL_MouseMotionEvent::yrel);
    PYCLASS_END(_sdl, SDL_MouseMotionEvent, MouseMotionEvent)

    PYCLASS_BEGIN(_sdl, SDL_MouseButtonEvent, MouseButtonEvent)
        MouseButtonEvent.def_readwrite("type", &SDL_MouseButtonEvent::type);
        MouseButtonEvent.def_readwrite("reserved", &SDL_MouseButtonEvent::reserved);
        MouseButtonEvent.def_readwrite("timestamp", &SDL_MouseButtonEvent::timestamp);
        MouseButtonEvent.def_readwrite("window_id", &SDL_MouseButtonEvent::windowID);
        MouseButtonEvent.def_readwrite("which", &SDL_MouseButtonEvent::which);
        MouseButtonEvent.def_readwrite("button", &SDL_MouseButtonEvent::button);
        MouseButtonEvent.def_readwrite("state", &SDL_MouseButtonEvent::state);
        MouseButtonEvent.def_readwrite("clicks", &SDL_MouseButtonEvent::clicks);
        MouseButtonEvent.def_readwrite("padding", &SDL_MouseButtonEvent::padding);
        MouseButtonEvent.def_readwrite("x", &SDL_MouseButtonEvent::x);
        MouseButtonEvent.def_readwrite("y", &SDL_MouseButtonEvent::y);
    PYCLASS_END(_sdl, SDL_MouseButtonEvent, MouseButtonEvent)

    PYCLASS_BEGIN(_sdl, SDL_MouseWheelEvent, MouseWheelEvent)
        MouseWheelEvent.def_readwrite("type", &SDL_MouseWheelEvent::type);
        MouseWheelEvent.def_readwrite("reserved", &SDL_MouseWheelEvent::reserved);
        MouseWheelEvent.def_readwrite("timestamp", &SDL_MouseWheelEvent::timestamp);
        MouseWheelEvent.def_readwrite("window_id", &SDL_MouseWheelEvent::windowID);
        MouseWheelEvent.def_readwrite("which", &SDL_MouseWheelEvent::which);
        MouseWheelEvent.def_readwrite("x", &SDL_MouseWheelEvent::x);
        MouseWheelEvent.def_readwrite("y", &SDL_MouseWheelEvent::y);
        MouseWheelEvent.def_readwrite("direction", &SDL_MouseWheelEvent::direction);
        MouseWheelEvent.def_readwrite("mouse_x", &SDL_MouseWheelEvent::mouse_x);
        MouseWheelEvent.def_readwrite("mouse_y", &SDL_MouseWheelEvent::mouse_y);
    PYCLASS_END(_sdl, SDL_MouseWheelEvent, MouseWheelEvent)

    PYCLASS_BEGIN(_sdl, SDL_JoyAxisEvent, JoyAxisEvent)
        JoyAxisEvent.def_readwrite("type", &SDL_JoyAxisEvent::type);
        JoyAxisEvent.def_readwrite("reserved", &SDL_JoyAxisEvent::reserved);
        JoyAxisEvent.def_readwrite("timestamp", &SDL_JoyAxisEvent::timestamp);
        JoyAxisEvent.def_readwrite("which", &SDL_JoyAxisEvent::which);
        JoyAxisEvent.def_readwrite("axis", &SDL_JoyAxisEvent::axis);
        JoyAxisEvent.def_readwrite("padding1", &SDL_JoyAxisEvent::padding1);
        JoyAxisEvent.def_readwrite("padding2", &SDL_JoyAxisEvent::padding2);
        JoyAxisEvent.def_readwrite("padding3", &SDL_JoyAxisEvent::padding3);
        JoyAxisEvent.def_readwrite("value", &SDL_JoyAxisEvent::value);
        JoyAxisEvent.def_readwrite("padding4", &SDL_JoyAxisEvent::padding4);
    PYCLASS_END(_sdl, SDL_JoyAxisEvent, JoyAxisEvent)

    PYCLASS_BEGIN(_sdl, SDL_JoyBallEvent, JoyBallEvent)
        JoyBallEvent.def_readwrite("type", &SDL_JoyBallEvent::type);
        JoyBallEvent.def_readwrite("reserved", &SDL_JoyBallEvent::reserved);
        JoyBallEvent.def_readwrite("timestamp", &SDL_JoyBallEvent::timestamp);
        JoyBallEvent.def_readwrite("which", &SDL_JoyBallEvent::which);
        JoyBallEvent.def_readwrite("ball", &SDL_JoyBallEvent::ball);
        JoyBallEvent.def_readwrite("padding1", &SDL_JoyBallEvent::padding1);
        JoyBallEvent.def_readwrite("padding2", &SDL_JoyBallEvent::padding2);
        JoyBallEvent.def_readwrite("padding3", &SDL_JoyBallEvent::padding3);
        JoyBallEvent.def_readwrite("xrel", &SDL_JoyBallEvent::xrel);
        JoyBallEvent.def_readwrite("yrel", &SDL_JoyBallEvent::yrel);
    PYCLASS_END(_sdl, SDL_JoyBallEvent, JoyBallEvent)

    PYCLASS_BEGIN(_sdl, SDL_JoyHatEvent, JoyHatEvent)
        JoyHatEvent.def_readwrite("type", &SDL_JoyHatEvent::type);
        JoyHatEvent.def_readwrite("reserved", &SDL_JoyHatEvent::reserved);
        JoyHatEvent.def_readwrite("timestamp", &SDL_JoyHatEvent::timestamp);
        JoyHatEvent.def_readwrite("which", &SDL_JoyHatEvent::which);
        JoyHatEvent.def_readwrite("hat", &SDL_JoyHatEvent::hat);
        JoyHatEvent.def_readwrite("value", &SDL_JoyHatEvent::value);
        JoyHatEvent.def_readwrite("padding1", &SDL_JoyHatEvent::padding1);
        JoyHatEvent.def_readwrite("padding2", &SDL_JoyHatEvent::padding2);
    PYCLASS_END(_sdl, SDL_JoyHatEvent, JoyHatEvent)

    PYCLASS_BEGIN(_sdl, SDL_JoyButtonEvent, JoyButtonEvent)
        JoyButtonEvent.def_readwrite("type", &SDL_JoyButtonEvent::type);
        JoyButtonEvent.def_readwrite("reserved", &SDL_JoyButtonEvent::reserved);
        JoyButtonEvent.def_readwrite("timestamp", &SDL_JoyButtonEvent::timestamp);
        JoyButtonEvent.def_readwrite("which", &SDL_JoyButtonEvent::which);
        JoyButtonEvent.def_readwrite("button", &SDL_JoyButtonEvent::button);
        JoyButtonEvent.def_readwrite("state", &SDL_JoyButtonEvent::state);
        JoyButtonEvent.def_readwrite("padding1", &SDL_JoyButtonEvent::padding1);
        JoyButtonEvent.def_readwrite("padding2", &SDL_JoyButtonEvent::padding2);
    PYCLASS_END(_sdl, SDL_JoyButtonEvent, JoyButtonEvent)

    PYCLASS_BEGIN(_sdl, SDL_JoyDeviceEvent, JoyDeviceEvent)
        JoyDeviceEvent.def_readwrite("type", &SDL_JoyDeviceEvent::type);
        JoyDeviceEvent.def_readwrite("reserved", &SDL_JoyDeviceEvent::reserved);
        JoyDeviceEvent.def_readwrite("timestamp", &SDL_JoyDeviceEvent::timestamp);
        JoyDeviceEvent.def_readwrite("which", &SDL_JoyDeviceEvent::which);
    PYCLASS_END(_sdl, SDL_JoyDeviceEvent, JoyDeviceEvent)

    PYCLASS_BEGIN(_sdl, SDL_JoyBatteryEvent, JoyBatteryEvent)
        JoyBatteryEvent.def_readwrite("type", &SDL_JoyBatteryEvent::type);
        JoyBatteryEvent.def_readwrite("reserved", &SDL_JoyBatteryEvent::reserved);
        JoyBatteryEvent.def_readwrite("timestamp", &SDL_JoyBatteryEvent::timestamp);
        JoyBatteryEvent.def_readwrite("which", &SDL_JoyBatteryEvent::which);
        JoyBatteryEvent.def_readwrite("state", &SDL_JoyBatteryEvent::state);
        JoyBatteryEvent.def_readwrite("percent", &SDL_JoyBatteryEvent::percent);
    PYCLASS_END(_sdl, SDL_JoyBatteryEvent, JoyBatteryEvent)

    PYCLASS_BEGIN(_sdl, SDL_GamepadAxisEvent, GamepadAxisEvent)
        GamepadAxisEvent.def_readwrite("type", &SDL_GamepadAxisEvent::type);
        GamepadAxisEvent.def_readwrite("reserved", &SDL_GamepadAxisEvent::reserved);
        GamepadAxisEvent.def_readwrite("timestamp", &SDL_GamepadAxisEvent::timestamp);
        GamepadAxisEvent.def_readwrite("which", &SDL_GamepadAxisEvent::which);
        GamepadAxisEvent.def_readwrite("axis", &SDL_GamepadAxisEvent::axis);
        GamepadAxisEvent.def_readwrite("padding1", &SDL_GamepadAxisEvent::padding1);
        GamepadAxisEvent.def_readwrite("padding2", &SDL_GamepadAxisEvent::padding2);
        GamepadAxisEvent.def_readwrite("padding3", &SDL_GamepadAxisEvent::padding3);
        GamepadAxisEvent.def_readwrite("value", &SDL_GamepadAxisEvent::value);
        GamepadAxisEvent.def_readwrite("padding4", &SDL_GamepadAxisEvent::padding4);
    PYCLASS_END(_sdl, SDL_GamepadAxisEvent, GamepadAxisEvent)

    PYCLASS_BEGIN(_sdl, SDL_GamepadButtonEvent, GamepadButtonEvent)
        GamepadButtonEvent.def_readwrite("type", &SDL_GamepadButtonEvent::type);
        GamepadButtonEvent.def_readwrite("reserved", &SDL_GamepadButtonEvent::reserved);
        GamepadButtonEvent.def_readwrite("timestamp", &SDL_GamepadButtonEvent::timestamp);
        GamepadButtonEvent.def_readwrite("which", &SDL_GamepadButtonEvent::which);
        GamepadButtonEvent.def_readwrite("button", &SDL_GamepadButtonEvent::button);
        GamepadButtonEvent.def_readwrite("state", &SDL_GamepadButtonEvent::state);
        GamepadButtonEvent.def_readwrite("padding1", &SDL_GamepadButtonEvent::padding1);
        GamepadButtonEvent.def_readwrite("padding2", &SDL_GamepadButtonEvent::padding2);
    PYCLASS_END(_sdl, SDL_GamepadButtonEvent, GamepadButtonEvent)

    PYCLASS_BEGIN(_sdl, SDL_GamepadDeviceEvent, GamepadDeviceEvent)
        GamepadDeviceEvent.def_readwrite("type", &SDL_GamepadDeviceEvent::type);
        GamepadDeviceEvent.def_readwrite("reserved", &SDL_GamepadDeviceEvent::reserved);
        GamepadDeviceEvent.def_readwrite("timestamp", &SDL_GamepadDeviceEvent::timestamp);
        GamepadDeviceEvent.def_readwrite("which", &SDL_GamepadDeviceEvent::which);
    PYCLASS_END(_sdl, SDL_GamepadDeviceEvent, GamepadDeviceEvent)

    PYCLASS_BEGIN(_sdl, SDL_GamepadTouchpadEvent, GamepadTouchpadEvent)
        GamepadTouchpadEvent.def_readwrite("type", &SDL_GamepadTouchpadEvent::type);
        GamepadTouchpadEvent.def_readwrite("reserved", &SDL_GamepadTouchpadEvent::reserved);
        GamepadTouchpadEvent.def_readwrite("timestamp", &SDL_GamepadTouchpadEvent::timestamp);
        GamepadTouchpadEvent.def_readwrite("which", &SDL_GamepadTouchpadEvent::which);
        GamepadTouchpadEvent.def_readwrite("touchpad", &SDL_GamepadTouchpadEvent::touchpad);
        GamepadTouchpadEvent.def_readwrite("finger", &SDL_GamepadTouchpadEvent::finger);
        GamepadTouchpadEvent.def_readwrite("x", &SDL_GamepadTouchpadEvent::x);
        GamepadTouchpadEvent.def_readwrite("y", &SDL_GamepadTouchpadEvent::y);
        GamepadTouchpadEvent.def_readwrite("pressure", &SDL_GamepadTouchpadEvent::pressure);
    PYCLASS_END(_sdl, SDL_GamepadTouchpadEvent, GamepadTouchpadEvent)

    PYCLASS_BEGIN(_sdl, SDL_GamepadSensorEvent, GamepadSensorEvent)
        GamepadSensorEvent.def_readwrite("type", &SDL_GamepadSensorEvent::type);
        GamepadSensorEvent.def_readwrite("reserved", &SDL_GamepadSensorEvent::reserved);
        GamepadSensorEvent.def_readwrite("timestamp", &SDL_GamepadSensorEvent::timestamp);
        GamepadSensorEvent.def_readwrite("which", &SDL_GamepadSensorEvent::which);
        GamepadSensorEvent.def_readwrite("sensor", &SDL_GamepadSensorEvent::sensor);
        GamepadSensorEvent.def_readonly("data", &SDL_GamepadSensorEvent::data);
        GamepadSensorEvent.def_readwrite("sensor_timestamp", &SDL_GamepadSensorEvent::sensor_timestamp);
    PYCLASS_END(_sdl, SDL_GamepadSensorEvent, GamepadSensorEvent)

    PYCLASS_BEGIN(_sdl, SDL_AudioDeviceEvent, AudioDeviceEvent)
        AudioDeviceEvent.def_readwrite("type", &SDL_AudioDeviceEvent::type);
        AudioDeviceEvent.def_readwrite("reserved", &SDL_AudioDeviceEvent::reserved);
        AudioDeviceEvent.def_readwrite("timestamp", &SDL_AudioDeviceEvent::timestamp);
        AudioDeviceEvent.def_readwrite("which", &SDL_AudioDeviceEvent::which);
        AudioDeviceEvent.def_readwrite("recording", &SDL_AudioDeviceEvent::recording);
        AudioDeviceEvent.def_readwrite("padding1", &SDL_AudioDeviceEvent::padding1);
        AudioDeviceEvent.def_readwrite("padding2", &SDL_AudioDeviceEvent::padding2);
        AudioDeviceEvent.def_readwrite("padding3", &SDL_AudioDeviceEvent::padding3);
    PYCLASS_END(_sdl, SDL_AudioDeviceEvent, AudioDeviceEvent)

    PYCLASS_BEGIN(_sdl, SDL_CameraDeviceEvent, CameraDeviceEvent)
        CameraDeviceEvent.def_readwrite("type", &SDL_CameraDeviceEvent::type);
        CameraDeviceEvent.def_readwrite("reserved", &SDL_CameraDeviceEvent::reserved);
        CameraDeviceEvent.def_readwrite("timestamp", &SDL_CameraDeviceEvent::timestamp);
        CameraDeviceEvent.def_readwrite("which", &SDL_CameraDeviceEvent::which);
    PYCLASS_END(_sdl, SDL_CameraDeviceEvent, CameraDeviceEvent)

    PYCLASS_BEGIN(_sdl, SDL_TouchFingerEvent, TouchFingerEvent)
        TouchFingerEvent.def_readwrite("type", &SDL_TouchFingerEvent::type);
        TouchFingerEvent.def_readwrite("reserved", &SDL_TouchFingerEvent::reserved);
        TouchFingerEvent.def_readwrite("timestamp", &SDL_TouchFingerEvent::timestamp);
        TouchFingerEvent.def_readwrite("touch_id", &SDL_TouchFingerEvent::touchID);
        TouchFingerEvent.def_readwrite("finger_id", &SDL_TouchFingerEvent::fingerID);
        TouchFingerEvent.def_readwrite("x", &SDL_TouchFingerEvent::x);
        TouchFingerEvent.def_readwrite("y", &SDL_TouchFingerEvent::y);
        TouchFingerEvent.def_readwrite("dx", &SDL_TouchFingerEvent::dx);
        TouchFingerEvent.def_readwrite("dy", &SDL_TouchFingerEvent::dy);
        TouchFingerEvent.def_readwrite("pressure", &SDL_TouchFingerEvent::pressure);
        TouchFingerEvent.def_readwrite("window_id", &SDL_TouchFingerEvent::windowID);
    PYCLASS_END(_sdl, SDL_TouchFingerEvent, TouchFingerEvent)

    PYCLASS_BEGIN(_sdl, SDL_PenTipEvent, PenTipEvent)
        PenTipEvent.def_readwrite("type", &SDL_PenTipEvent::type);
        PenTipEvent.def_readwrite("reserved", &SDL_PenTipEvent::reserved);
        PenTipEvent.def_readwrite("timestamp", &SDL_PenTipEvent::timestamp);
        PenTipEvent.def_readwrite("window_id", &SDL_PenTipEvent::windowID);
        PenTipEvent.def_readwrite("which", &SDL_PenTipEvent::which);
        PenTipEvent.def_readwrite("tip", &SDL_PenTipEvent::tip);
        PenTipEvent.def_readwrite("state", &SDL_PenTipEvent::state);
        PenTipEvent.def_readwrite("pen_state", &SDL_PenTipEvent::pen_state);
        PenTipEvent.def_readwrite("x", &SDL_PenTipEvent::x);
        PenTipEvent.def_readwrite("y", &SDL_PenTipEvent::y);
        PenTipEvent.def_readonly("axes", &SDL_PenTipEvent::axes);
    PYCLASS_END(_sdl, SDL_PenTipEvent, PenTipEvent)

    PYCLASS_BEGIN(_sdl, SDL_PenMotionEvent, PenMotionEvent)
        PenMotionEvent.def_readwrite("type", &SDL_PenMotionEvent::type);
        PenMotionEvent.def_readwrite("reserved", &SDL_PenMotionEvent::reserved);
        PenMotionEvent.def_readwrite("timestamp", &SDL_PenMotionEvent::timestamp);
        PenMotionEvent.def_readwrite("window_id", &SDL_PenMotionEvent::windowID);
        PenMotionEvent.def_readwrite("which", &SDL_PenMotionEvent::which);
        PenMotionEvent.def_readwrite("padding1", &SDL_PenMotionEvent::padding1);
        PenMotionEvent.def_readwrite("padding2", &SDL_PenMotionEvent::padding2);
        PenMotionEvent.def_readwrite("pen_state", &SDL_PenMotionEvent::pen_state);
        PenMotionEvent.def_readwrite("x", &SDL_PenMotionEvent::x);
        PenMotionEvent.def_readwrite("y", &SDL_PenMotionEvent::y);
        PenMotionEvent.def_readonly("axes", &SDL_PenMotionEvent::axes);
    PYCLASS_END(_sdl, SDL_PenMotionEvent, PenMotionEvent)

    PYCLASS_BEGIN(_sdl, SDL_PenButtonEvent, PenButtonEvent)
        PenButtonEvent.def_readwrite("type", &SDL_PenButtonEvent::type);
        PenButtonEvent.def_readwrite("reserved", &SDL_PenButtonEvent::reserved);
        PenButtonEvent.def_readwrite("timestamp", &SDL_PenButtonEvent::timestamp);
        PenButtonEvent.def_readwrite("window_id", &SDL_PenButtonEvent::windowID);
        PenButtonEvent.def_readwrite("which", &SDL_PenButtonEvent::which);
        PenButtonEvent.def_readwrite("button", &SDL_PenButtonEvent::button);
        PenButtonEvent.def_readwrite("state", &SDL_PenButtonEvent::state);
        PenButtonEvent.def_readwrite("pen_state", &SDL_PenButtonEvent::pen_state);
        PenButtonEvent.def_readwrite("x", &SDL_PenButtonEvent::x);
        PenButtonEvent.def_readwrite("y", &SDL_PenButtonEvent::y);
        PenButtonEvent.def_readonly("axes", &SDL_PenButtonEvent::axes);
    PYCLASS_END(_sdl, SDL_PenButtonEvent, PenButtonEvent)

    PYCLASS_BEGIN(_sdl, SDL_DropEvent, DropEvent)
        DropEvent.def_readwrite("type", &SDL_DropEvent::type);
        DropEvent.def_readwrite("reserved", &SDL_DropEvent::reserved);
        DropEvent.def_readwrite("timestamp", &SDL_DropEvent::timestamp);
        DropEvent.def_readwrite("window_id", &SDL_DropEvent::windowID);
        DropEvent.def_readwrite("x", &SDL_DropEvent::x);
        DropEvent.def_readwrite("y", &SDL_DropEvent::y);
        DropEvent.def_property("source",
            [](const SDL_DropEvent& self){ return self.source; },
            [](SDL_DropEvent& self, const char* source){ self.source = strdup(source); }
        );
        DropEvent.def_property("data",
            [](const SDL_DropEvent& self){ return self.data; },
            [](SDL_DropEvent& self, const char* source){ self.data = strdup(source); }
        );
    PYCLASS_END(_sdl, SDL_DropEvent, DropEvent)

    PYCLASS_BEGIN(_sdl, SDL_ClipboardEvent, ClipboardEvent)
        ClipboardEvent.def_readwrite("type", &SDL_ClipboardEvent::type);
        ClipboardEvent.def_readwrite("reserved", &SDL_ClipboardEvent::reserved);
        ClipboardEvent.def_readwrite("timestamp", &SDL_ClipboardEvent::timestamp);
    PYCLASS_END(_sdl, SDL_ClipboardEvent, ClipboardEvent)

    PYCLASS_BEGIN(_sdl, SDL_SensorEvent, SensorEvent)
        SensorEvent.def_readwrite("type", &SDL_SensorEvent::type);
        SensorEvent.def_readwrite("reserved", &SDL_SensorEvent::reserved);
        SensorEvent.def_readwrite("timestamp", &SDL_SensorEvent::timestamp);
        SensorEvent.def_readwrite("which", &SDL_SensorEvent::which);
        SensorEvent.def_readonly("data", &SDL_SensorEvent::data);
        SensorEvent.def_readwrite("sensor_timestamp", &SDL_SensorEvent::sensor_timestamp);
    PYCLASS_END(_sdl, SDL_SensorEvent, SensorEvent)

    PYCLASS_BEGIN(_sdl, SDL_QuitEvent, QuitEvent)
        QuitEvent.def_readwrite("type", &SDL_QuitEvent::type);
        QuitEvent.def_readwrite("reserved", &SDL_QuitEvent::reserved);
        QuitEvent.def_readwrite("timestamp", &SDL_QuitEvent::timestamp);
    PYCLASS_END(_sdl, SDL_QuitEvent, QuitEvent)

    PYCLASS_BEGIN(_sdl, SDL_UserEvent, UserEvent)
        UserEvent.def_readwrite("type", &SDL_UserEvent::type);
        UserEvent.def_readwrite("reserved", &SDL_UserEvent::reserved);
        UserEvent.def_readwrite("timestamp", &SDL_UserEvent::timestamp);
        UserEvent.def_readwrite("window_id", &SDL_UserEvent::windowID);
        UserEvent.def_readwrite("code", &SDL_UserEvent::code);
        UserEvent.def_readwrite("data1", &SDL_UserEvent::data1);
        UserEvent.def_readwrite("data2", &SDL_UserEvent::data2);
    PYCLASS_END(_sdl, SDL_UserEvent, UserEvent)

    _sdl.def("pump_events", &SDL_PumpEvents
    , py::return_value_policy::automatic_reference);

    py::enum_<SDL_EventAction>(_sdl, "EventAction", py::arithmetic())
        .value("ADDEVENT", SDL_EventAction::SDL_ADDEVENT)
        .value("PEEKEVENT", SDL_EventAction::SDL_PEEKEVENT)
        .value("GETEVENT", SDL_EventAction::SDL_GETEVENT)
        .export_values();

    _sdl.def("peep_events", &SDL_PeepEvents
    , py::arg("events")
    , py::arg("numevents")
    , py::arg("action")
    , py::arg("min_type")
    , py::arg("max_type")
    , py::return_value_policy::automatic_reference);

    _sdl.def("has_event", &SDL_HasEvent
    , py::arg("type")
    , py::return_value_policy::automatic_reference);

    _sdl.def("has_events", &SDL_HasEvents
    , py::arg("min_type")
    , py::arg("max_type")
    , py::return_value_policy::automatic_reference);

    _sdl.def("flush_event", &SDL_FlushEvent
    , py::arg("type")
    , py::return_value_policy::automatic_reference);

    _sdl.def("flush_events", &SDL_FlushEvents
    , py::arg("min_type")
    , py::arg("max_type")
    , py::return_value_policy::automatic_reference);

    _sdl.def("wait_event", &SDL_WaitEvent
    , py::arg("event")
    , py::return_value_policy::automatic_reference);

    _sdl.def("wait_event_timeout", &SDL_WaitEventTimeout
    , py::arg("event")
    , py::arg("timeout_ms")
    , py::return_value_policy::automatic_reference);

    _sdl.def("push_event", &SDL_PushEvent
    , py::arg("event")
    , py::return_value_policy::automatic_reference);

    _sdl.def("set_event_filter", &SDL_SetEventFilter
    , py::arg("filter")
    , py::arg("userdata")
    , py::return_value_policy::automatic_reference);

    _sdl.def("add_event_watch", &SDL_AddEventWatch
    , py::arg("filter")
    , py::arg("userdata")
    , py::return_value_policy::automatic_reference);

    _sdl.def("del_event_watch", &SDL_DelEventWatch
    , py::arg("filter")
    , py::arg("userdata")
    , py::return_value_policy::automatic_reference);

    _sdl.def("filter_events", &SDL_FilterEvents
    , py::arg("filter")
    , py::arg("userdata")
    , py::return_value_policy::automatic_reference);

    _sdl.def("set_event_enabled", &SDL_SetEventEnabled
    , py::arg("type")
    , py::arg("enabled")
    , py::return_value_policy::automatic_reference);

    _sdl.def("event_enabled", &SDL_EventEnabled
    , py::arg("type")
    , py::return_value_policy::automatic_reference);

    _sdl.def("register_events", &SDL_RegisterEvents
    , py::arg("numevents")
    , py::return_value_policy::automatic_reference);


}