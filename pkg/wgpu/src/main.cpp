#include <limits>
#include <filesystem>
#include <string>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>
#include <pybind11/iostream.h>

#include <dawn/webgpu_cpp.h>
// #include <wgpu.h>
#include <dawn/native/DawnNative.h>
#include <dawn/dawn_proc.h>

#include <cxbind/cxbind.h>
#include <crunge/wgpu/crunge-wgpu.h>
#include <crunge/wgpu/conversions.h>

//#include "callbacks.h"


using namespace crunge_wgpu;

namespace py = pybind11;

using namespace wgpu;

WGPU_IMPORT_BITMASK_OPERATORS

void CreateProcTable()
{
    DawnProcTable procs(dawn::native::GetProcs());
    dawnProcSetProcs(&procs);
}

PYBIND11_MAKE_OPAQUE(std::vector<wgpu::BindGroupLayout>)
PYBIND11_MAKE_OPAQUE(std::vector<wgpu::BindGroupLayoutEntry>)
PYBIND11_MAKE_OPAQUE(std::vector<wgpu::BindGroupEntry>)
PYBIND11_MAKE_OPAQUE(std::vector<wgpu::VertexAttribute>)
PYBIND11_MAKE_OPAQUE(std::vector<wgpu::ColorTargetState>)
PYBIND11_MAKE_OPAQUE(std::vector<wgpu::VertexBufferLayout>)
PYBIND11_MAKE_OPAQUE(std::vector<wgpu::RenderPassColorAttachment>)

void init_main(py::module &_wgpu, Registry &registry)
{
    _wgpu.def("create_proc_table", &CreateProcTable);

    py::bind_vector<std::vector<wgpu::BindGroupLayout>>(_wgpu, "BindGroupLayouts", "BindGroupLayout Vector");
    py::bind_vector<std::vector<wgpu::BindGroupLayoutEntry>>(_wgpu, "BindGroupLayoutEntries", "BindGroupLayoutEntry Vector");
    py::bind_vector<std::vector<wgpu::BindGroupEntry>>(_wgpu, "BindGroupEntries", "BindGroupEntry Vector");
    py::bind_vector<std::vector<wgpu::VertexAttribute>>(_wgpu, "VertexAttributes", "VertexAttribute Vector");
    py::bind_vector<std::vector<wgpu::ColorTargetState>>(_wgpu, "ColorTargetStates", "ColorTargetState Vector");
    py::bind_vector<std::vector<wgpu::VertexBufferLayout>>(_wgpu, "VertexBufferLayouts", "VertexBufferLayout Vector");
    py::bind_vector<std::vector<wgpu::RenderPassColorAttachment>>(_wgpu, "RenderPassColorAttachments", "RenderPassColorAttachment Vector");

    /*
    PYCLASS_BEGIN(_wgpu, wgpu::DeviceDescriptor, DeviceDescriptor)
    PYCLASS_END(_wgpu, wgpu::DeviceDescriptor, DeviceDescriptor)
    */

    PYEXTEND_BEGIN(wgpu::Instance, Instance)
    Instance.def("request_adapter", [](const wgpu::Instance &self)
                 {
        //Adapter adapter;
        static Adapter adapter;
        wgpu::RequestAdapterOptions options = {};
        options.compatibleSurface = nullptr;

        //auto cb = [&adapter](wgpu::RequestAdapterStatus status, wgpu::Adapter _adapter, wgpu::StringView message, void* userdata1, void* userdata2) {
        auto cb = [](WGPURequestAdapterStatus status, WGPUAdapter _adapter, WGPUStringView message, void* userdata1, void* userdata2) {
            py::scoped_ostream_redirect stream(
            std::cerr,                                // std::ostream&
            py::module_::import("sys").attr("stderr") // Python output
            );

            if (status != WGPURequestAdapterStatus::WGPURequestAdapterStatus_Success) {
                std::cerr << "Failed to get an adapter: " << message.data << std::endl;
                return;
            }
            //adapter = std::move(_adapter);
            adapter = static_cast<Adapter>(_adapter);
        };

        wgpu::RequestAdapterCallbackInfo callbackInfo = {
            //.mode = wgpu::CallbackMode::WaitAnyOnly,
            //.mode = WGPUCallbackMode_WaitAnyOnly,
            .mode = WGPUCallbackMode_AllowProcessEvents,
            .callback = cb
        };
    
        auto f = self.RequestAdapter(&options, callbackInfo);
        FutureWaitInfo waitInfo { f };
        self.WaitAny(1, &waitInfo, UINT64_MAX);

        return adapter; });
    PYEXTEND_END

    /*
    PYEXTEND_BEGIN(wgpu::Instance, Instance)
    Instance.def("request_adapter", [](const wgpu::Instance& self)
    {
        Adapter adapter;
        wgpu::RequestAdapterOptions options = {};
        options.compatibleSurface = nullptr;
        wgpu::RequestAdapterCallbackInfo callbackInfo = {};

        self.WaitAny(self.RequestAdapter(
            &options, wgpu::CallbackMode::WaitAnyOnly,
            [&adapter](wgpu::RequestAdapterStatus status, wgpu::Adapter _adapter,
               wgpu::StringView message) {
                if (status != wgpu::RequestAdapterStatus::Success) {
                    std::cerr << "Failed to get an adapter: " << message.data << std::endl;
                    // abort();
                    return;
                }
                adapter = std::move(_adapter);
            }), UINT64_MAX);
        return adapter;
    });
    PYEXTEND_END
    */

    /*
    PYEXTEND_BEGIN(wgpu::Instance, Instance)
    Instance.def("request_adapter", [](const wgpu::Instance& self)
    {
        RequestAdapterOptions options;
        //typedef void (*WGPURequestAdapterCallback)(WGPURequestAdapterStatus status, WGPUAdapter adapter, char const * message, void * userdata);
        static Adapter adapter;
        auto cb = [](WGPURequestAdapterStatus status, WGPUAdapter _adapter, char const* message, void* userdata) {
            py::scoped_ostream_redirect stream(
            std::cerr,                                // std::ostream&
            py::module_::import("sys").attr("stderr") // Python output
            );

            adapter = static_cast<Adapter>(_adapter);
            std::cerr << message << std::endl;
        };
        int userdata = 0;
        self.RequestAdapter(&options, cb, &userdata);
        return adapter;
    });
    PYEXTEND_END
    */

    // void SetUncapturedErrorCallback(ErrorCallback callback, void * userdata) const;
    // void Device::SetLoggingCallback(WGPULoggingCallback callback, void* userdata) {
    // void Device::SetDeviceLostCallback(WGPUDeviceLostCallback callback, void* userdata) {

    // typedef void (*WGPUErrorCallback)(WGPUErrorType type, char const * message, void * userdata);
    // typedef void (*WGPULoggingCallback)(WGPULoggingType type, char const * message, void * userdata);
    // typedef void (*WGPUDeviceLostCallback)(WGPUDeviceLostReason reason, char const * message, void * userdata);

    PYEXTEND_BEGIN(wgpu::Device, Device)
    Device.def_property_readonly("queue", [](const wgpu::Device &self)
                                 { return self.GetQueue(); }, py::return_value_policy::automatic_reference);

    /*
    Device.def("enable_logging",
               [](const wgpu::Device &self)
               {
                   //self.SetUncapturedErrorCallback(crunge::wgpu::ErrorCallback, nullptr);

                   //self.SetLoggingCallback(crunge::wgpu::LoggingCallback, nullptr);

                   //self.SetDeviceLostCallback(crunge::wgpu::DeviceLostCallback, nullptr);
               });
    */
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::Extent3D, Extent3D)
    Extent3D.def(py::init<uint32_t, uint32_t, uint32_t>(), py::arg("width"), py::arg("height") = 1, py::arg("depth") = 1);
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::Origin3D, Origin3D)
    Origin3D.def(py::init<uint32_t, uint32_t, uint32_t>(), py::arg("x"), py::arg("y"), py::arg("z"));
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::Color, Color)
    Color.def(py::init<float, float, float, float>(), py::arg("r"), py::arg("g"), py::arg("b"), py::arg("a"));
    PYEXTEND_END

    // TODO: Getting incompatible argument types when both signatures match.  Makes no sense ...
    /*
    TypeError: set_bind_group(): incompatible function arguments. The following argument types are supported:
        1. (self: crunge.wgpu._wgpu.ComputePassEncoder, group_index: int, group: crunge.wgpu._wgpu.BindGroup, dynamic_offset_count: int = 0, dynamic_offsets: int = None) -> None

    Invoked with: <crunge.wgpu._wgpu.ComputePassEncoder object at 0x7f7a6a76a8f0>, 0, <crunge.wgpu._wgpu.BindGroup object at 0x7f7a6a77c230>
    */

    // void RenderPassEncoder::SetBindGroup(uint32_t groupIndex, BindGroup const& group, uint32_t dynamicOffsetCount, uint32_t const * dynamicOffsets) const {
    PYEXTEND_BEGIN(wgpu::RenderPassEncoder, RenderPassEncoder)
    RenderPassEncoder.def("set_bind_group", [](wgpu::RenderPassEncoder &self, uint32_t groupIndex, BindGroup const &group)
                          { self.SetBindGroup(groupIndex, group, 0, nullptr); }, py::arg("group_index"), py::arg("group")
                          //, py::arg("dynamic_offset_count") = 0
                          //, py::arg("dynamic_offsets") = nullptr
                          ,
                          py::return_value_policy::automatic_reference);
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::ComputePassEncoder, ComputePassEncoder)
    ComputePassEncoder.def("set_bind_group", [](wgpu::ComputePassEncoder &self, uint32_t groupIndex, BindGroup const &group)
                           { self.SetBindGroup(groupIndex, group, 0, nullptr); }, py::arg("group_index"), py::arg("group")
                           //, py::arg("dynamic_offset_count") = 0
                           //, py::arg("dynamic_offsets") = nullptr
                           ,
                           py::return_value_policy::automatic_reference);
    PYEXTEND_END
}
