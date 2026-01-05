#pragma once
//#include <dawn/webgpu_cpp.h>
//#include <wgpu.h>
#include <pybind11/pybind11.h>

#include <crunge/wgpu/pywgpu.h>
#include <crunge/wgpu/callbacks.h>


namespace py = pybind11;

namespace pybind11 { namespace detail {

template <> struct type_caster<pywgpu::Bool> {
public:
    PYBIND11_TYPE_CASTER(pywgpu::Bool, _("Bool"));
    bool load(handle src, bool implicit) {
        if (!PyBool_Check(src.ptr())) {
            return false;
        }
        value = pywgpu::Bool{src.cast<bool>()};
        return true;
    }
    
    static handle cast(pywgpu::Bool src, return_value_policy /* policy */, handle /* parent */) {
        return PyBool_FromLong(static_cast<long>(src));
    }
};

template <> struct type_caster<pywgpu::OptionalBool> {
    public:
        PYBIND11_TYPE_CASTER(pywgpu::OptionalBool, _("OptionalBool"));
        bool load(handle src, bool implicit) {
            if (!PyBool_Check(src.ptr())) {
                return false;
            }
            value = pywgpu::OptionalBool{src.cast<bool>()};
            return true;
        }
        
        static handle cast(pywgpu::OptionalBool src, return_value_policy /* policy */, handle /* parent */) {
            return PyBool_FromLong(static_cast<long>(src));
        }
    };
    
template <> struct type_caster<pywgpu::StringView> {
    public:
        PYBIND11_TYPE_CASTER(pywgpu::StringView, _("StringView"));
        bool load(handle src, bool implicit) {
            if (!PyUnicode_Check(src.ptr())) {
                return false;
            }
            value = pywgpu::StringView{src.cast<std::string_view>()};
            return true;
        }
        
        static handle cast(pywgpu::StringView src, return_value_policy /* policy */, handle /* parent */) {
            if (src.data == nullptr) {
                return py::none().inc_ref(); // return None instead of crashing
            }
            return PyUnicode_FromString(src.data);
        }
    };
    
template<>
    struct type_caster<pywgpu::RequestAdapterCallbackInfo> {
    public:
        PYBIND11_TYPE_CASTER(pywgpu::RequestAdapterCallbackInfo, _("RequestAdapterCallbackInfo"));
    
        // Python -> C++
        bool load(py::handle src, bool) {
            crunge_wgpu::PyRequestAdapterCallbackInfo* info = src.cast<crunge_wgpu::PyRequestAdapterCallbackInfo*>();
            if (info == nullptr) {
                return false;
            }
            value = *info;
            //std::cout << value.mode << std::endl;
    
            return true;
        }
    
        // C++ -> Python (not usually needed, but provided for completeness)
        static py::handle cast(const pywgpu::RequestAdapterCallbackInfo& src, py::return_value_policy, py::handle) {
            py::object py_mode = py::cast(src.mode);
            py::object py_callback = py::none(); // callbacks aren't typically convertible back to Python from native pointers
    
            py::object py_obj = py::module_::import("wgpu").attr("RequestAdapterCallbackInfo")(py_mode, py_callback);
            return py_obj.release();
        }
    };

template<>
    struct type_caster<pywgpu::DeviceLostCallbackInfo> {
    public:
        PYBIND11_TYPE_CASTER(pywgpu::DeviceLostCallbackInfo, _("DeviceLostCallbackInfo"));
    
        // Python -> C++
        bool load(py::handle src, bool) {
            crunge_wgpu::PyDeviceLostCallbackInfo* info = src.cast<crunge_wgpu::PyDeviceLostCallbackInfo*>();
            if (info == nullptr) {
                return false;
            }
            value = *info;
            //std::cout << value.mode << std::endl;
    
            return true;
        }
    
        // C++ -> Python (not usually needed, but provided for completeness)
        static py::handle cast(const pywgpu::DeviceLostCallbackInfo& src, py::return_value_policy, py::handle) {
            py::object py_mode = py::cast(src.mode);
            py::object py_callback = py::none(); // callbacks aren't typically convertible back to Python from native pointers
    
            py::object py_obj = py::module_::import("wgpu").attr("DeviceLostCallbackInfo")(py_mode, py_callback);
            return py_obj.release();
        }
    };

    template<>
    struct type_caster<pywgpu::UncapturedErrorCallbackInfo> {
    public:
        PYBIND11_TYPE_CASTER(pywgpu::UncapturedErrorCallbackInfo, _("UncapturedErrorCallbackInfo"));
    
        // Python -> C++
        bool load(py::handle src, bool) {
            crunge_wgpu::PyUncapturedErrorCallbackInfo* info = src.cast<crunge_wgpu::PyUncapturedErrorCallbackInfo*>();
            if (info == nullptr) {
                return false;
            }
            value = *info;
            //std::cout << value.mode << std::endl;
    
            return true;
        }
    
        // C++ -> Python (not usually needed, but provided for completeness)
        static py::handle cast(const pywgpu::UncapturedErrorCallbackInfo& src, py::return_value_policy, py::handle) {
            py::object py_callback = py::none(); // callbacks aren't typically convertible back to Python from native pointers
    
            py::object py_obj = py::module_::import("wgpu").attr("UncapturedErrorCallbackInfo")(py_callback);
            return py_obj.release();
        }
    };

    template<>
    struct type_caster<pywgpu::LoggingCallbackInfo> {
    public:
        PYBIND11_TYPE_CASTER(pywgpu::LoggingCallbackInfo, _("LoggingCallbackInfo"));
    
        // Python -> C++
        bool load(py::handle src, bool) {
            crunge_wgpu::PyLoggingCallbackInfo* info = src.cast<crunge_wgpu::PyLoggingCallbackInfo*>();
            if (info == nullptr) {
                return false;
            }
            value = *info;
            //std::cout << value.mode << std::endl;
    
            return true;
        }
    
        // C++ -> Python (not usually needed, but provided for completeness)
        static py::handle cast(const pywgpu::LoggingCallbackInfo& src, py::return_value_policy, py::handle) {
            py::object py_callback = py::none(); // callbacks aren't typically convertible back to Python from native pointers
    
            py::object py_obj = py::module_::import("wgpu").attr("LoggingCallbackInfo")(py_callback);
            return py_obj.release();
        }
    };

}} // namespace pybind11::detail