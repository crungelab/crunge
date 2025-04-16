#pragma once
#include <dawn/webgpu_cpp.h>
//#include <wgpu.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace pybind11 { namespace detail {

template <> struct type_caster<wgpu::Bool> {
public:
    PYBIND11_TYPE_CASTER(wgpu::Bool, _("Bool"));
    bool load(handle src, bool implicit) {
        if (!PyBool_Check(src.ptr())) {
            return false;
        }
        value = wgpu::Bool{src.cast<bool>()};
        return true;
    }
    
    static handle cast(wgpu::Bool src, return_value_policy /* policy */, handle /* parent */) {
        return PyBool_FromLong(static_cast<long>(src));
    }
};

template <> struct type_caster<wgpu::OptionalBool> {
    public:
        PYBIND11_TYPE_CASTER(wgpu::OptionalBool, _("OptionalBool"));
        bool load(handle src, bool implicit) {
            if (!PyBool_Check(src.ptr())) {
                return false;
            }
            value = wgpu::OptionalBool{src.cast<bool>()};
            return true;
        }
        
        static handle cast(wgpu::OptionalBool src, return_value_policy /* policy */, handle /* parent */) {
            return PyBool_FromLong(static_cast<long>(src));
        }
    };
    
template <> struct type_caster<wgpu::StringView> {
    public:
        PYBIND11_TYPE_CASTER(wgpu::StringView, _("StringView"));
        bool load(handle src, bool implicit) {
            if (!PyUnicode_Check(src.ptr())) {
                return false;
            }
            value = wgpu::StringView{src.cast<std::string_view>()};
            return true;
        }
        
        static handle cast(wgpu::StringView src, return_value_policy /* policy */, handle /* parent */) {
            return PyUnicode_FromString(src.data);
        }
    };
    
}} // namespace pybind11::detail