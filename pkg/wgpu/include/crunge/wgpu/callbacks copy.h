#pragma once

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <dawn/webgpu_cpp.h>

namespace py = pybind11;

namespace crunge_wgpu {

struct PyDeviceLostCallbackInfo {
    wgpu::CallbackMode mode;
    py::function py_callback;

    PyDeviceLostCallbackInfo(
        wgpu::CallbackMode mode,
        py::function py_callback
    ) : mode(mode), py_callback(py_callback) {}

    //wgpu::DeviceLostCallbackInfo to_native() {
    operator wgpu::DeviceLostCallbackInfo() {
        auto callback = [](WGPUDevice const * device,
                            WGPUDeviceLostReason reason,
                            struct WGPUStringView message,
                           void* userdata1,
                           void* userdata2) {
            //py::function* py_cb = reinterpret_cast<py::function*>(userdata1);
            auto self = reinterpret_cast<PyDeviceLostCallbackInfo*>(userdata1);
            py::gil_scoped_acquire gil;

            auto apiDevice = wgpu::Device::Acquire(*device);
            //(*py_cb)(apiDevice, static_cast<wgpu::DeviceLostReason>(reason), static_cast<wgpu::StringView>(message));
            self->py_callback(apiDevice, static_cast<wgpu::DeviceLostReason>(reason), static_cast<wgpu::StringView>(message));

            // Clean up callback function
            //delete py_cb;
        };

        // Important: We store the Python callback pointer as userdata.
        //py::function* callback_storage = new py::function(py_callback);

        wgpu::DeviceLostCallbackInfo native_info = {};
        native_info.mode = static_cast<WGPUCallbackMode>(mode);
        native_info.callback = callback;
        //native_info.userdata1 = callback_storage;
        native_info.userdata1 = this;
        native_info.userdata2 = nullptr;

        return native_info;
    }
};

}  // namespace crunge_wgpu