#pragma once
#include <dawn/webgpu_cpp.h>
//#include <wgpu.h>
#include <pybind11/pybind11.h>

#include <crunge/wgpu/callbacks.h>


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
    
    template<>
    struct type_caster<wgpu::DeviceLostCallbackInfo> {
    public:
        PYBIND11_TYPE_CASTER(wgpu::DeviceLostCallbackInfo, _("DeviceLostCallbackInfo"));
    
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
        static py::handle cast(const wgpu::DeviceLostCallbackInfo& src, py::return_value_policy, py::handle) {
            py::object py_mode = py::cast(src.mode);
            py::object py_callback = py::none(); // callbacks aren't typically convertible back to Python from native pointers
    
            py::object py_obj = py::module_::import("wgpu").attr("DeviceLostCallbackInfo")(py_mode, py_callback);
            return py_obj.release();
        }
    };

    /*
    template<>
    struct type_caster<wgpu::DeviceLostCallbackInfo> {
    public:
        PYBIND11_TYPE_CASTER(wgpu::DeviceLostCallbackInfo, _("DeviceLostCallbackInfo"));
    
        // Python -> C++
        bool load(py::handle src, bool) {
            py::object obj = py::reinterpret_borrow<py::object>(src);
    
            // Extract fields from Python object
            py::object mode_obj = obj.attr("mode");
            py::object callback_obj = obj.attr("callback");
    
            value.mode = static_cast<WGPUCallbackMode>(mode_obj.cast<wgpu::CallbackMode>());
    
            // Allocate Python function to userdata
            py::function* cb = new py::function(callback_obj);
    
            value.userdata1 = cb;
            value.userdata2 = nullptr;
    
            // Define the native callback lambda
            value.callback = [](WGPUDevice const * device,
                                WGPUDeviceLostReason reason,
                                struct WGPUStringView message,
                                void* userdata1,
                                void* userdata2) {
                py::function* py_cb = reinterpret_cast<py::function*>(userdata1);
                py::gil_scoped_acquire gil;
    
                auto apiDevice = wgpu::Device::Acquire(*device);
                (*py_cb)(apiDevice, static_cast<wgpu::DeviceLostReason>(reason), static_cast<wgpu::StringView>(message));
    
                // Clean up after callback invocation
                delete py_cb;
            };
    
            return true;
        }
    
        // C++ -> Python (not usually needed, but provided for completeness)
        static py::handle cast(const wgpu::DeviceLostCallbackInfo& src, py::return_value_policy, py::handle) {
            py::object py_mode = py::cast(src.mode);
            py::object py_callback = py::none(); // callbacks aren't typically convertible back to Python from native pointers
    
            py::object py_obj = py::module_::import("wgpu").attr("DeviceLostCallbackInfo")(py_mode, py_callback);
            return py_obj.release();
        }
    };
    */

    /*
    template<>
    struct type_caster<wgpu::UncapturedErrorCallbackInfo> {
    public:
        PYBIND11_TYPE_CASTER(wgpu::UncapturedErrorCallbackInfo, _("UncapturedErrorCallbackInfo"));
    
        // Python -> C++
        bool load(py::handle src, bool) {
            py::object obj = py::reinterpret_borrow<py::object>(src);
    
            // Extract fields from Python object
            py::object callback_obj = obj.attr("callback");
        
            // Allocate Python function to userdata
            py::function* cb = new py::function(callback_obj);
    
            value.userdata1 = cb;
            value.userdata2 = nullptr;
    
            // Define the native callback lambda
            value.callback = [](WGPUDevice const * device,
                                WGPUErrorType type,
                                struct WGPUStringView message,
                                void* userdata1,
                                void* userdata2) {
                py::function* py_cb = reinterpret_cast<py::function*>(userdata1);
                py::gil_scoped_acquire gil;
    
                auto apiDevice = wgpu::Device::Acquire(*device);
                (*py_cb)(apiDevice, static_cast<wgpu::ErrorType>(type), static_cast<wgpu::StringView>(message));
    
                // Clean up after callback invocation
                delete py_cb;
            };
    
            return true;
        }
    
        // C++ -> Python (not usually needed, but provided for completeness)
        static py::handle cast(const wgpu::UncapturedErrorCallbackInfo& src, py::return_value_policy, py::handle) {
            py::object py_callback = py::none(); // callbacks aren't typically convertible back to Python from native pointers
    
            py::object py_obj = py::module_::import("wgpu").attr("UncapturedErrorCallbackInfo")(py_callback);
            return py_obj.release();
        }
    };
    */

    template<>
    struct type_caster<wgpu::UncapturedErrorCallbackInfo> {
    public:
        PYBIND11_TYPE_CASTER(wgpu::UncapturedErrorCallbackInfo, _("UncapturedErrorCallbackInfo"));
    
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
        static py::handle cast(const wgpu::UncapturedErrorCallbackInfo& src, py::return_value_policy, py::handle) {
            py::object py_callback = py::none(); // callbacks aren't typically convertible back to Python from native pointers
    
            py::object py_obj = py::module_::import("wgpu").attr("UncapturedErrorCallbackInfo")(py_callback);
            return py_obj.release();
        }
    };

    /*
    template<>
    struct type_caster<wgpu::LoggingCallbackInfo> {
    public:
        PYBIND11_TYPE_CASTER(wgpu::LoggingCallbackInfo, _("LoggingCallbackInfo"));
    
        // Python -> C++
        bool load(py::handle src, bool) {
            py::object obj = py::reinterpret_borrow<py::object>(src);
    
            // Extract fields from Python object
            py::object callback_obj = obj.attr("callback");
        
            // Allocate Python function to userdata
            py::function* cb = new py::function(callback_obj);
    
            value.userdata1 = cb;
            value.userdata2 = nullptr;
    
            // Define the native callback lambda
            value.callback = [](WGPULoggingType type,
                                WGPUStringView message,
                                void* userdata1,
                                void* userdata2) {
                py::function* py_cb = reinterpret_cast<py::function*>(userdata1);
                py::gil_scoped_acquire gil;
    
                (*py_cb)(type, message);
    
                // Clean up after callback invocation
                delete py_cb;
            };
    
            return true;
        }
    
        // C++ -> Python (not usually needed, but provided for completeness)
        static py::handle cast(const wgpu::LoggingCallbackInfo& src, py::return_value_policy, py::handle) {
            py::object py_callback = py::none(); // callbacks aren't typically convertible back to Python from native pointers
    
            py::object py_obj = py::module_::import("wgpu").attr("LoggingCallbackInfo")(py_callback);
            return py_obj.release();
        }
    };
    */

    template<>
    struct type_caster<wgpu::LoggingCallbackInfo> {
    public:
        PYBIND11_TYPE_CASTER(wgpu::LoggingCallbackInfo, _("LoggingCallbackInfo"));
    
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
        static py::handle cast(const wgpu::LoggingCallbackInfo& src, py::return_value_policy, py::handle) {
            py::object py_callback = py::none(); // callbacks aren't typically convertible back to Python from native pointers
    
            py::object py_obj = py::module_::import("wgpu").attr("LoggingCallbackInfo")(py_callback);
            return py_obj.release();
        }
    };

}} // namespace pybind11::detail