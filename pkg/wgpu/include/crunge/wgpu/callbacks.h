#pragma once

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
//#include <dawn/webgpu_cpp.h>

#include <crunge/wgpu/pywgpu.h>

namespace py = pybind11;

namespace crunge_wgpu {

struct PyRequestAdapterCallbackInfo {
    pywgpu::CallbackMode mode;
    py::function py_callback;

    PyRequestAdapterCallbackInfo(
        pywgpu::CallbackMode mode,
        py::function py_callback
    ) : mode(mode), py_callback(py_callback) {}

    /*PyDeviceLostCallbackInfo(
        pywgpu::CallbackMode mode_,
        py::function callback_
    ) : mode(mode_), py_callback(std::move(callback_)) {}*/

    operator WGPURequestAdapterCallbackInfo() {
        auto callback = [](WGPURequestAdapterStatus status,
                            WGPUAdapter adapter,
                            WGPUStringView message,
                            void* userdata1,
                            void* userdata2) {
            auto self = reinterpret_cast<PyRequestAdapterCallbackInfo*>(userdata1);
            py::gil_scoped_acquire gil;

            auto apiAdapter = pywgpu::Adapter::Acquire(adapter);
            //std::cout << "RequestAdapterCallbackInfo: " << message.data << std::endl;
            self->py_callback(static_cast<pywgpu::RequestAdapterStatus>(status), apiAdapter, static_cast<pywgpu::StringView>(message));
        };

        WGPURequestAdapterCallbackInfo native_info = {};
        native_info.mode = static_cast<WGPUCallbackMode>(mode);
        native_info.callback = callback;
        native_info.userdata1 = this;
        native_info.userdata2 = nullptr;

        return native_info;
    }
};

struct PyDeviceLostCallbackInfo {
    pywgpu::CallbackMode mode;
    py::function py_callback;

    PyDeviceLostCallbackInfo(
        pywgpu::CallbackMode mode,
        py::function py_callback
    ) : mode(mode), py_callback(py_callback) {}

    /*PyDeviceLostCallbackInfo(
        pywgpu::CallbackMode mode_,
        py::function callback_
    ) : mode(mode_), py_callback(std::move(callback_)) {}*/

    operator WGPUDeviceLostCallbackInfo() {
        auto callback = [](WGPUDevice const * device,
                            WGPUDeviceLostReason reason,
                            struct WGPUStringView message,
                           void* userdata1,
                           void* userdata2) {

            // Check if Python interpreter is still alive
            if (Py_IsInitialized()) {
                auto self = reinterpret_cast<PyDeviceLostCallbackInfo*>(userdata1);
                py::gil_scoped_acquire gil;

                auto apiDevice = pywgpu::Device::Acquire(*device);
                //std::cout << "DeviceLostCallbackInfo: " << message.data << std::endl;
                self->py_callback(apiDevice, static_cast<pywgpu::DeviceLostReason>(reason), static_cast<pywgpu::StringView>(message));
            }
        };

        WGPUDeviceLostCallbackInfo native_info = {};
        native_info.mode = static_cast<WGPUCallbackMode>(mode);
        native_info.callback = callback;
        native_info.userdata1 = this;
        native_info.userdata2 = nullptr;

        return native_info;
    }
};

struct PyUncapturedErrorCallbackInfo {
    py::function py_callback;

    PyUncapturedErrorCallbackInfo(
        py::function py_callback
    ) : py_callback(py_callback) {}

    operator WGPUUncapturedErrorCallbackInfo() {
        auto callback = [](WGPUDevice const * device,
                            WGPUErrorType type,
                            struct WGPUStringView message,
                           void* userdata1,
                           void* userdata2) {
            auto self = reinterpret_cast<PyUncapturedErrorCallbackInfo*>(userdata1);
            py::gil_scoped_acquire gil;

            auto apiDevice = pywgpu::Device::Acquire(*device);
            //std::cout << "UncapturedErrorCallbackInfo: " << message.data << std::endl;
            self->py_callback(apiDevice, static_cast<pywgpu::ErrorType>(type), static_cast<pywgpu::StringView>(message));
        };

        WGPUUncapturedErrorCallbackInfo native_info = {};
        native_info.callback = callback;
        native_info.userdata1 = this;
        native_info.userdata2 = nullptr;

        return native_info;
    }
};

struct PyLoggingCallbackInfo {
    py::function py_callback;

    PyLoggingCallbackInfo(
        py::function py_callback
    ) : py_callback(py_callback) {}

    operator WGPULoggingCallbackInfo() {
        auto callback = [](WGPULoggingType type,
                           struct WGPUStringView message,
                           void* userdata1,
                           void* userdata2) {
            auto self = reinterpret_cast<PyUncapturedErrorCallbackInfo*>(userdata1);
            py::gil_scoped_acquire gil;

            //std::cout << "UncapturedErrorCallbackInfo: " << message.data << std::endl;
            self->py_callback(static_cast<pywgpu::LoggingType>(type), static_cast<pywgpu::StringView>(message));
        };

        WGPULoggingCallbackInfo native_info = {};
        native_info.callback = callback;
        native_info.userdata1 = this;
        native_info.userdata2 = nullptr;

        return native_info;
    }
};

}  // namespace crunge_wgpu