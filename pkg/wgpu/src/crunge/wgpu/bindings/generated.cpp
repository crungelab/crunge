#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>
#include <limits>

#include <dawn/webgpu_cpp.h>

#include <crunge/core/bindtools.h>
#include <crunge/wgpu/conversions.h>

namespace py = pybind11;

void init_generated(py::module &_wgpu, Registry &registry) {
    _wgpu.def("constexpr_max", &wgpu::detail::ConstexprMax
    , py::arg("a")
    , py::arg("b")
    , py::return_value_policy::automatic_reference);

    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::AdapterType, AdapterType)
    AdapterType
        .value("DISCRETE_GPU", wgpu::AdapterType::DiscreteGPU)
        .value("INTEGRATED_GPU", wgpu::AdapterType::IntegratedGPU)
        .value("CPU", wgpu::AdapterType::CPU)
        .value("UNKNOWN", wgpu::AdapterType::Unknown)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::AdapterType, AdapterType)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::AddressMode, AddressMode)
    AddressMode
        .value("REPEAT", wgpu::AddressMode::Repeat)
        .value("MIRROR_REPEAT", wgpu::AddressMode::MirrorRepeat)
        .value("CLAMP_TO_EDGE", wgpu::AddressMode::ClampToEdge)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::AddressMode, AddressMode)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::AlphaMode, AlphaMode)
    AlphaMode
        .value("PREMULTIPLIED", wgpu::AlphaMode::Premultiplied)
        .value("UNPREMULTIPLIED", wgpu::AlphaMode::Unpremultiplied)
        .value("OPAQUE", wgpu::AlphaMode::Opaque)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::AlphaMode, AlphaMode)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::BackendType, BackendType)
    BackendType
        .value("NULL", wgpu::BackendType::Null)
        .value("WEB_GPU", wgpu::BackendType::WebGPU)
        .value("D3_D11", wgpu::BackendType::D3D11)
        .value("D3_D12", wgpu::BackendType::D3D12)
        .value("METAL", wgpu::BackendType::Metal)
        .value("VULKAN", wgpu::BackendType::Vulkan)
        .value("OPEN_GL", wgpu::BackendType::OpenGL)
        .value("OPEN_GLES", wgpu::BackendType::OpenGLES)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::BackendType, BackendType)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::BlendFactor, BlendFactor)
    BlendFactor
        .value("ZERO", wgpu::BlendFactor::Zero)
        .value("ONE", wgpu::BlendFactor::One)
        .value("SRC", wgpu::BlendFactor::Src)
        .value("ONE_MINUS_SRC", wgpu::BlendFactor::OneMinusSrc)
        .value("SRC_ALPHA", wgpu::BlendFactor::SrcAlpha)
        .value("ONE_MINUS_SRC_ALPHA", wgpu::BlendFactor::OneMinusSrcAlpha)
        .value("DST", wgpu::BlendFactor::Dst)
        .value("ONE_MINUS_DST", wgpu::BlendFactor::OneMinusDst)
        .value("DST_ALPHA", wgpu::BlendFactor::DstAlpha)
        .value("ONE_MINUS_DST_ALPHA", wgpu::BlendFactor::OneMinusDstAlpha)
        .value("SRC_ALPHA_SATURATED", wgpu::BlendFactor::SrcAlphaSaturated)
        .value("CONSTANT", wgpu::BlendFactor::Constant)
        .value("ONE_MINUS_CONSTANT", wgpu::BlendFactor::OneMinusConstant)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::BlendFactor, BlendFactor)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::BlendOperation, BlendOperation)
    BlendOperation
        .value("ADD", wgpu::BlendOperation::Add)
        .value("SUBTRACT", wgpu::BlendOperation::Subtract)
        .value("REVERSE_SUBTRACT", wgpu::BlendOperation::ReverseSubtract)
        .value("MIN", wgpu::BlendOperation::Min)
        .value("MAX", wgpu::BlendOperation::Max)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::BlendOperation, BlendOperation)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::BufferBindingType, BufferBindingType)
    BufferBindingType
        .value("UNDEFINED", wgpu::BufferBindingType::Undefined)
        .value("UNIFORM", wgpu::BufferBindingType::Uniform)
        .value("STORAGE", wgpu::BufferBindingType::Storage)
        .value("READ_ONLY_STORAGE", wgpu::BufferBindingType::ReadOnlyStorage)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::BufferBindingType, BufferBindingType)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::BufferMapAsyncStatus, BufferMapAsyncStatus)
    BufferMapAsyncStatus
        .value("SUCCESS", wgpu::BufferMapAsyncStatus::Success)
        .value("ERROR", wgpu::BufferMapAsyncStatus::Error)
        .value("UNKNOWN", wgpu::BufferMapAsyncStatus::Unknown)
        .value("DEVICE_LOST", wgpu::BufferMapAsyncStatus::DeviceLost)
        .value("DESTROYED_BEFORE_CALLBACK", wgpu::BufferMapAsyncStatus::DestroyedBeforeCallback)
        .value("UNMAPPED_BEFORE_CALLBACK", wgpu::BufferMapAsyncStatus::UnmappedBeforeCallback)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::BufferMapAsyncStatus, BufferMapAsyncStatus)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::CompareFunction, CompareFunction)
    CompareFunction
        .value("UNDEFINED", wgpu::CompareFunction::Undefined)
        .value("NEVER", wgpu::CompareFunction::Never)
        .value("LESS", wgpu::CompareFunction::Less)
        .value("LESS_EQUAL", wgpu::CompareFunction::LessEqual)
        .value("GREATER", wgpu::CompareFunction::Greater)
        .value("GREATER_EQUAL", wgpu::CompareFunction::GreaterEqual)
        .value("EQUAL", wgpu::CompareFunction::Equal)
        .value("NOT_EQUAL", wgpu::CompareFunction::NotEqual)
        .value("ALWAYS", wgpu::CompareFunction::Always)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::CompareFunction, CompareFunction)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::CompilationInfoRequestStatus, CompilationInfoRequestStatus)
    CompilationInfoRequestStatus
        .value("SUCCESS", wgpu::CompilationInfoRequestStatus::Success)
        .value("ERROR", wgpu::CompilationInfoRequestStatus::Error)
        .value("DEVICE_LOST", wgpu::CompilationInfoRequestStatus::DeviceLost)
        .value("UNKNOWN", wgpu::CompilationInfoRequestStatus::Unknown)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::CompilationInfoRequestStatus, CompilationInfoRequestStatus)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::CompilationMessageType, CompilationMessageType)
    CompilationMessageType
        .value("ERROR", wgpu::CompilationMessageType::Error)
        .value("WARNING", wgpu::CompilationMessageType::Warning)
        .value("INFO", wgpu::CompilationMessageType::Info)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::CompilationMessageType, CompilationMessageType)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::ComputePassTimestampLocation, ComputePassTimestampLocation)
    ComputePassTimestampLocation
        .value("BEGINNING", wgpu::ComputePassTimestampLocation::Beginning)
        .value("END", wgpu::ComputePassTimestampLocation::End)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::ComputePassTimestampLocation, ComputePassTimestampLocation)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::CreatePipelineAsyncStatus, CreatePipelineAsyncStatus)
    CreatePipelineAsyncStatus
        .value("SUCCESS", wgpu::CreatePipelineAsyncStatus::Success)
        .value("ERROR", wgpu::CreatePipelineAsyncStatus::Error)
        .value("DEVICE_LOST", wgpu::CreatePipelineAsyncStatus::DeviceLost)
        .value("DEVICE_DESTROYED", wgpu::CreatePipelineAsyncStatus::DeviceDestroyed)
        .value("UNKNOWN", wgpu::CreatePipelineAsyncStatus::Unknown)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::CreatePipelineAsyncStatus, CreatePipelineAsyncStatus)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::CullMode, CullMode)
    CullMode
        .value("NONE", wgpu::CullMode::None)
        .value("FRONT", wgpu::CullMode::Front)
        .value("BACK", wgpu::CullMode::Back)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::CullMode, CullMode)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::DeviceLostReason, DeviceLostReason)
    DeviceLostReason
        .value("UNDEFINED", wgpu::DeviceLostReason::Undefined)
        .value("DESTROYED", wgpu::DeviceLostReason::Destroyed)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::DeviceLostReason, DeviceLostReason)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::ErrorFilter, ErrorFilter)
    ErrorFilter
        .value("VALIDATION", wgpu::ErrorFilter::Validation)
        .value("OUT_OF_MEMORY", wgpu::ErrorFilter::OutOfMemory)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::ErrorFilter, ErrorFilter)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::ErrorType, ErrorType)
    ErrorType
        .value("NO_ERROR", wgpu::ErrorType::NoError)
        .value("VALIDATION", wgpu::ErrorType::Validation)
        .value("OUT_OF_MEMORY", wgpu::ErrorType::OutOfMemory)
        .value("UNKNOWN", wgpu::ErrorType::Unknown)
        .value("DEVICE_LOST", wgpu::ErrorType::DeviceLost)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::ErrorType, ErrorType)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::FeatureName, FeatureName)
    FeatureName
        .value("UNDEFINED", wgpu::FeatureName::Undefined)
        .value("DEPTH_CLIP_CONTROL", wgpu::FeatureName::DepthClipControl)
        .value("DEPTH32_FLOAT_STENCIL8", wgpu::FeatureName::Depth32FloatStencil8)
        .value("TIMESTAMP_QUERY", wgpu::FeatureName::TimestampQuery)
        .value("PIPELINE_STATISTICS_QUERY", wgpu::FeatureName::PipelineStatisticsQuery)
        .value("TEXTURE_COMPRESSION_BC", wgpu::FeatureName::TextureCompressionBC)
        .value("TEXTURE_COMPRESSION_ETC2", wgpu::FeatureName::TextureCompressionETC2)
        .value("TEXTURE_COMPRESSION_ASTC", wgpu::FeatureName::TextureCompressionASTC)
        .value("INDIRECT_FIRST_INSTANCE", wgpu::FeatureName::IndirectFirstInstance)
        .value("DAWN_SHADER_FLOAT16", wgpu::FeatureName::DawnShaderFloat16)
        .value("DAWN_INTERNAL_USAGES", wgpu::FeatureName::DawnInternalUsages)
        .value("DAWN_MULTI_PLANAR_FORMATS", wgpu::FeatureName::DawnMultiPlanarFormats)
        .value("DAWN_NATIVE", wgpu::FeatureName::DawnNative)
        .value("CHROMIUM_EXPERIMENTAL_DP4A", wgpu::FeatureName::ChromiumExperimentalDp4a)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::FeatureName, FeatureName)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::FilterMode, FilterMode)
    FilterMode
        .value("NEAREST", wgpu::FilterMode::Nearest)
        .value("LINEAR", wgpu::FilterMode::Linear)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::FilterMode, FilterMode)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::FrontFace, FrontFace)
    FrontFace
        .value("CCW", wgpu::FrontFace::CCW)
        .value("CW", wgpu::FrontFace::CW)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::FrontFace, FrontFace)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::IndexFormat, IndexFormat)
    IndexFormat
        .value("UNDEFINED", wgpu::IndexFormat::Undefined)
        .value("UINT16", wgpu::IndexFormat::Uint16)
        .value("UINT32", wgpu::IndexFormat::Uint32)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::IndexFormat, IndexFormat)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::LoadOp, LoadOp)
    LoadOp
        .value("UNDEFINED", wgpu::LoadOp::Undefined)
        .value("CLEAR", wgpu::LoadOp::Clear)
        .value("LOAD", wgpu::LoadOp::Load)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::LoadOp, LoadOp)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::LoggingType, LoggingType)
    LoggingType
        .value("VERBOSE", wgpu::LoggingType::Verbose)
        .value("INFO", wgpu::LoggingType::Info)
        .value("WARNING", wgpu::LoggingType::Warning)
        .value("ERROR", wgpu::LoggingType::Error)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::LoggingType, LoggingType)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::PipelineStatisticName, PipelineStatisticName)
    PipelineStatisticName
        .value("VERTEX_SHADER_INVOCATIONS", wgpu::PipelineStatisticName::VertexShaderInvocations)
        .value("CLIPPER_INVOCATIONS", wgpu::PipelineStatisticName::ClipperInvocations)
        .value("CLIPPER_PRIMITIVES_OUT", wgpu::PipelineStatisticName::ClipperPrimitivesOut)
        .value("FRAGMENT_SHADER_INVOCATIONS", wgpu::PipelineStatisticName::FragmentShaderInvocations)
        .value("COMPUTE_SHADER_INVOCATIONS", wgpu::PipelineStatisticName::ComputeShaderInvocations)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::PipelineStatisticName, PipelineStatisticName)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::PowerPreference, PowerPreference)
    PowerPreference
        .value("UNDEFINED", wgpu::PowerPreference::Undefined)
        .value("LOW_POWER", wgpu::PowerPreference::LowPower)
        .value("HIGH_PERFORMANCE", wgpu::PowerPreference::HighPerformance)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::PowerPreference, PowerPreference)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::PresentMode, PresentMode)
    PresentMode
        .value("IMMEDIATE", wgpu::PresentMode::Immediate)
        .value("MAILBOX", wgpu::PresentMode::Mailbox)
        .value("FIFO", wgpu::PresentMode::Fifo)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::PresentMode, PresentMode)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::PrimitiveTopology, PrimitiveTopology)
    PrimitiveTopology
        .value("POINT_LIST", wgpu::PrimitiveTopology::PointList)
        .value("LINE_LIST", wgpu::PrimitiveTopology::LineList)
        .value("LINE_STRIP", wgpu::PrimitiveTopology::LineStrip)
        .value("TRIANGLE_LIST", wgpu::PrimitiveTopology::TriangleList)
        .value("TRIANGLE_STRIP", wgpu::PrimitiveTopology::TriangleStrip)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::PrimitiveTopology, PrimitiveTopology)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::QueryType, QueryType)
    QueryType
        .value("OCCLUSION", wgpu::QueryType::Occlusion)
        .value("PIPELINE_STATISTICS", wgpu::QueryType::PipelineStatistics)
        .value("TIMESTAMP", wgpu::QueryType::Timestamp)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::QueryType, QueryType)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::QueueWorkDoneStatus, QueueWorkDoneStatus)
    QueueWorkDoneStatus
        .value("SUCCESS", wgpu::QueueWorkDoneStatus::Success)
        .value("ERROR", wgpu::QueueWorkDoneStatus::Error)
        .value("UNKNOWN", wgpu::QueueWorkDoneStatus::Unknown)
        .value("DEVICE_LOST", wgpu::QueueWorkDoneStatus::DeviceLost)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::QueueWorkDoneStatus, QueueWorkDoneStatus)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::RenderPassTimestampLocation, RenderPassTimestampLocation)
    RenderPassTimestampLocation
        .value("BEGINNING", wgpu::RenderPassTimestampLocation::Beginning)
        .value("END", wgpu::RenderPassTimestampLocation::End)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::RenderPassTimestampLocation, RenderPassTimestampLocation)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::RequestAdapterStatus, RequestAdapterStatus)
    RequestAdapterStatus
        .value("SUCCESS", wgpu::RequestAdapterStatus::Success)
        .value("UNAVAILABLE", wgpu::RequestAdapterStatus::Unavailable)
        .value("ERROR", wgpu::RequestAdapterStatus::Error)
        .value("UNKNOWN", wgpu::RequestAdapterStatus::Unknown)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::RequestAdapterStatus, RequestAdapterStatus)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::RequestDeviceStatus, RequestDeviceStatus)
    RequestDeviceStatus
        .value("SUCCESS", wgpu::RequestDeviceStatus::Success)
        .value("ERROR", wgpu::RequestDeviceStatus::Error)
        .value("UNKNOWN", wgpu::RequestDeviceStatus::Unknown)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::RequestDeviceStatus, RequestDeviceStatus)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::SType, SType)
    SType
        .value("INVALID", wgpu::SType::Invalid)
        .value("SURFACE_DESCRIPTOR_FROM_METAL_LAYER", wgpu::SType::SurfaceDescriptorFromMetalLayer)
        .value("SURFACE_DESCRIPTOR_FROM_WINDOWS_HWND", wgpu::SType::SurfaceDescriptorFromWindowsHWND)
        .value("SURFACE_DESCRIPTOR_FROM_XLIB_WINDOW", wgpu::SType::SurfaceDescriptorFromXlibWindow)
        .value("SURFACE_DESCRIPTOR_FROM_CANVAS_HTML_SELECTOR", wgpu::SType::SurfaceDescriptorFromCanvasHTMLSelector)
        .value("SHADER_MODULE_SPIRV_DESCRIPTOR", wgpu::SType::ShaderModuleSPIRVDescriptor)
        .value("SHADER_MODULE_WGSL_DESCRIPTOR", wgpu::SType::ShaderModuleWGSLDescriptor)
        .value("PRIMITIVE_DEPTH_CLIP_CONTROL", wgpu::SType::PrimitiveDepthClipControl)
        .value("SURFACE_DESCRIPTOR_FROM_WAYLAND_SURFACE", wgpu::SType::SurfaceDescriptorFromWaylandSurface)
        .value("SURFACE_DESCRIPTOR_FROM_ANDROID_NATIVE_WINDOW", wgpu::SType::SurfaceDescriptorFromAndroidNativeWindow)
        .value("SURFACE_DESCRIPTOR_FROM_WINDOWS_CORE_WINDOW", wgpu::SType::SurfaceDescriptorFromWindowsCoreWindow)
        .value("EXTERNAL_TEXTURE_BINDING_ENTRY", wgpu::SType::ExternalTextureBindingEntry)
        .value("EXTERNAL_TEXTURE_BINDING_LAYOUT", wgpu::SType::ExternalTextureBindingLayout)
        .value("SURFACE_DESCRIPTOR_FROM_WINDOWS_SWAP_CHAIN_PANEL", wgpu::SType::SurfaceDescriptorFromWindowsSwapChainPanel)
        .value("RENDER_PASS_DESCRIPTOR_MAX_DRAW_COUNT", wgpu::SType::RenderPassDescriptorMaxDrawCount)
        .value("DAWN_TEXTURE_INTERNAL_USAGE_DESCRIPTOR", wgpu::SType::DawnTextureInternalUsageDescriptor)
        .value("DAWN_TOGGLES_DEVICE_DESCRIPTOR", wgpu::SType::DawnTogglesDeviceDescriptor)
        .value("DAWN_ENCODER_INTERNAL_USAGE_DESCRIPTOR", wgpu::SType::DawnEncoderInternalUsageDescriptor)
        .value("DAWN_INSTANCE_DESCRIPTOR", wgpu::SType::DawnInstanceDescriptor)
        .value("DAWN_CACHE_DEVICE_DESCRIPTOR", wgpu::SType::DawnCacheDeviceDescriptor)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::SType, SType)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::SamplerBindingType, SamplerBindingType)
    SamplerBindingType
        .value("UNDEFINED", wgpu::SamplerBindingType::Undefined)
        .value("FILTERING", wgpu::SamplerBindingType::Filtering)
        .value("NON_FILTERING", wgpu::SamplerBindingType::NonFiltering)
        .value("COMPARISON", wgpu::SamplerBindingType::Comparison)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::SamplerBindingType, SamplerBindingType)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::StencilOperation, StencilOperation)
    StencilOperation
        .value("KEEP", wgpu::StencilOperation::Keep)
        .value("ZERO", wgpu::StencilOperation::Zero)
        .value("REPLACE", wgpu::StencilOperation::Replace)
        .value("INVERT", wgpu::StencilOperation::Invert)
        .value("INCREMENT_CLAMP", wgpu::StencilOperation::IncrementClamp)
        .value("DECREMENT_CLAMP", wgpu::StencilOperation::DecrementClamp)
        .value("INCREMENT_WRAP", wgpu::StencilOperation::IncrementWrap)
        .value("DECREMENT_WRAP", wgpu::StencilOperation::DecrementWrap)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::StencilOperation, StencilOperation)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::StorageTextureAccess, StorageTextureAccess)
    StorageTextureAccess
        .value("UNDEFINED", wgpu::StorageTextureAccess::Undefined)
        .value("WRITE_ONLY", wgpu::StorageTextureAccess::WriteOnly)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::StorageTextureAccess, StorageTextureAccess)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::StoreOp, StoreOp)
    StoreOp
        .value("UNDEFINED", wgpu::StoreOp::Undefined)
        .value("STORE", wgpu::StoreOp::Store)
        .value("DISCARD", wgpu::StoreOp::Discard)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::StoreOp, StoreOp)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::TextureAspect, TextureAspect)
    TextureAspect
        .value("ALL", wgpu::TextureAspect::All)
        .value("STENCIL_ONLY", wgpu::TextureAspect::StencilOnly)
        .value("DEPTH_ONLY", wgpu::TextureAspect::DepthOnly)
        .value("PLANE0_ONLY", wgpu::TextureAspect::Plane0Only)
        .value("PLANE1_ONLY", wgpu::TextureAspect::Plane1Only)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::TextureAspect, TextureAspect)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::TextureComponentType, TextureComponentType)
    TextureComponentType
        .value("FLOAT", wgpu::TextureComponentType::Float)
        .value("SINT", wgpu::TextureComponentType::Sint)
        .value("UINT", wgpu::TextureComponentType::Uint)
        .value("DEPTH_COMPARISON", wgpu::TextureComponentType::DepthComparison)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::TextureComponentType, TextureComponentType)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::TextureDimension, TextureDimension)
    TextureDimension
        .value("E1_D", wgpu::TextureDimension::e1D)
        .value("E2_D", wgpu::TextureDimension::e2D)
        .value("E3_D", wgpu::TextureDimension::e3D)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::TextureDimension, TextureDimension)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::TextureFormat, TextureFormat)
    TextureFormat
        .value("UNDEFINED", wgpu::TextureFormat::Undefined)
        .value("R8_UNORM", wgpu::TextureFormat::R8Unorm)
        .value("R8_SNORM", wgpu::TextureFormat::R8Snorm)
        .value("R8_UINT", wgpu::TextureFormat::R8Uint)
        .value("R8_SINT", wgpu::TextureFormat::R8Sint)
        .value("R16_UINT", wgpu::TextureFormat::R16Uint)
        .value("R16_SINT", wgpu::TextureFormat::R16Sint)
        .value("R16_FLOAT", wgpu::TextureFormat::R16Float)
        .value("RG8_UNORM", wgpu::TextureFormat::RG8Unorm)
        .value("RG8_SNORM", wgpu::TextureFormat::RG8Snorm)
        .value("RG8_UINT", wgpu::TextureFormat::RG8Uint)
        .value("RG8_SINT", wgpu::TextureFormat::RG8Sint)
        .value("R32_FLOAT", wgpu::TextureFormat::R32Float)
        .value("R32_UINT", wgpu::TextureFormat::R32Uint)
        .value("R32_SINT", wgpu::TextureFormat::R32Sint)
        .value("RG16_UINT", wgpu::TextureFormat::RG16Uint)
        .value("RG16_SINT", wgpu::TextureFormat::RG16Sint)
        .value("RG16_FLOAT", wgpu::TextureFormat::RG16Float)
        .value("RGBA8_UNORM", wgpu::TextureFormat::RGBA8Unorm)
        .value("RGBA8_UNORM_SRGB", wgpu::TextureFormat::RGBA8UnormSrgb)
        .value("RGBA8_SNORM", wgpu::TextureFormat::RGBA8Snorm)
        .value("RGBA8_UINT", wgpu::TextureFormat::RGBA8Uint)
        .value("RGBA8_SINT", wgpu::TextureFormat::RGBA8Sint)
        .value("BGRA8_UNORM", wgpu::TextureFormat::BGRA8Unorm)
        .value("BGRA8_UNORM_SRGB", wgpu::TextureFormat::BGRA8UnormSrgb)
        .value("RGB10_A2_UNORM", wgpu::TextureFormat::RGB10A2Unorm)
        .value("RG11_B10_UFLOAT", wgpu::TextureFormat::RG11B10Ufloat)
        .value("RGB9_E5_UFLOAT", wgpu::TextureFormat::RGB9E5Ufloat)
        .value("RG32_FLOAT", wgpu::TextureFormat::RG32Float)
        .value("RG32_UINT", wgpu::TextureFormat::RG32Uint)
        .value("RG32_SINT", wgpu::TextureFormat::RG32Sint)
        .value("RGBA16_UINT", wgpu::TextureFormat::RGBA16Uint)
        .value("RGBA16_SINT", wgpu::TextureFormat::RGBA16Sint)
        .value("RGBA16_FLOAT", wgpu::TextureFormat::RGBA16Float)
        .value("RGBA32_FLOAT", wgpu::TextureFormat::RGBA32Float)
        .value("RGBA32_UINT", wgpu::TextureFormat::RGBA32Uint)
        .value("RGBA32_SINT", wgpu::TextureFormat::RGBA32Sint)
        .value("STENCIL8", wgpu::TextureFormat::Stencil8)
        .value("DEPTH16_UNORM", wgpu::TextureFormat::Depth16Unorm)
        .value("DEPTH24_PLUS", wgpu::TextureFormat::Depth24Plus)
        .value("DEPTH24_PLUS_STENCIL8", wgpu::TextureFormat::Depth24PlusStencil8)
        .value("DEPTH32_FLOAT", wgpu::TextureFormat::Depth32Float)
        .value("DEPTH32_FLOAT_STENCIL8", wgpu::TextureFormat::Depth32FloatStencil8)
        .value("BC1_RGBA_UNORM", wgpu::TextureFormat::BC1RGBAUnorm)
        .value("BC1_RGBA_UNORM_SRGB", wgpu::TextureFormat::BC1RGBAUnormSrgb)
        .value("BC2_RGBA_UNORM", wgpu::TextureFormat::BC2RGBAUnorm)
        .value("BC2_RGBA_UNORM_SRGB", wgpu::TextureFormat::BC2RGBAUnormSrgb)
        .value("BC3_RGBA_UNORM", wgpu::TextureFormat::BC3RGBAUnorm)
        .value("BC3_RGBA_UNORM_SRGB", wgpu::TextureFormat::BC3RGBAUnormSrgb)
        .value("BC4_R_UNORM", wgpu::TextureFormat::BC4RUnorm)
        .value("BC4_R_SNORM", wgpu::TextureFormat::BC4RSnorm)
        .value("BC5_RG_UNORM", wgpu::TextureFormat::BC5RGUnorm)
        .value("BC5_RG_SNORM", wgpu::TextureFormat::BC5RGSnorm)
        .value("BC6_HRGB_UFLOAT", wgpu::TextureFormat::BC6HRGBUfloat)
        .value("BC6_HRGB_FLOAT", wgpu::TextureFormat::BC6HRGBFloat)
        .value("BC7_RGBA_UNORM", wgpu::TextureFormat::BC7RGBAUnorm)
        .value("BC7_RGBA_UNORM_SRGB", wgpu::TextureFormat::BC7RGBAUnormSrgb)
        .value("ETC2_RGB8_UNORM", wgpu::TextureFormat::ETC2RGB8Unorm)
        .value("ETC2_RGB8_UNORM_SRGB", wgpu::TextureFormat::ETC2RGB8UnormSrgb)
        .value("ETC2_RGB8_A1_UNORM", wgpu::TextureFormat::ETC2RGB8A1Unorm)
        .value("ETC2_RGB8_A1_UNORM_SRGB", wgpu::TextureFormat::ETC2RGB8A1UnormSrgb)
        .value("ETC2_RGBA8_UNORM", wgpu::TextureFormat::ETC2RGBA8Unorm)
        .value("ETC2_RGBA8_UNORM_SRGB", wgpu::TextureFormat::ETC2RGBA8UnormSrgb)
        .value("EACR11_UNORM", wgpu::TextureFormat::EACR11Unorm)
        .value("EACR11_SNORM", wgpu::TextureFormat::EACR11Snorm)
        .value("EACRG11_UNORM", wgpu::TextureFormat::EACRG11Unorm)
        .value("EACRG11_SNORM", wgpu::TextureFormat::EACRG11Snorm)
        .value("ASTC4X4_UNORM", wgpu::TextureFormat::ASTC4x4Unorm)
        .value("ASTC4X4_UNORM_SRGB", wgpu::TextureFormat::ASTC4x4UnormSrgb)
        .value("ASTC5X4_UNORM", wgpu::TextureFormat::ASTC5x4Unorm)
        .value("ASTC5X4_UNORM_SRGB", wgpu::TextureFormat::ASTC5x4UnormSrgb)
        .value("ASTC5X5_UNORM", wgpu::TextureFormat::ASTC5x5Unorm)
        .value("ASTC5X5_UNORM_SRGB", wgpu::TextureFormat::ASTC5x5UnormSrgb)
        .value("ASTC6X5_UNORM", wgpu::TextureFormat::ASTC6x5Unorm)
        .value("ASTC6X5_UNORM_SRGB", wgpu::TextureFormat::ASTC6x5UnormSrgb)
        .value("ASTC6X6_UNORM", wgpu::TextureFormat::ASTC6x6Unorm)
        .value("ASTC6X6_UNORM_SRGB", wgpu::TextureFormat::ASTC6x6UnormSrgb)
        .value("ASTC8X5_UNORM", wgpu::TextureFormat::ASTC8x5Unorm)
        .value("ASTC8X5_UNORM_SRGB", wgpu::TextureFormat::ASTC8x5UnormSrgb)
        .value("ASTC8X6_UNORM", wgpu::TextureFormat::ASTC8x6Unorm)
        .value("ASTC8X6_UNORM_SRGB", wgpu::TextureFormat::ASTC8x6UnormSrgb)
        .value("ASTC8X8_UNORM", wgpu::TextureFormat::ASTC8x8Unorm)
        .value("ASTC8X8_UNORM_SRGB", wgpu::TextureFormat::ASTC8x8UnormSrgb)
        .value("ASTC10X5_UNORM", wgpu::TextureFormat::ASTC10x5Unorm)
        .value("ASTC10X5_UNORM_SRGB", wgpu::TextureFormat::ASTC10x5UnormSrgb)
        .value("ASTC10X6_UNORM", wgpu::TextureFormat::ASTC10x6Unorm)
        .value("ASTC10X6_UNORM_SRGB", wgpu::TextureFormat::ASTC10x6UnormSrgb)
        .value("ASTC10X8_UNORM", wgpu::TextureFormat::ASTC10x8Unorm)
        .value("ASTC10X8_UNORM_SRGB", wgpu::TextureFormat::ASTC10x8UnormSrgb)
        .value("ASTC10X10_UNORM", wgpu::TextureFormat::ASTC10x10Unorm)
        .value("ASTC10X10_UNORM_SRGB", wgpu::TextureFormat::ASTC10x10UnormSrgb)
        .value("ASTC12X10_UNORM", wgpu::TextureFormat::ASTC12x10Unorm)
        .value("ASTC12X10_UNORM_SRGB", wgpu::TextureFormat::ASTC12x10UnormSrgb)
        .value("ASTC12X12_UNORM", wgpu::TextureFormat::ASTC12x12Unorm)
        .value("ASTC12X12_UNORM_SRGB", wgpu::TextureFormat::ASTC12x12UnormSrgb)
        .value("R8_BG8_BIPLANAR420_UNORM", wgpu::TextureFormat::R8BG8Biplanar420Unorm)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::TextureFormat, TextureFormat)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::TextureSampleType, TextureSampleType)
    TextureSampleType
        .value("UNDEFINED", wgpu::TextureSampleType::Undefined)
        .value("FLOAT", wgpu::TextureSampleType::Float)
        .value("UNFILTERABLE_FLOAT", wgpu::TextureSampleType::UnfilterableFloat)
        .value("DEPTH", wgpu::TextureSampleType::Depth)
        .value("SINT", wgpu::TextureSampleType::Sint)
        .value("UINT", wgpu::TextureSampleType::Uint)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::TextureSampleType, TextureSampleType)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::TextureViewDimension, TextureViewDimension)
    TextureViewDimension
        .value("UNDEFINED", wgpu::TextureViewDimension::Undefined)
        .value("E1_D", wgpu::TextureViewDimension::e1D)
        .value("E2_D", wgpu::TextureViewDimension::e2D)
        .value("E2_D_ARRAY", wgpu::TextureViewDimension::e2DArray)
        .value("CUBE", wgpu::TextureViewDimension::Cube)
        .value("CUBE_ARRAY", wgpu::TextureViewDimension::CubeArray)
        .value("E3_D", wgpu::TextureViewDimension::e3D)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::TextureViewDimension, TextureViewDimension)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::VertexFormat, VertexFormat)
    VertexFormat
        .value("UNDEFINED", wgpu::VertexFormat::Undefined)
        .value("UINT8X2", wgpu::VertexFormat::Uint8x2)
        .value("UINT8X4", wgpu::VertexFormat::Uint8x4)
        .value("SINT8X2", wgpu::VertexFormat::Sint8x2)
        .value("SINT8X4", wgpu::VertexFormat::Sint8x4)
        .value("UNORM8X2", wgpu::VertexFormat::Unorm8x2)
        .value("UNORM8X4", wgpu::VertexFormat::Unorm8x4)
        .value("SNORM8X2", wgpu::VertexFormat::Snorm8x2)
        .value("SNORM8X4", wgpu::VertexFormat::Snorm8x4)
        .value("UINT16X2", wgpu::VertexFormat::Uint16x2)
        .value("UINT16X4", wgpu::VertexFormat::Uint16x4)
        .value("SINT16X2", wgpu::VertexFormat::Sint16x2)
        .value("SINT16X4", wgpu::VertexFormat::Sint16x4)
        .value("UNORM16X2", wgpu::VertexFormat::Unorm16x2)
        .value("UNORM16X4", wgpu::VertexFormat::Unorm16x4)
        .value("SNORM16X2", wgpu::VertexFormat::Snorm16x2)
        .value("SNORM16X4", wgpu::VertexFormat::Snorm16x4)
        .value("FLOAT16X2", wgpu::VertexFormat::Float16x2)
        .value("FLOAT16X4", wgpu::VertexFormat::Float16x4)
        .value("FLOAT32", wgpu::VertexFormat::Float32)
        .value("FLOAT32X2", wgpu::VertexFormat::Float32x2)
        .value("FLOAT32X3", wgpu::VertexFormat::Float32x3)
        .value("FLOAT32X4", wgpu::VertexFormat::Float32x4)
        .value("UINT32", wgpu::VertexFormat::Uint32)
        .value("UINT32X2", wgpu::VertexFormat::Uint32x2)
        .value("UINT32X3", wgpu::VertexFormat::Uint32x3)
        .value("UINT32X4", wgpu::VertexFormat::Uint32x4)
        .value("SINT32", wgpu::VertexFormat::Sint32)
        .value("SINT32X2", wgpu::VertexFormat::Sint32x2)
        .value("SINT32X3", wgpu::VertexFormat::Sint32x3)
        .value("SINT32X4", wgpu::VertexFormat::Sint32x4)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::VertexFormat, VertexFormat)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::VertexStepMode, VertexStepMode)
    VertexStepMode
        .value("VERTEX", wgpu::VertexStepMode::Vertex)
        .value("INSTANCE", wgpu::VertexStepMode::Instance)
        .value("VERTEX_BUFFER_NOT_USED", wgpu::VertexStepMode::VertexBufferNotUsed)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::VertexStepMode, VertexStepMode)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::BufferUsage, BufferUsage)
    BufferUsage
        .value("NONE", wgpu::BufferUsage::None)
        .value("MAP_READ", wgpu::BufferUsage::MapRead)
        .value("MAP_WRITE", wgpu::BufferUsage::MapWrite)
        .value("COPY_SRC", wgpu::BufferUsage::CopySrc)
        .value("COPY_DST", wgpu::BufferUsage::CopyDst)
        .value("INDEX", wgpu::BufferUsage::Index)
        .value("VERTEX", wgpu::BufferUsage::Vertex)
        .value("UNIFORM", wgpu::BufferUsage::Uniform)
        .value("STORAGE", wgpu::BufferUsage::Storage)
        .value("INDIRECT", wgpu::BufferUsage::Indirect)
        .value("QUERY_RESOLVE", wgpu::BufferUsage::QueryResolve)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::BufferUsage, BufferUsage)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::ColorWriteMask, ColorWriteMask)
    ColorWriteMask
        .value("NONE", wgpu::ColorWriteMask::None)
        .value("RED", wgpu::ColorWriteMask::Red)
        .value("GREEN", wgpu::ColorWriteMask::Green)
        .value("BLUE", wgpu::ColorWriteMask::Blue)
        .value("ALPHA", wgpu::ColorWriteMask::Alpha)
        .value("ALL", wgpu::ColorWriteMask::All)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::ColorWriteMask, ColorWriteMask)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::MapMode, MapMode)
    MapMode
        .value("NONE", wgpu::MapMode::None)
        .value("READ", wgpu::MapMode::Read)
        .value("WRITE", wgpu::MapMode::Write)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::MapMode, MapMode)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::ShaderStage, ShaderStage)
    ShaderStage
        .value("NONE", wgpu::ShaderStage::None)
        .value("VERTEX", wgpu::ShaderStage::Vertex)
        .value("FRAGMENT", wgpu::ShaderStage::Fragment)
        .value("COMPUTE", wgpu::ShaderStage::Compute)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::ShaderStage, ShaderStage)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::TextureUsage, TextureUsage)
    TextureUsage
        .value("NONE", wgpu::TextureUsage::None)
        .value("COPY_SRC", wgpu::TextureUsage::CopySrc)
        .value("COPY_DST", wgpu::TextureUsage::CopyDst)
        .value("TEXTURE_BINDING", wgpu::TextureUsage::TextureBinding)
        .value("STORAGE_BINDING", wgpu::TextureUsage::StorageBinding)
        .value("RENDER_ATTACHMENT", wgpu::TextureUsage::RenderAttachment)
        .value("PRESENT", wgpu::TextureUsage::Present)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::TextureUsage, TextureUsage)


    PYCLASS_BEGIN(_wgpu, wgpu::Adapter, Adapter)

        Adapter.def("create_device", &wgpu::Adapter::CreateDevice
        , py::arg("descriptor") = nullptr
        , py::return_value_policy::automatic_reference);

        Adapter.def("enumerate_features", &wgpu::Adapter::EnumerateFeatures
        , py::arg("features")
        , py::return_value_policy::automatic_reference);

        Adapter.def("get_limits", &wgpu::Adapter::GetLimits
        , py::arg("limits")
        , py::return_value_policy::automatic_reference);

        Adapter.def("get_properties", &wgpu::Adapter::GetProperties
        , py::arg("properties")
        , py::return_value_policy::automatic_reference);

        Adapter.def("has_feature", &wgpu::Adapter::HasFeature
        , py::arg("feature")
        , py::return_value_policy::automatic_reference);

        Adapter.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::Adapter, Adapter)

    PYCLASS_BEGIN(_wgpu, wgpu::BindGroup, BindGroup)

        BindGroup.def("set_label", &wgpu::BindGroup::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

        BindGroup.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::BindGroup, BindGroup)

    PYCLASS_BEGIN(_wgpu, wgpu::BindGroupLayout, BindGroupLayout)

        BindGroupLayout.def("set_label", &wgpu::BindGroupLayout::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

        BindGroupLayout.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::BindGroupLayout, BindGroupLayout)

    PYCLASS_BEGIN(_wgpu, wgpu::Buffer, Buffer)

        Buffer.def("destroy", &wgpu::Buffer::Destroy
        , py::return_value_policy::automatic_reference);

        Buffer.def("get_const_mapped_range", &wgpu::Buffer::GetConstMappedRange
        , py::arg("offset") = 0
        , py::arg("size") = WGPU_WHOLE_MAP_SIZE
        , py::return_value_policy::automatic_reference);

        Buffer.def("get_mapped_range", &wgpu::Buffer::GetMappedRange
        , py::arg("offset") = 0
        , py::arg("size") = WGPU_WHOLE_MAP_SIZE
        , py::return_value_policy::automatic_reference);

        Buffer.def("get_size", &wgpu::Buffer::GetSize
        , py::return_value_policy::automatic_reference);

        Buffer.def("get_usage", &wgpu::Buffer::GetUsage
        , py::return_value_policy::automatic_reference);

        Buffer.def("set_label", &wgpu::Buffer::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

        Buffer.def("unmap", &wgpu::Buffer::Unmap
        , py::return_value_policy::automatic_reference);

        Buffer.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::Buffer, Buffer)

    PYCLASS_BEGIN(_wgpu, wgpu::CommandBuffer, CommandBuffer)

        CommandBuffer.def("set_label", &wgpu::CommandBuffer::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

        CommandBuffer.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::CommandBuffer, CommandBuffer)

    PYCLASS_BEGIN(_wgpu, wgpu::CommandEncoder, CommandEncoder)

        CommandEncoder.def("begin_compute_pass", &wgpu::CommandEncoder::BeginComputePass
        , py::arg("descriptor") = nullptr
        , py::return_value_policy::automatic_reference);

        CommandEncoder.def("begin_render_pass", &wgpu::CommandEncoder::BeginRenderPass
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference);

        CommandEncoder.def("clear_buffer", &wgpu::CommandEncoder::ClearBuffer
        , py::arg("buffer")
        , py::arg("offset") = 0
        , py::arg("size") = WGPU_WHOLE_SIZE
        , py::return_value_policy::automatic_reference);

        CommandEncoder.def("copy_buffer_to_buffer", &wgpu::CommandEncoder::CopyBufferToBuffer
        , py::arg("source")
        , py::arg("source_offset")
        , py::arg("destination")
        , py::arg("destination_offset")
        , py::arg("size")
        , py::return_value_policy::automatic_reference);

        CommandEncoder.def("copy_buffer_to_texture", &wgpu::CommandEncoder::CopyBufferToTexture
        , py::arg("source")
        , py::arg("destination")
        , py::arg("copy_size")
        , py::return_value_policy::automatic_reference);

        CommandEncoder.def("copy_texture_to_buffer", &wgpu::CommandEncoder::CopyTextureToBuffer
        , py::arg("source")
        , py::arg("destination")
        , py::arg("copy_size")
        , py::return_value_policy::automatic_reference);

        CommandEncoder.def("copy_texture_to_texture", &wgpu::CommandEncoder::CopyTextureToTexture
        , py::arg("source")
        , py::arg("destination")
        , py::arg("copy_size")
        , py::return_value_policy::automatic_reference);

        CommandEncoder.def("copy_texture_to_texture_internal", &wgpu::CommandEncoder::CopyTextureToTextureInternal
        , py::arg("source")
        , py::arg("destination")
        , py::arg("copy_size")
        , py::return_value_policy::automatic_reference);

        CommandEncoder.def("finish", &wgpu::CommandEncoder::Finish
        , py::arg("descriptor") = nullptr
        , py::return_value_policy::automatic_reference);

        CommandEncoder.def("inject_validation_error", &wgpu::CommandEncoder::InjectValidationError
        , py::arg("message")
        , py::return_value_policy::automatic_reference);

        CommandEncoder.def("insert_debug_marker", &wgpu::CommandEncoder::InsertDebugMarker
        , py::arg("marker_label")
        , py::return_value_policy::automatic_reference);

        CommandEncoder.def("pop_debug_group", &wgpu::CommandEncoder::PopDebugGroup
        , py::return_value_policy::automatic_reference);

        CommandEncoder.def("push_debug_group", &wgpu::CommandEncoder::PushDebugGroup
        , py::arg("group_label")
        , py::return_value_policy::automatic_reference);

        CommandEncoder.def("resolve_query_set", &wgpu::CommandEncoder::ResolveQuerySet
        , py::arg("query_set")
        , py::arg("first_query")
        , py::arg("query_count")
        , py::arg("destination")
        , py::arg("destination_offset")
        , py::return_value_policy::automatic_reference);

        CommandEncoder.def("set_label", &wgpu::CommandEncoder::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

        CommandEncoder.def("write_buffer", &wgpu::CommandEncoder::WriteBuffer
        , py::arg("buffer")
        , py::arg("buffer_offset")
        , py::arg("data")
        , py::arg("size")
        , py::return_value_policy::automatic_reference);

        CommandEncoder.def("write_timestamp", &wgpu::CommandEncoder::WriteTimestamp
        , py::arg("query_set")
        , py::arg("query_index")
        , py::return_value_policy::automatic_reference);

        CommandEncoder.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::CommandEncoder, CommandEncoder)

    PYCLASS_BEGIN(_wgpu, wgpu::ComputePassEncoder, ComputePassEncoder)

        ComputePassEncoder.def("dispatch", &wgpu::ComputePassEncoder::Dispatch
        , py::arg("workgroup_count_x")
        , py::arg("workgroup_count_y") = 1
        , py::arg("workgroup_count_z") = 1
        , py::return_value_policy::automatic_reference);

        ComputePassEncoder.def("dispatch_indirect", &wgpu::ComputePassEncoder::DispatchIndirect
        , py::arg("indirect_buffer")
        , py::arg("indirect_offset")
        , py::return_value_policy::automatic_reference);

        ComputePassEncoder.def("dispatch_workgroups", &wgpu::ComputePassEncoder::DispatchWorkgroups
        , py::arg("workgroup_count_x")
        , py::arg("workgroup_count_y") = 1
        , py::arg("workgroup_count_z") = 1
        , py::return_value_policy::automatic_reference);

        ComputePassEncoder.def("dispatch_workgroups_indirect", &wgpu::ComputePassEncoder::DispatchWorkgroupsIndirect
        , py::arg("indirect_buffer")
        , py::arg("indirect_offset")
        , py::return_value_policy::automatic_reference);

        ComputePassEncoder.def("end", &wgpu::ComputePassEncoder::End
        , py::return_value_policy::automatic_reference);

        ComputePassEncoder.def("end_pass", &wgpu::ComputePassEncoder::EndPass
        , py::return_value_policy::automatic_reference);

        ComputePassEncoder.def("insert_debug_marker", &wgpu::ComputePassEncoder::InsertDebugMarker
        , py::arg("marker_label")
        , py::return_value_policy::automatic_reference);

        ComputePassEncoder.def("pop_debug_group", &wgpu::ComputePassEncoder::PopDebugGroup
        , py::return_value_policy::automatic_reference);

        ComputePassEncoder.def("push_debug_group", &wgpu::ComputePassEncoder::PushDebugGroup
        , py::arg("group_label")
        , py::return_value_policy::automatic_reference);

        ComputePassEncoder.def("set_bind_group", &wgpu::ComputePassEncoder::SetBindGroup
        , py::arg("group_index")
        , py::arg("group")
        , py::arg("dynamic_offset_count") = 0
        , py::arg("dynamic_offsets") = nullptr
        , py::return_value_policy::automatic_reference);

        ComputePassEncoder.def("set_label", &wgpu::ComputePassEncoder::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

        ComputePassEncoder.def("set_pipeline", &wgpu::ComputePassEncoder::SetPipeline
        , py::arg("pipeline")
        , py::return_value_policy::automatic_reference);

        ComputePassEncoder.def("write_timestamp", &wgpu::ComputePassEncoder::WriteTimestamp
        , py::arg("query_set")
        , py::arg("query_index")
        , py::return_value_policy::automatic_reference);

        ComputePassEncoder.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::ComputePassEncoder, ComputePassEncoder)

    PYCLASS_BEGIN(_wgpu, wgpu::ComputePipeline, ComputePipeline)

        ComputePipeline.def("get_bind_group_layout", &wgpu::ComputePipeline::GetBindGroupLayout
        , py::arg("group_index")
        , py::return_value_policy::automatic_reference);

        ComputePipeline.def("set_label", &wgpu::ComputePipeline::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

        ComputePipeline.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::ComputePipeline, ComputePipeline)

    PYCLASS_BEGIN(_wgpu, wgpu::Device, Device)

        Device.def("create_bind_group", &wgpu::Device::CreateBindGroup
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference);

        Device.def("create_bind_group_layout", &wgpu::Device::CreateBindGroupLayout
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference);

        Device.def("create_buffer", &wgpu::Device::CreateBuffer
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference);

        Device.def("create_command_encoder", &wgpu::Device::CreateCommandEncoder
        , py::arg("descriptor") = nullptr
        , py::return_value_policy::automatic_reference);

        Device.def("create_compute_pipeline", &wgpu::Device::CreateComputePipeline
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference);

        Device.def("create_error_buffer", &wgpu::Device::CreateErrorBuffer
        , py::return_value_policy::automatic_reference);

        Device.def("create_error_external_texture", &wgpu::Device::CreateErrorExternalTexture
        , py::return_value_policy::automatic_reference);

        Device.def("create_error_texture", &wgpu::Device::CreateErrorTexture
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference);

        Device.def("create_external_texture", &wgpu::Device::CreateExternalTexture
        , py::arg("external_texture_descriptor")
        , py::return_value_policy::automatic_reference);

        Device.def("create_pipeline_layout", &wgpu::Device::CreatePipelineLayout
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference);

        Device.def("create_query_set", &wgpu::Device::CreateQuerySet
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference);

        Device.def("create_render_bundle_encoder", &wgpu::Device::CreateRenderBundleEncoder
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference);

        Device.def("create_render_pipeline", &wgpu::Device::CreateRenderPipeline
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference);

        Device.def("create_sampler", &wgpu::Device::CreateSampler
        , py::arg("descriptor") = nullptr
        , py::return_value_policy::automatic_reference);

        Device.def("create_shader_module", &wgpu::Device::CreateShaderModule
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference);

        Device.def("create_swap_chain", &wgpu::Device::CreateSwapChain
        , py::arg("surface")
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference);

        Device.def("create_texture", &wgpu::Device::CreateTexture
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference);

        Device.def("destroy", &wgpu::Device::Destroy
        , py::return_value_policy::automatic_reference);

        Device.def("enumerate_features", &wgpu::Device::EnumerateFeatures
        , py::arg("features")
        , py::return_value_policy::automatic_reference);

        Device.def("get_adapter", &wgpu::Device::GetAdapter
        , py::return_value_policy::automatic_reference);

        Device.def("get_limits", &wgpu::Device::GetLimits
        , py::arg("limits")
        , py::return_value_policy::automatic_reference);

        Device.def("get_queue", &wgpu::Device::GetQueue
        , py::return_value_policy::automatic_reference);

        Device.def("has_feature", &wgpu::Device::HasFeature
        , py::arg("feature")
        , py::return_value_policy::automatic_reference);

        Device.def("inject_error", &wgpu::Device::InjectError
        , py::arg("type")
        , py::arg("message")
        , py::return_value_policy::automatic_reference);

        Device.def("lose_for_testing", &wgpu::Device::LoseForTesting
        , py::return_value_policy::automatic_reference);

        Device.def("push_error_scope", &wgpu::Device::PushErrorScope
        , py::arg("filter")
        , py::return_value_policy::automatic_reference);

        Device.def("set_label", &wgpu::Device::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

        Device.def("tick", &wgpu::Device::Tick
        , py::return_value_policy::automatic_reference);

        Device.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::Device, Device)

    PYCLASS_BEGIN(_wgpu, wgpu::ExternalTexture, ExternalTexture)

        ExternalTexture.def("destroy", &wgpu::ExternalTexture::Destroy
        , py::return_value_policy::automatic_reference);

        ExternalTexture.def("set_label", &wgpu::ExternalTexture::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

        ExternalTexture.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::ExternalTexture, ExternalTexture)

    PYCLASS_BEGIN(_wgpu, wgpu::Instance, Instance)

        Instance.def("create_surface", &wgpu::Instance::CreateSurface
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference);

        Instance.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::Instance, Instance)

    PYCLASS_BEGIN(_wgpu, wgpu::PipelineLayout, PipelineLayout)

        PipelineLayout.def("set_label", &wgpu::PipelineLayout::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

        PipelineLayout.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::PipelineLayout, PipelineLayout)

    PYCLASS_BEGIN(_wgpu, wgpu::QuerySet, QuerySet)

        QuerySet.def("destroy", &wgpu::QuerySet::Destroy
        , py::return_value_policy::automatic_reference);

        QuerySet.def("get_count", &wgpu::QuerySet::GetCount
        , py::return_value_policy::automatic_reference);

        QuerySet.def("get_type", &wgpu::QuerySet::GetType
        , py::return_value_policy::automatic_reference);

        QuerySet.def("set_label", &wgpu::QuerySet::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

        QuerySet.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::QuerySet, QuerySet)

    PYCLASS_BEGIN(_wgpu, wgpu::Queue, Queue)

        Queue.def("copy_texture_for_browser", &wgpu::Queue::CopyTextureForBrowser
        , py::arg("source")
        , py::arg("destination")
        , py::arg("copy_size")
        , py::arg("options")
        , py::return_value_policy::automatic_reference);

        Queue.def("set_label", &wgpu::Queue::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

        Queue.def("submit", &wgpu::Queue::Submit
        , py::arg("command_count")
        , py::arg("commands")
        , py::return_value_policy::automatic_reference);

        Queue.def("write_buffer", &wgpu::Queue::WriteBuffer
        , py::arg("buffer")
        , py::arg("buffer_offset")
        , py::arg("data")
        , py::arg("size")
        , py::return_value_policy::automatic_reference);

        Queue.def("write_texture", &wgpu::Queue::WriteTexture
        , py::arg("destination")
        , py::arg("data")
        , py::arg("data_size")
        , py::arg("data_layout")
        , py::arg("write_size")
        , py::return_value_policy::automatic_reference);

        Queue.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::Queue, Queue)

    PYCLASS_BEGIN(_wgpu, wgpu::RenderBundle, RenderBundle)

        RenderBundle.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::RenderBundle, RenderBundle)

    PYCLASS_BEGIN(_wgpu, wgpu::RenderBundleEncoder, RenderBundleEncoder)

        RenderBundleEncoder.def("draw", &wgpu::RenderBundleEncoder::Draw
        , py::arg("vertex_count")
        , py::arg("instance_count") = 1
        , py::arg("first_vertex") = 0
        , py::arg("first_instance") = 0
        , py::return_value_policy::automatic_reference);

        RenderBundleEncoder.def("draw_indexed", &wgpu::RenderBundleEncoder::DrawIndexed
        , py::arg("index_count")
        , py::arg("instance_count") = 1
        , py::arg("first_index") = 0
        , py::arg("base_vertex") = 0
        , py::arg("first_instance") = 0
        , py::return_value_policy::automatic_reference);

        RenderBundleEncoder.def("draw_indexed_indirect", &wgpu::RenderBundleEncoder::DrawIndexedIndirect
        , py::arg("indirect_buffer")
        , py::arg("indirect_offset")
        , py::return_value_policy::automatic_reference);

        RenderBundleEncoder.def("draw_indirect", &wgpu::RenderBundleEncoder::DrawIndirect
        , py::arg("indirect_buffer")
        , py::arg("indirect_offset")
        , py::return_value_policy::automatic_reference);

        RenderBundleEncoder.def("finish", &wgpu::RenderBundleEncoder::Finish
        , py::arg("descriptor") = nullptr
        , py::return_value_policy::automatic_reference);

        RenderBundleEncoder.def("insert_debug_marker", &wgpu::RenderBundleEncoder::InsertDebugMarker
        , py::arg("marker_label")
        , py::return_value_policy::automatic_reference);

        RenderBundleEncoder.def("pop_debug_group", &wgpu::RenderBundleEncoder::PopDebugGroup
        , py::return_value_policy::automatic_reference);

        RenderBundleEncoder.def("push_debug_group", &wgpu::RenderBundleEncoder::PushDebugGroup
        , py::arg("group_label")
        , py::return_value_policy::automatic_reference);

        RenderBundleEncoder.def("set_bind_group", &wgpu::RenderBundleEncoder::SetBindGroup
        , py::arg("group_index")
        , py::arg("group")
        , py::arg("dynamic_offset_count") = 0
        , py::arg("dynamic_offsets") = nullptr
        , py::return_value_policy::automatic_reference);

        RenderBundleEncoder.def("set_index_buffer", &wgpu::RenderBundleEncoder::SetIndexBuffer
        , py::arg("buffer")
        , py::arg("format")
        , py::arg("offset") = 0
        , py::arg("size") = WGPU_WHOLE_SIZE
        , py::return_value_policy::automatic_reference);

        RenderBundleEncoder.def("set_label", &wgpu::RenderBundleEncoder::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

        RenderBundleEncoder.def("set_pipeline", &wgpu::RenderBundleEncoder::SetPipeline
        , py::arg("pipeline")
        , py::return_value_policy::automatic_reference);

        RenderBundleEncoder.def("set_vertex_buffer", &wgpu::RenderBundleEncoder::SetVertexBuffer
        , py::arg("slot")
        , py::arg("buffer")
        , py::arg("offset") = 0
        , py::arg("size") = WGPU_WHOLE_SIZE
        , py::return_value_policy::automatic_reference);

        RenderBundleEncoder.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::RenderBundleEncoder, RenderBundleEncoder)

    PYCLASS_BEGIN(_wgpu, wgpu::RenderPassEncoder, RenderPassEncoder)

        RenderPassEncoder.def("begin_occlusion_query", &wgpu::RenderPassEncoder::BeginOcclusionQuery
        , py::arg("query_index")
        , py::return_value_policy::automatic_reference);

        RenderPassEncoder.def("draw", &wgpu::RenderPassEncoder::Draw
        , py::arg("vertex_count")
        , py::arg("instance_count") = 1
        , py::arg("first_vertex") = 0
        , py::arg("first_instance") = 0
        , py::return_value_policy::automatic_reference);

        RenderPassEncoder.def("draw_indexed", &wgpu::RenderPassEncoder::DrawIndexed
        , py::arg("index_count")
        , py::arg("instance_count") = 1
        , py::arg("first_index") = 0
        , py::arg("base_vertex") = 0
        , py::arg("first_instance") = 0
        , py::return_value_policy::automatic_reference);

        RenderPassEncoder.def("draw_indexed_indirect", &wgpu::RenderPassEncoder::DrawIndexedIndirect
        , py::arg("indirect_buffer")
        , py::arg("indirect_offset")
        , py::return_value_policy::automatic_reference);

        RenderPassEncoder.def("draw_indirect", &wgpu::RenderPassEncoder::DrawIndirect
        , py::arg("indirect_buffer")
        , py::arg("indirect_offset")
        , py::return_value_policy::automatic_reference);

        RenderPassEncoder.def("end", &wgpu::RenderPassEncoder::End
        , py::return_value_policy::automatic_reference);

        RenderPassEncoder.def("end_occlusion_query", &wgpu::RenderPassEncoder::EndOcclusionQuery
        , py::return_value_policy::automatic_reference);

        RenderPassEncoder.def("end_pass", &wgpu::RenderPassEncoder::EndPass
        , py::return_value_policy::automatic_reference);

        RenderPassEncoder.def("execute_bundles", &wgpu::RenderPassEncoder::ExecuteBundles
        , py::arg("bundles_count")
        , py::arg("bundles")
        , py::return_value_policy::automatic_reference);

        RenderPassEncoder.def("insert_debug_marker", &wgpu::RenderPassEncoder::InsertDebugMarker
        , py::arg("marker_label")
        , py::return_value_policy::automatic_reference);

        RenderPassEncoder.def("pop_debug_group", &wgpu::RenderPassEncoder::PopDebugGroup
        , py::return_value_policy::automatic_reference);

        RenderPassEncoder.def("push_debug_group", &wgpu::RenderPassEncoder::PushDebugGroup
        , py::arg("group_label")
        , py::return_value_policy::automatic_reference);

        RenderPassEncoder.def("set_blend_constant", &wgpu::RenderPassEncoder::SetBlendConstant
        , py::arg("color")
        , py::return_value_policy::automatic_reference);

        RenderPassEncoder.def("set_index_buffer", &wgpu::RenderPassEncoder::SetIndexBuffer
        , py::arg("buffer")
        , py::arg("format")
        , py::arg("offset") = 0
        , py::arg("size") = WGPU_WHOLE_SIZE
        , py::return_value_policy::automatic_reference);

        RenderPassEncoder.def("set_label", &wgpu::RenderPassEncoder::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

        RenderPassEncoder.def("set_pipeline", &wgpu::RenderPassEncoder::SetPipeline
        , py::arg("pipeline")
        , py::return_value_policy::automatic_reference);

        RenderPassEncoder.def("set_scissor_rect", &wgpu::RenderPassEncoder::SetScissorRect
        , py::arg("x")
        , py::arg("y")
        , py::arg("width")
        , py::arg("height")
        , py::return_value_policy::automatic_reference);

        RenderPassEncoder.def("set_stencil_reference", &wgpu::RenderPassEncoder::SetStencilReference
        , py::arg("reference")
        , py::return_value_policy::automatic_reference);

        RenderPassEncoder.def("set_vertex_buffer", &wgpu::RenderPassEncoder::SetVertexBuffer
        , py::arg("slot")
        , py::arg("buffer")
        , py::arg("offset") = 0
        , py::arg("size") = WGPU_WHOLE_SIZE
        , py::return_value_policy::automatic_reference);

        RenderPassEncoder.def("set_viewport", &wgpu::RenderPassEncoder::SetViewport
        , py::arg("x")
        , py::arg("y")
        , py::arg("width")
        , py::arg("height")
        , py::arg("min_depth")
        , py::arg("max_depth")
        , py::return_value_policy::automatic_reference);

        RenderPassEncoder.def("write_timestamp", &wgpu::RenderPassEncoder::WriteTimestamp
        , py::arg("query_set")
        , py::arg("query_index")
        , py::return_value_policy::automatic_reference);

        RenderPassEncoder.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::RenderPassEncoder, RenderPassEncoder)

    PYCLASS_BEGIN(_wgpu, wgpu::RenderPipeline, RenderPipeline)

        RenderPipeline.def("get_bind_group_layout", &wgpu::RenderPipeline::GetBindGroupLayout
        , py::arg("group_index")
        , py::return_value_policy::automatic_reference);

        RenderPipeline.def("set_label", &wgpu::RenderPipeline::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

        RenderPipeline.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::RenderPipeline, RenderPipeline)

    PYCLASS_BEGIN(_wgpu, wgpu::Sampler, Sampler)

        Sampler.def("set_label", &wgpu::Sampler::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

        Sampler.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::Sampler, Sampler)

    PYCLASS_BEGIN(_wgpu, wgpu::ShaderModule, ShaderModule)

        ShaderModule.def("set_label", &wgpu::ShaderModule::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

        ShaderModule.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::ShaderModule, ShaderModule)

    PYCLASS_BEGIN(_wgpu, wgpu::Surface, Surface)

        Surface.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::Surface, Surface)

    PYCLASS_BEGIN(_wgpu, wgpu::SwapChain, SwapChain)

        SwapChain.def("configure", &wgpu::SwapChain::Configure
        , py::arg("format")
        , py::arg("allowed_usage")
        , py::arg("width")
        , py::arg("height")
        , py::return_value_policy::automatic_reference);

        SwapChain.def("get_current_texture_view", &wgpu::SwapChain::GetCurrentTextureView
        , py::return_value_policy::automatic_reference);

        SwapChain.def("present", &wgpu::SwapChain::Present
        , py::return_value_policy::automatic_reference);

        SwapChain.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::SwapChain, SwapChain)

    PYCLASS_BEGIN(_wgpu, wgpu::Texture, Texture)

        Texture.def("create_view", &wgpu::Texture::CreateView
        , py::arg("descriptor") = nullptr
        , py::return_value_policy::automatic_reference);

        Texture.def("destroy", &wgpu::Texture::Destroy
        , py::return_value_policy::automatic_reference);

        Texture.def("get_depth_or_array_layers", &wgpu::Texture::GetDepthOrArrayLayers
        , py::return_value_policy::automatic_reference);

        Texture.def("get_dimension", &wgpu::Texture::GetDimension
        , py::return_value_policy::automatic_reference);

        Texture.def("get_format", &wgpu::Texture::GetFormat
        , py::return_value_policy::automatic_reference);

        Texture.def("get_height", &wgpu::Texture::GetHeight
        , py::return_value_policy::automatic_reference);

        Texture.def("get_mip_level_count", &wgpu::Texture::GetMipLevelCount
        , py::return_value_policy::automatic_reference);

        Texture.def("get_sample_count", &wgpu::Texture::GetSampleCount
        , py::return_value_policy::automatic_reference);

        Texture.def("get_usage", &wgpu::Texture::GetUsage
        , py::return_value_policy::automatic_reference);

        Texture.def("get_width", &wgpu::Texture::GetWidth
        , py::return_value_policy::automatic_reference);

        Texture.def("set_label", &wgpu::Texture::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

        Texture.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::Texture, Texture)

    PYCLASS_BEGIN(_wgpu, wgpu::TextureView, TextureView)

        TextureView.def("set_label", &wgpu::TextureView::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

        TextureView.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::TextureView, TextureView)

    _wgpu.def("create_instance", &wgpu::CreateInstance
    , py::arg("descriptor") = nullptr
    , py::return_value_policy::automatic_reference);

    _wgpu.def("get_proc_address", &wgpu::GetProcAddress
    , py::arg("device")
    , py::arg("proc_name")
    , py::return_value_policy::automatic_reference);

    PYCLASS_BEGIN(_wgpu, wgpu::ChainedStruct, ChainedStruct)

        ChainedStruct.def_readwrite("next_in_chain", &wgpu::ChainedStruct::nextInChain);
        ChainedStruct.def_readwrite("s_type", &wgpu::ChainedStruct::sType);
        ChainedStruct.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::ChainedStruct, ChainedStruct)

    PYCLASS_BEGIN(_wgpu, wgpu::ChainedStructOut, ChainedStructOut)

        ChainedStructOut.def_readwrite("next_in_chain", &wgpu::ChainedStructOut::nextInChain);
        ChainedStructOut.def_readwrite("s_type", &wgpu::ChainedStructOut::sType);
        ChainedStructOut.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::ChainedStructOut, ChainedStructOut)

    PYCLASS_BEGIN(_wgpu, wgpu::AdapterProperties, AdapterProperties)

        AdapterProperties.def_readwrite("next_in_chain", &wgpu::AdapterProperties::nextInChain);
        AdapterProperties.def_readwrite("vendor_id", &wgpu::AdapterProperties::vendorID);
        AdapterProperties.def_property("vendor_name",
            [](const wgpu::AdapterProperties& self){ return self.vendorName; },[](wgpu::AdapterProperties& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.vendorName = c; }
        );
        AdapterProperties.def_property("architecture",
            [](const wgpu::AdapterProperties& self){ return self.architecture; },[](wgpu::AdapterProperties& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.architecture = c; }
        );
        AdapterProperties.def_readwrite("device_id", &wgpu::AdapterProperties::deviceID);
        AdapterProperties.def_property("name",
            [](const wgpu::AdapterProperties& self){ return self.name; },[](wgpu::AdapterProperties& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.name = c; }
        );
        AdapterProperties.def_property("driver_description",
            [](const wgpu::AdapterProperties& self){ return self.driverDescription; },[](wgpu::AdapterProperties& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.driverDescription = c; }
        );
        AdapterProperties.def_readwrite("adapter_type", &wgpu::AdapterProperties::adapterType);
        AdapterProperties.def_readwrite("backend_type", &wgpu::AdapterProperties::backendType);
        AdapterProperties.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::AdapterProperties, AdapterProperties)

    PYCLASS_BEGIN(_wgpu, wgpu::BindGroupEntry, BindGroupEntry)

        BindGroupEntry.def_readwrite("next_in_chain", &wgpu::BindGroupEntry::nextInChain);
        BindGroupEntry.def_readwrite("binding", &wgpu::BindGroupEntry::binding);
        BindGroupEntry.def_readwrite("buffer", &wgpu::BindGroupEntry::buffer);
        BindGroupEntry.def_readwrite("offset", &wgpu::BindGroupEntry::offset);
        BindGroupEntry.def_readwrite("size", &wgpu::BindGroupEntry::size);
        BindGroupEntry.def_readwrite("sampler", &wgpu::BindGroupEntry::sampler);
        BindGroupEntry.def_readwrite("texture_view", &wgpu::BindGroupEntry::textureView);
        BindGroupEntry.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::BindGroupEntry, BindGroupEntry)

    PYCLASS_BEGIN(_wgpu, wgpu::BlendComponent, BlendComponent)

        BlendComponent.def_readwrite("operation", &wgpu::BlendComponent::operation);
        BlendComponent.def_readwrite("src_factor", &wgpu::BlendComponent::srcFactor);
        BlendComponent.def_readwrite("dst_factor", &wgpu::BlendComponent::dstFactor);
        BlendComponent.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::BlendComponent, BlendComponent)

    PYCLASS_BEGIN(_wgpu, wgpu::BufferBindingLayout, BufferBindingLayout)

        BufferBindingLayout.def_readwrite("next_in_chain", &wgpu::BufferBindingLayout::nextInChain);
        BufferBindingLayout.def_readwrite("type", &wgpu::BufferBindingLayout::type);
        BufferBindingLayout.def_readwrite("has_dynamic_offset", &wgpu::BufferBindingLayout::hasDynamicOffset);
        BufferBindingLayout.def_readwrite("min_binding_size", &wgpu::BufferBindingLayout::minBindingSize);
        BufferBindingLayout.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::BufferBindingLayout, BufferBindingLayout)

    PYCLASS_BEGIN(_wgpu, wgpu::BufferDescriptor, BufferDescriptor)

        BufferDescriptor.def_readwrite("next_in_chain", &wgpu::BufferDescriptor::nextInChain);
        BufferDescriptor.def_property("label",
            [](const wgpu::BufferDescriptor& self){ return self.label; },[](wgpu::BufferDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        BufferDescriptor.def_readwrite("usage", &wgpu::BufferDescriptor::usage);
        BufferDescriptor.def_readwrite("size", &wgpu::BufferDescriptor::size);
        BufferDescriptor.def_readwrite("mapped_at_creation", &wgpu::BufferDescriptor::mappedAtCreation);
        BufferDescriptor.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::BufferDescriptor, BufferDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::Color, Color)

        Color.def_readwrite("r", &wgpu::Color::r);
        Color.def_readwrite("g", &wgpu::Color::g);
        Color.def_readwrite("b", &wgpu::Color::b);
        Color.def_readwrite("a", &wgpu::Color::a);
        Color.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::Color, Color)

    PYCLASS_BEGIN(_wgpu, wgpu::CommandBufferDescriptor, CommandBufferDescriptor)

        CommandBufferDescriptor.def_readwrite("next_in_chain", &wgpu::CommandBufferDescriptor::nextInChain);
        CommandBufferDescriptor.def_property("label",
            [](const wgpu::CommandBufferDescriptor& self){ return self.label; },[](wgpu::CommandBufferDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        CommandBufferDescriptor.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::CommandBufferDescriptor, CommandBufferDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::CommandEncoderDescriptor, CommandEncoderDescriptor)

        CommandEncoderDescriptor.def_readwrite("next_in_chain", &wgpu::CommandEncoderDescriptor::nextInChain);
        CommandEncoderDescriptor.def_property("label",
            [](const wgpu::CommandEncoderDescriptor& self){ return self.label; },[](wgpu::CommandEncoderDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        CommandEncoderDescriptor.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::CommandEncoderDescriptor, CommandEncoderDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::CompilationMessage, CompilationMessage)

        CompilationMessage.def_readwrite("next_in_chain", &wgpu::CompilationMessage::nextInChain);
        CompilationMessage.def_property("message",
            [](const wgpu::CompilationMessage& self){ return self.message; },[](wgpu::CompilationMessage& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.message = c; }
        );
        CompilationMessage.def_readwrite("type", &wgpu::CompilationMessage::type);
        CompilationMessage.def_readwrite("line_num", &wgpu::CompilationMessage::lineNum);
        CompilationMessage.def_readwrite("line_pos", &wgpu::CompilationMessage::linePos);
        CompilationMessage.def_readwrite("offset", &wgpu::CompilationMessage::offset);
        CompilationMessage.def_readwrite("length", &wgpu::CompilationMessage::length);
        CompilationMessage.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::CompilationMessage, CompilationMessage)

    PYCLASS_BEGIN(_wgpu, wgpu::ComputePassTimestampWrite, ComputePassTimestampWrite)

        ComputePassTimestampWrite.def_readwrite("query_set", &wgpu::ComputePassTimestampWrite::querySet);
        ComputePassTimestampWrite.def_readwrite("query_index", &wgpu::ComputePassTimestampWrite::queryIndex);
        ComputePassTimestampWrite.def_readwrite("location", &wgpu::ComputePassTimestampWrite::location);
        ComputePassTimestampWrite.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::ComputePassTimestampWrite, ComputePassTimestampWrite)

    PYCLASS_BEGIN(_wgpu, wgpu::ConstantEntry, ConstantEntry)

        ConstantEntry.def_readwrite("next_in_chain", &wgpu::ConstantEntry::nextInChain);
        ConstantEntry.def_property("key",
            [](const wgpu::ConstantEntry& self){ return self.key; },[](wgpu::ConstantEntry& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.key = c; }
        );
        ConstantEntry.def_readwrite("value", &wgpu::ConstantEntry::value);
        ConstantEntry.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::ConstantEntry, ConstantEntry)

    PYCLASS_BEGIN(_wgpu, wgpu::CopyTextureForBrowserOptions, CopyTextureForBrowserOptions)

        CopyTextureForBrowserOptions.def_readwrite("next_in_chain", &wgpu::CopyTextureForBrowserOptions::nextInChain);
        CopyTextureForBrowserOptions.def_readwrite("flip_y", &wgpu::CopyTextureForBrowserOptions::flipY);
        CopyTextureForBrowserOptions.def_readwrite("needs_color_space_conversion", &wgpu::CopyTextureForBrowserOptions::needsColorSpaceConversion);
        CopyTextureForBrowserOptions.def_readwrite("src_alpha_mode", &wgpu::CopyTextureForBrowserOptions::srcAlphaMode);
        CopyTextureForBrowserOptions.def_readwrite("src_transfer_function_parameters", &wgpu::CopyTextureForBrowserOptions::srcTransferFunctionParameters);
        CopyTextureForBrowserOptions.def_readwrite("conversion_matrix", &wgpu::CopyTextureForBrowserOptions::conversionMatrix);
        CopyTextureForBrowserOptions.def_readwrite("dst_transfer_function_parameters", &wgpu::CopyTextureForBrowserOptions::dstTransferFunctionParameters);
        CopyTextureForBrowserOptions.def_readwrite("dst_alpha_mode", &wgpu::CopyTextureForBrowserOptions::dstAlphaMode);
        CopyTextureForBrowserOptions.def_readwrite("internal_usage", &wgpu::CopyTextureForBrowserOptions::internalUsage);
        CopyTextureForBrowserOptions.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::CopyTextureForBrowserOptions, CopyTextureForBrowserOptions)

    PYCLASS_INHERIT_BEGIN(_wgpu, wgpu::DawnCacheDeviceDescriptor, struct wgpu::ChainedStruct, DawnCacheDeviceDescriptor)

        DawnCacheDeviceDescriptor.def(py::init<>());
        DawnCacheDeviceDescriptor.def_property("isolation_key",
            [](const wgpu::DawnCacheDeviceDescriptor& self){ return self.isolationKey; },[](wgpu::DawnCacheDeviceDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.isolationKey = c; }
        );
    PYCLASS_END(_wgpu, wgpu::DawnCacheDeviceDescriptor, DawnCacheDeviceDescriptor)

    PYCLASS_INHERIT_BEGIN(_wgpu, wgpu::DawnEncoderInternalUsageDescriptor, struct wgpu::ChainedStruct, DawnEncoderInternalUsageDescriptor)

        DawnEncoderInternalUsageDescriptor.def(py::init<>());
        DawnEncoderInternalUsageDescriptor.def_readwrite("use_internal_usages", &wgpu::DawnEncoderInternalUsageDescriptor::useInternalUsages);
    PYCLASS_END(_wgpu, wgpu::DawnEncoderInternalUsageDescriptor, DawnEncoderInternalUsageDescriptor)

    PYCLASS_INHERIT_BEGIN(_wgpu, wgpu::DawnInstanceDescriptor, struct wgpu::ChainedStruct, DawnInstanceDescriptor)

        DawnInstanceDescriptor.def(py::init<>());
        DawnInstanceDescriptor.def_readwrite("additional_runtime_search_paths_count", &wgpu::DawnInstanceDescriptor::additionalRuntimeSearchPathsCount);
    PYCLASS_END(_wgpu, wgpu::DawnInstanceDescriptor, DawnInstanceDescriptor)

    PYCLASS_INHERIT_BEGIN(_wgpu, wgpu::DawnTextureInternalUsageDescriptor, struct wgpu::ChainedStruct, DawnTextureInternalUsageDescriptor)

        DawnTextureInternalUsageDescriptor.def(py::init<>());
        DawnTextureInternalUsageDescriptor.def_readwrite("internal_usage", &wgpu::DawnTextureInternalUsageDescriptor::internalUsage);
    PYCLASS_END(_wgpu, wgpu::DawnTextureInternalUsageDescriptor, DawnTextureInternalUsageDescriptor)

    PYCLASS_INHERIT_BEGIN(_wgpu, wgpu::DawnTogglesDeviceDescriptor, struct wgpu::ChainedStruct, DawnTogglesDeviceDescriptor)

        DawnTogglesDeviceDescriptor.def(py::init<>());
        DawnTogglesDeviceDescriptor.def_readwrite("force_enabled_toggles_count", &wgpu::DawnTogglesDeviceDescriptor::forceEnabledTogglesCount);
        DawnTogglesDeviceDescriptor.def_readwrite("force_disabled_toggles_count", &wgpu::DawnTogglesDeviceDescriptor::forceDisabledTogglesCount);
    PYCLASS_END(_wgpu, wgpu::DawnTogglesDeviceDescriptor, DawnTogglesDeviceDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::Extent3D, Extent3D)

        Extent3D.def_readwrite("width", &wgpu::Extent3D::width);
        Extent3D.def_readwrite("height", &wgpu::Extent3D::height);
        Extent3D.def_readwrite("depth_or_array_layers", &wgpu::Extent3D::depthOrArrayLayers);
        Extent3D.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::Extent3D, Extent3D)

    PYCLASS_INHERIT_BEGIN(_wgpu, wgpu::ExternalTextureBindingEntry, struct wgpu::ChainedStruct, ExternalTextureBindingEntry)

        ExternalTextureBindingEntry.def(py::init<>());
        ExternalTextureBindingEntry.def_readwrite("external_texture", &wgpu::ExternalTextureBindingEntry::externalTexture);
    PYCLASS_END(_wgpu, wgpu::ExternalTextureBindingEntry, ExternalTextureBindingEntry)

    PYCLASS_INHERIT_BEGIN(_wgpu, wgpu::ExternalTextureBindingLayout, struct wgpu::ChainedStruct, ExternalTextureBindingLayout)

        ExternalTextureBindingLayout.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::ExternalTextureBindingLayout, ExternalTextureBindingLayout)

    PYCLASS_BEGIN(_wgpu, wgpu::ExternalTextureDescriptor, ExternalTextureDescriptor)

        ExternalTextureDescriptor.def_readwrite("next_in_chain", &wgpu::ExternalTextureDescriptor::nextInChain);
        ExternalTextureDescriptor.def_property("label",
            [](const wgpu::ExternalTextureDescriptor& self){ return self.label; },[](wgpu::ExternalTextureDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        ExternalTextureDescriptor.def_readwrite("plane0", &wgpu::ExternalTextureDescriptor::plane0);
        ExternalTextureDescriptor.def_readwrite("plane1", &wgpu::ExternalTextureDescriptor::plane1);
        ExternalTextureDescriptor.def_readwrite("do_yuv_to_rgb_conversion_only", &wgpu::ExternalTextureDescriptor::doYuvToRgbConversionOnly);
        ExternalTextureDescriptor.def_readwrite("yuv_to_rgb_conversion_matrix", &wgpu::ExternalTextureDescriptor::yuvToRgbConversionMatrix);
        ExternalTextureDescriptor.def_readwrite("src_transfer_function_parameters", &wgpu::ExternalTextureDescriptor::srcTransferFunctionParameters);
        ExternalTextureDescriptor.def_readwrite("dst_transfer_function_parameters", &wgpu::ExternalTextureDescriptor::dstTransferFunctionParameters);
        ExternalTextureDescriptor.def_readwrite("gamut_conversion_matrix", &wgpu::ExternalTextureDescriptor::gamutConversionMatrix);
        ExternalTextureDescriptor.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::ExternalTextureDescriptor, ExternalTextureDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::InstanceDescriptor, InstanceDescriptor)

        InstanceDescriptor.def_readwrite("next_in_chain", &wgpu::InstanceDescriptor::nextInChain);
        InstanceDescriptor.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::InstanceDescriptor, InstanceDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::Limits, Limits)

        Limits.def_readwrite("max_texture_dimension1_d", &wgpu::Limits::maxTextureDimension1D);
        Limits.def_readwrite("max_texture_dimension2_d", &wgpu::Limits::maxTextureDimension2D);
        Limits.def_readwrite("max_texture_dimension3_d", &wgpu::Limits::maxTextureDimension3D);
        Limits.def_readwrite("max_texture_array_layers", &wgpu::Limits::maxTextureArrayLayers);
        Limits.def_readwrite("max_bind_groups", &wgpu::Limits::maxBindGroups);
        Limits.def_readwrite("max_dynamic_uniform_buffers_per_pipeline_layout", &wgpu::Limits::maxDynamicUniformBuffersPerPipelineLayout);
        Limits.def_readwrite("max_dynamic_storage_buffers_per_pipeline_layout", &wgpu::Limits::maxDynamicStorageBuffersPerPipelineLayout);
        Limits.def_readwrite("max_sampled_textures_per_shader_stage", &wgpu::Limits::maxSampledTexturesPerShaderStage);
        Limits.def_readwrite("max_samplers_per_shader_stage", &wgpu::Limits::maxSamplersPerShaderStage);
        Limits.def_readwrite("max_storage_buffers_per_shader_stage", &wgpu::Limits::maxStorageBuffersPerShaderStage);
        Limits.def_readwrite("max_storage_textures_per_shader_stage", &wgpu::Limits::maxStorageTexturesPerShaderStage);
        Limits.def_readwrite("max_uniform_buffers_per_shader_stage", &wgpu::Limits::maxUniformBuffersPerShaderStage);
        Limits.def_readwrite("max_uniform_buffer_binding_size", &wgpu::Limits::maxUniformBufferBindingSize);
        Limits.def_readwrite("max_storage_buffer_binding_size", &wgpu::Limits::maxStorageBufferBindingSize);
        Limits.def_readwrite("min_uniform_buffer_offset_alignment", &wgpu::Limits::minUniformBufferOffsetAlignment);
        Limits.def_readwrite("min_storage_buffer_offset_alignment", &wgpu::Limits::minStorageBufferOffsetAlignment);
        Limits.def_readwrite("max_vertex_buffers", &wgpu::Limits::maxVertexBuffers);
        Limits.def_readwrite("max_vertex_attributes", &wgpu::Limits::maxVertexAttributes);
        Limits.def_readwrite("max_vertex_buffer_array_stride", &wgpu::Limits::maxVertexBufferArrayStride);
        Limits.def_readwrite("max_inter_stage_shader_components", &wgpu::Limits::maxInterStageShaderComponents);
        Limits.def_readwrite("max_inter_stage_shader_variables", &wgpu::Limits::maxInterStageShaderVariables);
        Limits.def_readwrite("max_color_attachments", &wgpu::Limits::maxColorAttachments);
        Limits.def_readwrite("max_compute_workgroup_storage_size", &wgpu::Limits::maxComputeWorkgroupStorageSize);
        Limits.def_readwrite("max_compute_invocations_per_workgroup", &wgpu::Limits::maxComputeInvocationsPerWorkgroup);
        Limits.def_readwrite("max_compute_workgroup_size_x", &wgpu::Limits::maxComputeWorkgroupSizeX);
        Limits.def_readwrite("max_compute_workgroup_size_y", &wgpu::Limits::maxComputeWorkgroupSizeY);
        Limits.def_readwrite("max_compute_workgroup_size_z", &wgpu::Limits::maxComputeWorkgroupSizeZ);
        Limits.def_readwrite("max_compute_workgroups_per_dimension", &wgpu::Limits::maxComputeWorkgroupsPerDimension);
        Limits.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::Limits, Limits)

    PYCLASS_BEGIN(_wgpu, wgpu::MultisampleState, MultisampleState)

        MultisampleState.def_readwrite("next_in_chain", &wgpu::MultisampleState::nextInChain);
        MultisampleState.def_readwrite("count", &wgpu::MultisampleState::count);
        MultisampleState.def_readwrite("mask", &wgpu::MultisampleState::mask);
        MultisampleState.def_readwrite("alpha_to_coverage_enabled", &wgpu::MultisampleState::alphaToCoverageEnabled);
        MultisampleState.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::MultisampleState, MultisampleState)

    PYCLASS_BEGIN(_wgpu, wgpu::Origin3D, Origin3D)

        Origin3D.def_readwrite("x", &wgpu::Origin3D::x);
        Origin3D.def_readwrite("y", &wgpu::Origin3D::y);
        Origin3D.def_readwrite("z", &wgpu::Origin3D::z);
        Origin3D.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::Origin3D, Origin3D)

    PYCLASS_BEGIN(_wgpu, wgpu::PipelineLayoutDescriptor, PipelineLayoutDescriptor)

        PipelineLayoutDescriptor.def_readwrite("next_in_chain", &wgpu::PipelineLayoutDescriptor::nextInChain);
        PipelineLayoutDescriptor.def_property("label",
            [](const wgpu::PipelineLayoutDescriptor& self){ return self.label; },[](wgpu::PipelineLayoutDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        PipelineLayoutDescriptor.def_readwrite("bind_group_layout_count", &wgpu::PipelineLayoutDescriptor::bindGroupLayoutCount);
        PipelineLayoutDescriptor.def_readwrite("bind_group_layouts", &wgpu::PipelineLayoutDescriptor::bindGroupLayouts);
        PipelineLayoutDescriptor.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::PipelineLayoutDescriptor, PipelineLayoutDescriptor)

    PYCLASS_INHERIT_BEGIN(_wgpu, wgpu::PrimitiveDepthClipControl, struct wgpu::ChainedStruct, PrimitiveDepthClipControl)

        PrimitiveDepthClipControl.def(py::init<>());
        PrimitiveDepthClipControl.def_readwrite("unclipped_depth", &wgpu::PrimitiveDepthClipControl::unclippedDepth);
    PYCLASS_END(_wgpu, wgpu::PrimitiveDepthClipControl, PrimitiveDepthClipControl)

    PYCLASS_BEGIN(_wgpu, wgpu::PrimitiveState, PrimitiveState)

        PrimitiveState.def_readwrite("next_in_chain", &wgpu::PrimitiveState::nextInChain);
        PrimitiveState.def_readwrite("topology", &wgpu::PrimitiveState::topology);
        PrimitiveState.def_readwrite("strip_index_format", &wgpu::PrimitiveState::stripIndexFormat);
        PrimitiveState.def_readwrite("front_face", &wgpu::PrimitiveState::frontFace);
        PrimitiveState.def_readwrite("cull_mode", &wgpu::PrimitiveState::cullMode);
        PrimitiveState.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::PrimitiveState, PrimitiveState)

    PYCLASS_BEGIN(_wgpu, wgpu::QuerySetDescriptor, QuerySetDescriptor)

        QuerySetDescriptor.def_readwrite("next_in_chain", &wgpu::QuerySetDescriptor::nextInChain);
        QuerySetDescriptor.def_property("label",
            [](const wgpu::QuerySetDescriptor& self){ return self.label; },[](wgpu::QuerySetDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        QuerySetDescriptor.def_readwrite("type", &wgpu::QuerySetDescriptor::type);
        QuerySetDescriptor.def_readwrite("count", &wgpu::QuerySetDescriptor::count);
        QuerySetDescriptor.def_readwrite("pipeline_statistics", &wgpu::QuerySetDescriptor::pipelineStatistics);
        QuerySetDescriptor.def_readwrite("pipeline_statistics_count", &wgpu::QuerySetDescriptor::pipelineStatisticsCount);
        QuerySetDescriptor.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::QuerySetDescriptor, QuerySetDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::QueueDescriptor, QueueDescriptor)

        QueueDescriptor.def_readwrite("next_in_chain", &wgpu::QueueDescriptor::nextInChain);
        QueueDescriptor.def_property("label",
            [](const wgpu::QueueDescriptor& self){ return self.label; },[](wgpu::QueueDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        QueueDescriptor.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::QueueDescriptor, QueueDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::RenderBundleDescriptor, RenderBundleDescriptor)

        RenderBundleDescriptor.def_readwrite("next_in_chain", &wgpu::RenderBundleDescriptor::nextInChain);
        RenderBundleDescriptor.def_property("label",
            [](const wgpu::RenderBundleDescriptor& self){ return self.label; },[](wgpu::RenderBundleDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        RenderBundleDescriptor.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::RenderBundleDescriptor, RenderBundleDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::RenderBundleEncoderDescriptor, RenderBundleEncoderDescriptor)

        RenderBundleEncoderDescriptor.def_readwrite("next_in_chain", &wgpu::RenderBundleEncoderDescriptor::nextInChain);
        RenderBundleEncoderDescriptor.def_property("label",
            [](const wgpu::RenderBundleEncoderDescriptor& self){ return self.label; },[](wgpu::RenderBundleEncoderDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        RenderBundleEncoderDescriptor.def_readwrite("color_formats_count", &wgpu::RenderBundleEncoderDescriptor::colorFormatsCount);
        RenderBundleEncoderDescriptor.def_readwrite("color_formats", &wgpu::RenderBundleEncoderDescriptor::colorFormats);
        RenderBundleEncoderDescriptor.def_readwrite("depth_stencil_format", &wgpu::RenderBundleEncoderDescriptor::depthStencilFormat);
        RenderBundleEncoderDescriptor.def_readwrite("sample_count", &wgpu::RenderBundleEncoderDescriptor::sampleCount);
        RenderBundleEncoderDescriptor.def_readwrite("depth_read_only", &wgpu::RenderBundleEncoderDescriptor::depthReadOnly);
        RenderBundleEncoderDescriptor.def_readwrite("stencil_read_only", &wgpu::RenderBundleEncoderDescriptor::stencilReadOnly);
        RenderBundleEncoderDescriptor.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::RenderBundleEncoderDescriptor, RenderBundleEncoderDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::RenderPassDepthStencilAttachment, RenderPassDepthStencilAttachment)

        RenderPassDepthStencilAttachment.def_readwrite("view", &wgpu::RenderPassDepthStencilAttachment::view);
        RenderPassDepthStencilAttachment.def_readwrite("depth_load_op", &wgpu::RenderPassDepthStencilAttachment::depthLoadOp);
        RenderPassDepthStencilAttachment.def_readwrite("depth_store_op", &wgpu::RenderPassDepthStencilAttachment::depthStoreOp);
        RenderPassDepthStencilAttachment.def_readwrite("clear_depth", &wgpu::RenderPassDepthStencilAttachment::clearDepth);
        RenderPassDepthStencilAttachment.def_readwrite("depth_clear_value", &wgpu::RenderPassDepthStencilAttachment::depthClearValue);
        RenderPassDepthStencilAttachment.def_readwrite("depth_read_only", &wgpu::RenderPassDepthStencilAttachment::depthReadOnly);
        RenderPassDepthStencilAttachment.def_readwrite("stencil_load_op", &wgpu::RenderPassDepthStencilAttachment::stencilLoadOp);
        RenderPassDepthStencilAttachment.def_readwrite("stencil_store_op", &wgpu::RenderPassDepthStencilAttachment::stencilStoreOp);
        RenderPassDepthStencilAttachment.def_readwrite("clear_stencil", &wgpu::RenderPassDepthStencilAttachment::clearStencil);
        RenderPassDepthStencilAttachment.def_readwrite("stencil_clear_value", &wgpu::RenderPassDepthStencilAttachment::stencilClearValue);
        RenderPassDepthStencilAttachment.def_readwrite("stencil_read_only", &wgpu::RenderPassDepthStencilAttachment::stencilReadOnly);
        RenderPassDepthStencilAttachment.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::RenderPassDepthStencilAttachment, RenderPassDepthStencilAttachment)

    PYCLASS_INHERIT_BEGIN(_wgpu, wgpu::RenderPassDescriptorMaxDrawCount, struct wgpu::ChainedStruct, RenderPassDescriptorMaxDrawCount)

        RenderPassDescriptorMaxDrawCount.def(py::init<>());
        RenderPassDescriptorMaxDrawCount.def_readwrite("max_draw_count", &wgpu::RenderPassDescriptorMaxDrawCount::maxDrawCount);
    PYCLASS_END(_wgpu, wgpu::RenderPassDescriptorMaxDrawCount, RenderPassDescriptorMaxDrawCount)

    PYCLASS_BEGIN(_wgpu, wgpu::RenderPassTimestampWrite, RenderPassTimestampWrite)

        RenderPassTimestampWrite.def_readwrite("query_set", &wgpu::RenderPassTimestampWrite::querySet);
        RenderPassTimestampWrite.def_readwrite("query_index", &wgpu::RenderPassTimestampWrite::queryIndex);
        RenderPassTimestampWrite.def_readwrite("location", &wgpu::RenderPassTimestampWrite::location);
        RenderPassTimestampWrite.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::RenderPassTimestampWrite, RenderPassTimestampWrite)

    PYCLASS_BEGIN(_wgpu, wgpu::RequestAdapterOptions, RequestAdapterOptions)

        RequestAdapterOptions.def_readwrite("next_in_chain", &wgpu::RequestAdapterOptions::nextInChain);
        RequestAdapterOptions.def_readwrite("compatible_surface", &wgpu::RequestAdapterOptions::compatibleSurface);
        RequestAdapterOptions.def_readwrite("power_preference", &wgpu::RequestAdapterOptions::powerPreference);
        RequestAdapterOptions.def_readwrite("force_fallback_adapter", &wgpu::RequestAdapterOptions::forceFallbackAdapter);
        RequestAdapterOptions.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::RequestAdapterOptions, RequestAdapterOptions)

    PYCLASS_BEGIN(_wgpu, wgpu::SamplerBindingLayout, SamplerBindingLayout)

        SamplerBindingLayout.def_readwrite("next_in_chain", &wgpu::SamplerBindingLayout::nextInChain);
        SamplerBindingLayout.def_readwrite("type", &wgpu::SamplerBindingLayout::type);
        SamplerBindingLayout.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::SamplerBindingLayout, SamplerBindingLayout)

    PYCLASS_BEGIN(_wgpu, wgpu::SamplerDescriptor, SamplerDescriptor)

        SamplerDescriptor.def_readwrite("next_in_chain", &wgpu::SamplerDescriptor::nextInChain);
        SamplerDescriptor.def_property("label",
            [](const wgpu::SamplerDescriptor& self){ return self.label; },[](wgpu::SamplerDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        SamplerDescriptor.def_readwrite("address_mode_u", &wgpu::SamplerDescriptor::addressModeU);
        SamplerDescriptor.def_readwrite("address_mode_v", &wgpu::SamplerDescriptor::addressModeV);
        SamplerDescriptor.def_readwrite("address_mode_w", &wgpu::SamplerDescriptor::addressModeW);
        SamplerDescriptor.def_readwrite("mag_filter", &wgpu::SamplerDescriptor::magFilter);
        SamplerDescriptor.def_readwrite("min_filter", &wgpu::SamplerDescriptor::minFilter);
        SamplerDescriptor.def_readwrite("mipmap_filter", &wgpu::SamplerDescriptor::mipmapFilter);
        SamplerDescriptor.def_readwrite("lod_min_clamp", &wgpu::SamplerDescriptor::lodMinClamp);
        SamplerDescriptor.def_readwrite("lod_max_clamp", &wgpu::SamplerDescriptor::lodMaxClamp);
        SamplerDescriptor.def_readwrite("compare", &wgpu::SamplerDescriptor::compare);
        SamplerDescriptor.def_readwrite("max_anisotropy", &wgpu::SamplerDescriptor::maxAnisotropy);
        SamplerDescriptor.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::SamplerDescriptor, SamplerDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::ShaderModuleDescriptor, ShaderModuleDescriptor)

        ShaderModuleDescriptor.def_readwrite("next_in_chain", &wgpu::ShaderModuleDescriptor::nextInChain);
        ShaderModuleDescriptor.def_property("label",
            [](const wgpu::ShaderModuleDescriptor& self){ return self.label; },[](wgpu::ShaderModuleDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        ShaderModuleDescriptor.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::ShaderModuleDescriptor, ShaderModuleDescriptor)

    PYCLASS_INHERIT_BEGIN(_wgpu, wgpu::ShaderModuleSPIRVDescriptor, struct wgpu::ChainedStruct, ShaderModuleSPIRVDescriptor)

        ShaderModuleSPIRVDescriptor.def(py::init<>());
        ShaderModuleSPIRVDescriptor.def_readwrite("code_size", &wgpu::ShaderModuleSPIRVDescriptor::codeSize);
        ShaderModuleSPIRVDescriptor.def_readwrite("code", &wgpu::ShaderModuleSPIRVDescriptor::code);
    PYCLASS_END(_wgpu, wgpu::ShaderModuleSPIRVDescriptor, ShaderModuleSPIRVDescriptor)

    PYCLASS_INHERIT_BEGIN(_wgpu, wgpu::ShaderModuleWGSLDescriptor, struct wgpu::ChainedStruct, ShaderModuleWGSLDescriptor)

        ShaderModuleWGSLDescriptor.def(py::init<>());
        ShaderModuleWGSLDescriptor.def_property("source",
            [](const wgpu::ShaderModuleWGSLDescriptor& self){ return self.source; },[](wgpu::ShaderModuleWGSLDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.source = c; }
        );
    PYCLASS_END(_wgpu, wgpu::ShaderModuleWGSLDescriptor, ShaderModuleWGSLDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::StencilFaceState, StencilFaceState)

        StencilFaceState.def_readwrite("compare", &wgpu::StencilFaceState::compare);
        StencilFaceState.def_readwrite("fail_op", &wgpu::StencilFaceState::failOp);
        StencilFaceState.def_readwrite("depth_fail_op", &wgpu::StencilFaceState::depthFailOp);
        StencilFaceState.def_readwrite("pass_op", &wgpu::StencilFaceState::passOp);
        StencilFaceState.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::StencilFaceState, StencilFaceState)

    PYCLASS_BEGIN(_wgpu, wgpu::StorageTextureBindingLayout, StorageTextureBindingLayout)

        StorageTextureBindingLayout.def_readwrite("next_in_chain", &wgpu::StorageTextureBindingLayout::nextInChain);
        StorageTextureBindingLayout.def_readwrite("access", &wgpu::StorageTextureBindingLayout::access);
        StorageTextureBindingLayout.def_readwrite("format", &wgpu::StorageTextureBindingLayout::format);
        StorageTextureBindingLayout.def_readwrite("view_dimension", &wgpu::StorageTextureBindingLayout::viewDimension);
        StorageTextureBindingLayout.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::StorageTextureBindingLayout, StorageTextureBindingLayout)

    PYCLASS_BEGIN(_wgpu, wgpu::SurfaceDescriptor, SurfaceDescriptor)

        SurfaceDescriptor.def_readwrite("next_in_chain", &wgpu::SurfaceDescriptor::nextInChain);
        SurfaceDescriptor.def_property("label",
            [](const wgpu::SurfaceDescriptor& self){ return self.label; },[](wgpu::SurfaceDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        SurfaceDescriptor.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::SurfaceDescriptor, SurfaceDescriptor)

    PYCLASS_INHERIT_BEGIN(_wgpu, wgpu::SurfaceDescriptorFromAndroidNativeWindow, struct wgpu::ChainedStruct, SurfaceDescriptorFromAndroidNativeWindow)

        SurfaceDescriptorFromAndroidNativeWindow.def(py::init<>());
        SurfaceDescriptorFromAndroidNativeWindow.def_readwrite("window", &wgpu::SurfaceDescriptorFromAndroidNativeWindow::window);
    PYCLASS_END(_wgpu, wgpu::SurfaceDescriptorFromAndroidNativeWindow, SurfaceDescriptorFromAndroidNativeWindow)

    PYCLASS_INHERIT_BEGIN(_wgpu, wgpu::SurfaceDescriptorFromCanvasHTMLSelector, struct wgpu::ChainedStruct, SurfaceDescriptorFromCanvasHTMLSelector)

        SurfaceDescriptorFromCanvasHTMLSelector.def(py::init<>());
        SurfaceDescriptorFromCanvasHTMLSelector.def_property("selector",
            [](const wgpu::SurfaceDescriptorFromCanvasHTMLSelector& self){ return self.selector; },[](wgpu::SurfaceDescriptorFromCanvasHTMLSelector& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.selector = c; }
        );
    PYCLASS_END(_wgpu, wgpu::SurfaceDescriptorFromCanvasHTMLSelector, SurfaceDescriptorFromCanvasHTMLSelector)

    PYCLASS_INHERIT_BEGIN(_wgpu, wgpu::SurfaceDescriptorFromMetalLayer, struct wgpu::ChainedStruct, SurfaceDescriptorFromMetalLayer)

        SurfaceDescriptorFromMetalLayer.def(py::init<>());
        SurfaceDescriptorFromMetalLayer.def_readwrite("layer", &wgpu::SurfaceDescriptorFromMetalLayer::layer);
    PYCLASS_END(_wgpu, wgpu::SurfaceDescriptorFromMetalLayer, SurfaceDescriptorFromMetalLayer)

    PYCLASS_INHERIT_BEGIN(_wgpu, wgpu::SurfaceDescriptorFromWaylandSurface, struct wgpu::ChainedStruct, SurfaceDescriptorFromWaylandSurface)

        SurfaceDescriptorFromWaylandSurface.def(py::init<>());
        SurfaceDescriptorFromWaylandSurface.def_readwrite("display", &wgpu::SurfaceDescriptorFromWaylandSurface::display);
        SurfaceDescriptorFromWaylandSurface.def_readwrite("surface", &wgpu::SurfaceDescriptorFromWaylandSurface::surface);
    PYCLASS_END(_wgpu, wgpu::SurfaceDescriptorFromWaylandSurface, SurfaceDescriptorFromWaylandSurface)

    PYCLASS_INHERIT_BEGIN(_wgpu, wgpu::SurfaceDescriptorFromWindowsCoreWindow, struct wgpu::ChainedStruct, SurfaceDescriptorFromWindowsCoreWindow)

        SurfaceDescriptorFromWindowsCoreWindow.def(py::init<>());
        SurfaceDescriptorFromWindowsCoreWindow.def_readwrite("core_window", &wgpu::SurfaceDescriptorFromWindowsCoreWindow::coreWindow);
    PYCLASS_END(_wgpu, wgpu::SurfaceDescriptorFromWindowsCoreWindow, SurfaceDescriptorFromWindowsCoreWindow)

    PYCLASS_INHERIT_BEGIN(_wgpu, wgpu::SurfaceDescriptorFromWindowsHWND, struct wgpu::ChainedStruct, SurfaceDescriptorFromWindowsHWND)

        SurfaceDescriptorFromWindowsHWND.def(py::init<>());
        SurfaceDescriptorFromWindowsHWND.def_readwrite("hinstance", &wgpu::SurfaceDescriptorFromWindowsHWND::hinstance);
        SurfaceDescriptorFromWindowsHWND.def_readwrite("hwnd", &wgpu::SurfaceDescriptorFromWindowsHWND::hwnd);
    PYCLASS_END(_wgpu, wgpu::SurfaceDescriptorFromWindowsHWND, SurfaceDescriptorFromWindowsHWND)

    PYCLASS_INHERIT_BEGIN(_wgpu, wgpu::SurfaceDescriptorFromWindowsSwapChainPanel, struct wgpu::ChainedStruct, SurfaceDescriptorFromWindowsSwapChainPanel)

        SurfaceDescriptorFromWindowsSwapChainPanel.def(py::init<>());
        SurfaceDescriptorFromWindowsSwapChainPanel.def_readwrite("swap_chain_panel", &wgpu::SurfaceDescriptorFromWindowsSwapChainPanel::swapChainPanel);
    PYCLASS_END(_wgpu, wgpu::SurfaceDescriptorFromWindowsSwapChainPanel, SurfaceDescriptorFromWindowsSwapChainPanel)

    PYCLASS_INHERIT_BEGIN(_wgpu, wgpu::SurfaceDescriptorFromXlibWindow, struct wgpu::ChainedStruct, SurfaceDescriptorFromXlibWindow)

        SurfaceDescriptorFromXlibWindow.def(py::init<>());
        SurfaceDescriptorFromXlibWindow.def_readwrite("display", &wgpu::SurfaceDescriptorFromXlibWindow::display);
        SurfaceDescriptorFromXlibWindow.def_readwrite("window", &wgpu::SurfaceDescriptorFromXlibWindow::window);
    PYCLASS_END(_wgpu, wgpu::SurfaceDescriptorFromXlibWindow, SurfaceDescriptorFromXlibWindow)

    PYCLASS_BEGIN(_wgpu, wgpu::SwapChainDescriptor, SwapChainDescriptor)

        SwapChainDescriptor.def_readwrite("next_in_chain", &wgpu::SwapChainDescriptor::nextInChain);
        SwapChainDescriptor.def_property("label",
            [](const wgpu::SwapChainDescriptor& self){ return self.label; },[](wgpu::SwapChainDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        SwapChainDescriptor.def_readwrite("usage", &wgpu::SwapChainDescriptor::usage);
        SwapChainDescriptor.def_readwrite("format", &wgpu::SwapChainDescriptor::format);
        SwapChainDescriptor.def_readwrite("width", &wgpu::SwapChainDescriptor::width);
        SwapChainDescriptor.def_readwrite("height", &wgpu::SwapChainDescriptor::height);
        SwapChainDescriptor.def_readwrite("present_mode", &wgpu::SwapChainDescriptor::presentMode);
        SwapChainDescriptor.def_readwrite("implementation", &wgpu::SwapChainDescriptor::implementation);
        SwapChainDescriptor.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::SwapChainDescriptor, SwapChainDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::TextureBindingLayout, TextureBindingLayout)

        TextureBindingLayout.def_readwrite("next_in_chain", &wgpu::TextureBindingLayout::nextInChain);
        TextureBindingLayout.def_readwrite("sample_type", &wgpu::TextureBindingLayout::sampleType);
        TextureBindingLayout.def_readwrite("view_dimension", &wgpu::TextureBindingLayout::viewDimension);
        TextureBindingLayout.def_readwrite("multisampled", &wgpu::TextureBindingLayout::multisampled);
        TextureBindingLayout.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::TextureBindingLayout, TextureBindingLayout)

    PYCLASS_BEGIN(_wgpu, wgpu::TextureDataLayout, TextureDataLayout)

        TextureDataLayout.def_readwrite("next_in_chain", &wgpu::TextureDataLayout::nextInChain);
        TextureDataLayout.def_readwrite("offset", &wgpu::TextureDataLayout::offset);
        TextureDataLayout.def_readwrite("bytes_per_row", &wgpu::TextureDataLayout::bytesPerRow);
        TextureDataLayout.def_readwrite("rows_per_image", &wgpu::TextureDataLayout::rowsPerImage);
        TextureDataLayout.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::TextureDataLayout, TextureDataLayout)

    PYCLASS_BEGIN(_wgpu, wgpu::TextureViewDescriptor, TextureViewDescriptor)

        TextureViewDescriptor.def_readwrite("next_in_chain", &wgpu::TextureViewDescriptor::nextInChain);
        TextureViewDescriptor.def_property("label",
            [](const wgpu::TextureViewDescriptor& self){ return self.label; },[](wgpu::TextureViewDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        TextureViewDescriptor.def_readwrite("format", &wgpu::TextureViewDescriptor::format);
        TextureViewDescriptor.def_readwrite("dimension", &wgpu::TextureViewDescriptor::dimension);
        TextureViewDescriptor.def_readwrite("base_mip_level", &wgpu::TextureViewDescriptor::baseMipLevel);
        TextureViewDescriptor.def_readwrite("mip_level_count", &wgpu::TextureViewDescriptor::mipLevelCount);
        TextureViewDescriptor.def_readwrite("base_array_layer", &wgpu::TextureViewDescriptor::baseArrayLayer);
        TextureViewDescriptor.def_readwrite("array_layer_count", &wgpu::TextureViewDescriptor::arrayLayerCount);
        TextureViewDescriptor.def_readwrite("aspect", &wgpu::TextureViewDescriptor::aspect);
        TextureViewDescriptor.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::TextureViewDescriptor, TextureViewDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::VertexAttribute, VertexAttribute)

        VertexAttribute.def_readwrite("format", &wgpu::VertexAttribute::format);
        VertexAttribute.def_readwrite("offset", &wgpu::VertexAttribute::offset);
        VertexAttribute.def_readwrite("shader_location", &wgpu::VertexAttribute::shaderLocation);
        VertexAttribute.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::VertexAttribute, VertexAttribute)

    PYCLASS_BEGIN(_wgpu, wgpu::BindGroupDescriptor, BindGroupDescriptor)

        BindGroupDescriptor.def_readwrite("next_in_chain", &wgpu::BindGroupDescriptor::nextInChain);
        BindGroupDescriptor.def_property("label",
            [](const wgpu::BindGroupDescriptor& self){ return self.label; },[](wgpu::BindGroupDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        BindGroupDescriptor.def_readwrite("layout", &wgpu::BindGroupDescriptor::layout);
        BindGroupDescriptor.def_readwrite("entry_count", &wgpu::BindGroupDescriptor::entryCount);
        BindGroupDescriptor.def_readwrite("entries", &wgpu::BindGroupDescriptor::entries);
        BindGroupDescriptor.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::BindGroupDescriptor, BindGroupDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::BindGroupLayoutEntry, BindGroupLayoutEntry)

        BindGroupLayoutEntry.def_readwrite("next_in_chain", &wgpu::BindGroupLayoutEntry::nextInChain);
        BindGroupLayoutEntry.def_readwrite("binding", &wgpu::BindGroupLayoutEntry::binding);
        BindGroupLayoutEntry.def_readwrite("visibility", &wgpu::BindGroupLayoutEntry::visibility);
        BindGroupLayoutEntry.def_readwrite("buffer", &wgpu::BindGroupLayoutEntry::buffer);
        BindGroupLayoutEntry.def_readwrite("sampler", &wgpu::BindGroupLayoutEntry::sampler);
        BindGroupLayoutEntry.def_readwrite("texture", &wgpu::BindGroupLayoutEntry::texture);
        BindGroupLayoutEntry.def_readwrite("storage_texture", &wgpu::BindGroupLayoutEntry::storageTexture);
        BindGroupLayoutEntry.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::BindGroupLayoutEntry, BindGroupLayoutEntry)

    PYCLASS_BEGIN(_wgpu, wgpu::BlendState, BlendState)

        BlendState.def_readwrite("color", &wgpu::BlendState::color);
        BlendState.def_readwrite("alpha", &wgpu::BlendState::alpha);
        BlendState.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::BlendState, BlendState)

    PYCLASS_BEGIN(_wgpu, wgpu::CompilationInfo, CompilationInfo)

        CompilationInfo.def_readwrite("next_in_chain", &wgpu::CompilationInfo::nextInChain);
        CompilationInfo.def_readwrite("message_count", &wgpu::CompilationInfo::messageCount);
        CompilationInfo.def_readwrite("messages", &wgpu::CompilationInfo::messages);
        CompilationInfo.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::CompilationInfo, CompilationInfo)

    PYCLASS_BEGIN(_wgpu, wgpu::ComputePassDescriptor, ComputePassDescriptor)

        ComputePassDescriptor.def_readwrite("next_in_chain", &wgpu::ComputePassDescriptor::nextInChain);
        ComputePassDescriptor.def_property("label",
            [](const wgpu::ComputePassDescriptor& self){ return self.label; },[](wgpu::ComputePassDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        ComputePassDescriptor.def_readwrite("timestamp_write_count", &wgpu::ComputePassDescriptor::timestampWriteCount);
        ComputePassDescriptor.def_readwrite("timestamp_writes", &wgpu::ComputePassDescriptor::timestampWrites);
        ComputePassDescriptor.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::ComputePassDescriptor, ComputePassDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::DepthStencilState, DepthStencilState)

        DepthStencilState.def_readwrite("next_in_chain", &wgpu::DepthStencilState::nextInChain);
        DepthStencilState.def_readwrite("format", &wgpu::DepthStencilState::format);
        DepthStencilState.def_readwrite("depth_write_enabled", &wgpu::DepthStencilState::depthWriteEnabled);
        DepthStencilState.def_readwrite("depth_compare", &wgpu::DepthStencilState::depthCompare);
        DepthStencilState.def_readwrite("stencil_front", &wgpu::DepthStencilState::stencilFront);
        DepthStencilState.def_readwrite("stencil_back", &wgpu::DepthStencilState::stencilBack);
        DepthStencilState.def_readwrite("stencil_read_mask", &wgpu::DepthStencilState::stencilReadMask);
        DepthStencilState.def_readwrite("stencil_write_mask", &wgpu::DepthStencilState::stencilWriteMask);
        DepthStencilState.def_readwrite("depth_bias", &wgpu::DepthStencilState::depthBias);
        DepthStencilState.def_readwrite("depth_bias_slope_scale", &wgpu::DepthStencilState::depthBiasSlopeScale);
        DepthStencilState.def_readwrite("depth_bias_clamp", &wgpu::DepthStencilState::depthBiasClamp);
        DepthStencilState.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::DepthStencilState, DepthStencilState)

    PYCLASS_BEGIN(_wgpu, wgpu::ImageCopyBuffer, ImageCopyBuffer)

        ImageCopyBuffer.def_readwrite("next_in_chain", &wgpu::ImageCopyBuffer::nextInChain);
        ImageCopyBuffer.def_readwrite("layout", &wgpu::ImageCopyBuffer::layout);
        ImageCopyBuffer.def_readwrite("buffer", &wgpu::ImageCopyBuffer::buffer);
        ImageCopyBuffer.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::ImageCopyBuffer, ImageCopyBuffer)

    PYCLASS_BEGIN(_wgpu, wgpu::ImageCopyTexture, ImageCopyTexture)

        ImageCopyTexture.def_readwrite("next_in_chain", &wgpu::ImageCopyTexture::nextInChain);
        ImageCopyTexture.def_readwrite("texture", &wgpu::ImageCopyTexture::texture);
        ImageCopyTexture.def_readwrite("mip_level", &wgpu::ImageCopyTexture::mipLevel);
        ImageCopyTexture.def_readwrite("origin", &wgpu::ImageCopyTexture::origin);
        ImageCopyTexture.def_readwrite("aspect", &wgpu::ImageCopyTexture::aspect);
        ImageCopyTexture.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::ImageCopyTexture, ImageCopyTexture)

    PYCLASS_BEGIN(_wgpu, wgpu::ProgrammableStageDescriptor, ProgrammableStageDescriptor)

        ProgrammableStageDescriptor.def_readwrite("next_in_chain", &wgpu::ProgrammableStageDescriptor::nextInChain);
        ProgrammableStageDescriptor.def_readwrite("module", &wgpu::ProgrammableStageDescriptor::module);
        ProgrammableStageDescriptor.def_property("entry_point",
            [](const wgpu::ProgrammableStageDescriptor& self){ return self.entryPoint; },[](wgpu::ProgrammableStageDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.entryPoint = c; }
        );
        ProgrammableStageDescriptor.def_readwrite("constant_count", &wgpu::ProgrammableStageDescriptor::constantCount);
        ProgrammableStageDescriptor.def_readwrite("constants", &wgpu::ProgrammableStageDescriptor::constants);
        ProgrammableStageDescriptor.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::ProgrammableStageDescriptor, ProgrammableStageDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::RenderPassColorAttachment, RenderPassColorAttachment)

        RenderPassColorAttachment.def_readwrite("view", &wgpu::RenderPassColorAttachment::view);
        RenderPassColorAttachment.def_readwrite("resolve_target", &wgpu::RenderPassColorAttachment::resolveTarget);
        RenderPassColorAttachment.def_readwrite("load_op", &wgpu::RenderPassColorAttachment::loadOp);
        RenderPassColorAttachment.def_readwrite("store_op", &wgpu::RenderPassColorAttachment::storeOp);
        RenderPassColorAttachment.def_readwrite("clear_color", &wgpu::RenderPassColorAttachment::clearColor);
        RenderPassColorAttachment.def_readwrite("clear_value", &wgpu::RenderPassColorAttachment::clearValue);
        RenderPassColorAttachment.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::RenderPassColorAttachment, RenderPassColorAttachment)

    PYCLASS_BEGIN(_wgpu, wgpu::RequiredLimits, RequiredLimits)

        RequiredLimits.def_readwrite("next_in_chain", &wgpu::RequiredLimits::nextInChain);
        RequiredLimits.def_readwrite("limits", &wgpu::RequiredLimits::limits);
        RequiredLimits.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::RequiredLimits, RequiredLimits)

    PYCLASS_BEGIN(_wgpu, wgpu::SupportedLimits, SupportedLimits)

        SupportedLimits.def_readwrite("next_in_chain", &wgpu::SupportedLimits::nextInChain);
        SupportedLimits.def_readwrite("limits", &wgpu::SupportedLimits::limits);
        SupportedLimits.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::SupportedLimits, SupportedLimits)

    PYCLASS_BEGIN(_wgpu, wgpu::TextureDescriptor, TextureDescriptor)

        TextureDescriptor.def_readwrite("next_in_chain", &wgpu::TextureDescriptor::nextInChain);
        TextureDescriptor.def_property("label",
            [](const wgpu::TextureDescriptor& self){ return self.label; },[](wgpu::TextureDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        TextureDescriptor.def_readwrite("usage", &wgpu::TextureDescriptor::usage);
        TextureDescriptor.def_readwrite("dimension", &wgpu::TextureDescriptor::dimension);
        TextureDescriptor.def_readwrite("size", &wgpu::TextureDescriptor::size);
        TextureDescriptor.def_readwrite("format", &wgpu::TextureDescriptor::format);
        TextureDescriptor.def_readwrite("mip_level_count", &wgpu::TextureDescriptor::mipLevelCount);
        TextureDescriptor.def_readwrite("sample_count", &wgpu::TextureDescriptor::sampleCount);
        TextureDescriptor.def_readwrite("view_format_count", &wgpu::TextureDescriptor::viewFormatCount);
        TextureDescriptor.def_readwrite("view_formats", &wgpu::TextureDescriptor::viewFormats);
        TextureDescriptor.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::TextureDescriptor, TextureDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::VertexBufferLayout, VertexBufferLayout)

        VertexBufferLayout.def_readwrite("array_stride", &wgpu::VertexBufferLayout::arrayStride);
        VertexBufferLayout.def_readwrite("step_mode", &wgpu::VertexBufferLayout::stepMode);
        VertexBufferLayout.def_readwrite("attribute_count", &wgpu::VertexBufferLayout::attributeCount);
        VertexBufferLayout.def_readwrite("attributes", &wgpu::VertexBufferLayout::attributes);
        VertexBufferLayout.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::VertexBufferLayout, VertexBufferLayout)

    PYCLASS_BEGIN(_wgpu, wgpu::BindGroupLayoutDescriptor, BindGroupLayoutDescriptor)

        BindGroupLayoutDescriptor.def_readwrite("next_in_chain", &wgpu::BindGroupLayoutDescriptor::nextInChain);
        BindGroupLayoutDescriptor.def_property("label",
            [](const wgpu::BindGroupLayoutDescriptor& self){ return self.label; },[](wgpu::BindGroupLayoutDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        BindGroupLayoutDescriptor.def_readwrite("entry_count", &wgpu::BindGroupLayoutDescriptor::entryCount);
        BindGroupLayoutDescriptor.def_readwrite("entries", &wgpu::BindGroupLayoutDescriptor::entries);
        BindGroupLayoutDescriptor.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::BindGroupLayoutDescriptor, BindGroupLayoutDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::ColorTargetState, ColorTargetState)

        ColorTargetState.def_readwrite("next_in_chain", &wgpu::ColorTargetState::nextInChain);
        ColorTargetState.def_readwrite("format", &wgpu::ColorTargetState::format);
        ColorTargetState.def_readwrite("blend", &wgpu::ColorTargetState::blend);
        ColorTargetState.def_readwrite("write_mask", &wgpu::ColorTargetState::writeMask);
        ColorTargetState.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::ColorTargetState, ColorTargetState)

    PYCLASS_BEGIN(_wgpu, wgpu::ComputePipelineDescriptor, ComputePipelineDescriptor)

        ComputePipelineDescriptor.def_readwrite("next_in_chain", &wgpu::ComputePipelineDescriptor::nextInChain);
        ComputePipelineDescriptor.def_property("label",
            [](const wgpu::ComputePipelineDescriptor& self){ return self.label; },[](wgpu::ComputePipelineDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        ComputePipelineDescriptor.def_readwrite("layout", &wgpu::ComputePipelineDescriptor::layout);
        ComputePipelineDescriptor.def_readwrite("compute", &wgpu::ComputePipelineDescriptor::compute);
        ComputePipelineDescriptor.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::ComputePipelineDescriptor, ComputePipelineDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::DeviceDescriptor, DeviceDescriptor)

        DeviceDescriptor.def_readwrite("next_in_chain", &wgpu::DeviceDescriptor::nextInChain);
        DeviceDescriptor.def_property("label",
            [](const wgpu::DeviceDescriptor& self){ return self.label; },[](wgpu::DeviceDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        DeviceDescriptor.def_readwrite("required_features_count", &wgpu::DeviceDescriptor::requiredFeaturesCount);
        DeviceDescriptor.def_readwrite("required_features", &wgpu::DeviceDescriptor::requiredFeatures);
        DeviceDescriptor.def_readwrite("required_limits", &wgpu::DeviceDescriptor::requiredLimits);
        DeviceDescriptor.def_readwrite("default_queue", &wgpu::DeviceDescriptor::defaultQueue);
        DeviceDescriptor.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::DeviceDescriptor, DeviceDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::RenderPassDescriptor, RenderPassDescriptor)

        RenderPassDescriptor.def_readwrite("next_in_chain", &wgpu::RenderPassDescriptor::nextInChain);
        RenderPassDescriptor.def_property("label",
            [](const wgpu::RenderPassDescriptor& self){ return self.label; },[](wgpu::RenderPassDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        RenderPassDescriptor.def_readwrite("color_attachment_count", &wgpu::RenderPassDescriptor::colorAttachmentCount);
        RenderPassDescriptor.def_readwrite("color_attachments", &wgpu::RenderPassDescriptor::colorAttachments);
        RenderPassDescriptor.def_readwrite("depth_stencil_attachment", &wgpu::RenderPassDescriptor::depthStencilAttachment);
        RenderPassDescriptor.def_readwrite("occlusion_query_set", &wgpu::RenderPassDescriptor::occlusionQuerySet);
        RenderPassDescriptor.def_readwrite("timestamp_write_count", &wgpu::RenderPassDescriptor::timestampWriteCount);
        RenderPassDescriptor.def_readwrite("timestamp_writes", &wgpu::RenderPassDescriptor::timestampWrites);
        RenderPassDescriptor.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::RenderPassDescriptor, RenderPassDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::VertexState, VertexState)

        VertexState.def_readwrite("next_in_chain", &wgpu::VertexState::nextInChain);
        VertexState.def_readwrite("module", &wgpu::VertexState::module);
        VertexState.def_property("entry_point",
            [](const wgpu::VertexState& self){ return self.entryPoint; },[](wgpu::VertexState& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.entryPoint = c; }
        );
        VertexState.def_readwrite("constant_count", &wgpu::VertexState::constantCount);
        VertexState.def_readwrite("constants", &wgpu::VertexState::constants);
        VertexState.def_readwrite("buffer_count", &wgpu::VertexState::bufferCount);
        VertexState.def_readwrite("buffers", &wgpu::VertexState::buffers);
        VertexState.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::VertexState, VertexState)

    PYCLASS_BEGIN(_wgpu, wgpu::FragmentState, FragmentState)

        FragmentState.def_readwrite("next_in_chain", &wgpu::FragmentState::nextInChain);
        FragmentState.def_readwrite("module", &wgpu::FragmentState::module);
        FragmentState.def_property("entry_point",
            [](const wgpu::FragmentState& self){ return self.entryPoint; },[](wgpu::FragmentState& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.entryPoint = c; }
        );
        FragmentState.def_readwrite("constant_count", &wgpu::FragmentState::constantCount);
        FragmentState.def_readwrite("constants", &wgpu::FragmentState::constants);
        FragmentState.def_readwrite("target_count", &wgpu::FragmentState::targetCount);
        FragmentState.def_readwrite("targets", &wgpu::FragmentState::targets);
        FragmentState.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::FragmentState, FragmentState)

    PYCLASS_BEGIN(_wgpu, wgpu::RenderPipelineDescriptor, RenderPipelineDescriptor)

        RenderPipelineDescriptor.def_readwrite("next_in_chain", &wgpu::RenderPipelineDescriptor::nextInChain);
        RenderPipelineDescriptor.def_property("label",
            [](const wgpu::RenderPipelineDescriptor& self){ return self.label; },[](wgpu::RenderPipelineDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        RenderPipelineDescriptor.def_readwrite("layout", &wgpu::RenderPipelineDescriptor::layout);
        RenderPipelineDescriptor.def_readwrite("vertex", &wgpu::RenderPipelineDescriptor::vertex);
        RenderPipelineDescriptor.def_readwrite("primitive", &wgpu::RenderPipelineDescriptor::primitive);
        RenderPipelineDescriptor.def_readwrite("depth_stencil", &wgpu::RenderPipelineDescriptor::depthStencil);
        RenderPipelineDescriptor.def_readwrite("multisample", &wgpu::RenderPipelineDescriptor::multisample);
        RenderPipelineDescriptor.def_readwrite("fragment", &wgpu::RenderPipelineDescriptor::fragment);
        RenderPipelineDescriptor.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::RenderPipelineDescriptor, RenderPipelineDescriptor)


}