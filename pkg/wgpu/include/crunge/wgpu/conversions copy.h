#pragma once
#include <dawn/webgpu_cpp.h>
//#include <wgpu.h>
#include <pybind11/pybind11.h>

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
            return PyUnicode_FromString(src.data);
        }
    };
    
    /*template<>
    struct pybind11::detail::type_caster<pywgpu::RequestAdapterCallbackInfo> {
    public:
        PYBIND11_TYPE_CASTER(pywgpu::RequestAdapterCallbackInfo, _("RequestAdapterCallbackInfo"));
    
        // Python -> C++
        bool load(py::handle src, bool) {
            py::object obj = py::reinterpret_borrow<py::object>(src);
    
            // Extract fields from Python object
            py::object mode_obj = obj.attr("mode");
            py::object callback_obj = obj.attr("callback");
    
            value.mode = mode_obj.cast<pywgpu::CallbackMode>();
    
            // Allocate Python function to userdata
            py::function* cb = new py::function(callback_obj);
    
            value.userdata1 = cb;
            value.userdata2 = nullptr;
    
            // Define the native callback lambda
            value.callback = [](pywgpu::RequestAdapterStatus status,
                                pywgpu::Adapter adapter,
                                pywgpu::StringView message,
                                void* userdata1,
                                void* userdata2) {
                py::function* py_cb = reinterpret_cast<py::function*>(userdata1);
                py::gil_scoped_acquire gil;
    
                if (status == pywgpu::RequestAdapterStatus::Success) {
                    (*py_cb)(true, adapter);
                } else {
                    std::string msg(message.data, message.length);
                    (*py_cb)(false, msg);
                }
    
                // Clean up after callback invocation
                delete py_cb;
            };
    
            return true;
        }
    
        // C++ -> Python (not usually needed, but provided for completeness)
        static py::handle cast(const pywgpu::RequestAdapterCallbackInfo& src, py::return_value_policy, py::handle) {
            py::object py_mode = py::cast(src.mode);
            py::object py_callback = py::none(); // callbacks aren't typically convertible back to Python from native pointers
    
            py::object py_obj = py::module_::import("your_module").attr("RequestAdapterCallbackInfo")(py_mode, py_callback);
            return py_obj.release();
        }
    };*/

    template<>
    struct type_caster<pywgpu::LoggingCallbackInfo> {
    public:
        PYBIND11_TYPE_CASTER(pywgpu::LoggingCallbackInfo, _("LoggingCallbackInfo"));
    
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
        static py::handle cast(const pywgpu::LoggingCallbackInfo& src, py::return_value_policy, py::handle) {
            py::object py_callback = py::none(); // callbacks aren't typically convertible back to Python from native pointers
    
            py::object py_obj = py::module_::import("wgpu").attr("LoggingCallbackInfo")(py_callback);
            return py_obj.release();
        }
    };

    /*
    template <typename F, typename T, typename Cb, typename>
    void DeviceDescriptor::SetDeviceLostCallback(CallbackMode callbackMode, F callback, T userdata) {
        assert(deviceLostCallbackInfo.callback == nullptr);

        deviceLostCallbackInfo.mode = static_cast<WGPUCallbackMode>(callbackMode);
        deviceLostCallbackInfo.callback = [](WGPUDevice const * device, WGPUDeviceLostReason reason, WGPUStringView message, void* callback_param, void* userdata_param) {
            auto cb = reinterpret_cast<Cb*>(callback_param);
            // We manually acquire and release the device to avoid changing any ref counts.
            auto apiDevice = Device::Acquire(*device);
            (*cb)(apiDevice, static_cast<DeviceLostReason>(reason), message, static_cast<T>(userdata_param));
            apiDevice.MoveToCHandle();
        };
        deviceLostCallbackInfo.userdata1 = reinterpret_cast<void*>(+callback);
        deviceLostCallbackInfo.userdata2 = reinterpret_cast<void*>(userdata);
    }
    */
    template<>
    struct type_caster<pywgpu::DeviceLostCallbackInfo> {
    public:
        PYBIND11_TYPE_CASTER(pywgpu::DeviceLostCallbackInfo, _("DeviceLostCallbackInfo"));
    
        // Python -> C++
        bool load(py::handle src, bool) {
            py::object obj = py::reinterpret_borrow<py::object>(src);
    
            // Extract fields from Python object
            py::object mode_obj = obj.attr("mode");
            py::object callback_obj = obj.attr("callback");
    
            value.mode = static_cast<WGPUCallbackMode>(mode_obj.cast<pywgpu::CallbackMode>());
    
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
    
                auto apiDevice = pywgpu::Device::Acquire(*device);
                (*py_cb)(apiDevice, static_cast<pywgpu::DeviceLostReason>(reason), static_cast<pywgpu::StringView>(message));
    
                // Clean up after callback invocation
                delete py_cb;
            };
    
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
    
                auto apiDevice = pywgpu::Device::Acquire(*device);
                (*py_cb)(apiDevice, static_cast<pywgpu::ErrorType>(type), static_cast<pywgpu::StringView>(message));
    
                // Clean up after callback invocation
                delete py_cb;
            };
    
            return true;
        }
    
        // C++ -> Python (not usually needed, but provided for completeness)
        static py::handle cast(const pywgpu::UncapturedErrorCallbackInfo& src, py::return_value_policy, py::handle) {
            py::object py_callback = py::none(); // callbacks aren't typically convertible back to Python from native pointers
    
            py::object py_obj = py::module_::import("wgpu").attr("UncapturedErrorCallbackInfo")(py_callback);
            return py_obj.release();
        }
    };

}} // namespace pybind11::detail