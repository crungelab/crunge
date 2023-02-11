#include <limits>
#include <filesystem>
#include <string>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

#include <dawn/webgpu_cpp.h>
#include "dawn/native/DawnNative.h"
#include <dawn/dawn_proc.h>

#include <crunge/core/bindtools.h>
#include <crunge/wgpu/crunge-wgpu.h>
#include <crunge/wgpu/conversions.h>

namespace py = pybind11;

using namespace wgpu;

void CreateProcTable() {
    DawnProcTable procs(dawn::native::GetProcs());
    dawnProcSetProcs(&procs);
}

namespace wgpu {
    typedef std::vector<BindGroupLayoutEntry> BindGroupLayoutEntries;
}

PYBIND11_MAKE_OPAQUE(BindGroupLayoutEntries)

void init_main(py::module &_wgpu, Registry &registry) {
    _wgpu.def("create_proc_table", &CreateProcTable);

    py::bind_vector<BindGroupLayoutEntries>(_wgpu, "BindGroupLayoutEntries", "BindGroupLayoutEntry Vector");

    PYEXTEND_BEGIN(wgpu::Instance, Instance)
    Instance.def("request_adapter", [](const wgpu::Instance& self)
    {
        RequestAdapterOptions options;
        //typedef void (*WGPURequestAdapterCallback)(WGPURequestAdapterStatus status, WGPUAdapter adapter, char const * message, void * userdata);
        static Adapter adapter;
        auto cb = [](WGPURequestAdapterStatus status, WGPUAdapter _adapter, char const* message, void* userdata) {
            adapter = static_cast<Adapter>(_adapter);
        };
        int userdata = 0;
        self.RequestAdapter(&options, cb, &userdata);
		return adapter;
    });
    PYEXTEND_END

        //void SetUncapturedErrorCallback(ErrorCallback callback, void * userdata) const;
        //void Device::SetLoggingCallback(WGPULoggingCallback callback, void* userdata) {
        //void Device::SetDeviceLostCallback(WGPUDeviceLostCallback callback, void* userdata) {

        //typedef void (*WGPUErrorCallback)(WGPUErrorType type, char const * message, void * userdata);
        //typedef void (*WGPULoggingCallback)(WGPULoggingType type, char const * message, void * userdata);
        //typedef void (*WGPUDeviceLostCallback)(WGPUDeviceLostReason reason, char const * message, void * userdata);

        PYEXTEND_BEGIN(wgpu::Device, Device)
        Device.def_property_readonly("queue", [](const wgpu::Device& self) {
            return self.GetQueue();
        }, py::return_value_policy::automatic_reference);
    
    Device.def("enable_logging",
        [](const wgpu::Device& self) {
            self.SetUncapturedErrorCallback([](WGPUErrorType type, char const * message, void * userdata){
                printf(message);
            }, nullptr);

            self.SetLoggingCallback([](WGPULoggingType type, char const * message, void * userdata){
                printf(message);
            }, nullptr);

            self.SetDeviceLostCallback([](WGPUDeviceLostReason reason, char const * message, void * userdata){
                printf(message); printf("\n");
            }, nullptr);
    });

    /*Device.def("set_uncaptured_error_callback",
        [](const wgpu::Device& self, ErrorCallback callback, py::object userdata) {
            self.SetUncapturedErrorCallback(callback, userdata.ptr());
    }
    , py::arg("callback")
    , py::arg("userdata"));*/
    PYEXTEND_END

    /*PYEXTEND_BEGIN(wgpu::AdapterProperties, AdapterProperties)
        AdapterProperties.def(py::init<>());
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::BindGroupLayoutDescriptor, BindGroupLayoutDescriptor)
        BindGroupLayoutDescriptor.def(py::init<>());
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::BindGroupDescriptor, BindGroupDescriptor)
        BindGroupDescriptor.def(py::init<>());
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::ShaderModuleDescriptor, ShaderModuleDescriptor)
        ShaderModuleDescriptor.def(py::init<>());
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::TextureDescriptor, TextureDescriptor)
        TextureDescriptor.def(py::init<>());
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::BufferDescriptor, BufferDescriptor)
        BufferDescriptor.def(py::init<>());
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::PipelineLayoutDescriptor, PipelineLayoutDescriptor)
        PipelineLayoutDescriptor.def(py::init<>());
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::ColorTargetState, ColorTargetState)
        ColorTargetState.def(py::init<>());
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::FragmentState, FragmentState)
        FragmentState.def(py::init<>());
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::DepthStencilState, DepthStencilState)
        DepthStencilState.def(py::init<>());
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::RenderPipelineDescriptor, RenderPipelineDescriptor)
        RenderPipelineDescriptor.def(py::init<>());
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::RenderPassColorAttachment, RenderPassColorAttachment)
        RenderPassColorAttachment.def(py::init<>());
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::RenderPassDescriptor, RenderPassDescriptor)
        RenderPassDescriptor.def(py::init<>());
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::RenderPassDepthStencilAttachment, RenderPassDepthStencilAttachment)
        RenderPassDepthStencilAttachment.def(py::init<>());
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::CommandBuffer, CommandBuffer)
        CommandBuffer.def(py::init<>());
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::SurfaceDescriptor, SurfaceDescriptor)
        SurfaceDescriptor.def(py::init<>());
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::SwapChainDescriptor, SwapChainDescriptor)
        SwapChainDescriptor.def(py::init<>());
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::ImageCopyBuffer, ImageCopyBuffer)
        ImageCopyBuffer.def(py::init<>());
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::ImageCopyTexture, ImageCopyTexture)
        ImageCopyTexture.def(py::init<>());
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::TextureDataLayout, TextureDataLayout)
        TextureDataLayout.def(py::init<>());
    PYEXTEND_END

    */

    //TODO:GENERATE: need to define our own bitwise operators for scoped enums.
    PYEXTEND_SCOPED_ENUM_BEGIN(wgpu::TextureUsage, TextureUsage)
        //TextureUsage.def(py::self | py::self); //Doesn't work
        TextureUsage.def("__or__", [](wgpu::TextureUsage& a, wgpu::TextureUsage& b) {
        return (wgpu::TextureUsage)(a | b);
            }, py::is_operator());
    PYEXTEND_END

    PYEXTEND_SCOPED_ENUM_BEGIN(wgpu::BufferUsage, BufferUsage)
        //TextureUsage.def(py::self | py::self); //Doesn't work
        BufferUsage.def("__or__", [](wgpu::BufferUsage& a, wgpu::BufferUsage& b) {
        return (wgpu::BufferUsage)(a | b);
            }, py::is_operator());
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::Extent3D, Extent3D)
        Extent3D.def(py::init<uint32_t, uint32_t, uint32_t>()
        , py::arg("width")
        , py::arg("height")
        , py::arg("depth")
        );
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::Origin3D, Origin3D)
        Origin3D.def(py::init<uint32_t, uint32_t, uint32_t>()
        , py::arg("x")
        , py::arg("y")
        , py::arg("z")
        );
    PYEXTEND_END


    PYEXTEND_BEGIN(wgpu::Color, Color)
        Color.def(py::init<float, float, float, float>()
        , py::arg("r")
        , py::arg("g")
        , py::arg("b")
        , py::arg("a")
        );
    PYEXTEND_END


    /*PYEXTEND_BEGIN(wgpu::ShaderModuleWGSLDescriptor, ShaderModuleWGSLDescriptor)
        //ShaderModuleWGSLDescriptor.def_readwrite("source", &wgpu::ShaderModuleWGSLDescriptor::source);
        ShaderModuleWGSLDescriptor.def_property("source",
            [](const wgpu::ShaderModuleWGSLDescriptor& self) {
                return self.source;
            },
            [](wgpu::ShaderModuleWGSLDescriptor& self, std::string source) {
                //self.source = source.c_str();
                char* c = (char *)malloc(source.size());
                strcpy(c, source.c_str());
                self.source = c;
            }
        );
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::VertexState, VertexState)
        VertexState.def_property("entry_point",
            [](const wgpu::VertexState& self) {
                return self.entryPoint;
            },
            [](wgpu::VertexState& self, std::string source) {
                char* c = (char *)malloc(source.size());
                strcpy(c, source.c_str());
                self.entryPoint = c;
            }
        );
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::FragmentState, FragmentState)
        FragmentState.def(py::init<>());
        FragmentState.def_property("entry_point",
            [](const wgpu::FragmentState& self) {
                return self.entryPoint;
            },
            [](wgpu::FragmentState& self, std::string source) {
                char* c = (char *)malloc(source.size());
                strcpy(c, source.c_str());
                self.entryPoint = c;
            }
        );
    PYEXTEND_END*/

}