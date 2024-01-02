#pragma once
#include <dawn/webgpu_cpp.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace pybind11 { namespace detail {

template <> struct type_caster<wgpu::Bool> {
public:
    PYBIND11_TYPE_CASTER(wgpu::Bool, _("Bool"));
    bool load(handle src, bool implicit) {
        //value.mValue = PyBool_Check(src.ptr());
        value = wgpu::Bool{static_cast<bool>(PyBool_Check(src.ptr()))};
        return !PyErr_Occurred();
    }
    static handle cast(wgpu::Bool src, return_value_policy, handle) {
        //return PyBool_FromLong(src.mValue);
        return PyBool_FromLong(src);
    }
};

}} // namespace pybind11::detail