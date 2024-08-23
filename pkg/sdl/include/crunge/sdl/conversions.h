#include <pybind11/pybind11.h>


namespace py = pybind11;

namespace pybind11 { namespace detail {

/*struct SDL_Window;

class WindowHandle {
public:
    WindowHandle() = default;
    WindowHandle(SDL_Window* window) : window(window) {}
    SDL_Window* window;
};

template <> struct type_caster<WindowHandle> {
public:
    PYBIND11_TYPE_CASTER(WindowHandle, _("Window"));
    bool load(handle src, bool implicit) {
        //value = wgpu::Bool{static_cast<bool>(PyBool_Check(src.ptr()))};
        //value = SDL_Window{};
        value = WindowHandle{static_cast<void*>(src.ptr())};
        return !PyErr_Occurred();
    }
    static handle cast(void* src, return_value_policy, handle) {
        //return PyBool_FromLong(src);
        return PyCapsule_New(src, nullptr, nullptr);
    }
};*/

}} // namespace pybind11::detail