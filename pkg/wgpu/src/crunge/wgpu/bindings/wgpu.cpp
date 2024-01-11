#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>
#include <limits>

#include <dawn/webgpu_cpp.h>

#include <crunge/core/bindtools.h>
#include <crunge/wgpu/conversions.h>

namespace py = pybind11;

using namespace wgpu;

void init_wgpu(py::module &_wgpu, Registry &registry) {
    _wgpu.def("constexpr_max", &wgpu::detail::ConstexprMax
    , py::arg("a")
    , py::arg("b")
    , py::return_value_policy::automatic_reference);

    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::WGSLFeatureName, WGSLFeatureName)
    WGSLFeatureName
        .value("UNDEFINED", wgpu::WGSLFeatureName::Undefined)
        .value("READONLY_AND_READWRITE_STORAGE_TEXTURES", wgpu::WGSLFeatureName::ReadonlyAndReadwriteStorageTextures)
        .value("PACKED4X8_INTEGER_DOT_PRODUCT", wgpu::WGSLFeatureName::Packed4x8IntegerDotProduct)
        .value("UNRESTRICTED_POINTER_PARAMETERS", wgpu::WGSLFeatureName::UnrestrictedPointerParameters)
        .value("POINTER_COMPOSITE_ACCESS", wgpu::WGSLFeatureName::PointerCompositeAccess)
        .value("CHROMIUM_TESTING_UNIMPLEMENTED", wgpu::WGSLFeatureName::ChromiumTestingUnimplemented)
        .value("CHROMIUM_TESTING_UNSAFE_EXPERIMENTAL", wgpu::WGSLFeatureName::ChromiumTestingUnsafeExperimental)
        .value("CHROMIUM_TESTING_EXPERIMENTAL", wgpu::WGSLFeatureName::ChromiumTestingExperimental)
        .value("CHROMIUM_TESTING_SHIPPED_WITH_KILLSWITCH", wgpu::WGSLFeatureName::ChromiumTestingShippedWithKillswitch)
        .value("CHROMIUM_TESTING_SHIPPED", wgpu::WGSLFeatureName::ChromiumTestingShipped)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::WGSLFeatureName, WGSLFeatureName)


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
        .value("OPAQUE", wgpu::AlphaMode::Opaque)
        .value("PREMULTIPLIED", wgpu::AlphaMode::Premultiplied)
        .value("UNPREMULTIPLIED", wgpu::AlphaMode::Unpremultiplied)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::AlphaMode, AlphaMode)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::BackendType, BackendType)
    BackendType
        .value("UNDEFINED", wgpu::BackendType::Undefined)
        .value("NULL", wgpu::BackendType::Null)
        .value("WEB_GPU", wgpu::BackendType::WebGPU)
        .value("D3D11", wgpu::BackendType::D3D11)
        .value("D3D12", wgpu::BackendType::D3D12)
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
        .value("SRC1", wgpu::BlendFactor::Src1)
        .value("ONE_MINUS_SRC1", wgpu::BlendFactor::OneMinusSrc1)
        .value("SRC1_ALPHA", wgpu::BlendFactor::Src1Alpha)
        .value("ONE_MINUS_SRC1_ALPHA", wgpu::BlendFactor::OneMinusSrc1Alpha)
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
        .value("VALIDATION_ERROR", wgpu::BufferMapAsyncStatus::ValidationError)
        .value("UNKNOWN", wgpu::BufferMapAsyncStatus::Unknown)
        .value("DEVICE_LOST", wgpu::BufferMapAsyncStatus::DeviceLost)
        .value("DESTROYED_BEFORE_CALLBACK", wgpu::BufferMapAsyncStatus::DestroyedBeforeCallback)
        .value("UNMAPPED_BEFORE_CALLBACK", wgpu::BufferMapAsyncStatus::UnmappedBeforeCallback)
        .value("MAPPING_ALREADY_PENDING", wgpu::BufferMapAsyncStatus::MappingAlreadyPending)
        .value("OFFSET_OUT_OF_RANGE", wgpu::BufferMapAsyncStatus::OffsetOutOfRange)
        .value("SIZE_OUT_OF_RANGE", wgpu::BufferMapAsyncStatus::SizeOutOfRange)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::BufferMapAsyncStatus, BufferMapAsyncStatus)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::BufferMapState, BufferMapState)
    BufferMapState
        .value("UNMAPPED", wgpu::BufferMapState::Unmapped)
        .value("PENDING", wgpu::BufferMapState::Pending)
        .value("MAPPED", wgpu::BufferMapState::Mapped)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::BufferMapState, BufferMapState)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::CallbackMode, CallbackMode)
    CallbackMode
        .value("WAIT_ANY_ONLY", wgpu::CallbackMode::WaitAnyOnly)
        .value("ALLOW_PROCESS_EVENTS", wgpu::CallbackMode::AllowProcessEvents)
        .value("ALLOW_SPONTANEOUS", wgpu::CallbackMode::AllowSpontaneous)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::CallbackMode, CallbackMode)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::CompareFunction, CompareFunction)
    CompareFunction
        .value("UNDEFINED", wgpu::CompareFunction::Undefined)
        .value("NEVER", wgpu::CompareFunction::Never)
        .value("LESS", wgpu::CompareFunction::Less)
        .value("EQUAL", wgpu::CompareFunction::Equal)
        .value("LESS_EQUAL", wgpu::CompareFunction::LessEqual)
        .value("GREATER", wgpu::CompareFunction::Greater)
        .value("NOT_EQUAL", wgpu::CompareFunction::NotEqual)
        .value("GREATER_EQUAL", wgpu::CompareFunction::GreaterEqual)
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


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::CreatePipelineAsyncStatus, CreatePipelineAsyncStatus)
    CreatePipelineAsyncStatus
        .value("SUCCESS", wgpu::CreatePipelineAsyncStatus::Success)
        .value("VALIDATION_ERROR", wgpu::CreatePipelineAsyncStatus::ValidationError)
        .value("INTERNAL_ERROR", wgpu::CreatePipelineAsyncStatus::InternalError)
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
        .value("INTERNAL", wgpu::ErrorFilter::Internal)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::ErrorFilter, ErrorFilter)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::ErrorType, ErrorType)
    ErrorType
        .value("NO_ERROR", wgpu::ErrorType::NoError)
        .value("VALIDATION", wgpu::ErrorType::Validation)
        .value("OUT_OF_MEMORY", wgpu::ErrorType::OutOfMemory)
        .value("INTERNAL", wgpu::ErrorType::Internal)
        .value("UNKNOWN", wgpu::ErrorType::Unknown)
        .value("DEVICE_LOST", wgpu::ErrorType::DeviceLost)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::ErrorType, ErrorType)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::ExternalTextureRotation, ExternalTextureRotation)
    ExternalTextureRotation
        .value("ROTATE0_DEGREES", wgpu::ExternalTextureRotation::Rotate0Degrees)
        .value("ROTATE90_DEGREES", wgpu::ExternalTextureRotation::Rotate90Degrees)
        .value("ROTATE180_DEGREES", wgpu::ExternalTextureRotation::Rotate180Degrees)
        .value("ROTATE270_DEGREES", wgpu::ExternalTextureRotation::Rotate270Degrees)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::ExternalTextureRotation, ExternalTextureRotation)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::FeatureName, FeatureName)
    FeatureName
        .value("UNDEFINED", wgpu::FeatureName::Undefined)
        .value("DEPTH_CLIP_CONTROL", wgpu::FeatureName::DepthClipControl)
        .value("DEPTH32_FLOAT_STENCIL8", wgpu::FeatureName::Depth32FloatStencil8)
        .value("TIMESTAMP_QUERY", wgpu::FeatureName::TimestampQuery)
        .value("TEXTURE_COMPRESSION_BC", wgpu::FeatureName::TextureCompressionBC)
        .value("TEXTURE_COMPRESSION_ETC2", wgpu::FeatureName::TextureCompressionETC2)
        .value("TEXTURE_COMPRESSION_ASTC", wgpu::FeatureName::TextureCompressionASTC)
        .value("INDIRECT_FIRST_INSTANCE", wgpu::FeatureName::IndirectFirstInstance)
        .value("SHADER_F16", wgpu::FeatureName::ShaderF16)
        .value("RG11B10_UFLOAT_RENDERABLE", wgpu::FeatureName::RG11B10UfloatRenderable)
        .value("BGRA8_UNORM_STORAGE", wgpu::FeatureName::BGRA8UnormStorage)
        .value("FLOAT32_FILTERABLE", wgpu::FeatureName::Float32Filterable)
        .value("DAWN_INTERNAL_USAGES", wgpu::FeatureName::DawnInternalUsages)
        .value("DAWN_MULTI_PLANAR_FORMATS", wgpu::FeatureName::DawnMultiPlanarFormats)
        .value("DAWN_NATIVE", wgpu::FeatureName::DawnNative)
        .value("CHROMIUM_EXPERIMENTAL_TIMESTAMP_QUERY_INSIDE_PASSES", wgpu::FeatureName::ChromiumExperimentalTimestampQueryInsidePasses)
        .value("IMPLICIT_DEVICE_SYNCHRONIZATION", wgpu::FeatureName::ImplicitDeviceSynchronization)
        .value("SURFACE_CAPABILITIES", wgpu::FeatureName::SurfaceCapabilities)
        .value("TRANSIENT_ATTACHMENTS", wgpu::FeatureName::TransientAttachments)
        .value("MSAA_RENDER_TO_SINGLE_SAMPLED", wgpu::FeatureName::MSAARenderToSingleSampled)
        .value("DUAL_SOURCE_BLENDING", wgpu::FeatureName::DualSourceBlending)
        .value("D3D11_MULTITHREAD_PROTECTED", wgpu::FeatureName::D3D11MultithreadProtected)
        .value("ANGLE_TEXTURE_SHARING", wgpu::FeatureName::ANGLETextureSharing)
        .value("CHROMIUM_EXPERIMENTAL_SUBGROUPS", wgpu::FeatureName::ChromiumExperimentalSubgroups)
        .value("CHROMIUM_EXPERIMENTAL_SUBGROUP_UNIFORM_CONTROL_FLOW", wgpu::FeatureName::ChromiumExperimentalSubgroupUniformControlFlow)
        .value("PIXEL_LOCAL_STORAGE_COHERENT", wgpu::FeatureName::PixelLocalStorageCoherent)
        .value("PIXEL_LOCAL_STORAGE_NON_COHERENT", wgpu::FeatureName::PixelLocalStorageNonCoherent)
        .value("NORM16_TEXTURE_FORMATS", wgpu::FeatureName::Norm16TextureFormats)
        .value("MULTI_PLANAR_FORMAT_EXTENDED_USAGES", wgpu::FeatureName::MultiPlanarFormatExtendedUsages)
        .value("MULTI_PLANAR_FORMAT_P010", wgpu::FeatureName::MultiPlanarFormatP010)
        .value("HOST_MAPPED_POINTER", wgpu::FeatureName::HostMappedPointer)
        .value("MULTI_PLANAR_RENDER_TARGETS", wgpu::FeatureName::MultiPlanarRenderTargets)
        .value("MULTI_PLANAR_FORMAT_NV12A", wgpu::FeatureName::MultiPlanarFormatNv12a)
        .value("FRAMEBUFFER_FETCH", wgpu::FeatureName::FramebufferFetch)
        .value("BUFFER_MAP_EXTENDED_USAGES", wgpu::FeatureName::BufferMapExtendedUsages)
        .value("ADAPTER_PROPERTIES_MEMORY_HEAPS", wgpu::FeatureName::AdapterPropertiesMemoryHeaps)
        .value("SHARED_TEXTURE_MEMORY_VK_DEDICATED_ALLOCATION", wgpu::FeatureName::SharedTextureMemoryVkDedicatedAllocation)
        .value("SHARED_TEXTURE_MEMORY_A_HARDWARE_BUFFER", wgpu::FeatureName::SharedTextureMemoryAHardwareBuffer)
        .value("SHARED_TEXTURE_MEMORY_DMA_BUF", wgpu::FeatureName::SharedTextureMemoryDmaBuf)
        .value("SHARED_TEXTURE_MEMORY_OPAQUE_FD", wgpu::FeatureName::SharedTextureMemoryOpaqueFD)
        .value("SHARED_TEXTURE_MEMORY_ZIRCON_HANDLE", wgpu::FeatureName::SharedTextureMemoryZirconHandle)
        .value("SHARED_TEXTURE_MEMORY_DXGI_SHARED_HANDLE", wgpu::FeatureName::SharedTextureMemoryDXGISharedHandle)
        .value("SHARED_TEXTURE_MEMORY_D3D11_TEXTURE2D", wgpu::FeatureName::SharedTextureMemoryD3D11Texture2D)
        .value("SHARED_TEXTURE_MEMORY_IO_SURFACE", wgpu::FeatureName::SharedTextureMemoryIOSurface)
        .value("SHARED_TEXTURE_MEMORY_EGL_IMAGE", wgpu::FeatureName::SharedTextureMemoryEGLImage)
        .value("SHARED_FENCE_VK_SEMAPHORE_OPAQUE_FD", wgpu::FeatureName::SharedFenceVkSemaphoreOpaqueFD)
        .value("SHARED_FENCE_VK_SEMAPHORE_SYNC_FD", wgpu::FeatureName::SharedFenceVkSemaphoreSyncFD)
        .value("SHARED_FENCE_VK_SEMAPHORE_ZIRCON_HANDLE", wgpu::FeatureName::SharedFenceVkSemaphoreZirconHandle)
        .value("SHARED_FENCE_DXGI_SHARED_HANDLE", wgpu::FeatureName::SharedFenceDXGISharedHandle)
        .value("SHARED_FENCE_MTL_SHARED_EVENT", wgpu::FeatureName::SharedFenceMTLSharedEvent)
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


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::MipmapFilterMode, MipmapFilterMode)
    MipmapFilterMode
        .value("NEAREST", wgpu::MipmapFilterMode::Nearest)
        .value("LINEAR", wgpu::MipmapFilterMode::Linear)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::MipmapFilterMode, MipmapFilterMode)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::PowerPreference, PowerPreference)
    PowerPreference
        .value("UNDEFINED", wgpu::PowerPreference::Undefined)
        .value("LOW_POWER", wgpu::PowerPreference::LowPower)
        .value("HIGH_PERFORMANCE", wgpu::PowerPreference::HighPerformance)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::PowerPreference, PowerPreference)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::PresentMode, PresentMode)
    PresentMode
        .value("FIFO", wgpu::PresentMode::Fifo)
        .value("IMMEDIATE", wgpu::PresentMode::Immediate)
        .value("MAILBOX", wgpu::PresentMode::Mailbox)
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
        .value("DEPTH_STENCIL_STATE_DEPTH_WRITE_DEFINED_DAWN", wgpu::SType::DepthStencilStateDepthWriteDefinedDawn)
        .value("TEXTURE_BINDING_VIEW_DIMENSION_DESCRIPTOR", wgpu::SType::TextureBindingViewDimensionDescriptor)
        .value("DAWN_TEXTURE_INTERNAL_USAGE_DESCRIPTOR", wgpu::SType::DawnTextureInternalUsageDescriptor)
        .value("DAWN_ENCODER_INTERNAL_USAGE_DESCRIPTOR", wgpu::SType::DawnEncoderInternalUsageDescriptor)
        .value("DAWN_INSTANCE_DESCRIPTOR", wgpu::SType::DawnInstanceDescriptor)
        .value("DAWN_CACHE_DEVICE_DESCRIPTOR", wgpu::SType::DawnCacheDeviceDescriptor)
        .value("DAWN_ADAPTER_PROPERTIES_POWER_PREFERENCE", wgpu::SType::DawnAdapterPropertiesPowerPreference)
        .value("DAWN_BUFFER_DESCRIPTOR_ERROR_INFO_FROM_WIRE_CLIENT", wgpu::SType::DawnBufferDescriptorErrorInfoFromWireClient)
        .value("DAWN_TOGGLES_DESCRIPTOR", wgpu::SType::DawnTogglesDescriptor)
        .value("DAWN_SHADER_MODULE_SPIRV_OPTIONS_DESCRIPTOR", wgpu::SType::DawnShaderModuleSPIRVOptionsDescriptor)
        .value("REQUEST_ADAPTER_OPTIONS_LUID", wgpu::SType::RequestAdapterOptionsLUID)
        .value("REQUEST_ADAPTER_OPTIONS_GET_GL_PROC", wgpu::SType::RequestAdapterOptionsGetGLProc)
        .value("REQUEST_ADAPTER_OPTIONS_D3D11_DEVICE", wgpu::SType::RequestAdapterOptionsD3D11Device)
        .value("DAWN_MULTISAMPLE_STATE_RENDER_TO_SINGLE_SAMPLED", wgpu::SType::DawnMultisampleStateRenderToSingleSampled)
        .value("DAWN_RENDER_PASS_COLOR_ATTACHMENT_RENDER_TO_SINGLE_SAMPLED", wgpu::SType::DawnRenderPassColorAttachmentRenderToSingleSampled)
        .value("RENDER_PASS_PIXEL_LOCAL_STORAGE", wgpu::SType::RenderPassPixelLocalStorage)
        .value("PIPELINE_LAYOUT_PIXEL_LOCAL_STORAGE", wgpu::SType::PipelineLayoutPixelLocalStorage)
        .value("BUFFER_HOST_MAPPED_POINTER", wgpu::SType::BufferHostMappedPointer)
        .value("DAWN_EXPERIMENTAL_SUBGROUP_LIMITS", wgpu::SType::DawnExperimentalSubgroupLimits)
        .value("ADAPTER_PROPERTIES_MEMORY_HEAPS", wgpu::SType::AdapterPropertiesMemoryHeaps)
        .value("DAWN_COMPUTE_PIPELINE_FULL_SUBGROUPS", wgpu::SType::DawnComputePipelineFullSubgroups)
        .value("DAWN_WIRE_WGSL_CONTROL", wgpu::SType::DawnWireWGSLControl)
        .value("DAWN_WGSL_BLOCKLIST", wgpu::SType::DawnWGSLBlocklist)
        .value("SHARED_TEXTURE_MEMORY_VK_IMAGE_DESCRIPTOR", wgpu::SType::SharedTextureMemoryVkImageDescriptor)
        .value("SHARED_TEXTURE_MEMORY_VK_DEDICATED_ALLOCATION_DESCRIPTOR", wgpu::SType::SharedTextureMemoryVkDedicatedAllocationDescriptor)
        .value("SHARED_TEXTURE_MEMORY_A_HARDWARE_BUFFER_DESCRIPTOR", wgpu::SType::SharedTextureMemoryAHardwareBufferDescriptor)
        .value("SHARED_TEXTURE_MEMORY_DMA_BUF_DESCRIPTOR", wgpu::SType::SharedTextureMemoryDmaBufDescriptor)
        .value("SHARED_TEXTURE_MEMORY_OPAQUE_FD_DESCRIPTOR", wgpu::SType::SharedTextureMemoryOpaqueFDDescriptor)
        .value("SHARED_TEXTURE_MEMORY_ZIRCON_HANDLE_DESCRIPTOR", wgpu::SType::SharedTextureMemoryZirconHandleDescriptor)
        .value("SHARED_TEXTURE_MEMORY_DXGI_SHARED_HANDLE_DESCRIPTOR", wgpu::SType::SharedTextureMemoryDXGISharedHandleDescriptor)
        .value("SHARED_TEXTURE_MEMORY_D3D11_TEXTURE2D_DESCRIPTOR", wgpu::SType::SharedTextureMemoryD3D11Texture2DDescriptor)
        .value("SHARED_TEXTURE_MEMORY_IO_SURFACE_DESCRIPTOR", wgpu::SType::SharedTextureMemoryIOSurfaceDescriptor)
        .value("SHARED_TEXTURE_MEMORY_EGL_IMAGE_DESCRIPTOR", wgpu::SType::SharedTextureMemoryEGLImageDescriptor)
        .value("SHARED_TEXTURE_MEMORY_INITIALIZED_BEGIN_STATE", wgpu::SType::SharedTextureMemoryInitializedBeginState)
        .value("SHARED_TEXTURE_MEMORY_INITIALIZED_END_STATE", wgpu::SType::SharedTextureMemoryInitializedEndState)
        .value("SHARED_TEXTURE_MEMORY_VK_IMAGE_LAYOUT_BEGIN_STATE", wgpu::SType::SharedTextureMemoryVkImageLayoutBeginState)
        .value("SHARED_TEXTURE_MEMORY_VK_IMAGE_LAYOUT_END_STATE", wgpu::SType::SharedTextureMemoryVkImageLayoutEndState)
        .value("SHARED_FENCE_VK_SEMAPHORE_OPAQUE_FD_DESCRIPTOR", wgpu::SType::SharedFenceVkSemaphoreOpaqueFDDescriptor)
        .value("SHARED_FENCE_VK_SEMAPHORE_OPAQUE_FD_EXPORT_INFO", wgpu::SType::SharedFenceVkSemaphoreOpaqueFDExportInfo)
        .value("SHARED_FENCE_VK_SEMAPHORE_SYNC_FD_DESCRIPTOR", wgpu::SType::SharedFenceVkSemaphoreSyncFDDescriptor)
        .value("SHARED_FENCE_VK_SEMAPHORE_SYNC_FD_EXPORT_INFO", wgpu::SType::SharedFenceVkSemaphoreSyncFDExportInfo)
        .value("SHARED_FENCE_VK_SEMAPHORE_ZIRCON_HANDLE_DESCRIPTOR", wgpu::SType::SharedFenceVkSemaphoreZirconHandleDescriptor)
        .value("SHARED_FENCE_VK_SEMAPHORE_ZIRCON_HANDLE_EXPORT_INFO", wgpu::SType::SharedFenceVkSemaphoreZirconHandleExportInfo)
        .value("SHARED_FENCE_DXGI_SHARED_HANDLE_DESCRIPTOR", wgpu::SType::SharedFenceDXGISharedHandleDescriptor)
        .value("SHARED_FENCE_DXGI_SHARED_HANDLE_EXPORT_INFO", wgpu::SType::SharedFenceDXGISharedHandleExportInfo)
        .value("SHARED_FENCE_MTL_SHARED_EVENT_DESCRIPTOR", wgpu::SType::SharedFenceMTLSharedEventDescriptor)
        .value("SHARED_FENCE_MTL_SHARED_EVENT_EXPORT_INFO", wgpu::SType::SharedFenceMTLSharedEventExportInfo)
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


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::SharedFenceType, SharedFenceType)
    SharedFenceType
        .value("UNDEFINED", wgpu::SharedFenceType::Undefined)
        .value("VK_SEMAPHORE_OPAQUE_FD", wgpu::SharedFenceType::VkSemaphoreOpaqueFD)
        .value("VK_SEMAPHORE_SYNC_FD", wgpu::SharedFenceType::VkSemaphoreSyncFD)
        .value("VK_SEMAPHORE_ZIRCON_HANDLE", wgpu::SharedFenceType::VkSemaphoreZirconHandle)
        .value("DXGI_SHARED_HANDLE", wgpu::SharedFenceType::DXGISharedHandle)
        .value("MTL_SHARED_EVENT", wgpu::SharedFenceType::MTLSharedEvent)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::SharedFenceType, SharedFenceType)


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
        .value("READ_ONLY", wgpu::StorageTextureAccess::ReadOnly)
        .value("READ_WRITE", wgpu::StorageTextureAccess::ReadWrite)
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
        .value("PLANE2_ONLY", wgpu::TextureAspect::Plane2Only)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::TextureAspect, TextureAspect)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::TextureDimension, TextureDimension)
    TextureDimension
        .value("E1D", wgpu::TextureDimension::e1D)
        .value("E2D", wgpu::TextureDimension::e2D)
        .value("E3D", wgpu::TextureDimension::e3D)
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
        .value("RGB10A2_UINT", wgpu::TextureFormat::RGB10A2Uint)
        .value("RGB10A2_UNORM", wgpu::TextureFormat::RGB10A2Unorm)
        .value("RG11B10_UFLOAT", wgpu::TextureFormat::RG11B10Ufloat)
        .value("RGB9E5_UFLOAT", wgpu::TextureFormat::RGB9E5Ufloat)
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
        .value("BC1RGBA_UNORM", wgpu::TextureFormat::BC1RGBAUnorm)
        .value("BC1RGBA_UNORM_SRGB", wgpu::TextureFormat::BC1RGBAUnormSrgb)
        .value("BC2RGBA_UNORM", wgpu::TextureFormat::BC2RGBAUnorm)
        .value("BC2RGBA_UNORM_SRGB", wgpu::TextureFormat::BC2RGBAUnormSrgb)
        .value("BC3RGBA_UNORM", wgpu::TextureFormat::BC3RGBAUnorm)
        .value("BC3RGBA_UNORM_SRGB", wgpu::TextureFormat::BC3RGBAUnormSrgb)
        .value("BC4R_UNORM", wgpu::TextureFormat::BC4RUnorm)
        .value("BC4R_SNORM", wgpu::TextureFormat::BC4RSnorm)
        .value("BC5RG_UNORM", wgpu::TextureFormat::BC5RGUnorm)
        .value("BC5RG_SNORM", wgpu::TextureFormat::BC5RGSnorm)
        .value("BC6HRGB_UFLOAT", wgpu::TextureFormat::BC6HRGBUfloat)
        .value("BC6HRGB_FLOAT", wgpu::TextureFormat::BC6HRGBFloat)
        .value("BC7RGBA_UNORM", wgpu::TextureFormat::BC7RGBAUnorm)
        .value("BC7RGBA_UNORM_SRGB", wgpu::TextureFormat::BC7RGBAUnormSrgb)
        .value("ETC2RGB8_UNORM", wgpu::TextureFormat::ETC2RGB8Unorm)
        .value("ETC2RGB8_UNORM_SRGB", wgpu::TextureFormat::ETC2RGB8UnormSrgb)
        .value("ETC2RGB8A1_UNORM", wgpu::TextureFormat::ETC2RGB8A1Unorm)
        .value("ETC2RGB8A1_UNORM_SRGB", wgpu::TextureFormat::ETC2RGB8A1UnormSrgb)
        .value("ETC2RGBA8_UNORM", wgpu::TextureFormat::ETC2RGBA8Unorm)
        .value("ETC2RGBA8_UNORM_SRGB", wgpu::TextureFormat::ETC2RGBA8UnormSrgb)
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
        .value("R16_UNORM", wgpu::TextureFormat::R16Unorm)
        .value("RG16_UNORM", wgpu::TextureFormat::RG16Unorm)
        .value("RGBA16_UNORM", wgpu::TextureFormat::RGBA16Unorm)
        .value("R16_SNORM", wgpu::TextureFormat::R16Snorm)
        .value("RG16_SNORM", wgpu::TextureFormat::RG16Snorm)
        .value("RGBA16_SNORM", wgpu::TextureFormat::RGBA16Snorm)
        .value("R8BG8_BIPLANAR420_UNORM", wgpu::TextureFormat::R8BG8Biplanar420Unorm)
        .value("R10X6BG10X6_BIPLANAR420_UNORM", wgpu::TextureFormat::R10X6BG10X6Biplanar420Unorm)
        .value("R8BG8A8_TRIPLANAR420_UNORM", wgpu::TextureFormat::R8BG8A8Triplanar420Unorm)
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
        .value("E1D", wgpu::TextureViewDimension::e1D)
        .value("E2D", wgpu::TextureViewDimension::e2D)
        .value("E2D_ARRAY", wgpu::TextureViewDimension::e2DArray)
        .value("CUBE", wgpu::TextureViewDimension::Cube)
        .value("CUBE_ARRAY", wgpu::TextureViewDimension::CubeArray)
        .value("E3D", wgpu::TextureViewDimension::e3D)
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
        .value("UNORM10_10_10_2", wgpu::VertexFormat::Unorm10_10_10_2)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::VertexFormat, VertexFormat)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::VertexStepMode, VertexStepMode)
    VertexStepMode
        .value("VERTEX", wgpu::VertexStepMode::Vertex)
        .value("INSTANCE", wgpu::VertexStepMode::Instance)
        .value("VERTEX_BUFFER_NOT_USED", wgpu::VertexStepMode::VertexBufferNotUsed)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::VertexStepMode, VertexStepMode)


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::WaitStatus, WaitStatus)
    WaitStatus
        .value("SUCCESS", wgpu::WaitStatus::Success)
        .value("TIMED_OUT", wgpu::WaitStatus::TimedOut)
        .value("UNSUPPORTED_TIMEOUT", wgpu::WaitStatus::UnsupportedTimeout)
        .value("UNSUPPORTED_COUNT", wgpu::WaitStatus::UnsupportedCount)
        .value("UNSUPPORTED_MIXED_SOURCES", wgpu::WaitStatus::UnsupportedMixedSources)
        .value("UNKNOWN", wgpu::WaitStatus::Unknown)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::WaitStatus, WaitStatus)


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


    PYENUM_SCOPED_BEGIN(_wgpu, wgpu::HeapProperty, HeapProperty)
    HeapProperty
        .value("UNDEFINED", wgpu::HeapProperty::Undefined)
        .value("DEVICE_LOCAL", wgpu::HeapProperty::DeviceLocal)
        .value("HOST_VISIBLE", wgpu::HeapProperty::HostVisible)
        .value("HOST_COHERENT", wgpu::HeapProperty::HostCoherent)
        .value("HOST_UNCACHED", wgpu::HeapProperty::HostUncached)
        .value("HOST_CACHED", wgpu::HeapProperty::HostCached)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::HeapProperty, HeapProperty)


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
        .value("TRANSIENT_ATTACHMENT", wgpu::TextureUsage::TransientAttachment)
        .value("STORAGE_ATTACHMENT", wgpu::TextureUsage::StorageAttachment)
        .export_values();
    PYENUM_SCOPED_END(_wgpu, wgpu::TextureUsage, TextureUsage)


    PYCLASS_BEGIN(_wgpu, wgpu::Bool, Bool)
        Bool.def(py::init<>());
        Bool.def(py::init<bool>()
        , py::arg("value")
        );
        Bool.def(py::init<WGPUBool>()
        , py::arg("value")
        );
    PYCLASS_END(_wgpu, wgpu::Bool, Bool)

    PYCLASS_BEGIN(_wgpu, wgpu::Adapter, Adapter)
        Adapter.def("create_device", &wgpu::Adapter::CreateDevice
        , py::arg("descriptor") = nullptr
        , py::return_value_policy::automatic_reference);

        Adapter.def("enumerate_features", &wgpu::Adapter::EnumerateFeatures
        , py::arg("features")
        , py::return_value_policy::automatic_reference);

        Adapter.def("get_instance", &wgpu::Adapter::GetInstance
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

    PYCLASS_END(_wgpu, wgpu::Adapter, Adapter)

    PYCLASS_BEGIN(_wgpu, wgpu::BindGroup, BindGroup)
        BindGroup.def("set_label", &wgpu::BindGroup::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

    PYCLASS_END(_wgpu, wgpu::BindGroup, BindGroup)

    PYCLASS_BEGIN(_wgpu, wgpu::BindGroupLayout, BindGroupLayout)
        BindGroupLayout.def("set_label", &wgpu::BindGroupLayout::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

    PYCLASS_END(_wgpu, wgpu::BindGroupLayout, BindGroupLayout)

    PYCLASS_BEGIN(_wgpu, wgpu::Buffer, Buffer)
        Buffer.def("destroy", &wgpu::Buffer::Destroy
        , py::return_value_policy::automatic_reference);

        Buffer.def("get_const_mapped_range", &wgpu::Buffer::GetConstMappedRange
        , py::arg("offset") = 0
        , py::arg("size") = WGPU_WHOLE_MAP_SIZE
        , py::return_value_policy::automatic_reference);

        Buffer.def("get_map_state", &wgpu::Buffer::GetMapState
        , py::return_value_policy::automatic_reference);

        Buffer.def("get_mapped_range", &wgpu::Buffer::GetMappedRange
        , py::arg("offset") = 0
        , py::arg("size") = WGPU_WHOLE_MAP_SIZE
        , py::return_value_policy::automatic_reference);

        Buffer.def("get_size", &wgpu::Buffer::GetSize
        , py::return_value_policy::automatic_reference);

        Buffer.def("get_usage", &wgpu::Buffer::GetUsage
        , py::return_value_policy::automatic_reference);

        Buffer.def("map_async_f", &wgpu::Buffer::MapAsyncF
        , py::arg("mode")
        , py::arg("offset")
        , py::arg("size")
        , py::arg("callback_info")
        , py::return_value_policy::automatic_reference);

        Buffer.def("set_label", &wgpu::Buffer::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

        Buffer.def("unmap", &wgpu::Buffer::Unmap
        , py::return_value_policy::automatic_reference);

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

    PYCLASS_END(_wgpu, wgpu::CommandEncoder, CommandEncoder)

    PYCLASS_BEGIN(_wgpu, wgpu::ComputePassEncoder, ComputePassEncoder)
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

    PYCLASS_END(_wgpu, wgpu::ComputePassEncoder, ComputePassEncoder)

    PYCLASS_BEGIN(_wgpu, wgpu::ComputePipeline, ComputePipeline)
        ComputePipeline.def("get_bind_group_layout", &wgpu::ComputePipeline::GetBindGroupLayout
        , py::arg("group_index")
        , py::return_value_policy::automatic_reference);

        ComputePipeline.def("set_label", &wgpu::ComputePipeline::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

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
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference);

        Device.def("create_error_external_texture", &wgpu::Device::CreateErrorExternalTexture
        , py::return_value_policy::automatic_reference);

        Device.def("create_error_shader_module", &wgpu::Device::CreateErrorShaderModule
        , py::arg("descriptor")
        , py::arg("error_message")
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

        Device.def("force_loss", &wgpu::Device::ForceLoss
        , py::arg("type")
        , py::arg("message")
        , py::return_value_policy::automatic_reference);

        Device.def("get_adapter", &wgpu::Device::GetAdapter
        , py::return_value_policy::automatic_reference);

        Device.def("get_limits", &wgpu::Device::GetLimits
        , py::arg("limits")
        , py::return_value_policy::automatic_reference);

        Device.def("get_queue", &wgpu::Device::GetQueue
        , py::return_value_policy::automatic_reference);

        Device.def("get_supported_surface_usage", &wgpu::Device::GetSupportedSurfaceUsage
        , py::arg("surface")
        , py::return_value_policy::automatic_reference);

        Device.def("has_feature", &wgpu::Device::HasFeature
        , py::arg("feature")
        , py::return_value_policy::automatic_reference);

        Device.def("import_shared_fence", &wgpu::Device::ImportSharedFence
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference);

        Device.def("import_shared_texture_memory", &wgpu::Device::ImportSharedTextureMemory
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference);

        Device.def("inject_error", &wgpu::Device::InjectError
        , py::arg("type")
        , py::arg("message")
        , py::return_value_policy::automatic_reference);

        Device.def("push_error_scope", &wgpu::Device::PushErrorScope
        , py::arg("filter")
        , py::return_value_policy::automatic_reference);

        Device.def("set_label", &wgpu::Device::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

        Device.def("tick", &wgpu::Device::Tick
        , py::return_value_policy::automatic_reference);

        Device.def("validate_texture_descriptor", &wgpu::Device::ValidateTextureDescriptor
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference);

    PYCLASS_END(_wgpu, wgpu::Device, Device)

    PYCLASS_BEGIN(_wgpu, wgpu::ExternalTexture, ExternalTexture)
        ExternalTexture.def("destroy", &wgpu::ExternalTexture::Destroy
        , py::return_value_policy::automatic_reference);

        ExternalTexture.def("expire", &wgpu::ExternalTexture::Expire
        , py::return_value_policy::automatic_reference);

        ExternalTexture.def("refresh", &wgpu::ExternalTexture::Refresh
        , py::return_value_policy::automatic_reference);

        ExternalTexture.def("set_label", &wgpu::ExternalTexture::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

    PYCLASS_END(_wgpu, wgpu::ExternalTexture, ExternalTexture)

    PYCLASS_BEGIN(_wgpu, wgpu::Instance, Instance)
        Instance.def("create_surface", &wgpu::Instance::CreateSurface
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference);

        Instance.def("enumerate_wgsl_language_features", &wgpu::Instance::EnumerateWGSLLanguageFeatures
        , py::arg("features")
        , py::return_value_policy::automatic_reference);

        Instance.def("has_wgsl_language_feature", &wgpu::Instance::HasWGSLLanguageFeature
        , py::arg("feature")
        , py::return_value_policy::automatic_reference);

        Instance.def("process_events", &wgpu::Instance::ProcessEvents
        , py::return_value_policy::automatic_reference);

        Instance.def("request_adapter_f", &wgpu::Instance::RequestAdapterF
        , py::arg("options")
        , py::arg("callback_info")
        , py::return_value_policy::automatic_reference);

        Instance.def("wait_any", &wgpu::Instance::WaitAny
        , py::arg("future_count")
        , py::arg("futures")
        , py::arg("timeout_ns")
        , py::return_value_policy::automatic_reference);

    PYCLASS_END(_wgpu, wgpu::Instance, Instance)

    PYCLASS_BEGIN(_wgpu, wgpu::PipelineLayout, PipelineLayout)
        PipelineLayout.def("set_label", &wgpu::PipelineLayout::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

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

    PYCLASS_END(_wgpu, wgpu::QuerySet, QuerySet)

    PYCLASS_BEGIN(_wgpu, wgpu::Queue, Queue)
        Queue.def("copy_external_texture_for_browser", &wgpu::Queue::CopyExternalTextureForBrowser
        , py::arg("source")
        , py::arg("destination")
        , py::arg("copy_size")
        , py::arg("options")
        , py::return_value_policy::automatic_reference);

        Queue.def("copy_texture_for_browser", &wgpu::Queue::CopyTextureForBrowser
        , py::arg("source")
        , py::arg("destination")
        , py::arg("copy_size")
        , py::arg("options")
        , py::return_value_policy::automatic_reference);

        Queue.def("on_submitted_work_done_f", &wgpu::Queue::OnSubmittedWorkDoneF
        , py::arg("callback_info")
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

    PYCLASS_END(_wgpu, wgpu::Queue, Queue)

    PYCLASS_BEGIN(_wgpu, wgpu::RenderBundle, RenderBundle)
        RenderBundle.def("set_label", &wgpu::RenderBundle::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

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

        RenderPassEncoder.def("execute_bundles", &wgpu::RenderPassEncoder::ExecuteBundles
        , py::arg("bundle_count")
        , py::arg("bundles")
        , py::return_value_policy::automatic_reference);

        RenderPassEncoder.def("insert_debug_marker", &wgpu::RenderPassEncoder::InsertDebugMarker
        , py::arg("marker_label")
        , py::return_value_policy::automatic_reference);

        RenderPassEncoder.def("pixel_local_storage_barrier", &wgpu::RenderPassEncoder::PixelLocalStorageBarrier
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

    PYCLASS_END(_wgpu, wgpu::RenderPassEncoder, RenderPassEncoder)

    PYCLASS_BEGIN(_wgpu, wgpu::RenderPipeline, RenderPipeline)
        RenderPipeline.def("get_bind_group_layout", &wgpu::RenderPipeline::GetBindGroupLayout
        , py::arg("group_index")
        , py::return_value_policy::automatic_reference);

        RenderPipeline.def("set_label", &wgpu::RenderPipeline::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

    PYCLASS_END(_wgpu, wgpu::RenderPipeline, RenderPipeline)

    PYCLASS_BEGIN(_wgpu, wgpu::Sampler, Sampler)
        Sampler.def("set_label", &wgpu::Sampler::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

    PYCLASS_END(_wgpu, wgpu::Sampler, Sampler)

    PYCLASS_BEGIN(_wgpu, wgpu::ShaderModule, ShaderModule)
        ShaderModule.def("set_label", &wgpu::ShaderModule::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

    PYCLASS_END(_wgpu, wgpu::ShaderModule, ShaderModule)

    PYCLASS_BEGIN(_wgpu, wgpu::SharedFence, SharedFence)
        SharedFence.def("export_info", &wgpu::SharedFence::ExportInfo
        , py::arg("info")
        , py::return_value_policy::automatic_reference);

    PYCLASS_END(_wgpu, wgpu::SharedFence, SharedFence)

    PYCLASS_BEGIN(_wgpu, wgpu::SharedTextureMemory, SharedTextureMemory)
        SharedTextureMemory.def("begin_access", &wgpu::SharedTextureMemory::BeginAccess
        , py::arg("texture")
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference);

        SharedTextureMemory.def("create_texture", &wgpu::SharedTextureMemory::CreateTexture
        , py::arg("descriptor") = nullptr
        , py::return_value_policy::automatic_reference);

        SharedTextureMemory.def("end_access", &wgpu::SharedTextureMemory::EndAccess
        , py::arg("texture")
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference);

        SharedTextureMemory.def("get_properties", &wgpu::SharedTextureMemory::GetProperties
        , py::arg("properties")
        , py::return_value_policy::automatic_reference);

        SharedTextureMemory.def("is_device_lost", &wgpu::SharedTextureMemory::IsDeviceLost
        , py::return_value_policy::automatic_reference);

        SharedTextureMemory.def("set_label", &wgpu::SharedTextureMemory::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

    PYCLASS_END(_wgpu, wgpu::SharedTextureMemory, SharedTextureMemory)

    PYCLASS_BEGIN(_wgpu, wgpu::Surface, Surface)
    PYCLASS_END(_wgpu, wgpu::Surface, Surface)

    PYCLASS_BEGIN(_wgpu, wgpu::SwapChain, SwapChain)
        SwapChain.def("get_current_texture", &wgpu::SwapChain::GetCurrentTexture
        , py::return_value_policy::automatic_reference);

        SwapChain.def("get_current_texture_view", &wgpu::SwapChain::GetCurrentTextureView
        , py::return_value_policy::automatic_reference);

        SwapChain.def("present", &wgpu::SwapChain::Present
        , py::return_value_policy::automatic_reference);

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

    PYCLASS_END(_wgpu, wgpu::Texture, Texture)

    PYCLASS_BEGIN(_wgpu, wgpu::TextureView, TextureView)
        TextureView.def("set_label", &wgpu::TextureView::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference);

    PYCLASS_END(_wgpu, wgpu::TextureView, TextureView)

    _wgpu.def("create_instance", &wgpu::CreateInstance
    , py::arg("descriptor") = nullptr
    , py::return_value_policy::automatic_reference);

    _wgpu.def("get_instance_features", &wgpu::GetInstanceFeatures
    , py::arg("features")
    , py::return_value_policy::automatic_reference);

    PYCLASS_BEGIN(_wgpu, wgpu::AdapterProperties, AdapterProperties)
        AdapterProperties.def_readonly("next_in_chain", &wgpu::AdapterProperties::nextInChain);
        AdapterProperties.def_readonly("vendor_id", &wgpu::AdapterProperties::vendorID);
        AdapterProperties.def_readonly("vendor_name", &wgpu::AdapterProperties::vendorName);
        AdapterProperties.def_readonly("architecture", &wgpu::AdapterProperties::architecture);
        AdapterProperties.def_readonly("device_id", &wgpu::AdapterProperties::deviceID);
        AdapterProperties.def_readonly("name", &wgpu::AdapterProperties::name);
        AdapterProperties.def_readonly("driver_description", &wgpu::AdapterProperties::driverDescription);
        AdapterProperties.def_readonly("adapter_type", &wgpu::AdapterProperties::adapterType);
        AdapterProperties.def_readonly("backend_type", &wgpu::AdapterProperties::backendType);
        AdapterProperties.def_readonly("compatibility_mode", &wgpu::AdapterProperties::compatibilityMode);
    PYCLASS_END(_wgpu, wgpu::AdapterProperties, AdapterProperties)

    PYCLASS_BEGIN(_wgpu, wgpu::BindGroupEntry, BindGroupEntry)
        BindGroupEntry.def_readwrite("next_in_chain", &wgpu::BindGroupEntry::nextInChain);
        BindGroupEntry.def_readwrite("binding", &wgpu::BindGroupEntry::binding);
        BindGroupEntry.def_readwrite("buffer", &wgpu::BindGroupEntry::buffer);
        BindGroupEntry.def_readwrite("offset", &wgpu::BindGroupEntry::offset);
        BindGroupEntry.def_readwrite("size", &wgpu::BindGroupEntry::size);
        BindGroupEntry.def_readwrite("sampler", &wgpu::BindGroupEntry::sampler);
        BindGroupEntry.def_readwrite("texture_view", &wgpu::BindGroupEntry::textureView);
        BindGroupEntry.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::BindGroupEntry obj;
            if (kwargs.contains("next_in_chain"))
            {
                auto value = kwargs["next_in_chain"].cast<const wgpu::ChainedStruct *>();
                obj.nextInChain = value;
            }
            if (kwargs.contains("binding"))
            {
                auto value = kwargs["binding"].cast<uint32_t>();
                obj.binding = value;
            }
            if (kwargs.contains("buffer"))
            {
                auto value = kwargs["buffer"].cast<wgpu::Buffer>();
                obj.buffer = value;
            }
            if (kwargs.contains("offset"))
            {
                auto value = kwargs["offset"].cast<uint64_t>();
                obj.offset = value;
            }
            if (kwargs.contains("size"))
            {
                auto value = kwargs["size"].cast<uint64_t>();
                obj.size = value;
            }
            if (kwargs.contains("sampler"))
            {
                auto value = kwargs["sampler"].cast<wgpu::Sampler>();
                obj.sampler = value;
            }
            if (kwargs.contains("texture_view"))
            {
                auto value = kwargs["texture_view"].cast<wgpu::TextureView>();
                obj.textureView = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
    PYCLASS_END(_wgpu, wgpu::BindGroupEntry, BindGroupEntry)

    PYCLASS_BEGIN(_wgpu, wgpu::BlendComponent, BlendComponent)
        BlendComponent.def_readwrite("operation", &wgpu::BlendComponent::operation);
        BlendComponent.def_readwrite("src_factor", &wgpu::BlendComponent::srcFactor);
        BlendComponent.def_readwrite("dst_factor", &wgpu::BlendComponent::dstFactor);
        BlendComponent.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::BlendComponent obj;
            if (kwargs.contains("operation"))
            {
                auto value = kwargs["operation"].cast<wgpu::BlendOperation>();
                obj.operation = value;
            }
            if (kwargs.contains("src_factor"))
            {
                auto value = kwargs["src_factor"].cast<wgpu::BlendFactor>();
                obj.srcFactor = value;
            }
            if (kwargs.contains("dst_factor"))
            {
                auto value = kwargs["dst_factor"].cast<wgpu::BlendFactor>();
                obj.dstFactor = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
    PYCLASS_END(_wgpu, wgpu::BlendComponent, BlendComponent)

    PYCLASS_BEGIN(_wgpu, wgpu::BufferBindingLayout, BufferBindingLayout)
        BufferBindingLayout.def_readwrite("next_in_chain", &wgpu::BufferBindingLayout::nextInChain);
        BufferBindingLayout.def_readwrite("type", &wgpu::BufferBindingLayout::type);
        BufferBindingLayout.def_readwrite("has_dynamic_offset", &wgpu::BufferBindingLayout::hasDynamicOffset);
        BufferBindingLayout.def_readwrite("min_binding_size", &wgpu::BufferBindingLayout::minBindingSize);
        BufferBindingLayout.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::BufferBindingLayout obj;
            if (kwargs.contains("next_in_chain"))
            {
                auto value = kwargs["next_in_chain"].cast<const wgpu::ChainedStruct *>();
                obj.nextInChain = value;
            }
            if (kwargs.contains("type"))
            {
                auto value = kwargs["type"].cast<wgpu::BufferBindingType>();
                obj.type = value;
            }
            if (kwargs.contains("has_dynamic_offset"))
            {
                auto value = kwargs["has_dynamic_offset"].cast<wgpu::Bool>();
                obj.hasDynamicOffset = value;
            }
            if (kwargs.contains("min_binding_size"))
            {
                auto value = kwargs["min_binding_size"].cast<uint64_t>();
                obj.minBindingSize = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
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

    PYSUBCLASS_BEGIN(_wgpu, wgpu::BufferHostMappedPointer, struct wgpu::ChainedStruct, BufferHostMappedPointer)
        BufferHostMappedPointer.def(py::init<>());
        BufferHostMappedPointer.def_readwrite("pointer", &wgpu::BufferHostMappedPointer::pointer);
        BufferHostMappedPointer.def_readwrite("userdata", &wgpu::BufferHostMappedPointer::userdata);
    PYCLASS_END(_wgpu, wgpu::BufferHostMappedPointer, BufferHostMappedPointer)

    PYCLASS_BEGIN(_wgpu, wgpu::BufferMapCallbackInfo, BufferMapCallbackInfo)
        BufferMapCallbackInfo.def_readwrite("next_in_chain", &wgpu::BufferMapCallbackInfo::nextInChain);
        BufferMapCallbackInfo.def_readwrite("mode", &wgpu::BufferMapCallbackInfo::mode);
        BufferMapCallbackInfo.def_readwrite("userdata", &wgpu::BufferMapCallbackInfo::userdata);
    PYCLASS_END(_wgpu, wgpu::BufferMapCallbackInfo, BufferMapCallbackInfo)

    PYCLASS_BEGIN(_wgpu, wgpu::Color, Color)
        Color.def_readwrite("r", &wgpu::Color::r);
        Color.def_readwrite("g", &wgpu::Color::g);
        Color.def_readwrite("b", &wgpu::Color::b);
        Color.def_readwrite("a", &wgpu::Color::a);
    PYCLASS_END(_wgpu, wgpu::Color, Color)

    PYCLASS_BEGIN(_wgpu, wgpu::CommandBufferDescriptor, CommandBufferDescriptor)
        CommandBufferDescriptor.def_readwrite("next_in_chain", &wgpu::CommandBufferDescriptor::nextInChain);
        CommandBufferDescriptor.def_property("label",
            [](const wgpu::CommandBufferDescriptor& self){ return self.label; },[](wgpu::CommandBufferDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
    PYCLASS_END(_wgpu, wgpu::CommandBufferDescriptor, CommandBufferDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::CommandEncoderDescriptor, CommandEncoderDescriptor)
        CommandEncoderDescriptor.def_readwrite("next_in_chain", &wgpu::CommandEncoderDescriptor::nextInChain);
        CommandEncoderDescriptor.def_property("label",
            [](const wgpu::CommandEncoderDescriptor& self){ return self.label; },[](wgpu::CommandEncoderDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
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
        CompilationMessage.def_readwrite("utf16_line_pos", &wgpu::CompilationMessage::utf16LinePos);
        CompilationMessage.def_readwrite("utf16_offset", &wgpu::CompilationMessage::utf16Offset);
        CompilationMessage.def_readwrite("utf16_length", &wgpu::CompilationMessage::utf16Length);
    PYCLASS_END(_wgpu, wgpu::CompilationMessage, CompilationMessage)

    PYCLASS_BEGIN(_wgpu, wgpu::ComputePassTimestampWrites, ComputePassTimestampWrites)
        ComputePassTimestampWrites.def_readwrite("query_set", &wgpu::ComputePassTimestampWrites::querySet);
        ComputePassTimestampWrites.def_readwrite("beginning_of_pass_write_index", &wgpu::ComputePassTimestampWrites::beginningOfPassWriteIndex);
        ComputePassTimestampWrites.def_readwrite("end_of_pass_write_index", &wgpu::ComputePassTimestampWrites::endOfPassWriteIndex);
    PYCLASS_END(_wgpu, wgpu::ComputePassTimestampWrites, ComputePassTimestampWrites)

    PYCLASS_BEGIN(_wgpu, wgpu::ConstantEntry, ConstantEntry)
        ConstantEntry.def_readwrite("next_in_chain", &wgpu::ConstantEntry::nextInChain);
        ConstantEntry.def_property("key",
            [](const wgpu::ConstantEntry& self){ return self.key; },[](wgpu::ConstantEntry& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.key = c; }
        );
        ConstantEntry.def_readwrite("value", &wgpu::ConstantEntry::value);
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
    PYCLASS_END(_wgpu, wgpu::CopyTextureForBrowserOptions, CopyTextureForBrowserOptions)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::DawnWGSLBlocklist, struct wgpu::ChainedStruct, DawnWGSLBlocklist)
        DawnWGSLBlocklist.def(py::init<>());
        DawnWGSLBlocklist.def_readwrite("blocklisted_feature_count", &wgpu::DawnWGSLBlocklist::blocklistedFeatureCount);
    PYCLASS_END(_wgpu, wgpu::DawnWGSLBlocklist, DawnWGSLBlocklist)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::DawnAdapterPropertiesPowerPreference, struct wgpu::ChainedStructOut, DawnAdapterPropertiesPowerPreference)
        DawnAdapterPropertiesPowerPreference.def(py::init<>());
        DawnAdapterPropertiesPowerPreference.def_readwrite("power_preference", &wgpu::DawnAdapterPropertiesPowerPreference::powerPreference);
    PYCLASS_END(_wgpu, wgpu::DawnAdapterPropertiesPowerPreference, DawnAdapterPropertiesPowerPreference)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::DawnBufferDescriptorErrorInfoFromWireClient, struct wgpu::ChainedStruct, DawnBufferDescriptorErrorInfoFromWireClient)
        DawnBufferDescriptorErrorInfoFromWireClient.def(py::init<>());
        DawnBufferDescriptorErrorInfoFromWireClient.def_readwrite("out_of_memory", &wgpu::DawnBufferDescriptorErrorInfoFromWireClient::outOfMemory);
    PYCLASS_END(_wgpu, wgpu::DawnBufferDescriptorErrorInfoFromWireClient, DawnBufferDescriptorErrorInfoFromWireClient)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::DawnCacheDeviceDescriptor, struct wgpu::ChainedStruct, DawnCacheDeviceDescriptor)
        DawnCacheDeviceDescriptor.def(py::init<>());
        DawnCacheDeviceDescriptor.def_property("isolation_key",
            [](const wgpu::DawnCacheDeviceDescriptor& self){ return self.isolationKey; },[](wgpu::DawnCacheDeviceDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.isolationKey = c; }
        );
    PYCLASS_END(_wgpu, wgpu::DawnCacheDeviceDescriptor, DawnCacheDeviceDescriptor)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::DawnComputePipelineFullSubgroups, struct wgpu::ChainedStruct, DawnComputePipelineFullSubgroups)
        DawnComputePipelineFullSubgroups.def(py::init<>());
        DawnComputePipelineFullSubgroups.def_readwrite("requires_full_subgroups", &wgpu::DawnComputePipelineFullSubgroups::requiresFullSubgroups);
    PYCLASS_END(_wgpu, wgpu::DawnComputePipelineFullSubgroups, DawnComputePipelineFullSubgroups)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::DawnEncoderInternalUsageDescriptor, struct wgpu::ChainedStruct, DawnEncoderInternalUsageDescriptor)
        DawnEncoderInternalUsageDescriptor.def(py::init<>());
        DawnEncoderInternalUsageDescriptor.def_readwrite("use_internal_usages", &wgpu::DawnEncoderInternalUsageDescriptor::useInternalUsages);
    PYCLASS_END(_wgpu, wgpu::DawnEncoderInternalUsageDescriptor, DawnEncoderInternalUsageDescriptor)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::DawnExperimentalSubgroupLimits, struct wgpu::ChainedStructOut, DawnExperimentalSubgroupLimits)
        DawnExperimentalSubgroupLimits.def(py::init<>());
        DawnExperimentalSubgroupLimits.def_readwrite("min_subgroup_size", &wgpu::DawnExperimentalSubgroupLimits::minSubgroupSize);
        DawnExperimentalSubgroupLimits.def_readwrite("max_subgroup_size", &wgpu::DawnExperimentalSubgroupLimits::maxSubgroupSize);
    PYCLASS_END(_wgpu, wgpu::DawnExperimentalSubgroupLimits, DawnExperimentalSubgroupLimits)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::DawnMultisampleStateRenderToSingleSampled, struct wgpu::ChainedStruct, DawnMultisampleStateRenderToSingleSampled)
        DawnMultisampleStateRenderToSingleSampled.def(py::init<>());
        DawnMultisampleStateRenderToSingleSampled.def_readwrite("enabled", &wgpu::DawnMultisampleStateRenderToSingleSampled::enabled);
    PYCLASS_END(_wgpu, wgpu::DawnMultisampleStateRenderToSingleSampled, DawnMultisampleStateRenderToSingleSampled)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::DawnRenderPassColorAttachmentRenderToSingleSampled, struct wgpu::ChainedStruct, DawnRenderPassColorAttachmentRenderToSingleSampled)
        DawnRenderPassColorAttachmentRenderToSingleSampled.def(py::init<>());
        DawnRenderPassColorAttachmentRenderToSingleSampled.def_readwrite("implicit_sample_count", &wgpu::DawnRenderPassColorAttachmentRenderToSingleSampled::implicitSampleCount);
    PYCLASS_END(_wgpu, wgpu::DawnRenderPassColorAttachmentRenderToSingleSampled, DawnRenderPassColorAttachmentRenderToSingleSampled)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::DawnShaderModuleSPIRVOptionsDescriptor, struct wgpu::ChainedStruct, DawnShaderModuleSPIRVOptionsDescriptor)
        DawnShaderModuleSPIRVOptionsDescriptor.def(py::init<>());
        DawnShaderModuleSPIRVOptionsDescriptor.def_readwrite("allow_non_uniform_derivatives", &wgpu::DawnShaderModuleSPIRVOptionsDescriptor::allowNonUniformDerivatives);
    PYCLASS_END(_wgpu, wgpu::DawnShaderModuleSPIRVOptionsDescriptor, DawnShaderModuleSPIRVOptionsDescriptor)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::DawnTextureInternalUsageDescriptor, struct wgpu::ChainedStruct, DawnTextureInternalUsageDescriptor)
        DawnTextureInternalUsageDescriptor.def(py::init<>());
        DawnTextureInternalUsageDescriptor.def_readwrite("internal_usage", &wgpu::DawnTextureInternalUsageDescriptor::internalUsage);
    PYCLASS_END(_wgpu, wgpu::DawnTextureInternalUsageDescriptor, DawnTextureInternalUsageDescriptor)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::DawnTogglesDescriptor, struct wgpu::ChainedStruct, DawnTogglesDescriptor)
        DawnTogglesDescriptor.def(py::init<>());
        DawnTogglesDescriptor.def_readwrite("enabled_toggle_count", &wgpu::DawnTogglesDescriptor::enabledToggleCount);
        DawnTogglesDescriptor.def_readwrite("disabled_toggle_count", &wgpu::DawnTogglesDescriptor::disabledToggleCount);
    PYCLASS_END(_wgpu, wgpu::DawnTogglesDescriptor, DawnTogglesDescriptor)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::DawnWireWGSLControl, struct wgpu::ChainedStruct, DawnWireWGSLControl)
        DawnWireWGSLControl.def(py::init<>());
        DawnWireWGSLControl.def_readwrite("enable_experimental", &wgpu::DawnWireWGSLControl::enableExperimental);
        DawnWireWGSLControl.def_readwrite("enable_unsafe", &wgpu::DawnWireWGSLControl::enableUnsafe);
        DawnWireWGSLControl.def_readwrite("enable_testing", &wgpu::DawnWireWGSLControl::enableTesting);
    PYCLASS_END(_wgpu, wgpu::DawnWireWGSLControl, DawnWireWGSLControl)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::DepthStencilStateDepthWriteDefinedDawn, struct wgpu::ChainedStruct, DepthStencilStateDepthWriteDefinedDawn)
        DepthStencilStateDepthWriteDefinedDawn.def(py::init<>());
        DepthStencilStateDepthWriteDefinedDawn.def_readwrite("depth_write_defined", &wgpu::DepthStencilStateDepthWriteDefinedDawn::depthWriteDefined);
    PYCLASS_END(_wgpu, wgpu::DepthStencilStateDepthWriteDefinedDawn, DepthStencilStateDepthWriteDefinedDawn)

    PYCLASS_BEGIN(_wgpu, wgpu::Extent2D, Extent2D)
        Extent2D.def_readwrite("width", &wgpu::Extent2D::width);
        Extent2D.def_readwrite("height", &wgpu::Extent2D::height);
    PYCLASS_END(_wgpu, wgpu::Extent2D, Extent2D)

    PYCLASS_BEGIN(_wgpu, wgpu::Extent3D, Extent3D)
        Extent3D.def_readwrite("width", &wgpu::Extent3D::width);
        Extent3D.def_readwrite("height", &wgpu::Extent3D::height);
        Extent3D.def_readwrite("depth_or_array_layers", &wgpu::Extent3D::depthOrArrayLayers);
        Extent3D.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::Extent3D, Extent3D)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::ExternalTextureBindingEntry, struct wgpu::ChainedStruct, ExternalTextureBindingEntry)
        ExternalTextureBindingEntry.def(py::init<>());
        ExternalTextureBindingEntry.def_readwrite("external_texture", &wgpu::ExternalTextureBindingEntry::externalTexture);
    PYCLASS_END(_wgpu, wgpu::ExternalTextureBindingEntry, ExternalTextureBindingEntry)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::ExternalTextureBindingLayout, struct wgpu::ChainedStruct, ExternalTextureBindingLayout)
        ExternalTextureBindingLayout.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::ExternalTextureBindingLayout, ExternalTextureBindingLayout)

    PYCLASS_BEGIN(_wgpu, wgpu::Future, Future)
        Future.def_readwrite("id", &wgpu::Future::id);
    PYCLASS_END(_wgpu, wgpu::Future, Future)

    PYCLASS_BEGIN(_wgpu, wgpu::InstanceFeatures, InstanceFeatures)
        InstanceFeatures.def_readwrite("next_in_chain", &wgpu::InstanceFeatures::nextInChain);
        InstanceFeatures.def_readwrite("timed_wait_any_enable", &wgpu::InstanceFeatures::timedWaitAnyEnable);
        InstanceFeatures.def_readwrite("timed_wait_any_max_count", &wgpu::InstanceFeatures::timedWaitAnyMaxCount);
    PYCLASS_END(_wgpu, wgpu::InstanceFeatures, InstanceFeatures)

    PYCLASS_BEGIN(_wgpu, wgpu::Limits, Limits)
        Limits.def_readwrite("max_texture_dimension1d", &wgpu::Limits::maxTextureDimension1D);
        Limits.def_readwrite("max_texture_dimension2d", &wgpu::Limits::maxTextureDimension2D);
        Limits.def_readwrite("max_texture_dimension3d", &wgpu::Limits::maxTextureDimension3D);
        Limits.def_readwrite("max_texture_array_layers", &wgpu::Limits::maxTextureArrayLayers);
        Limits.def_readwrite("max_bind_groups", &wgpu::Limits::maxBindGroups);
        Limits.def_readwrite("max_bind_groups_plus_vertex_buffers", &wgpu::Limits::maxBindGroupsPlusVertexBuffers);
        Limits.def_readwrite("max_bindings_per_bind_group", &wgpu::Limits::maxBindingsPerBindGroup);
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
        Limits.def_readwrite("max_buffer_size", &wgpu::Limits::maxBufferSize);
        Limits.def_readwrite("max_vertex_attributes", &wgpu::Limits::maxVertexAttributes);
        Limits.def_readwrite("max_vertex_buffer_array_stride", &wgpu::Limits::maxVertexBufferArrayStride);
        Limits.def_readwrite("max_inter_stage_shader_components", &wgpu::Limits::maxInterStageShaderComponents);
        Limits.def_readwrite("max_inter_stage_shader_variables", &wgpu::Limits::maxInterStageShaderVariables);
        Limits.def_readwrite("max_color_attachments", &wgpu::Limits::maxColorAttachments);
        Limits.def_readwrite("max_color_attachment_bytes_per_sample", &wgpu::Limits::maxColorAttachmentBytesPerSample);
        Limits.def_readwrite("max_compute_workgroup_storage_size", &wgpu::Limits::maxComputeWorkgroupStorageSize);
        Limits.def_readwrite("max_compute_invocations_per_workgroup", &wgpu::Limits::maxComputeInvocationsPerWorkgroup);
        Limits.def_readwrite("max_compute_workgroup_size_x", &wgpu::Limits::maxComputeWorkgroupSizeX);
        Limits.def_readwrite("max_compute_workgroup_size_y", &wgpu::Limits::maxComputeWorkgroupSizeY);
        Limits.def_readwrite("max_compute_workgroup_size_z", &wgpu::Limits::maxComputeWorkgroupSizeZ);
        Limits.def_readwrite("max_compute_workgroups_per_dimension", &wgpu::Limits::maxComputeWorkgroupsPerDimension);
    PYCLASS_END(_wgpu, wgpu::Limits, Limits)

    PYCLASS_BEGIN(_wgpu, wgpu::MemoryHeapInfo, MemoryHeapInfo)
        MemoryHeapInfo.def_readwrite("properties", &wgpu::MemoryHeapInfo::properties);
        MemoryHeapInfo.def_readwrite("size", &wgpu::MemoryHeapInfo::size);
    PYCLASS_END(_wgpu, wgpu::MemoryHeapInfo, MemoryHeapInfo)

    PYCLASS_BEGIN(_wgpu, wgpu::MultisampleState, MultisampleState)
        MultisampleState.def_readwrite("next_in_chain", &wgpu::MultisampleState::nextInChain);
        MultisampleState.def_readwrite("count", &wgpu::MultisampleState::count);
        MultisampleState.def_readwrite("mask", &wgpu::MultisampleState::mask);
        MultisampleState.def_readwrite("alpha_to_coverage_enabled", &wgpu::MultisampleState::alphaToCoverageEnabled);
    PYCLASS_END(_wgpu, wgpu::MultisampleState, MultisampleState)

    PYCLASS_BEGIN(_wgpu, wgpu::Origin2D, Origin2D)
        Origin2D.def_readwrite("x", &wgpu::Origin2D::x);
        Origin2D.def_readwrite("y", &wgpu::Origin2D::y);
    PYCLASS_END(_wgpu, wgpu::Origin2D, Origin2D)

    PYCLASS_BEGIN(_wgpu, wgpu::Origin3D, Origin3D)
        Origin3D.def_readwrite("x", &wgpu::Origin3D::x);
        Origin3D.def_readwrite("y", &wgpu::Origin3D::y);
        Origin3D.def_readwrite("z", &wgpu::Origin3D::z);
    PYCLASS_END(_wgpu, wgpu::Origin3D, Origin3D)

    PYCLASS_BEGIN(_wgpu, wgpu::PipelineLayoutDescriptor, PipelineLayoutDescriptor)
        PipelineLayoutDescriptor.def_readwrite("next_in_chain", &wgpu::PipelineLayoutDescriptor::nextInChain);
        PipelineLayoutDescriptor.def_property("label",
            [](const wgpu::PipelineLayoutDescriptor& self){ return self.label; },[](wgpu::PipelineLayoutDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        PipelineLayoutDescriptor.def_readwrite("bind_group_layout_count", &wgpu::PipelineLayoutDescriptor::bindGroupLayoutCount);
        PipelineLayoutDescriptor.def_readwrite("bind_group_layouts", &wgpu::PipelineLayoutDescriptor::bindGroupLayouts);
        PipelineLayoutDescriptor.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::PipelineLayoutDescriptor obj;
            if (kwargs.contains("next_in_chain"))
            {
                auto value = kwargs["next_in_chain"].cast<const wgpu::ChainedStruct *>();
                obj.nextInChain = value;
            }
            if (kwargs.contains("label"))
            {
                auto _value = kwargs["label"].cast<std::string>();
                char* value = (char*)malloc(_value.size());
                strcpy(value, _value.c_str());
                obj.label = value;
            }
            if (kwargs.contains("bind_group_layout_count"))
            {
                auto value = kwargs["bind_group_layout_count"].cast<size_t>();
                obj.bindGroupLayoutCount = value;
            }
            if (kwargs.contains("bind_group_layouts"))
            {
                auto value = kwargs["bind_group_layouts"].cast<const wgpu::BindGroupLayout *>();
                obj.bindGroupLayouts = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
    PYCLASS_END(_wgpu, wgpu::PipelineLayoutDescriptor, PipelineLayoutDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::PipelineLayoutStorageAttachment, PipelineLayoutStorageAttachment)
        PipelineLayoutStorageAttachment.def_readwrite("next_in_chain", &wgpu::PipelineLayoutStorageAttachment::nextInChain);
        PipelineLayoutStorageAttachment.def_readwrite("offset", &wgpu::PipelineLayoutStorageAttachment::offset);
        PipelineLayoutStorageAttachment.def_readwrite("format", &wgpu::PipelineLayoutStorageAttachment::format);
    PYCLASS_END(_wgpu, wgpu::PipelineLayoutStorageAttachment, PipelineLayoutStorageAttachment)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::PrimitiveDepthClipControl, struct wgpu::ChainedStruct, PrimitiveDepthClipControl)
        PrimitiveDepthClipControl.def(py::init<>());
        PrimitiveDepthClipControl.def_readwrite("unclipped_depth", &wgpu::PrimitiveDepthClipControl::unclippedDepth);
    PYCLASS_END(_wgpu, wgpu::PrimitiveDepthClipControl, PrimitiveDepthClipControl)

    PYCLASS_BEGIN(_wgpu, wgpu::PrimitiveState, PrimitiveState)
        PrimitiveState.def_readwrite("next_in_chain", &wgpu::PrimitiveState::nextInChain);
        PrimitiveState.def_readwrite("topology", &wgpu::PrimitiveState::topology);
        PrimitiveState.def_readwrite("strip_index_format", &wgpu::PrimitiveState::stripIndexFormat);
        PrimitiveState.def_readwrite("front_face", &wgpu::PrimitiveState::frontFace);
        PrimitiveState.def_readwrite("cull_mode", &wgpu::PrimitiveState::cullMode);
        PrimitiveState.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::PrimitiveState obj;
            if (kwargs.contains("next_in_chain"))
            {
                auto value = kwargs["next_in_chain"].cast<const wgpu::ChainedStruct *>();
                obj.nextInChain = value;
            }
            if (kwargs.contains("topology"))
            {
                auto value = kwargs["topology"].cast<wgpu::PrimitiveTopology>();
                obj.topology = value;
            }
            if (kwargs.contains("strip_index_format"))
            {
                auto value = kwargs["strip_index_format"].cast<wgpu::IndexFormat>();
                obj.stripIndexFormat = value;
            }
            if (kwargs.contains("front_face"))
            {
                auto value = kwargs["front_face"].cast<wgpu::FrontFace>();
                obj.frontFace = value;
            }
            if (kwargs.contains("cull_mode"))
            {
                auto value = kwargs["cull_mode"].cast<wgpu::CullMode>();
                obj.cullMode = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
    PYCLASS_END(_wgpu, wgpu::PrimitiveState, PrimitiveState)

    PYCLASS_BEGIN(_wgpu, wgpu::QuerySetDescriptor, QuerySetDescriptor)
        QuerySetDescriptor.def_readwrite("next_in_chain", &wgpu::QuerySetDescriptor::nextInChain);
        QuerySetDescriptor.def_property("label",
            [](const wgpu::QuerySetDescriptor& self){ return self.label; },[](wgpu::QuerySetDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        QuerySetDescriptor.def_readwrite("type", &wgpu::QuerySetDescriptor::type);
        QuerySetDescriptor.def_readwrite("count", &wgpu::QuerySetDescriptor::count);
    PYCLASS_END(_wgpu, wgpu::QuerySetDescriptor, QuerySetDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::QueueDescriptor, QueueDescriptor)
        QueueDescriptor.def_readwrite("next_in_chain", &wgpu::QueueDescriptor::nextInChain);
        QueueDescriptor.def_property("label",
            [](const wgpu::QueueDescriptor& self){ return self.label; },[](wgpu::QueueDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
    PYCLASS_END(_wgpu, wgpu::QueueDescriptor, QueueDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::QueueWorkDoneCallbackInfo, QueueWorkDoneCallbackInfo)
        QueueWorkDoneCallbackInfo.def_readwrite("next_in_chain", &wgpu::QueueWorkDoneCallbackInfo::nextInChain);
        QueueWorkDoneCallbackInfo.def_readwrite("mode", &wgpu::QueueWorkDoneCallbackInfo::mode);
        QueueWorkDoneCallbackInfo.def_readwrite("userdata", &wgpu::QueueWorkDoneCallbackInfo::userdata);
    PYCLASS_END(_wgpu, wgpu::QueueWorkDoneCallbackInfo, QueueWorkDoneCallbackInfo)

    PYCLASS_BEGIN(_wgpu, wgpu::RenderBundleDescriptor, RenderBundleDescriptor)
        RenderBundleDescriptor.def_readwrite("next_in_chain", &wgpu::RenderBundleDescriptor::nextInChain);
        RenderBundleDescriptor.def_property("label",
            [](const wgpu::RenderBundleDescriptor& self){ return self.label; },[](wgpu::RenderBundleDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
    PYCLASS_END(_wgpu, wgpu::RenderBundleDescriptor, RenderBundleDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::RenderBundleEncoderDescriptor, RenderBundleEncoderDescriptor)
        RenderBundleEncoderDescriptor.def_readwrite("next_in_chain", &wgpu::RenderBundleEncoderDescriptor::nextInChain);
        RenderBundleEncoderDescriptor.def_property("label",
            [](const wgpu::RenderBundleEncoderDescriptor& self){ return self.label; },[](wgpu::RenderBundleEncoderDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        RenderBundleEncoderDescriptor.def_readwrite("color_format_count", &wgpu::RenderBundleEncoderDescriptor::colorFormatCount);
        RenderBundleEncoderDescriptor.def_readwrite("color_formats", &wgpu::RenderBundleEncoderDescriptor::colorFormats);
        RenderBundleEncoderDescriptor.def_readwrite("depth_stencil_format", &wgpu::RenderBundleEncoderDescriptor::depthStencilFormat);
        RenderBundleEncoderDescriptor.def_readwrite("sample_count", &wgpu::RenderBundleEncoderDescriptor::sampleCount);
        RenderBundleEncoderDescriptor.def_readwrite("depth_read_only", &wgpu::RenderBundleEncoderDescriptor::depthReadOnly);
        RenderBundleEncoderDescriptor.def_readwrite("stencil_read_only", &wgpu::RenderBundleEncoderDescriptor::stencilReadOnly);
    PYCLASS_END(_wgpu, wgpu::RenderBundleEncoderDescriptor, RenderBundleEncoderDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::RenderPassDepthStencilAttachment, RenderPassDepthStencilAttachment)
        RenderPassDepthStencilAttachment.def_readwrite("view", &wgpu::RenderPassDepthStencilAttachment::view);
        RenderPassDepthStencilAttachment.def_readwrite("depth_load_op", &wgpu::RenderPassDepthStencilAttachment::depthLoadOp);
        RenderPassDepthStencilAttachment.def_readwrite("depth_store_op", &wgpu::RenderPassDepthStencilAttachment::depthStoreOp);
        RenderPassDepthStencilAttachment.def_readwrite("depth_clear_value", &wgpu::RenderPassDepthStencilAttachment::depthClearValue);
        RenderPassDepthStencilAttachment.def_readwrite("depth_read_only", &wgpu::RenderPassDepthStencilAttachment::depthReadOnly);
        RenderPassDepthStencilAttachment.def_readwrite("stencil_load_op", &wgpu::RenderPassDepthStencilAttachment::stencilLoadOp);
        RenderPassDepthStencilAttachment.def_readwrite("stencil_store_op", &wgpu::RenderPassDepthStencilAttachment::stencilStoreOp);
        RenderPassDepthStencilAttachment.def_readwrite("stencil_clear_value", &wgpu::RenderPassDepthStencilAttachment::stencilClearValue);
        RenderPassDepthStencilAttachment.def_readwrite("stencil_read_only", &wgpu::RenderPassDepthStencilAttachment::stencilReadOnly);
        RenderPassDepthStencilAttachment.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::RenderPassDepthStencilAttachment obj;
            if (kwargs.contains("view"))
            {
                auto value = kwargs["view"].cast<wgpu::TextureView>();
                obj.view = value;
            }
            if (kwargs.contains("depth_load_op"))
            {
                auto value = kwargs["depth_load_op"].cast<wgpu::LoadOp>();
                obj.depthLoadOp = value;
            }
            if (kwargs.contains("depth_store_op"))
            {
                auto value = kwargs["depth_store_op"].cast<wgpu::StoreOp>();
                obj.depthStoreOp = value;
            }
            if (kwargs.contains("depth_clear_value"))
            {
                auto value = kwargs["depth_clear_value"].cast<float>();
                obj.depthClearValue = value;
            }
            if (kwargs.contains("depth_read_only"))
            {
                auto value = kwargs["depth_read_only"].cast<wgpu::Bool>();
                obj.depthReadOnly = value;
            }
            if (kwargs.contains("stencil_load_op"))
            {
                auto value = kwargs["stencil_load_op"].cast<wgpu::LoadOp>();
                obj.stencilLoadOp = value;
            }
            if (kwargs.contains("stencil_store_op"))
            {
                auto value = kwargs["stencil_store_op"].cast<wgpu::StoreOp>();
                obj.stencilStoreOp = value;
            }
            if (kwargs.contains("stencil_clear_value"))
            {
                auto value = kwargs["stencil_clear_value"].cast<uint32_t>();
                obj.stencilClearValue = value;
            }
            if (kwargs.contains("stencil_read_only"))
            {
                auto value = kwargs["stencil_read_only"].cast<wgpu::Bool>();
                obj.stencilReadOnly = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
    PYCLASS_END(_wgpu, wgpu::RenderPassDepthStencilAttachment, RenderPassDepthStencilAttachment)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::RenderPassDescriptorMaxDrawCount, struct wgpu::ChainedStruct, RenderPassDescriptorMaxDrawCount)
        RenderPassDescriptorMaxDrawCount.def(py::init<>());
        RenderPassDescriptorMaxDrawCount.def_readwrite("max_draw_count", &wgpu::RenderPassDescriptorMaxDrawCount::maxDrawCount);
    PYCLASS_END(_wgpu, wgpu::RenderPassDescriptorMaxDrawCount, RenderPassDescriptorMaxDrawCount)

    PYCLASS_BEGIN(_wgpu, wgpu::RenderPassTimestampWrites, RenderPassTimestampWrites)
        RenderPassTimestampWrites.def_readwrite("query_set", &wgpu::RenderPassTimestampWrites::querySet);
        RenderPassTimestampWrites.def_readwrite("beginning_of_pass_write_index", &wgpu::RenderPassTimestampWrites::beginningOfPassWriteIndex);
        RenderPassTimestampWrites.def_readwrite("end_of_pass_write_index", &wgpu::RenderPassTimestampWrites::endOfPassWriteIndex);
    PYCLASS_END(_wgpu, wgpu::RenderPassTimestampWrites, RenderPassTimestampWrites)

    PYCLASS_BEGIN(_wgpu, wgpu::RequestAdapterCallbackInfo, RequestAdapterCallbackInfo)
        RequestAdapterCallbackInfo.def_readwrite("next_in_chain", &wgpu::RequestAdapterCallbackInfo::nextInChain);
        RequestAdapterCallbackInfo.def_readwrite("mode", &wgpu::RequestAdapterCallbackInfo::mode);
        RequestAdapterCallbackInfo.def_readwrite("userdata", &wgpu::RequestAdapterCallbackInfo::userdata);
    PYCLASS_END(_wgpu, wgpu::RequestAdapterCallbackInfo, RequestAdapterCallbackInfo)

    PYCLASS_BEGIN(_wgpu, wgpu::RequestAdapterOptions, RequestAdapterOptions)
        RequestAdapterOptions.def_readwrite("next_in_chain", &wgpu::RequestAdapterOptions::nextInChain);
        RequestAdapterOptions.def_readwrite("compatible_surface", &wgpu::RequestAdapterOptions::compatibleSurface);
        RequestAdapterOptions.def_readwrite("power_preference", &wgpu::RequestAdapterOptions::powerPreference);
        RequestAdapterOptions.def_readwrite("backend_type", &wgpu::RequestAdapterOptions::backendType);
        RequestAdapterOptions.def_readwrite("force_fallback_adapter", &wgpu::RequestAdapterOptions::forceFallbackAdapter);
        RequestAdapterOptions.def_readwrite("compatibility_mode", &wgpu::RequestAdapterOptions::compatibilityMode);
    PYCLASS_END(_wgpu, wgpu::RequestAdapterOptions, RequestAdapterOptions)

    PYCLASS_BEGIN(_wgpu, wgpu::SamplerBindingLayout, SamplerBindingLayout)
        SamplerBindingLayout.def_readwrite("next_in_chain", &wgpu::SamplerBindingLayout::nextInChain);
        SamplerBindingLayout.def_readwrite("type", &wgpu::SamplerBindingLayout::type);
        SamplerBindingLayout.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::SamplerBindingLayout obj;
            if (kwargs.contains("next_in_chain"))
            {
                auto value = kwargs["next_in_chain"].cast<const wgpu::ChainedStruct *>();
                obj.nextInChain = value;
            }
            if (kwargs.contains("type"))
            {
                auto value = kwargs["type"].cast<wgpu::SamplerBindingType>();
                obj.type = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
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
        SamplerDescriptor.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::SamplerDescriptor obj;
            if (kwargs.contains("next_in_chain"))
            {
                auto value = kwargs["next_in_chain"].cast<const wgpu::ChainedStruct *>();
                obj.nextInChain = value;
            }
            if (kwargs.contains("label"))
            {
                auto _value = kwargs["label"].cast<std::string>();
                char* value = (char*)malloc(_value.size());
                strcpy(value, _value.c_str());
                obj.label = value;
            }
            if (kwargs.contains("address_mode_u"))
            {
                auto value = kwargs["address_mode_u"].cast<wgpu::AddressMode>();
                obj.addressModeU = value;
            }
            if (kwargs.contains("address_mode_v"))
            {
                auto value = kwargs["address_mode_v"].cast<wgpu::AddressMode>();
                obj.addressModeV = value;
            }
            if (kwargs.contains("address_mode_w"))
            {
                auto value = kwargs["address_mode_w"].cast<wgpu::AddressMode>();
                obj.addressModeW = value;
            }
            if (kwargs.contains("mag_filter"))
            {
                auto value = kwargs["mag_filter"].cast<wgpu::FilterMode>();
                obj.magFilter = value;
            }
            if (kwargs.contains("min_filter"))
            {
                auto value = kwargs["min_filter"].cast<wgpu::FilterMode>();
                obj.minFilter = value;
            }
            if (kwargs.contains("mipmap_filter"))
            {
                auto value = kwargs["mipmap_filter"].cast<wgpu::MipmapFilterMode>();
                obj.mipmapFilter = value;
            }
            if (kwargs.contains("lod_min_clamp"))
            {
                auto value = kwargs["lod_min_clamp"].cast<float>();
                obj.lodMinClamp = value;
            }
            if (kwargs.contains("lod_max_clamp"))
            {
                auto value = kwargs["lod_max_clamp"].cast<float>();
                obj.lodMaxClamp = value;
            }
            if (kwargs.contains("compare"))
            {
                auto value = kwargs["compare"].cast<wgpu::CompareFunction>();
                obj.compare = value;
            }
            if (kwargs.contains("max_anisotropy"))
            {
                auto value = kwargs["max_anisotropy"].cast<uint16_t>();
                obj.maxAnisotropy = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
    PYCLASS_END(_wgpu, wgpu::SamplerDescriptor, SamplerDescriptor)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::ShaderModuleSPIRVDescriptor, struct wgpu::ChainedStruct, ShaderModuleSPIRVDescriptor)
        ShaderModuleSPIRVDescriptor.def(py::init<>());
        ShaderModuleSPIRVDescriptor.def_readwrite("code_size", &wgpu::ShaderModuleSPIRVDescriptor::codeSize);
        ShaderModuleSPIRVDescriptor.def_readwrite("code", &wgpu::ShaderModuleSPIRVDescriptor::code);
    PYCLASS_END(_wgpu, wgpu::ShaderModuleSPIRVDescriptor, ShaderModuleSPIRVDescriptor)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::ShaderModuleWGSLDescriptor, struct wgpu::ChainedStruct, ShaderModuleWGSLDescriptor)
        ShaderModuleWGSLDescriptor.def(py::init<>());
        ShaderModuleWGSLDescriptor.def_property("code",
            [](const wgpu::ShaderModuleWGSLDescriptor& self){ return self.code; },[](wgpu::ShaderModuleWGSLDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.code = c; }
        );
        ShaderModuleWGSLDescriptor.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::ShaderModuleWGSLDescriptor obj;
            if (kwargs.contains("code"))
            {
                auto _value = kwargs["code"].cast<std::string>();
                char* value = (char*)malloc(_value.size());
                strcpy(value, _value.c_str());
                obj.code = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
    PYCLASS_END(_wgpu, wgpu::ShaderModuleWGSLDescriptor, ShaderModuleWGSLDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::ShaderModuleDescriptor, ShaderModuleDescriptor)
        ShaderModuleDescriptor.def_readwrite("next_in_chain", &wgpu::ShaderModuleDescriptor::nextInChain);
        ShaderModuleDescriptor.def_property("label",
            [](const wgpu::ShaderModuleDescriptor& self){ return self.label; },[](wgpu::ShaderModuleDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        ShaderModuleDescriptor.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::ShaderModuleDescriptor obj;
            if (kwargs.contains("next_in_chain"))
            {
                auto value = kwargs["next_in_chain"].cast<const wgpu::ChainedStruct *>();
                obj.nextInChain = value;
            }
            if (kwargs.contains("label"))
            {
                auto _value = kwargs["label"].cast<std::string>();
                char* value = (char*)malloc(_value.size());
                strcpy(value, _value.c_str());
                obj.label = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
    PYCLASS_END(_wgpu, wgpu::ShaderModuleDescriptor, ShaderModuleDescriptor)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SharedFenceDXGISharedHandleDescriptor, struct wgpu::ChainedStruct, SharedFenceDXGISharedHandleDescriptor)
        SharedFenceDXGISharedHandleDescriptor.def(py::init<>());
        SharedFenceDXGISharedHandleDescriptor.def_readwrite("handle", &wgpu::SharedFenceDXGISharedHandleDescriptor::handle);
    PYCLASS_END(_wgpu, wgpu::SharedFenceDXGISharedHandleDescriptor, SharedFenceDXGISharedHandleDescriptor)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SharedFenceDXGISharedHandleExportInfo, struct wgpu::ChainedStructOut, SharedFenceDXGISharedHandleExportInfo)
        SharedFenceDXGISharedHandleExportInfo.def(py::init<>());
        SharedFenceDXGISharedHandleExportInfo.def_readwrite("handle", &wgpu::SharedFenceDXGISharedHandleExportInfo::handle);
    PYCLASS_END(_wgpu, wgpu::SharedFenceDXGISharedHandleExportInfo, SharedFenceDXGISharedHandleExportInfo)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SharedFenceMTLSharedEventDescriptor, struct wgpu::ChainedStruct, SharedFenceMTLSharedEventDescriptor)
        SharedFenceMTLSharedEventDescriptor.def(py::init<>());
        SharedFenceMTLSharedEventDescriptor.def_readwrite("shared_event", &wgpu::SharedFenceMTLSharedEventDescriptor::sharedEvent);
    PYCLASS_END(_wgpu, wgpu::SharedFenceMTLSharedEventDescriptor, SharedFenceMTLSharedEventDescriptor)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SharedFenceMTLSharedEventExportInfo, struct wgpu::ChainedStructOut, SharedFenceMTLSharedEventExportInfo)
        SharedFenceMTLSharedEventExportInfo.def(py::init<>());
        SharedFenceMTLSharedEventExportInfo.def_readwrite("shared_event", &wgpu::SharedFenceMTLSharedEventExportInfo::sharedEvent);
    PYCLASS_END(_wgpu, wgpu::SharedFenceMTLSharedEventExportInfo, SharedFenceMTLSharedEventExportInfo)

    PYCLASS_BEGIN(_wgpu, wgpu::SharedFenceDescriptor, SharedFenceDescriptor)
        SharedFenceDescriptor.def_readwrite("next_in_chain", &wgpu::SharedFenceDescriptor::nextInChain);
        SharedFenceDescriptor.def_property("label",
            [](const wgpu::SharedFenceDescriptor& self){ return self.label; },[](wgpu::SharedFenceDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
    PYCLASS_END(_wgpu, wgpu::SharedFenceDescriptor, SharedFenceDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::SharedFenceExportInfo, SharedFenceExportInfo)
        SharedFenceExportInfo.def_readwrite("next_in_chain", &wgpu::SharedFenceExportInfo::nextInChain);
        SharedFenceExportInfo.def_readwrite("type", &wgpu::SharedFenceExportInfo::type);
    PYCLASS_END(_wgpu, wgpu::SharedFenceExportInfo, SharedFenceExportInfo)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SharedFenceVkSemaphoreOpaqueFDDescriptor, struct wgpu::ChainedStruct, SharedFenceVkSemaphoreOpaqueFDDescriptor)
        SharedFenceVkSemaphoreOpaqueFDDescriptor.def(py::init<>());
        SharedFenceVkSemaphoreOpaqueFDDescriptor.def_readwrite("handle", &wgpu::SharedFenceVkSemaphoreOpaqueFDDescriptor::handle);
    PYCLASS_END(_wgpu, wgpu::SharedFenceVkSemaphoreOpaqueFDDescriptor, SharedFenceVkSemaphoreOpaqueFDDescriptor)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SharedFenceVkSemaphoreOpaqueFDExportInfo, struct wgpu::ChainedStructOut, SharedFenceVkSemaphoreOpaqueFDExportInfo)
        SharedFenceVkSemaphoreOpaqueFDExportInfo.def(py::init<>());
        SharedFenceVkSemaphoreOpaqueFDExportInfo.def_readwrite("handle", &wgpu::SharedFenceVkSemaphoreOpaqueFDExportInfo::handle);
    PYCLASS_END(_wgpu, wgpu::SharedFenceVkSemaphoreOpaqueFDExportInfo, SharedFenceVkSemaphoreOpaqueFDExportInfo)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SharedFenceVkSemaphoreSyncFDDescriptor, struct wgpu::ChainedStruct, SharedFenceVkSemaphoreSyncFDDescriptor)
        SharedFenceVkSemaphoreSyncFDDescriptor.def(py::init<>());
        SharedFenceVkSemaphoreSyncFDDescriptor.def_readwrite("handle", &wgpu::SharedFenceVkSemaphoreSyncFDDescriptor::handle);
    PYCLASS_END(_wgpu, wgpu::SharedFenceVkSemaphoreSyncFDDescriptor, SharedFenceVkSemaphoreSyncFDDescriptor)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SharedFenceVkSemaphoreSyncFDExportInfo, struct wgpu::ChainedStructOut, SharedFenceVkSemaphoreSyncFDExportInfo)
        SharedFenceVkSemaphoreSyncFDExportInfo.def(py::init<>());
        SharedFenceVkSemaphoreSyncFDExportInfo.def_readwrite("handle", &wgpu::SharedFenceVkSemaphoreSyncFDExportInfo::handle);
    PYCLASS_END(_wgpu, wgpu::SharedFenceVkSemaphoreSyncFDExportInfo, SharedFenceVkSemaphoreSyncFDExportInfo)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SharedFenceVkSemaphoreZirconHandleDescriptor, struct wgpu::ChainedStruct, SharedFenceVkSemaphoreZirconHandleDescriptor)
        SharedFenceVkSemaphoreZirconHandleDescriptor.def(py::init<>());
        SharedFenceVkSemaphoreZirconHandleDescriptor.def_readwrite("handle", &wgpu::SharedFenceVkSemaphoreZirconHandleDescriptor::handle);
    PYCLASS_END(_wgpu, wgpu::SharedFenceVkSemaphoreZirconHandleDescriptor, SharedFenceVkSemaphoreZirconHandleDescriptor)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SharedFenceVkSemaphoreZirconHandleExportInfo, struct wgpu::ChainedStructOut, SharedFenceVkSemaphoreZirconHandleExportInfo)
        SharedFenceVkSemaphoreZirconHandleExportInfo.def(py::init<>());
        SharedFenceVkSemaphoreZirconHandleExportInfo.def_readwrite("handle", &wgpu::SharedFenceVkSemaphoreZirconHandleExportInfo::handle);
    PYCLASS_END(_wgpu, wgpu::SharedFenceVkSemaphoreZirconHandleExportInfo, SharedFenceVkSemaphoreZirconHandleExportInfo)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SharedTextureMemoryDXGISharedHandleDescriptor, struct wgpu::ChainedStruct, SharedTextureMemoryDXGISharedHandleDescriptor)
        SharedTextureMemoryDXGISharedHandleDescriptor.def(py::init<>());
        SharedTextureMemoryDXGISharedHandleDescriptor.def_readwrite("handle", &wgpu::SharedTextureMemoryDXGISharedHandleDescriptor::handle);
    PYCLASS_END(_wgpu, wgpu::SharedTextureMemoryDXGISharedHandleDescriptor, SharedTextureMemoryDXGISharedHandleDescriptor)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SharedTextureMemoryEGLImageDescriptor, struct wgpu::ChainedStruct, SharedTextureMemoryEGLImageDescriptor)
        SharedTextureMemoryEGLImageDescriptor.def(py::init<>());
        SharedTextureMemoryEGLImageDescriptor.def_readwrite("image", &wgpu::SharedTextureMemoryEGLImageDescriptor::image);
    PYCLASS_END(_wgpu, wgpu::SharedTextureMemoryEGLImageDescriptor, SharedTextureMemoryEGLImageDescriptor)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SharedTextureMemoryIOSurfaceDescriptor, struct wgpu::ChainedStruct, SharedTextureMemoryIOSurfaceDescriptor)
        SharedTextureMemoryIOSurfaceDescriptor.def(py::init<>());
        SharedTextureMemoryIOSurfaceDescriptor.def_readwrite("io_surface", &wgpu::SharedTextureMemoryIOSurfaceDescriptor::ioSurface);
    PYCLASS_END(_wgpu, wgpu::SharedTextureMemoryIOSurfaceDescriptor, SharedTextureMemoryIOSurfaceDescriptor)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SharedTextureMemoryAHardwareBufferDescriptor, struct wgpu::ChainedStruct, SharedTextureMemoryAHardwareBufferDescriptor)
        SharedTextureMemoryAHardwareBufferDescriptor.def(py::init<>());
        SharedTextureMemoryAHardwareBufferDescriptor.def_readwrite("handle", &wgpu::SharedTextureMemoryAHardwareBufferDescriptor::handle);
    PYCLASS_END(_wgpu, wgpu::SharedTextureMemoryAHardwareBufferDescriptor, SharedTextureMemoryAHardwareBufferDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::SharedTextureMemoryBeginAccessDescriptor, SharedTextureMemoryBeginAccessDescriptor)
        SharedTextureMemoryBeginAccessDescriptor.def_readwrite("next_in_chain", &wgpu::SharedTextureMemoryBeginAccessDescriptor::nextInChain);
        SharedTextureMemoryBeginAccessDescriptor.def_readwrite("initialized", &wgpu::SharedTextureMemoryBeginAccessDescriptor::initialized);
        SharedTextureMemoryBeginAccessDescriptor.def_readwrite("fence_count", &wgpu::SharedTextureMemoryBeginAccessDescriptor::fenceCount);
        SharedTextureMemoryBeginAccessDescriptor.def_readwrite("fences", &wgpu::SharedTextureMemoryBeginAccessDescriptor::fences);
        SharedTextureMemoryBeginAccessDescriptor.def_readwrite("signaled_values", &wgpu::SharedTextureMemoryBeginAccessDescriptor::signaledValues);
    PYCLASS_END(_wgpu, wgpu::SharedTextureMemoryBeginAccessDescriptor, SharedTextureMemoryBeginAccessDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::SharedTextureMemoryDescriptor, SharedTextureMemoryDescriptor)
        SharedTextureMemoryDescriptor.def_readwrite("next_in_chain", &wgpu::SharedTextureMemoryDescriptor::nextInChain);
        SharedTextureMemoryDescriptor.def_property("label",
            [](const wgpu::SharedTextureMemoryDescriptor& self){ return self.label; },[](wgpu::SharedTextureMemoryDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
    PYCLASS_END(_wgpu, wgpu::SharedTextureMemoryDescriptor, SharedTextureMemoryDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::SharedTextureMemoryDmaBufPlane, SharedTextureMemoryDmaBufPlane)
        SharedTextureMemoryDmaBufPlane.def_readwrite("fd", &wgpu::SharedTextureMemoryDmaBufPlane::fd);
        SharedTextureMemoryDmaBufPlane.def_readwrite("offset", &wgpu::SharedTextureMemoryDmaBufPlane::offset);
        SharedTextureMemoryDmaBufPlane.def_readwrite("stride", &wgpu::SharedTextureMemoryDmaBufPlane::stride);
    PYCLASS_END(_wgpu, wgpu::SharedTextureMemoryDmaBufPlane, SharedTextureMemoryDmaBufPlane)

    PYCLASS_BEGIN(_wgpu, wgpu::SharedTextureMemoryEndAccessState, SharedTextureMemoryEndAccessState)
        SharedTextureMemoryEndAccessState.def_readonly("next_in_chain", &wgpu::SharedTextureMemoryEndAccessState::nextInChain);
        SharedTextureMemoryEndAccessState.def_readonly("initialized", &wgpu::SharedTextureMemoryEndAccessState::initialized);
        SharedTextureMemoryEndAccessState.def_readonly("fence_count", &wgpu::SharedTextureMemoryEndAccessState::fenceCount);
        SharedTextureMemoryEndAccessState.def_readonly("fences", &wgpu::SharedTextureMemoryEndAccessState::fences);
        SharedTextureMemoryEndAccessState.def_readonly("signaled_values", &wgpu::SharedTextureMemoryEndAccessState::signaledValues);
    PYCLASS_END(_wgpu, wgpu::SharedTextureMemoryEndAccessState, SharedTextureMemoryEndAccessState)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SharedTextureMemoryOpaqueFDDescriptor, struct wgpu::ChainedStruct, SharedTextureMemoryOpaqueFDDescriptor)
        SharedTextureMemoryOpaqueFDDescriptor.def(py::init<>());
        SharedTextureMemoryOpaqueFDDescriptor.def_readwrite("vk_image_create_info", &wgpu::SharedTextureMemoryOpaqueFDDescriptor::vkImageCreateInfo);
        SharedTextureMemoryOpaqueFDDescriptor.def_readwrite("memory_fd", &wgpu::SharedTextureMemoryOpaqueFDDescriptor::memoryFD);
        SharedTextureMemoryOpaqueFDDescriptor.def_readwrite("memory_type_index", &wgpu::SharedTextureMemoryOpaqueFDDescriptor::memoryTypeIndex);
        SharedTextureMemoryOpaqueFDDescriptor.def_readwrite("allocation_size", &wgpu::SharedTextureMemoryOpaqueFDDescriptor::allocationSize);
        SharedTextureMemoryOpaqueFDDescriptor.def_readwrite("dedicated_allocation", &wgpu::SharedTextureMemoryOpaqueFDDescriptor::dedicatedAllocation);
    PYCLASS_END(_wgpu, wgpu::SharedTextureMemoryOpaqueFDDescriptor, SharedTextureMemoryOpaqueFDDescriptor)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SharedTextureMemoryVkDedicatedAllocationDescriptor, struct wgpu::ChainedStruct, SharedTextureMemoryVkDedicatedAllocationDescriptor)
        SharedTextureMemoryVkDedicatedAllocationDescriptor.def(py::init<>());
        SharedTextureMemoryVkDedicatedAllocationDescriptor.def_readwrite("dedicated_allocation", &wgpu::SharedTextureMemoryVkDedicatedAllocationDescriptor::dedicatedAllocation);
    PYCLASS_END(_wgpu, wgpu::SharedTextureMemoryVkDedicatedAllocationDescriptor, SharedTextureMemoryVkDedicatedAllocationDescriptor)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SharedTextureMemoryVkImageLayoutBeginState, struct wgpu::ChainedStruct, SharedTextureMemoryVkImageLayoutBeginState)
        SharedTextureMemoryVkImageLayoutBeginState.def(py::init<>());
        SharedTextureMemoryVkImageLayoutBeginState.def_readwrite("old_layout", &wgpu::SharedTextureMemoryVkImageLayoutBeginState::oldLayout);
        SharedTextureMemoryVkImageLayoutBeginState.def_readwrite("new_layout", &wgpu::SharedTextureMemoryVkImageLayoutBeginState::newLayout);
    PYCLASS_END(_wgpu, wgpu::SharedTextureMemoryVkImageLayoutBeginState, SharedTextureMemoryVkImageLayoutBeginState)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SharedTextureMemoryVkImageLayoutEndState, struct wgpu::ChainedStructOut, SharedTextureMemoryVkImageLayoutEndState)
        SharedTextureMemoryVkImageLayoutEndState.def(py::init<>());
        SharedTextureMemoryVkImageLayoutEndState.def_readwrite("old_layout", &wgpu::SharedTextureMemoryVkImageLayoutEndState::oldLayout);
        SharedTextureMemoryVkImageLayoutEndState.def_readwrite("new_layout", &wgpu::SharedTextureMemoryVkImageLayoutEndState::newLayout);
    PYCLASS_END(_wgpu, wgpu::SharedTextureMemoryVkImageLayoutEndState, SharedTextureMemoryVkImageLayoutEndState)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SharedTextureMemoryZirconHandleDescriptor, struct wgpu::ChainedStruct, SharedTextureMemoryZirconHandleDescriptor)
        SharedTextureMemoryZirconHandleDescriptor.def(py::init<>());
        SharedTextureMemoryZirconHandleDescriptor.def_readwrite("memory_fd", &wgpu::SharedTextureMemoryZirconHandleDescriptor::memoryFD);
        SharedTextureMemoryZirconHandleDescriptor.def_readwrite("allocation_size", &wgpu::SharedTextureMemoryZirconHandleDescriptor::allocationSize);
    PYCLASS_END(_wgpu, wgpu::SharedTextureMemoryZirconHandleDescriptor, SharedTextureMemoryZirconHandleDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::StencilFaceState, StencilFaceState)
        StencilFaceState.def_readwrite("compare", &wgpu::StencilFaceState::compare);
        StencilFaceState.def_readwrite("fail_op", &wgpu::StencilFaceState::failOp);
        StencilFaceState.def_readwrite("depth_fail_op", &wgpu::StencilFaceState::depthFailOp);
        StencilFaceState.def_readwrite("pass_op", &wgpu::StencilFaceState::passOp);
    PYCLASS_END(_wgpu, wgpu::StencilFaceState, StencilFaceState)

    PYCLASS_BEGIN(_wgpu, wgpu::StorageTextureBindingLayout, StorageTextureBindingLayout)
        StorageTextureBindingLayout.def_readwrite("next_in_chain", &wgpu::StorageTextureBindingLayout::nextInChain);
        StorageTextureBindingLayout.def_readwrite("access", &wgpu::StorageTextureBindingLayout::access);
        StorageTextureBindingLayout.def_readwrite("format", &wgpu::StorageTextureBindingLayout::format);
        StorageTextureBindingLayout.def_readwrite("view_dimension", &wgpu::StorageTextureBindingLayout::viewDimension);
    PYCLASS_END(_wgpu, wgpu::StorageTextureBindingLayout, StorageTextureBindingLayout)

    PYCLASS_BEGIN(_wgpu, wgpu::SurfaceDescriptor, SurfaceDescriptor)
        SurfaceDescriptor.def_readwrite("next_in_chain", &wgpu::SurfaceDescriptor::nextInChain);
        SurfaceDescriptor.def_property("label",
            [](const wgpu::SurfaceDescriptor& self){ return self.label; },[](wgpu::SurfaceDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        SurfaceDescriptor.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::SurfaceDescriptor obj;
            if (kwargs.contains("next_in_chain"))
            {
                auto value = kwargs["next_in_chain"].cast<const wgpu::ChainedStruct *>();
                obj.nextInChain = value;
            }
            if (kwargs.contains("label"))
            {
                auto _value = kwargs["label"].cast<std::string>();
                char* value = (char*)malloc(_value.size());
                strcpy(value, _value.c_str());
                obj.label = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
    PYCLASS_END(_wgpu, wgpu::SurfaceDescriptor, SurfaceDescriptor)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SurfaceDescriptorFromAndroidNativeWindow, struct wgpu::ChainedStruct, SurfaceDescriptorFromAndroidNativeWindow)
        SurfaceDescriptorFromAndroidNativeWindow.def(py::init<>());
        SurfaceDescriptorFromAndroidNativeWindow.def_readwrite("window", &wgpu::SurfaceDescriptorFromAndroidNativeWindow::window);
    PYCLASS_END(_wgpu, wgpu::SurfaceDescriptorFromAndroidNativeWindow, SurfaceDescriptorFromAndroidNativeWindow)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SurfaceDescriptorFromCanvasHTMLSelector, struct wgpu::ChainedStruct, SurfaceDescriptorFromCanvasHTMLSelector)
        SurfaceDescriptorFromCanvasHTMLSelector.def(py::init<>());
        SurfaceDescriptorFromCanvasHTMLSelector.def_property("selector",
            [](const wgpu::SurfaceDescriptorFromCanvasHTMLSelector& self){ return self.selector; },[](wgpu::SurfaceDescriptorFromCanvasHTMLSelector& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.selector = c; }
        );
    PYCLASS_END(_wgpu, wgpu::SurfaceDescriptorFromCanvasHTMLSelector, SurfaceDescriptorFromCanvasHTMLSelector)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SurfaceDescriptorFromMetalLayer, struct wgpu::ChainedStruct, SurfaceDescriptorFromMetalLayer)
        SurfaceDescriptorFromMetalLayer.def(py::init<>());
        SurfaceDescriptorFromMetalLayer.def_readwrite("layer", &wgpu::SurfaceDescriptorFromMetalLayer::layer);
    PYCLASS_END(_wgpu, wgpu::SurfaceDescriptorFromMetalLayer, SurfaceDescriptorFromMetalLayer)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SurfaceDescriptorFromWaylandSurface, struct wgpu::ChainedStruct, SurfaceDescriptorFromWaylandSurface)
        SurfaceDescriptorFromWaylandSurface.def(py::init<>());
        SurfaceDescriptorFromWaylandSurface.def_readwrite("display", &wgpu::SurfaceDescriptorFromWaylandSurface::display);
        SurfaceDescriptorFromWaylandSurface.def_readwrite("surface", &wgpu::SurfaceDescriptorFromWaylandSurface::surface);
    PYCLASS_END(_wgpu, wgpu::SurfaceDescriptorFromWaylandSurface, SurfaceDescriptorFromWaylandSurface)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SurfaceDescriptorFromWindowsHWND, struct wgpu::ChainedStruct, SurfaceDescriptorFromWindowsHWND)
        SurfaceDescriptorFromWindowsHWND.def(py::init<>());
        SurfaceDescriptorFromWindowsHWND.def_readwrite("hinstance", &wgpu::SurfaceDescriptorFromWindowsHWND::hinstance);
        SurfaceDescriptorFromWindowsHWND.def_readwrite("hwnd", &wgpu::SurfaceDescriptorFromWindowsHWND::hwnd);
        SurfaceDescriptorFromWindowsHWND.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::SurfaceDescriptorFromWindowsHWND obj;
            if (kwargs.contains("hinstance"))
            {
                auto value = kwargs["hinstance"].cast<void *>();
                obj.hinstance = value;
            }
            if (kwargs.contains("hwnd"))
            {
                auto value = kwargs["hwnd"].cast<void *>();
                obj.hwnd = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
    PYCLASS_END(_wgpu, wgpu::SurfaceDescriptorFromWindowsHWND, SurfaceDescriptorFromWindowsHWND)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SurfaceDescriptorFromWindowsCoreWindow, struct wgpu::ChainedStruct, SurfaceDescriptorFromWindowsCoreWindow)
        SurfaceDescriptorFromWindowsCoreWindow.def(py::init<>());
        SurfaceDescriptorFromWindowsCoreWindow.def_readwrite("core_window", &wgpu::SurfaceDescriptorFromWindowsCoreWindow::coreWindow);
    PYCLASS_END(_wgpu, wgpu::SurfaceDescriptorFromWindowsCoreWindow, SurfaceDescriptorFromWindowsCoreWindow)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SurfaceDescriptorFromWindowsSwapChainPanel, struct wgpu::ChainedStruct, SurfaceDescriptorFromWindowsSwapChainPanel)
        SurfaceDescriptorFromWindowsSwapChainPanel.def(py::init<>());
        SurfaceDescriptorFromWindowsSwapChainPanel.def_readwrite("swap_chain_panel", &wgpu::SurfaceDescriptorFromWindowsSwapChainPanel::swapChainPanel);
    PYCLASS_END(_wgpu, wgpu::SurfaceDescriptorFromWindowsSwapChainPanel, SurfaceDescriptorFromWindowsSwapChainPanel)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SurfaceDescriptorFromXlibWindow, struct wgpu::ChainedStruct, SurfaceDescriptorFromXlibWindow)
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
        SwapChainDescriptor.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::SwapChainDescriptor obj;
            if (kwargs.contains("next_in_chain"))
            {
                auto value = kwargs["next_in_chain"].cast<const wgpu::ChainedStruct *>();
                obj.nextInChain = value;
            }
            if (kwargs.contains("label"))
            {
                auto _value = kwargs["label"].cast<std::string>();
                char* value = (char*)malloc(_value.size());
                strcpy(value, _value.c_str());
                obj.label = value;
            }
            if (kwargs.contains("usage"))
            {
                auto value = kwargs["usage"].cast<wgpu::TextureUsage>();
                obj.usage = value;
            }
            if (kwargs.contains("format"))
            {
                auto value = kwargs["format"].cast<wgpu::TextureFormat>();
                obj.format = value;
            }
            if (kwargs.contains("width"))
            {
                auto value = kwargs["width"].cast<uint32_t>();
                obj.width = value;
            }
            if (kwargs.contains("height"))
            {
                auto value = kwargs["height"].cast<uint32_t>();
                obj.height = value;
            }
            if (kwargs.contains("present_mode"))
            {
                auto value = kwargs["present_mode"].cast<wgpu::PresentMode>();
                obj.presentMode = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
    PYCLASS_END(_wgpu, wgpu::SwapChainDescriptor, SwapChainDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::TextureBindingLayout, TextureBindingLayout)
        TextureBindingLayout.def_readwrite("next_in_chain", &wgpu::TextureBindingLayout::nextInChain);
        TextureBindingLayout.def_readwrite("sample_type", &wgpu::TextureBindingLayout::sampleType);
        TextureBindingLayout.def_readwrite("view_dimension", &wgpu::TextureBindingLayout::viewDimension);
        TextureBindingLayout.def_readwrite("multisampled", &wgpu::TextureBindingLayout::multisampled);
        TextureBindingLayout.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::TextureBindingLayout obj;
            if (kwargs.contains("next_in_chain"))
            {
                auto value = kwargs["next_in_chain"].cast<const wgpu::ChainedStruct *>();
                obj.nextInChain = value;
            }
            if (kwargs.contains("sample_type"))
            {
                auto value = kwargs["sample_type"].cast<wgpu::TextureSampleType>();
                obj.sampleType = value;
            }
            if (kwargs.contains("view_dimension"))
            {
                auto value = kwargs["view_dimension"].cast<wgpu::TextureViewDimension>();
                obj.viewDimension = value;
            }
            if (kwargs.contains("multisampled"))
            {
                auto value = kwargs["multisampled"].cast<wgpu::Bool>();
                obj.multisampled = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
    PYCLASS_END(_wgpu, wgpu::TextureBindingLayout, TextureBindingLayout)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::TextureBindingViewDimensionDescriptor, struct wgpu::ChainedStruct, TextureBindingViewDimensionDescriptor)
        TextureBindingViewDimensionDescriptor.def(py::init<>());
        TextureBindingViewDimensionDescriptor.def_readwrite("texture_binding_view_dimension", &wgpu::TextureBindingViewDimensionDescriptor::textureBindingViewDimension);
    PYCLASS_END(_wgpu, wgpu::TextureBindingViewDimensionDescriptor, TextureBindingViewDimensionDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::TextureDataLayout, TextureDataLayout)
        TextureDataLayout.def_readwrite("next_in_chain", &wgpu::TextureDataLayout::nextInChain);
        TextureDataLayout.def_readwrite("offset", &wgpu::TextureDataLayout::offset);
        TextureDataLayout.def_readwrite("bytes_per_row", &wgpu::TextureDataLayout::bytesPerRow);
        TextureDataLayout.def_readwrite("rows_per_image", &wgpu::TextureDataLayout::rowsPerImage);
        TextureDataLayout.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::TextureDataLayout obj;
            if (kwargs.contains("next_in_chain"))
            {
                auto value = kwargs["next_in_chain"].cast<const wgpu::ChainedStruct *>();
                obj.nextInChain = value;
            }
            if (kwargs.contains("offset"))
            {
                auto value = kwargs["offset"].cast<uint64_t>();
                obj.offset = value;
            }
            if (kwargs.contains("bytes_per_row"))
            {
                auto value = kwargs["bytes_per_row"].cast<uint32_t>();
                obj.bytesPerRow = value;
            }
            if (kwargs.contains("rows_per_image"))
            {
                auto value = kwargs["rows_per_image"].cast<uint32_t>();
                obj.rowsPerImage = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
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
    PYCLASS_END(_wgpu, wgpu::TextureViewDescriptor, TextureViewDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::VertexAttribute, VertexAttribute)
        VertexAttribute.def_readwrite("format", &wgpu::VertexAttribute::format);
        VertexAttribute.def_readwrite("offset", &wgpu::VertexAttribute::offset);
        VertexAttribute.def_readwrite("shader_location", &wgpu::VertexAttribute::shaderLocation);
        VertexAttribute.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::VertexAttribute obj;
            if (kwargs.contains("format"))
            {
                auto value = kwargs["format"].cast<wgpu::VertexFormat>();
                obj.format = value;
            }
            if (kwargs.contains("offset"))
            {
                auto value = kwargs["offset"].cast<uint64_t>();
                obj.offset = value;
            }
            if (kwargs.contains("shader_location"))
            {
                auto value = kwargs["shader_location"].cast<uint32_t>();
                obj.shaderLocation = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
    PYCLASS_END(_wgpu, wgpu::VertexAttribute, VertexAttribute)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::AdapterPropertiesMemoryHeaps, struct wgpu::ChainedStructOut, AdapterPropertiesMemoryHeaps)
        AdapterPropertiesMemoryHeaps.def_readonly("heap_count", &wgpu::AdapterPropertiesMemoryHeaps::heapCount);
        AdapterPropertiesMemoryHeaps.def_readonly("heap_info", &wgpu::AdapterPropertiesMemoryHeaps::heapInfo);
    PYCLASS_END(_wgpu, wgpu::AdapterPropertiesMemoryHeaps, AdapterPropertiesMemoryHeaps)

    PYCLASS_BEGIN(_wgpu, wgpu::BindGroupDescriptor, BindGroupDescriptor)
        BindGroupDescriptor.def_readwrite("next_in_chain", &wgpu::BindGroupDescriptor::nextInChain);
        BindGroupDescriptor.def_property("label",
            [](const wgpu::BindGroupDescriptor& self){ return self.label; },[](wgpu::BindGroupDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        BindGroupDescriptor.def_readwrite("layout", &wgpu::BindGroupDescriptor::layout);
        BindGroupDescriptor.def_readwrite("entry_count", &wgpu::BindGroupDescriptor::entryCount);
        BindGroupDescriptor.def_readwrite("entries", &wgpu::BindGroupDescriptor::entries);
        BindGroupDescriptor.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::BindGroupDescriptor obj;
            if (kwargs.contains("next_in_chain"))
            {
                auto value = kwargs["next_in_chain"].cast<const wgpu::ChainedStruct *>();
                obj.nextInChain = value;
            }
            if (kwargs.contains("label"))
            {
                auto _value = kwargs["label"].cast<std::string>();
                char* value = (char*)malloc(_value.size());
                strcpy(value, _value.c_str());
                obj.label = value;
            }
            if (kwargs.contains("layout"))
            {
                auto value = kwargs["layout"].cast<wgpu::BindGroupLayout>();
                obj.layout = value;
            }
            if (kwargs.contains("entry_count"))
            {
                auto value = kwargs["entry_count"].cast<size_t>();
                obj.entryCount = value;
            }
            if (kwargs.contains("entries"))
            {
                auto value = kwargs["entries"].cast<const wgpu::BindGroupEntry *>();
                obj.entries = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
    PYCLASS_END(_wgpu, wgpu::BindGroupDescriptor, BindGroupDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::BindGroupLayoutEntry, BindGroupLayoutEntry)
        BindGroupLayoutEntry.def_readwrite("next_in_chain", &wgpu::BindGroupLayoutEntry::nextInChain);
        BindGroupLayoutEntry.def_readwrite("binding", &wgpu::BindGroupLayoutEntry::binding);
        BindGroupLayoutEntry.def_readwrite("visibility", &wgpu::BindGroupLayoutEntry::visibility);
        BindGroupLayoutEntry.def_readwrite("buffer", &wgpu::BindGroupLayoutEntry::buffer);
        BindGroupLayoutEntry.def_readwrite("sampler", &wgpu::BindGroupLayoutEntry::sampler);
        BindGroupLayoutEntry.def_readwrite("texture", &wgpu::BindGroupLayoutEntry::texture);
        BindGroupLayoutEntry.def_readwrite("storage_texture", &wgpu::BindGroupLayoutEntry::storageTexture);
        BindGroupLayoutEntry.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::BindGroupLayoutEntry obj;
            if (kwargs.contains("next_in_chain"))
            {
                auto value = kwargs["next_in_chain"].cast<const wgpu::ChainedStruct *>();
                obj.nextInChain = value;
            }
            if (kwargs.contains("binding"))
            {
                auto value = kwargs["binding"].cast<uint32_t>();
                obj.binding = value;
            }
            if (kwargs.contains("visibility"))
            {
                auto value = kwargs["visibility"].cast<wgpu::ShaderStage>();
                obj.visibility = value;
            }
            if (kwargs.contains("buffer"))
            {
                auto value = kwargs["buffer"].cast<wgpu::BufferBindingLayout>();
                obj.buffer = value;
            }
            if (kwargs.contains("sampler"))
            {
                auto value = kwargs["sampler"].cast<wgpu::SamplerBindingLayout>();
                obj.sampler = value;
            }
            if (kwargs.contains("texture"))
            {
                auto value = kwargs["texture"].cast<wgpu::TextureBindingLayout>();
                obj.texture = value;
            }
            if (kwargs.contains("storage_texture"))
            {
                auto value = kwargs["storage_texture"].cast<wgpu::StorageTextureBindingLayout>();
                obj.storageTexture = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
    PYCLASS_END(_wgpu, wgpu::BindGroupLayoutEntry, BindGroupLayoutEntry)

    PYCLASS_BEGIN(_wgpu, wgpu::BlendState, BlendState)
        BlendState.def_readwrite("color", &wgpu::BlendState::color);
        BlendState.def_readwrite("alpha", &wgpu::BlendState::alpha);
        BlendState.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::BlendState obj;
            if (kwargs.contains("color"))
            {
                auto value = kwargs["color"].cast<wgpu::BlendComponent>();
                obj.color = value;
            }
            if (kwargs.contains("alpha"))
            {
                auto value = kwargs["alpha"].cast<wgpu::BlendComponent>();
                obj.alpha = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
    PYCLASS_END(_wgpu, wgpu::BlendState, BlendState)

    PYCLASS_BEGIN(_wgpu, wgpu::CompilationInfo, CompilationInfo)
        CompilationInfo.def_readwrite("next_in_chain", &wgpu::CompilationInfo::nextInChain);
        CompilationInfo.def_readwrite("message_count", &wgpu::CompilationInfo::messageCount);
        CompilationInfo.def_readwrite("messages", &wgpu::CompilationInfo::messages);
    PYCLASS_END(_wgpu, wgpu::CompilationInfo, CompilationInfo)

    PYCLASS_BEGIN(_wgpu, wgpu::ComputePassDescriptor, ComputePassDescriptor)
        ComputePassDescriptor.def_readwrite("next_in_chain", &wgpu::ComputePassDescriptor::nextInChain);
        ComputePassDescriptor.def_property("label",
            [](const wgpu::ComputePassDescriptor& self){ return self.label; },[](wgpu::ComputePassDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        ComputePassDescriptor.def_readwrite("timestamp_writes", &wgpu::ComputePassDescriptor::timestampWrites);
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
        DepthStencilState.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::DepthStencilState obj;
            if (kwargs.contains("next_in_chain"))
            {
                auto value = kwargs["next_in_chain"].cast<const wgpu::ChainedStruct *>();
                obj.nextInChain = value;
            }
            if (kwargs.contains("format"))
            {
                auto value = kwargs["format"].cast<wgpu::TextureFormat>();
                obj.format = value;
            }
            if (kwargs.contains("depth_write_enabled"))
            {
                auto value = kwargs["depth_write_enabled"].cast<wgpu::Bool>();
                obj.depthWriteEnabled = value;
            }
            if (kwargs.contains("depth_compare"))
            {
                auto value = kwargs["depth_compare"].cast<wgpu::CompareFunction>();
                obj.depthCompare = value;
            }
            if (kwargs.contains("stencil_front"))
            {
                auto value = kwargs["stencil_front"].cast<wgpu::StencilFaceState>();
                obj.stencilFront = value;
            }
            if (kwargs.contains("stencil_back"))
            {
                auto value = kwargs["stencil_back"].cast<wgpu::StencilFaceState>();
                obj.stencilBack = value;
            }
            if (kwargs.contains("stencil_read_mask"))
            {
                auto value = kwargs["stencil_read_mask"].cast<uint32_t>();
                obj.stencilReadMask = value;
            }
            if (kwargs.contains("stencil_write_mask"))
            {
                auto value = kwargs["stencil_write_mask"].cast<uint32_t>();
                obj.stencilWriteMask = value;
            }
            if (kwargs.contains("depth_bias"))
            {
                auto value = kwargs["depth_bias"].cast<int32_t>();
                obj.depthBias = value;
            }
            if (kwargs.contains("depth_bias_slope_scale"))
            {
                auto value = kwargs["depth_bias_slope_scale"].cast<float>();
                obj.depthBiasSlopeScale = value;
            }
            if (kwargs.contains("depth_bias_clamp"))
            {
                auto value = kwargs["depth_bias_clamp"].cast<float>();
                obj.depthBiasClamp = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
    PYCLASS_END(_wgpu, wgpu::DepthStencilState, DepthStencilState)

    PYCLASS_BEGIN(_wgpu, wgpu::ExternalTextureDescriptor, ExternalTextureDescriptor)
        ExternalTextureDescriptor.def_readwrite("next_in_chain", &wgpu::ExternalTextureDescriptor::nextInChain);
        ExternalTextureDescriptor.def_property("label",
            [](const wgpu::ExternalTextureDescriptor& self){ return self.label; },[](wgpu::ExternalTextureDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        ExternalTextureDescriptor.def_readwrite("plane0", &wgpu::ExternalTextureDescriptor::plane0);
        ExternalTextureDescriptor.def_readwrite("plane1", &wgpu::ExternalTextureDescriptor::plane1);
        ExternalTextureDescriptor.def_readwrite("visible_origin", &wgpu::ExternalTextureDescriptor::visibleOrigin);
        ExternalTextureDescriptor.def_readwrite("visible_size", &wgpu::ExternalTextureDescriptor::visibleSize);
        ExternalTextureDescriptor.def_readwrite("do_yuv_to_rgb_conversion_only", &wgpu::ExternalTextureDescriptor::doYuvToRgbConversionOnly);
        ExternalTextureDescriptor.def_readwrite("yuv_to_rgb_conversion_matrix", &wgpu::ExternalTextureDescriptor::yuvToRgbConversionMatrix);
        ExternalTextureDescriptor.def_readwrite("src_transfer_function_parameters", &wgpu::ExternalTextureDescriptor::srcTransferFunctionParameters);
        ExternalTextureDescriptor.def_readwrite("dst_transfer_function_parameters", &wgpu::ExternalTextureDescriptor::dstTransferFunctionParameters);
        ExternalTextureDescriptor.def_readwrite("gamut_conversion_matrix", &wgpu::ExternalTextureDescriptor::gamutConversionMatrix);
        ExternalTextureDescriptor.def_readwrite("flip_y", &wgpu::ExternalTextureDescriptor::flipY);
        ExternalTextureDescriptor.def_readwrite("rotation", &wgpu::ExternalTextureDescriptor::rotation);
    PYCLASS_END(_wgpu, wgpu::ExternalTextureDescriptor, ExternalTextureDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::FutureWaitInfo, FutureWaitInfo)
        FutureWaitInfo.def_readwrite("future", &wgpu::FutureWaitInfo::future);
        FutureWaitInfo.def_readwrite("completed", &wgpu::FutureWaitInfo::completed);
    PYCLASS_END(_wgpu, wgpu::FutureWaitInfo, FutureWaitInfo)

    PYCLASS_BEGIN(_wgpu, wgpu::ImageCopyBuffer, ImageCopyBuffer)
        ImageCopyBuffer.def_readwrite("next_in_chain", &wgpu::ImageCopyBuffer::nextInChain);
        ImageCopyBuffer.def_readwrite("layout", &wgpu::ImageCopyBuffer::layout);
        ImageCopyBuffer.def_readwrite("buffer", &wgpu::ImageCopyBuffer::buffer);
        ImageCopyBuffer.def(py::init<>());
    PYCLASS_END(_wgpu, wgpu::ImageCopyBuffer, ImageCopyBuffer)

    PYCLASS_BEGIN(_wgpu, wgpu::ImageCopyExternalTexture, ImageCopyExternalTexture)
        ImageCopyExternalTexture.def_readwrite("next_in_chain", &wgpu::ImageCopyExternalTexture::nextInChain);
        ImageCopyExternalTexture.def_readwrite("external_texture", &wgpu::ImageCopyExternalTexture::externalTexture);
        ImageCopyExternalTexture.def_readwrite("origin", &wgpu::ImageCopyExternalTexture::origin);
        ImageCopyExternalTexture.def_readwrite("natural_size", &wgpu::ImageCopyExternalTexture::naturalSize);
    PYCLASS_END(_wgpu, wgpu::ImageCopyExternalTexture, ImageCopyExternalTexture)

    PYCLASS_BEGIN(_wgpu, wgpu::ImageCopyTexture, ImageCopyTexture)
        ImageCopyTexture.def_readwrite("next_in_chain", &wgpu::ImageCopyTexture::nextInChain);
        ImageCopyTexture.def_readwrite("texture", &wgpu::ImageCopyTexture::texture);
        ImageCopyTexture.def_readwrite("mip_level", &wgpu::ImageCopyTexture::mipLevel);
        ImageCopyTexture.def_readwrite("origin", &wgpu::ImageCopyTexture::origin);
        ImageCopyTexture.def_readwrite("aspect", &wgpu::ImageCopyTexture::aspect);
        ImageCopyTexture.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::ImageCopyTexture obj;
            if (kwargs.contains("next_in_chain"))
            {
                auto value = kwargs["next_in_chain"].cast<const wgpu::ChainedStruct *>();
                obj.nextInChain = value;
            }
            if (kwargs.contains("texture"))
            {
                auto value = kwargs["texture"].cast<wgpu::Texture>();
                obj.texture = value;
            }
            if (kwargs.contains("mip_level"))
            {
                auto value = kwargs["mip_level"].cast<uint32_t>();
                obj.mipLevel = value;
            }
            if (kwargs.contains("origin"))
            {
                auto value = kwargs["origin"].cast<wgpu::Origin3D>();
                obj.origin = value;
            }
            if (kwargs.contains("aspect"))
            {
                auto value = kwargs["aspect"].cast<wgpu::TextureAspect>();
                obj.aspect = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
    PYCLASS_END(_wgpu, wgpu::ImageCopyTexture, ImageCopyTexture)

    PYCLASS_BEGIN(_wgpu, wgpu::InstanceDescriptor, InstanceDescriptor)
        InstanceDescriptor.def_readwrite("next_in_chain", &wgpu::InstanceDescriptor::nextInChain);
        InstanceDescriptor.def_readwrite("features", &wgpu::InstanceDescriptor::features);
    PYCLASS_END(_wgpu, wgpu::InstanceDescriptor, InstanceDescriptor)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::PipelineLayoutPixelLocalStorage, struct wgpu::ChainedStruct, PipelineLayoutPixelLocalStorage)
        PipelineLayoutPixelLocalStorage.def(py::init<>());
        PipelineLayoutPixelLocalStorage.def_readwrite("total_pixel_local_storage_size", &wgpu::PipelineLayoutPixelLocalStorage::totalPixelLocalStorageSize);
        PipelineLayoutPixelLocalStorage.def_readwrite("storage_attachment_count", &wgpu::PipelineLayoutPixelLocalStorage::storageAttachmentCount);
        PipelineLayoutPixelLocalStorage.def_readwrite("storage_attachments", &wgpu::PipelineLayoutPixelLocalStorage::storageAttachments);
    PYCLASS_END(_wgpu, wgpu::PipelineLayoutPixelLocalStorage, PipelineLayoutPixelLocalStorage)

    PYCLASS_BEGIN(_wgpu, wgpu::ProgrammableStageDescriptor, ProgrammableStageDescriptor)
        ProgrammableStageDescriptor.def_readwrite("next_in_chain", &wgpu::ProgrammableStageDescriptor::nextInChain);
        ProgrammableStageDescriptor.def_readwrite("module", &wgpu::ProgrammableStageDescriptor::module);
        ProgrammableStageDescriptor.def_property("entry_point",
            [](const wgpu::ProgrammableStageDescriptor& self){ return self.entryPoint; },[](wgpu::ProgrammableStageDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.entryPoint = c; }
        );
        ProgrammableStageDescriptor.def_readwrite("constant_count", &wgpu::ProgrammableStageDescriptor::constantCount);
        ProgrammableStageDescriptor.def_readwrite("constants", &wgpu::ProgrammableStageDescriptor::constants);
    PYCLASS_END(_wgpu, wgpu::ProgrammableStageDescriptor, ProgrammableStageDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::RenderPassColorAttachment, RenderPassColorAttachment)
        RenderPassColorAttachment.def_readwrite("next_in_chain", &wgpu::RenderPassColorAttachment::nextInChain);
        RenderPassColorAttachment.def_readwrite("view", &wgpu::RenderPassColorAttachment::view);
        RenderPassColorAttachment.def_readwrite("depth_slice", &wgpu::RenderPassColorAttachment::depthSlice);
        RenderPassColorAttachment.def_readwrite("resolve_target", &wgpu::RenderPassColorAttachment::resolveTarget);
        RenderPassColorAttachment.def_readwrite("load_op", &wgpu::RenderPassColorAttachment::loadOp);
        RenderPassColorAttachment.def_readwrite("store_op", &wgpu::RenderPassColorAttachment::storeOp);
        RenderPassColorAttachment.def_readwrite("clear_value", &wgpu::RenderPassColorAttachment::clearValue);
        RenderPassColorAttachment.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::RenderPassColorAttachment obj;
            if (kwargs.contains("next_in_chain"))
            {
                auto value = kwargs["next_in_chain"].cast<const wgpu::ChainedStruct *>();
                obj.nextInChain = value;
            }
            if (kwargs.contains("view"))
            {
                auto value = kwargs["view"].cast<wgpu::TextureView>();
                obj.view = value;
            }
            if (kwargs.contains("depth_slice"))
            {
                auto value = kwargs["depth_slice"].cast<uint32_t>();
                obj.depthSlice = value;
            }
            if (kwargs.contains("resolve_target"))
            {
                auto value = kwargs["resolve_target"].cast<wgpu::TextureView>();
                obj.resolveTarget = value;
            }
            if (kwargs.contains("load_op"))
            {
                auto value = kwargs["load_op"].cast<wgpu::LoadOp>();
                obj.loadOp = value;
            }
            if (kwargs.contains("store_op"))
            {
                auto value = kwargs["store_op"].cast<wgpu::StoreOp>();
                obj.storeOp = value;
            }
            if (kwargs.contains("clear_value"))
            {
                auto value = kwargs["clear_value"].cast<wgpu::Color>();
                obj.clearValue = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
    PYCLASS_END(_wgpu, wgpu::RenderPassColorAttachment, RenderPassColorAttachment)

    PYCLASS_BEGIN(_wgpu, wgpu::RenderPassStorageAttachment, RenderPassStorageAttachment)
        RenderPassStorageAttachment.def_readwrite("next_in_chain", &wgpu::RenderPassStorageAttachment::nextInChain);
        RenderPassStorageAttachment.def_readwrite("offset", &wgpu::RenderPassStorageAttachment::offset);
        RenderPassStorageAttachment.def_readwrite("storage", &wgpu::RenderPassStorageAttachment::storage);
        RenderPassStorageAttachment.def_readwrite("load_op", &wgpu::RenderPassStorageAttachment::loadOp);
        RenderPassStorageAttachment.def_readwrite("store_op", &wgpu::RenderPassStorageAttachment::storeOp);
        RenderPassStorageAttachment.def_readwrite("clear_value", &wgpu::RenderPassStorageAttachment::clearValue);
    PYCLASS_END(_wgpu, wgpu::RenderPassStorageAttachment, RenderPassStorageAttachment)

    PYCLASS_BEGIN(_wgpu, wgpu::RequiredLimits, RequiredLimits)
        RequiredLimits.def_readwrite("next_in_chain", &wgpu::RequiredLimits::nextInChain);
        RequiredLimits.def_readwrite("limits", &wgpu::RequiredLimits::limits);
    PYCLASS_END(_wgpu, wgpu::RequiredLimits, RequiredLimits)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SharedTextureMemoryDmaBufDescriptor, struct wgpu::ChainedStruct, SharedTextureMemoryDmaBufDescriptor)
        SharedTextureMemoryDmaBufDescriptor.def(py::init<>());
        SharedTextureMemoryDmaBufDescriptor.def_readwrite("size", &wgpu::SharedTextureMemoryDmaBufDescriptor::size);
        SharedTextureMemoryDmaBufDescriptor.def_readwrite("drm_format", &wgpu::SharedTextureMemoryDmaBufDescriptor::drmFormat);
        SharedTextureMemoryDmaBufDescriptor.def_readwrite("drm_modifier", &wgpu::SharedTextureMemoryDmaBufDescriptor::drmModifier);
        SharedTextureMemoryDmaBufDescriptor.def_readwrite("plane_count", &wgpu::SharedTextureMemoryDmaBufDescriptor::planeCount);
        SharedTextureMemoryDmaBufDescriptor.def_readwrite("planes", &wgpu::SharedTextureMemoryDmaBufDescriptor::planes);
    PYCLASS_END(_wgpu, wgpu::SharedTextureMemoryDmaBufDescriptor, SharedTextureMemoryDmaBufDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::SharedTextureMemoryProperties, SharedTextureMemoryProperties)
        SharedTextureMemoryProperties.def_readwrite("next_in_chain", &wgpu::SharedTextureMemoryProperties::nextInChain);
        SharedTextureMemoryProperties.def_readwrite("usage", &wgpu::SharedTextureMemoryProperties::usage);
        SharedTextureMemoryProperties.def_readwrite("size", &wgpu::SharedTextureMemoryProperties::size);
        SharedTextureMemoryProperties.def_readwrite("format", &wgpu::SharedTextureMemoryProperties::format);
    PYCLASS_END(_wgpu, wgpu::SharedTextureMemoryProperties, SharedTextureMemoryProperties)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::SharedTextureMemoryVkImageDescriptor, struct wgpu::ChainedStruct, SharedTextureMemoryVkImageDescriptor)
        SharedTextureMemoryVkImageDescriptor.def(py::init<>());
        SharedTextureMemoryVkImageDescriptor.def_readwrite("vk_format", &wgpu::SharedTextureMemoryVkImageDescriptor::vkFormat);
        SharedTextureMemoryVkImageDescriptor.def_readwrite("vk_usage_flags", &wgpu::SharedTextureMemoryVkImageDescriptor::vkUsageFlags);
        SharedTextureMemoryVkImageDescriptor.def_readwrite("vk_extent3d", &wgpu::SharedTextureMemoryVkImageDescriptor::vkExtent3D);
    PYCLASS_END(_wgpu, wgpu::SharedTextureMemoryVkImageDescriptor, SharedTextureMemoryVkImageDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::SupportedLimits, SupportedLimits)
        SupportedLimits.def_readwrite("next_in_chain", &wgpu::SupportedLimits::nextInChain);
        SupportedLimits.def_readwrite("limits", &wgpu::SupportedLimits::limits);
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
        TextureDescriptor.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::TextureDescriptor obj;
            if (kwargs.contains("next_in_chain"))
            {
                auto value = kwargs["next_in_chain"].cast<const wgpu::ChainedStruct *>();
                obj.nextInChain = value;
            }
            if (kwargs.contains("label"))
            {
                auto _value = kwargs["label"].cast<std::string>();
                char* value = (char*)malloc(_value.size());
                strcpy(value, _value.c_str());
                obj.label = value;
            }
            if (kwargs.contains("usage"))
            {
                auto value = kwargs["usage"].cast<wgpu::TextureUsage>();
                obj.usage = value;
            }
            if (kwargs.contains("dimension"))
            {
                auto value = kwargs["dimension"].cast<wgpu::TextureDimension>();
                obj.dimension = value;
            }
            if (kwargs.contains("size"))
            {
                auto value = kwargs["size"].cast<wgpu::Extent3D>();
                obj.size = value;
            }
            if (kwargs.contains("format"))
            {
                auto value = kwargs["format"].cast<wgpu::TextureFormat>();
                obj.format = value;
            }
            if (kwargs.contains("mip_level_count"))
            {
                auto value = kwargs["mip_level_count"].cast<uint32_t>();
                obj.mipLevelCount = value;
            }
            if (kwargs.contains("sample_count"))
            {
                auto value = kwargs["sample_count"].cast<uint32_t>();
                obj.sampleCount = value;
            }
            if (kwargs.contains("view_format_count"))
            {
                auto value = kwargs["view_format_count"].cast<size_t>();
                obj.viewFormatCount = value;
            }
            if (kwargs.contains("view_formats"))
            {
                auto value = kwargs["view_formats"].cast<const wgpu::TextureFormat *>();
                obj.viewFormats = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
    PYCLASS_END(_wgpu, wgpu::TextureDescriptor, TextureDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::VertexBufferLayout, VertexBufferLayout)
        VertexBufferLayout.def_readwrite("array_stride", &wgpu::VertexBufferLayout::arrayStride);
        VertexBufferLayout.def_readwrite("step_mode", &wgpu::VertexBufferLayout::stepMode);
        VertexBufferLayout.def_readwrite("attribute_count", &wgpu::VertexBufferLayout::attributeCount);
        VertexBufferLayout.def_readwrite("attributes", &wgpu::VertexBufferLayout::attributes);
        VertexBufferLayout.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::VertexBufferLayout obj;
            if (kwargs.contains("array_stride"))
            {
                auto value = kwargs["array_stride"].cast<uint64_t>();
                obj.arrayStride = value;
            }
            if (kwargs.contains("step_mode"))
            {
                auto value = kwargs["step_mode"].cast<wgpu::VertexStepMode>();
                obj.stepMode = value;
            }
            if (kwargs.contains("attribute_count"))
            {
                auto value = kwargs["attribute_count"].cast<size_t>();
                obj.attributeCount = value;
            }
            if (kwargs.contains("attributes"))
            {
                auto value = kwargs["attributes"].cast<const wgpu::VertexAttribute *>();
                obj.attributes = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
    PYCLASS_END(_wgpu, wgpu::VertexBufferLayout, VertexBufferLayout)

    PYCLASS_BEGIN(_wgpu, wgpu::BindGroupLayoutDescriptor, BindGroupLayoutDescriptor)
        BindGroupLayoutDescriptor.def_readwrite("next_in_chain", &wgpu::BindGroupLayoutDescriptor::nextInChain);
        BindGroupLayoutDescriptor.def_property("label",
            [](const wgpu::BindGroupLayoutDescriptor& self){ return self.label; },[](wgpu::BindGroupLayoutDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        BindGroupLayoutDescriptor.def_readwrite("entry_count", &wgpu::BindGroupLayoutDescriptor::entryCount);
        BindGroupLayoutDescriptor.def_readwrite("entries", &wgpu::BindGroupLayoutDescriptor::entries);
        BindGroupLayoutDescriptor.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::BindGroupLayoutDescriptor obj;
            if (kwargs.contains("next_in_chain"))
            {
                auto value = kwargs["next_in_chain"].cast<const wgpu::ChainedStruct *>();
                obj.nextInChain = value;
            }
            if (kwargs.contains("label"))
            {
                auto _value = kwargs["label"].cast<std::string>();
                char* value = (char*)malloc(_value.size());
                strcpy(value, _value.c_str());
                obj.label = value;
            }
            if (kwargs.contains("entry_count"))
            {
                auto value = kwargs["entry_count"].cast<size_t>();
                obj.entryCount = value;
            }
            if (kwargs.contains("entries"))
            {
                auto value = kwargs["entries"].cast<const wgpu::BindGroupLayoutEntry *>();
                obj.entries = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
    PYCLASS_END(_wgpu, wgpu::BindGroupLayoutDescriptor, BindGroupLayoutDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::ColorTargetState, ColorTargetState)
        ColorTargetState.def_readwrite("next_in_chain", &wgpu::ColorTargetState::nextInChain);
        ColorTargetState.def_readwrite("format", &wgpu::ColorTargetState::format);
        ColorTargetState.def_readwrite("blend", &wgpu::ColorTargetState::blend);
        ColorTargetState.def_readwrite("write_mask", &wgpu::ColorTargetState::writeMask);
        ColorTargetState.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::ColorTargetState obj;
            if (kwargs.contains("next_in_chain"))
            {
                auto value = kwargs["next_in_chain"].cast<const wgpu::ChainedStruct *>();
                obj.nextInChain = value;
            }
            if (kwargs.contains("format"))
            {
                auto value = kwargs["format"].cast<wgpu::TextureFormat>();
                obj.format = value;
            }
            if (kwargs.contains("blend"))
            {
                auto value = kwargs["blend"].cast<const wgpu::BlendState *>();
                obj.blend = value;
            }
            if (kwargs.contains("write_mask"))
            {
                auto value = kwargs["write_mask"].cast<wgpu::ColorWriteMask>();
                obj.writeMask = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
    PYCLASS_END(_wgpu, wgpu::ColorTargetState, ColorTargetState)

    PYCLASS_BEGIN(_wgpu, wgpu::ComputePipelineDescriptor, ComputePipelineDescriptor)
        ComputePipelineDescriptor.def_readwrite("next_in_chain", &wgpu::ComputePipelineDescriptor::nextInChain);
        ComputePipelineDescriptor.def_property("label",
            [](const wgpu::ComputePipelineDescriptor& self){ return self.label; },[](wgpu::ComputePipelineDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        ComputePipelineDescriptor.def_readwrite("layout", &wgpu::ComputePipelineDescriptor::layout);
        ComputePipelineDescriptor.def_readwrite("compute", &wgpu::ComputePipelineDescriptor::compute);
    PYCLASS_END(_wgpu, wgpu::ComputePipelineDescriptor, ComputePipelineDescriptor)

    PYCLASS_BEGIN(_wgpu, wgpu::DeviceDescriptor, DeviceDescriptor)
        DeviceDescriptor.def_readwrite("next_in_chain", &wgpu::DeviceDescriptor::nextInChain);
        DeviceDescriptor.def_property("label",
            [](const wgpu::DeviceDescriptor& self){ return self.label; },[](wgpu::DeviceDescriptor& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.label = c; }
        );
        DeviceDescriptor.def_readwrite("required_feature_count", &wgpu::DeviceDescriptor::requiredFeatureCount);
        DeviceDescriptor.def_readwrite("required_features", &wgpu::DeviceDescriptor::requiredFeatures);
        DeviceDescriptor.def_readwrite("required_limits", &wgpu::DeviceDescriptor::requiredLimits);
        DeviceDescriptor.def_readwrite("default_queue", &wgpu::DeviceDescriptor::defaultQueue);
        DeviceDescriptor.def_readwrite("device_lost_userdata", &wgpu::DeviceDescriptor::deviceLostUserdata);
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
        RenderPassDescriptor.def_readwrite("timestamp_writes", &wgpu::RenderPassDescriptor::timestampWrites);
        RenderPassDescriptor.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::RenderPassDescriptor obj;
            if (kwargs.contains("next_in_chain"))
            {
                auto value = kwargs["next_in_chain"].cast<const wgpu::ChainedStruct *>();
                obj.nextInChain = value;
            }
            if (kwargs.contains("label"))
            {
                auto _value = kwargs["label"].cast<std::string>();
                char* value = (char*)malloc(_value.size());
                strcpy(value, _value.c_str());
                obj.label = value;
            }
            if (kwargs.contains("color_attachment_count"))
            {
                auto value = kwargs["color_attachment_count"].cast<size_t>();
                obj.colorAttachmentCount = value;
            }
            if (kwargs.contains("color_attachments"))
            {
                auto value = kwargs["color_attachments"].cast<const wgpu::RenderPassColorAttachment *>();
                obj.colorAttachments = value;
            }
            if (kwargs.contains("depth_stencil_attachment"))
            {
                auto value = kwargs["depth_stencil_attachment"].cast<const wgpu::RenderPassDepthStencilAttachment *>();
                obj.depthStencilAttachment = value;
            }
            if (kwargs.contains("occlusion_query_set"))
            {
                auto value = kwargs["occlusion_query_set"].cast<wgpu::QuerySet>();
                obj.occlusionQuerySet = value;
            }
            if (kwargs.contains("timestamp_writes"))
            {
                auto value = kwargs["timestamp_writes"].cast<const wgpu::RenderPassTimestampWrites *>();
                obj.timestampWrites = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
    PYCLASS_END(_wgpu, wgpu::RenderPassDescriptor, RenderPassDescriptor)

    PYSUBCLASS_BEGIN(_wgpu, wgpu::RenderPassPixelLocalStorage, struct wgpu::ChainedStruct, RenderPassPixelLocalStorage)
        RenderPassPixelLocalStorage.def(py::init<>());
        RenderPassPixelLocalStorage.def_readwrite("total_pixel_local_storage_size", &wgpu::RenderPassPixelLocalStorage::totalPixelLocalStorageSize);
        RenderPassPixelLocalStorage.def_readwrite("storage_attachment_count", &wgpu::RenderPassPixelLocalStorage::storageAttachmentCount);
        RenderPassPixelLocalStorage.def_readwrite("storage_attachments", &wgpu::RenderPassPixelLocalStorage::storageAttachments);
    PYCLASS_END(_wgpu, wgpu::RenderPassPixelLocalStorage, RenderPassPixelLocalStorage)

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
        VertexState.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::VertexState obj;
            if (kwargs.contains("next_in_chain"))
            {
                auto value = kwargs["next_in_chain"].cast<const wgpu::ChainedStruct *>();
                obj.nextInChain = value;
            }
            if (kwargs.contains("module"))
            {
                auto value = kwargs["module"].cast<wgpu::ShaderModule>();
                obj.module = value;
            }
            if (kwargs.contains("entry_point"))
            {
                auto _value = kwargs["entry_point"].cast<std::string>();
                char* value = (char*)malloc(_value.size());
                strcpy(value, _value.c_str());
                obj.entryPoint = value;
            }
            if (kwargs.contains("constant_count"))
            {
                auto value = kwargs["constant_count"].cast<size_t>();
                obj.constantCount = value;
            }
            if (kwargs.contains("constants"))
            {
                auto value = kwargs["constants"].cast<const wgpu::ConstantEntry *>();
                obj.constants = value;
            }
            if (kwargs.contains("buffer_count"))
            {
                auto value = kwargs["buffer_count"].cast<size_t>();
                obj.bufferCount = value;
            }
            if (kwargs.contains("buffers"))
            {
                auto value = kwargs["buffers"].cast<const wgpu::VertexBufferLayout *>();
                obj.buffers = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
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
        FragmentState.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::FragmentState obj;
            if (kwargs.contains("next_in_chain"))
            {
                auto value = kwargs["next_in_chain"].cast<const wgpu::ChainedStruct *>();
                obj.nextInChain = value;
            }
            if (kwargs.contains("module"))
            {
                auto value = kwargs["module"].cast<wgpu::ShaderModule>();
                obj.module = value;
            }
            if (kwargs.contains("entry_point"))
            {
                auto _value = kwargs["entry_point"].cast<std::string>();
                char* value = (char*)malloc(_value.size());
                strcpy(value, _value.c_str());
                obj.entryPoint = value;
            }
            if (kwargs.contains("constant_count"))
            {
                auto value = kwargs["constant_count"].cast<size_t>();
                obj.constantCount = value;
            }
            if (kwargs.contains("constants"))
            {
                auto value = kwargs["constants"].cast<const wgpu::ConstantEntry *>();
                obj.constants = value;
            }
            if (kwargs.contains("target_count"))
            {
                auto value = kwargs["target_count"].cast<size_t>();
                obj.targetCount = value;
            }
            if (kwargs.contains("targets"))
            {
                auto value = kwargs["targets"].cast<const wgpu::ColorTargetState *>();
                obj.targets = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
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
        RenderPipelineDescriptor.def(py::init([](const py::kwargs& kwargs)
        {
            wgpu::RenderPipelineDescriptor obj;
            if (kwargs.contains("next_in_chain"))
            {
                auto value = kwargs["next_in_chain"].cast<const wgpu::ChainedStruct *>();
                obj.nextInChain = value;
            }
            if (kwargs.contains("label"))
            {
                auto _value = kwargs["label"].cast<std::string>();
                char* value = (char*)malloc(_value.size());
                strcpy(value, _value.c_str());
                obj.label = value;
            }
            if (kwargs.contains("layout"))
            {
                auto value = kwargs["layout"].cast<wgpu::PipelineLayout>();
                obj.layout = value;
            }
            if (kwargs.contains("vertex"))
            {
                auto value = kwargs["vertex"].cast<wgpu::VertexState>();
                obj.vertex = value;
            }
            if (kwargs.contains("primitive"))
            {
                auto value = kwargs["primitive"].cast<wgpu::PrimitiveState>();
                obj.primitive = value;
            }
            if (kwargs.contains("depth_stencil"))
            {
                auto value = kwargs["depth_stencil"].cast<const wgpu::DepthStencilState *>();
                obj.depthStencil = value;
            }
            if (kwargs.contains("multisample"))
            {
                auto value = kwargs["multisample"].cast<wgpu::MultisampleState>();
                obj.multisample = value;
            }
            if (kwargs.contains("fragment"))
            {
                auto value = kwargs["fragment"].cast<const wgpu::FragmentState *>();
                obj.fragment = value;
            }
            return obj;
        }), py::return_value_policy::automatic_reference);
    PYCLASS_END(_wgpu, wgpu::RenderPipelineDescriptor, RenderPipelineDescriptor)


}