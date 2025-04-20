#include <dawn/webgpu_cpp.h>
// #include "wgpu.h"

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/wgpu/crunge-wgpu.h>
#include <crunge/wgpu/conversions.h>
#include <crunge/wgpu/callbacks.h>

void init_callbacks(py::module &_wgpu, Registry &registry)
{
    PYCLASS_BEGIN(_wgpu, crunge_wgpu::PyRequestAdapterCallbackInfo, RequestAdapterCallbackInfo)
    RequestAdapterCallbackInfo.def(py::init<wgpu::CallbackMode, py::function>(),
                               py::arg("mode"),
                               py::arg("callback"));

    PYCLASS_END(_wgpu, crunge_wgpu::PyRequestAdapterCallbackInfo, RequestAdapterCallbackInfo)

    PYCLASS_BEGIN(_wgpu, crunge_wgpu::PyDeviceLostCallbackInfo, DeviceLostCallbackInfo)
    DeviceLostCallbackInfo.def(py::init<wgpu::CallbackMode, py::function>(),
                               py::arg("mode"),
                               py::arg("callback"));

    PYCLASS_END(_wgpu, crunge_wgpu::PyDeviceLostCallbackInfo, DeviceLostCallbackInfo)

    PYCLASS_BEGIN(_wgpu, crunge_wgpu::PyUncapturedErrorCallbackInfo, UncapturedErrorCallbackInfo)
    UncapturedErrorCallbackInfo.def(py::init<py::function>(),
                               py::arg("callback"));

    PYCLASS_END(_wgpu, crunge_wgpu::PyUncapturedErrorCallbackInfo, UncapturedErrorCallbackInfo)

    PYCLASS_BEGIN(_wgpu, crunge_wgpu::PyLoggingCallbackInfo, LoggingCallbackInfo)
    LoggingCallbackInfo.def(py::init<py::function>(),
                               py::arg("callback"));

    PYCLASS_END(_wgpu, crunge_wgpu::PyLoggingCallbackInfo, LoggingCallbackInfo)

}