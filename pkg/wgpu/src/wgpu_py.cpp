#include <dawn/webgpu_cpp.h>
//#include "wgpu.h"

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/wgpu/crunge-wgpu.h>
#include <crunge/wgpu/conversions.h>

namespace py = pybind11;

using namespace wgpu;

void init_wgpu(py::module &m, Registry &registry) {

py::enum_<RequestAdapterStatus>(m, "RequestAdapterStatus", py::arithmetic())
    .value("SUCCESS", RequestAdapterStatus::Success)    
    .value("INSTANCE_DROPPED", RequestAdapterStatus::InstanceDropped)    
    .value("UNAVAILABLE", RequestAdapterStatus::Unavailable)    
    .value("ERROR", RequestAdapterStatus::Error)    
    .value("UNKNOWN", RequestAdapterStatus::Unknown)    
;

py::enum_<AdapterType>(m, "AdapterType", py::arithmetic())
    .value("DISCRETE_GPU", AdapterType::DiscreteGPU)    
    .value("INTEGRATED_GPU", AdapterType::IntegratedGPU)    
    .value("CPU", AdapterType::CPU)    
    .value("UNKNOWN", AdapterType::Unknown)    
;

py::enum_<AddressMode>(m, "AddressMode", py::arithmetic())
    .value("UNDEFINED", AddressMode::Undefined)    
    .value("CLAMP_TO_EDGE", AddressMode::ClampToEdge)    
    .value("REPEAT", AddressMode::Repeat)    
    .value("MIRROR_REPEAT", AddressMode::MirrorRepeat)    
;

py::enum_<BackendType>(m, "BackendType", py::arithmetic())
    .value("UNDEFINED", BackendType::Undefined)    
    .value("NULL", BackendType::Null)    
    .value("WEB_GPU", BackendType::WebGPU)    
    .value("D3D11", BackendType::D3D11)    
    .value("D3D12", BackendType::D3D12)    
    .value("METAL", BackendType::Metal)    
    .value("VULKAN", BackendType::Vulkan)    
    .value("OPEN_GL", BackendType::OpenGL)    
    .value("OPEN_GLES", BackendType::OpenGLES)    
;

py::enum_<BufferBindingType>(m, "BufferBindingType", py::arithmetic())
    .value("UNDEFINED", BufferBindingType::Undefined)    
    .value("UNIFORM", BufferBindingType::Uniform)    
    .value("STORAGE", BufferBindingType::Storage)    
    .value("READ_ONLY_STORAGE", BufferBindingType::ReadOnlyStorage)    
;

py::enum_<SamplerBindingType>(m, "SamplerBindingType", py::arithmetic())
    .value("UNDEFINED", SamplerBindingType::Undefined)    
    .value("FILTERING", SamplerBindingType::Filtering)    
    .value("NON_FILTERING", SamplerBindingType::NonFiltering)    
    .value("COMPARISON", SamplerBindingType::Comparison)    
;

py::enum_<TextureSampleType>(m, "TextureSampleType", py::arithmetic())
    .value("UNDEFINED", TextureSampleType::Undefined)    
    .value("FLOAT", TextureSampleType::Float)    
    .value("UNFILTERABLE_FLOAT", TextureSampleType::UnfilterableFloat)    
    .value("DEPTH", TextureSampleType::Depth)    
    .value("SINT", TextureSampleType::Sint)    
    .value("UINT", TextureSampleType::Uint)    
;

py::enum_<StorageTextureAccess>(m, "StorageTextureAccess", py::arithmetic())
    .value("UNDEFINED", StorageTextureAccess::Undefined)    
    .value("WRITE_ONLY", StorageTextureAccess::WriteOnly)    
    .value("READ_ONLY", StorageTextureAccess::ReadOnly)    
    .value("READ_WRITE", StorageTextureAccess::ReadWrite)    
;

py::enum_<BlendFactor>(m, "BlendFactor", py::arithmetic())
    .value("UNDEFINED", BlendFactor::Undefined)    
    .value("ZERO", BlendFactor::Zero)    
    .value("ONE", BlendFactor::One)    
    .value("SRC", BlendFactor::Src)    
    .value("ONE_MINUS_SRC", BlendFactor::OneMinusSrc)    
    .value("SRC_ALPHA", BlendFactor::SrcAlpha)    
    .value("ONE_MINUS_SRC_ALPHA", BlendFactor::OneMinusSrcAlpha)    
    .value("DST", BlendFactor::Dst)    
    .value("ONE_MINUS_DST", BlendFactor::OneMinusDst)    
    .value("DST_ALPHA", BlendFactor::DstAlpha)    
    .value("ONE_MINUS_DST_ALPHA", BlendFactor::OneMinusDstAlpha)    
    .value("SRC_ALPHA_SATURATED", BlendFactor::SrcAlphaSaturated)    
    .value("CONSTANT", BlendFactor::Constant)    
    .value("ONE_MINUS_CONSTANT", BlendFactor::OneMinusConstant)    
    .value("SRC1", BlendFactor::Src1)    
    .value("ONE_MINUS_SRC1", BlendFactor::OneMinusSrc1)    
    .value("SRC1_ALPHA", BlendFactor::Src1Alpha)    
    .value("ONE_MINUS_SRC1_ALPHA", BlendFactor::OneMinusSrc1Alpha)    
;

py::enum_<BlendOperation>(m, "BlendOperation", py::arithmetic())
    .value("UNDEFINED", BlendOperation::Undefined)    
    .value("ADD", BlendOperation::Add)    
    .value("SUBTRACT", BlendOperation::Subtract)    
    .value("REVERSE_SUBTRACT", BlendOperation::ReverseSubtract)    
    .value("MIN", BlendOperation::Min)    
    .value("MAX", BlendOperation::Max)    
;

py::enum_<BufferMapAsyncStatus>(m, "BufferMapAsyncStatus", py::arithmetic())
    .value("SUCCESS", BufferMapAsyncStatus::Success)    
    .value("INSTANCE_DROPPED", BufferMapAsyncStatus::InstanceDropped)    
    .value("VALIDATION_ERROR", BufferMapAsyncStatus::ValidationError)    
    .value("UNKNOWN", BufferMapAsyncStatus::Unknown)    
    .value("DEVICE_LOST", BufferMapAsyncStatus::DeviceLost)    
    .value("DESTROYED_BEFORE_CALLBACK", BufferMapAsyncStatus::DestroyedBeforeCallback)    
    .value("UNMAPPED_BEFORE_CALLBACK", BufferMapAsyncStatus::UnmappedBeforeCallback)    
    .value("MAPPING_ALREADY_PENDING", BufferMapAsyncStatus::MappingAlreadyPending)    
    .value("OFFSET_OUT_OF_RANGE", BufferMapAsyncStatus::OffsetOutOfRange)    
    .value("SIZE_OUT_OF_RANGE", BufferMapAsyncStatus::SizeOutOfRange)    
;

py::enum_<MapAsyncStatus>(m, "MapAsyncStatus", py::arithmetic())
    .value("SUCCESS", MapAsyncStatus::Success)    
    .value("INSTANCE_DROPPED", MapAsyncStatus::InstanceDropped)    
    .value("ERROR", MapAsyncStatus::Error)    
    .value("ABORTED", MapAsyncStatus::Aborted)    
    .value("UNKNOWN", MapAsyncStatus::Unknown)    
;

py::enum_<BufferMapState>(m, "BufferMapState", py::arithmetic())
    .value("UNMAPPED", BufferMapState::Unmapped)    
    .value("PENDING", BufferMapState::Pending)    
    .value("MAPPED", BufferMapState::Mapped)    
;

py::enum_<CompareFunction>(m, "CompareFunction", py::arithmetic())
    .value("UNDEFINED", CompareFunction::Undefined)    
    .value("NEVER", CompareFunction::Never)    
    .value("LESS", CompareFunction::Less)    
    .value("EQUAL", CompareFunction::Equal)    
    .value("LESS_EQUAL", CompareFunction::LessEqual)    
    .value("GREATER", CompareFunction::Greater)    
    .value("NOT_EQUAL", CompareFunction::NotEqual)    
    .value("GREATER_EQUAL", CompareFunction::GreaterEqual)    
    .value("ALWAYS", CompareFunction::Always)    
;

py::enum_<CompilationInfoRequestStatus>(m, "CompilationInfoRequestStatus", py::arithmetic())
    .value("SUCCESS", CompilationInfoRequestStatus::Success)    
    .value("INSTANCE_DROPPED", CompilationInfoRequestStatus::InstanceDropped)    
    .value("ERROR", CompilationInfoRequestStatus::Error)    
    .value("DEVICE_LOST", CompilationInfoRequestStatus::DeviceLost)    
    .value("UNKNOWN", CompilationInfoRequestStatus::Unknown)    
;

py::enum_<CompilationMessageType>(m, "CompilationMessageType", py::arithmetic())
    .value("ERROR", CompilationMessageType::Error)    
    .value("WARNING", CompilationMessageType::Warning)    
    .value("INFO", CompilationMessageType::Info)    
;

py::enum_<CompositeAlphaMode>(m, "CompositeAlphaMode", py::arithmetic())
    .value("AUTO", CompositeAlphaMode::Auto)    
    .value("OPAQUE", CompositeAlphaMode::Opaque)    
    .value("PREMULTIPLIED", CompositeAlphaMode::Premultiplied)    
    .value("UNPREMULTIPLIED", CompositeAlphaMode::Unpremultiplied)    
    .value("INHERIT", CompositeAlphaMode::Inherit)    
;

py::enum_<AlphaMode>(m, "AlphaMode", py::arithmetic())
    .value("OPAQUE", AlphaMode::Opaque)    
    .value("PREMULTIPLIED", AlphaMode::Premultiplied)    
    .value("UNPREMULTIPLIED", AlphaMode::Unpremultiplied)    
;

py::enum_<CreatePipelineAsyncStatus>(m, "CreatePipelineAsyncStatus", py::arithmetic())
    .value("SUCCESS", CreatePipelineAsyncStatus::Success)    
    .value("INSTANCE_DROPPED", CreatePipelineAsyncStatus::InstanceDropped)    
    .value("VALIDATION_ERROR", CreatePipelineAsyncStatus::ValidationError)    
    .value("INTERNAL_ERROR", CreatePipelineAsyncStatus::InternalError)    
    .value("DEVICE_LOST", CreatePipelineAsyncStatus::DeviceLost)    
    .value("DEVICE_DESTROYED", CreatePipelineAsyncStatus::DeviceDestroyed)    
    .value("UNKNOWN", CreatePipelineAsyncStatus::Unknown)    
;

py::enum_<CullMode>(m, "CullMode", py::arithmetic())
    .value("UNDEFINED", CullMode::Undefined)    
    .value("NONE", CullMode::None)    
    .value("FRONT", CullMode::Front)    
    .value("BACK", CullMode::Back)    
;

py::enum_<DeviceLostReason>(m, "DeviceLostReason", py::arithmetic())
    .value("UNKNOWN", DeviceLostReason::Unknown)    
    .value("DESTROYED", DeviceLostReason::Destroyed)    
    .value("INSTANCE_DROPPED", DeviceLostReason::InstanceDropped)    
    .value("FAILED_CREATION", DeviceLostReason::FailedCreation)    
;

py::enum_<PopErrorScopeStatus>(m, "PopErrorScopeStatus", py::arithmetic())
    .value("SUCCESS", PopErrorScopeStatus::Success)    
    .value("INSTANCE_DROPPED", PopErrorScopeStatus::InstanceDropped)    
;

py::enum_<ErrorFilter>(m, "ErrorFilter", py::arithmetic())
    .value("VALIDATION", ErrorFilter::Validation)    
    .value("OUT_OF_MEMORY", ErrorFilter::OutOfMemory)    
    .value("INTERNAL", ErrorFilter::Internal)    
;

py::enum_<ErrorType>(m, "ErrorType", py::arithmetic())
    .value("NO_ERROR", ErrorType::NoError)    
    .value("VALIDATION", ErrorType::Validation)    
    .value("OUT_OF_MEMORY", ErrorType::OutOfMemory)    
    .value("INTERNAL", ErrorType::Internal)    
    .value("UNKNOWN", ErrorType::Unknown)    
    .value("DEVICE_LOST", ErrorType::DeviceLost)    
;

py::enum_<LoggingType>(m, "LoggingType", py::arithmetic())
    .value("VERBOSE", LoggingType::Verbose)    
    .value("INFO", LoggingType::Info)    
    .value("WARNING", LoggingType::Warning)    
    .value("ERROR", LoggingType::Error)    
;

py::enum_<ExternalTextureRotation>(m, "ExternalTextureRotation", py::arithmetic())
    .value("ROTATE0_DEGREES", ExternalTextureRotation::Rotate0Degrees)    
    .value("ROTATE90_DEGREES", ExternalTextureRotation::Rotate90Degrees)    
    .value("ROTATE180_DEGREES", ExternalTextureRotation::Rotate180Degrees)    
    .value("ROTATE270_DEGREES", ExternalTextureRotation::Rotate270Degrees)    
;

py::enum_<Status>(m, "Status", py::arithmetic())
    .value("SUCCESS", Status::Success)    
    .value("ERROR", Status::Error)    
;

py::enum_<SharedFenceType>(m, "SharedFenceType", py::arithmetic())
    .value("VK_SEMAPHORE_OPAQUE_FD", SharedFenceType::VkSemaphoreOpaqueFD)    
    .value("VK_SEMAPHORE_SYNC_FD", SharedFenceType::VkSemaphoreSyncFD)    
    .value("VK_SEMAPHORE_ZIRCON_HANDLE", SharedFenceType::VkSemaphoreZirconHandle)    
    .value("DXGI_SHARED_HANDLE", SharedFenceType::DXGISharedHandle)    
    .value("MTL_SHARED_EVENT", SharedFenceType::MTLSharedEvent)    
;

py::enum_<FeatureName>(m, "FeatureName", py::arithmetic())
    .value("DEPTH_CLIP_CONTROL", FeatureName::DepthClipControl)    
    .value("DEPTH32_FLOAT_STENCIL8", FeatureName::Depth32FloatStencil8)    
    .value("TIMESTAMP_QUERY", FeatureName::TimestampQuery)    
    .value("TEXTURE_COMPRESSION_BC", FeatureName::TextureCompressionBC)    
    .value("TEXTURE_COMPRESSION_ETC2", FeatureName::TextureCompressionETC2)    
    .value("TEXTURE_COMPRESSION_ASTC", FeatureName::TextureCompressionASTC)    
    .value("INDIRECT_FIRST_INSTANCE", FeatureName::IndirectFirstInstance)    
    .value("SHADER_F16", FeatureName::ShaderF16)    
    .value("RG11B10_UFLOAT_RENDERABLE", FeatureName::RG11B10UfloatRenderable)    
    .value("BGRA8_UNORM_STORAGE", FeatureName::BGRA8UnormStorage)    
    .value("FLOAT32_FILTERABLE", FeatureName::Float32Filterable)    
    .value("SUBGROUPS", FeatureName::Subgroups)    
    .value("SUBGROUPS_F16", FeatureName::SubgroupsF16)    
    .value("DAWN_INTERNAL_USAGES", FeatureName::DawnInternalUsages)    
    .value("DAWN_MULTI_PLANAR_FORMATS", FeatureName::DawnMultiPlanarFormats)    
    .value("DAWN_NATIVE", FeatureName::DawnNative)    
    .value("CHROMIUM_EXPERIMENTAL_TIMESTAMP_QUERY_INSIDE_PASSES", FeatureName::ChromiumExperimentalTimestampQueryInsidePasses)    
    .value("IMPLICIT_DEVICE_SYNCHRONIZATION", FeatureName::ImplicitDeviceSynchronization)    
    .value("SURFACE_CAPABILITIES", FeatureName::SurfaceCapabilities)    
    .value("TRANSIENT_ATTACHMENTS", FeatureName::TransientAttachments)    
    .value("MSAA_RENDER_TO_SINGLE_SAMPLED", FeatureName::MSAARenderToSingleSampled)    
    .value("DUAL_SOURCE_BLENDING", FeatureName::DualSourceBlending)    
    .value("D3D11_MULTITHREAD_PROTECTED", FeatureName::D3D11MultithreadProtected)    
    .value("ANGLE_TEXTURE_SHARING", FeatureName::ANGLETextureSharing)    
    .value("CHROMIUM_EXPERIMENTAL_SUBGROUPS", FeatureName::ChromiumExperimentalSubgroups)    
    .value("CHROMIUM_EXPERIMENTAL_SUBGROUP_UNIFORM_CONTROL_FLOW", FeatureName::ChromiumExperimentalSubgroupUniformControlFlow)    
    .value("PIXEL_LOCAL_STORAGE_COHERENT", FeatureName::PixelLocalStorageCoherent)    
    .value("PIXEL_LOCAL_STORAGE_NON_COHERENT", FeatureName::PixelLocalStorageNonCoherent)    
    .value("UNORM16_TEXTURE_FORMATS", FeatureName::Unorm16TextureFormats)    
    .value("SNORM16_TEXTURE_FORMATS", FeatureName::Snorm16TextureFormats)    
    .value("MULTI_PLANAR_FORMAT_EXTENDED_USAGES", FeatureName::MultiPlanarFormatExtendedUsages)    
    .value("MULTI_PLANAR_FORMAT_P010", FeatureName::MultiPlanarFormatP010)    
    .value("HOST_MAPPED_POINTER", FeatureName::HostMappedPointer)    
    .value("MULTI_PLANAR_RENDER_TARGETS", FeatureName::MultiPlanarRenderTargets)    
    .value("MULTI_PLANAR_FORMAT_NV12A", FeatureName::MultiPlanarFormatNv12a)    
    .value("FRAMEBUFFER_FETCH", FeatureName::FramebufferFetch)    
    .value("BUFFER_MAP_EXTENDED_USAGES", FeatureName::BufferMapExtendedUsages)    
    .value("ADAPTER_PROPERTIES_MEMORY_HEAPS", FeatureName::AdapterPropertiesMemoryHeaps)    
    .value("ADAPTER_PROPERTIES_D3D", FeatureName::AdapterPropertiesD3D)    
    .value("ADAPTER_PROPERTIES_VK", FeatureName::AdapterPropertiesVk)    
    .value("R8_UNORM_STORAGE", FeatureName::R8UnormStorage)    
    .value("FORMAT_CAPABILITIES", FeatureName::FormatCapabilities)    
    .value("DRM_FORMAT_CAPABILITIES", FeatureName::DrmFormatCapabilities)    
    .value("NORM16_TEXTURE_FORMATS", FeatureName::Norm16TextureFormats)    
    .value("MULTI_PLANAR_FORMAT_NV16", FeatureName::MultiPlanarFormatNv16)    
    .value("MULTI_PLANAR_FORMAT_NV24", FeatureName::MultiPlanarFormatNv24)    
    .value("MULTI_PLANAR_FORMAT_P210", FeatureName::MultiPlanarFormatP210)    
    .value("MULTI_PLANAR_FORMAT_P410", FeatureName::MultiPlanarFormatP410)    
    .value("SHARED_TEXTURE_MEMORY_VK_DEDICATED_ALLOCATION", FeatureName::SharedTextureMemoryVkDedicatedAllocation)    
    .value("SHARED_TEXTURE_MEMORY_A_HARDWARE_BUFFER", FeatureName::SharedTextureMemoryAHardwareBuffer)    
    .value("SHARED_TEXTURE_MEMORY_DMA_BUF", FeatureName::SharedTextureMemoryDmaBuf)    
    .value("SHARED_TEXTURE_MEMORY_OPAQUE_FD", FeatureName::SharedTextureMemoryOpaqueFD)    
    .value("SHARED_TEXTURE_MEMORY_ZIRCON_HANDLE", FeatureName::SharedTextureMemoryZirconHandle)    
    .value("SHARED_TEXTURE_MEMORY_DXGI_SHARED_HANDLE", FeatureName::SharedTextureMemoryDXGISharedHandle)    
    .value("SHARED_TEXTURE_MEMORY_D3D11_TEXTURE2D", FeatureName::SharedTextureMemoryD3D11Texture2D)    
    .value("SHARED_TEXTURE_MEMORY_IO_SURFACE", FeatureName::SharedTextureMemoryIOSurface)    
    .value("SHARED_TEXTURE_MEMORY_EGL_IMAGE", FeatureName::SharedTextureMemoryEGLImage)    
    .value("SHARED_FENCE_VK_SEMAPHORE_OPAQUE_FD", FeatureName::SharedFenceVkSemaphoreOpaqueFD)    
    .value("SHARED_FENCE_VK_SEMAPHORE_SYNC_FD", FeatureName::SharedFenceVkSemaphoreSyncFD)    
    .value("SHARED_FENCE_VK_SEMAPHORE_ZIRCON_HANDLE", FeatureName::SharedFenceVkSemaphoreZirconHandle)    
    .value("SHARED_FENCE_DXGI_SHARED_HANDLE", FeatureName::SharedFenceDXGISharedHandle)    
    .value("SHARED_FENCE_MTL_SHARED_EVENT", FeatureName::SharedFenceMTLSharedEvent)    
    .value("SHARED_BUFFER_MEMORY_D3D12_RESOURCE", FeatureName::SharedBufferMemoryD3D12Resource)    
    .value("STATIC_SAMPLERS", FeatureName::StaticSamplers)    
    .value("Y_CB_CR_VULKAN_SAMPLERS", FeatureName::YCbCrVulkanSamplers)    
    .value("SHADER_MODULE_COMPILATION_OPTIONS", FeatureName::ShaderModuleCompilationOptions)    
    .value("DAWN_LOAD_RESOLVE_TEXTURE", FeatureName::DawnLoadResolveTexture)    
;

py::enum_<FilterMode>(m, "FilterMode", py::arithmetic())
    .value("UNDEFINED", FilterMode::Undefined)    
    .value("NEAREST", FilterMode::Nearest)    
    .value("LINEAR", FilterMode::Linear)    
;

py::enum_<FrontFace>(m, "FrontFace", py::arithmetic())
    .value("UNDEFINED", FrontFace::Undefined)    
    .value("CCW", FrontFace::CCW)    
    .value("CW", FrontFace::CW)    
;

py::enum_<IndexFormat>(m, "IndexFormat", py::arithmetic())
    .value("UNDEFINED", IndexFormat::Undefined)    
    .value("UINT16", IndexFormat::Uint16)    
    .value("UINT32", IndexFormat::Uint32)    
;

py::enum_<CallbackMode>(m, "CallbackMode", py::arithmetic())
    .value("WAIT_ANY_ONLY", CallbackMode::WaitAnyOnly)    
    .value("ALLOW_PROCESS_EVENTS", CallbackMode::AllowProcessEvents)    
    .value("ALLOW_SPONTANEOUS", CallbackMode::AllowSpontaneous)    
;

py::enum_<WaitStatus>(m, "WaitStatus", py::arithmetic())
    .value("SUCCESS", WaitStatus::Success)    
    .value("TIMED_OUT", WaitStatus::TimedOut)    
    .value("UNSUPPORTED_TIMEOUT", WaitStatus::UnsupportedTimeout)    
    .value("UNSUPPORTED_COUNT", WaitStatus::UnsupportedCount)    
    .value("UNSUPPORTED_MIXED_SOURCES", WaitStatus::UnsupportedMixedSources)    
    .value("UNKNOWN", WaitStatus::Unknown)    
;

py::enum_<VertexStepMode>(m, "VertexStepMode", py::arithmetic())
    .value("UNDEFINED", VertexStepMode::Undefined)    
    .value("VERTEX_BUFFER_NOT_USED", VertexStepMode::VertexBufferNotUsed)    
    .value("VERTEX", VertexStepMode::Vertex)    
    .value("INSTANCE", VertexStepMode::Instance)    
;

py::enum_<LoadOp>(m, "LoadOp", py::arithmetic())
    .value("UNDEFINED", LoadOp::Undefined)    
    .value("CLEAR", LoadOp::Clear)    
    .value("LOAD", LoadOp::Load)    
    .value("EXPAND_RESOLVE_TEXTURE", LoadOp::ExpandResolveTexture)    
;

py::enum_<MipmapFilterMode>(m, "MipmapFilterMode", py::arithmetic())
    .value("UNDEFINED", MipmapFilterMode::Undefined)    
    .value("NEAREST", MipmapFilterMode::Nearest)    
    .value("LINEAR", MipmapFilterMode::Linear)    
;

py::enum_<StoreOp>(m, "StoreOp", py::arithmetic())
    .value("UNDEFINED", StoreOp::Undefined)    
    .value("STORE", StoreOp::Store)    
    .value("DISCARD", StoreOp::Discard)    
;

py::enum_<PowerPreference>(m, "PowerPreference", py::arithmetic())
    .value("UNDEFINED", PowerPreference::Undefined)    
    .value("LOW_POWER", PowerPreference::LowPower)    
    .value("HIGH_PERFORMANCE", PowerPreference::HighPerformance)    
;

py::enum_<PresentMode>(m, "PresentMode", py::arithmetic())
    .value("FIFO", PresentMode::Fifo)    
    .value("FIFO_RELAXED", PresentMode::FifoRelaxed)    
    .value("IMMEDIATE", PresentMode::Immediate)    
    .value("MAILBOX", PresentMode::Mailbox)    
;

py::enum_<PrimitiveTopology>(m, "PrimitiveTopology", py::arithmetic())
    .value("UNDEFINED", PrimitiveTopology::Undefined)    
    .value("POINT_LIST", PrimitiveTopology::PointList)    
    .value("LINE_LIST", PrimitiveTopology::LineList)    
    .value("LINE_STRIP", PrimitiveTopology::LineStrip)    
    .value("TRIANGLE_LIST", PrimitiveTopology::TriangleList)    
    .value("TRIANGLE_STRIP", PrimitiveTopology::TriangleStrip)    
;

py::enum_<QueryType>(m, "QueryType", py::arithmetic())
    .value("OCCLUSION", QueryType::Occlusion)    
    .value("TIMESTAMP", QueryType::Timestamp)    
;

py::enum_<QueueWorkDoneStatus>(m, "QueueWorkDoneStatus", py::arithmetic())
    .value("SUCCESS", QueueWorkDoneStatus::Success)    
    .value("INSTANCE_DROPPED", QueueWorkDoneStatus::InstanceDropped)    
    .value("ERROR", QueueWorkDoneStatus::Error)    
    .value("UNKNOWN", QueueWorkDoneStatus::Unknown)    
    .value("DEVICE_LOST", QueueWorkDoneStatus::DeviceLost)    
;

py::enum_<RequestDeviceStatus>(m, "RequestDeviceStatus", py::arithmetic())
    .value("SUCCESS", RequestDeviceStatus::Success)    
    .value("INSTANCE_DROPPED", RequestDeviceStatus::InstanceDropped)    
    .value("ERROR", RequestDeviceStatus::Error)    
    .value("UNKNOWN", RequestDeviceStatus::Unknown)    
;

py::enum_<StencilOperation>(m, "StencilOperation", py::arithmetic())
    .value("UNDEFINED", StencilOperation::Undefined)    
    .value("KEEP", StencilOperation::Keep)    
    .value("ZERO", StencilOperation::Zero)    
    .value("REPLACE", StencilOperation::Replace)    
    .value("INVERT", StencilOperation::Invert)    
    .value("INCREMENT_CLAMP", StencilOperation::IncrementClamp)    
    .value("DECREMENT_CLAMP", StencilOperation::DecrementClamp)    
    .value("INCREMENT_WRAP", StencilOperation::IncrementWrap)    
    .value("DECREMENT_WRAP", StencilOperation::DecrementWrap)    
;

py::enum_<SType>(m, "SType", py::arithmetic())
    .value("SHADER_MODULE_SPIRV_DESCRIPTOR", SType::ShaderModuleSPIRVDescriptor)    
    .value("SHADER_MODULE_WGSL_DESCRIPTOR", SType::ShaderModuleWGSLDescriptor)    
    .value("PRIMITIVE_DEPTH_CLIP_CONTROL", SType::PrimitiveDepthClipControl)    
    .value("RENDER_PASS_DESCRIPTOR_MAX_DRAW_COUNT", SType::RenderPassDescriptorMaxDrawCount)    
    .value("TEXTURE_BINDING_VIEW_DIMENSION_DESCRIPTOR", SType::TextureBindingViewDimensionDescriptor)    
    .value("SURFACE_DESCRIPTOR_FROM_CANVAS_HTML_SELECTOR", SType::SurfaceDescriptorFromCanvasHTMLSelector)    
    .value("SURFACE_DESCRIPTOR_FROM_METAL_LAYER", SType::SurfaceDescriptorFromMetalLayer)    
    .value("SURFACE_DESCRIPTOR_FROM_WINDOWS_HWND", SType::SurfaceDescriptorFromWindowsHWND)    
    .value("SURFACE_DESCRIPTOR_FROM_XLIB_WINDOW", SType::SurfaceDescriptorFromXlibWindow)    
    .value("SURFACE_DESCRIPTOR_FROM_WAYLAND_SURFACE", SType::SurfaceDescriptorFromWaylandSurface)    
    .value("SURFACE_DESCRIPTOR_FROM_ANDROID_NATIVE_WINDOW", SType::SurfaceDescriptorFromAndroidNativeWindow)    
    .value("SURFACE_DESCRIPTOR_FROM_XCB_WINDOW", SType::SurfaceDescriptorFromXcbWindow)    
    .value("SURFACE_DESCRIPTOR_FROM_WINDOWS_CORE_WINDOW", SType::SurfaceDescriptorFromWindowsCoreWindow)    
    .value("EXTERNAL_TEXTURE_BINDING_ENTRY", SType::ExternalTextureBindingEntry)    
    .value("EXTERNAL_TEXTURE_BINDING_LAYOUT", SType::ExternalTextureBindingLayout)    
    .value("SURFACE_DESCRIPTOR_FROM_WINDOWS_SWAP_CHAIN_PANEL", SType::SurfaceDescriptorFromWindowsSwapChainPanel)    
    .value("DEPTH_STENCIL_STATE_DEPTH_WRITE_DEFINED_DAWN", SType::DepthStencilStateDepthWriteDefinedDawn)    
    .value("DAWN_TEXTURE_INTERNAL_USAGE_DESCRIPTOR", SType::DawnTextureInternalUsageDescriptor)    
    .value("DAWN_ENCODER_INTERNAL_USAGE_DESCRIPTOR", SType::DawnEncoderInternalUsageDescriptor)    
    .value("DAWN_INSTANCE_DESCRIPTOR", SType::DawnInstanceDescriptor)    
    .value("DAWN_CACHE_DEVICE_DESCRIPTOR", SType::DawnCacheDeviceDescriptor)    
    .value("DAWN_ADAPTER_PROPERTIES_POWER_PREFERENCE", SType::DawnAdapterPropertiesPowerPreference)    
    .value("DAWN_BUFFER_DESCRIPTOR_ERROR_INFO_FROM_WIRE_CLIENT", SType::DawnBufferDescriptorErrorInfoFromWireClient)    
    .value("DAWN_TOGGLES_DESCRIPTOR", SType::DawnTogglesDescriptor)    
    .value("DAWN_SHADER_MODULE_SPIRV_OPTIONS_DESCRIPTOR", SType::DawnShaderModuleSPIRVOptionsDescriptor)    
    .value("REQUEST_ADAPTER_OPTIONS_LUID", SType::RequestAdapterOptionsLUID)    
    .value("REQUEST_ADAPTER_OPTIONS_GET_GL_PROC", SType::RequestAdapterOptionsGetGLProc)    
    .value("REQUEST_ADAPTER_OPTIONS_D3D11_DEVICE", SType::RequestAdapterOptionsD3D11Device)    
    .value("DAWN_RENDER_PASS_COLOR_ATTACHMENT_RENDER_TO_SINGLE_SAMPLED", SType::DawnRenderPassColorAttachmentRenderToSingleSampled)    
    .value("RENDER_PASS_PIXEL_LOCAL_STORAGE", SType::RenderPassPixelLocalStorage)    
    .value("PIPELINE_LAYOUT_PIXEL_LOCAL_STORAGE", SType::PipelineLayoutPixelLocalStorage)    
    .value("BUFFER_HOST_MAPPED_POINTER", SType::BufferHostMappedPointer)    
    .value("DAWN_EXPERIMENTAL_SUBGROUP_LIMITS", SType::DawnExperimentalSubgroupLimits)    
    .value("ADAPTER_PROPERTIES_MEMORY_HEAPS", SType::AdapterPropertiesMemoryHeaps)    
    .value("ADAPTER_PROPERTIES_D3D", SType::AdapterPropertiesD3D)    
    .value("ADAPTER_PROPERTIES_VK", SType::AdapterPropertiesVk)    
    .value("DAWN_COMPUTE_PIPELINE_FULL_SUBGROUPS", SType::DawnComputePipelineFullSubgroups)    
    .value("DAWN_WIRE_WGSL_CONTROL", SType::DawnWireWGSLControl)    
    .value("DAWN_WGSL_BLOCKLIST", SType::DawnWGSLBlocklist)    
    .value("DRM_FORMAT_CAPABILITIES", SType::DrmFormatCapabilities)    
    .value("SHADER_MODULE_COMPILATION_OPTIONS", SType::ShaderModuleCompilationOptions)    
    .value("COLOR_TARGET_STATE_EXPAND_RESOLVE_TEXTURE_DAWN", SType::ColorTargetStateExpandResolveTextureDawn)    
    .value("SHARED_TEXTURE_MEMORY_VK_DEDICATED_ALLOCATION_DESCRIPTOR", SType::SharedTextureMemoryVkDedicatedAllocationDescriptor)    
    .value("SHARED_TEXTURE_MEMORY_A_HARDWARE_BUFFER_DESCRIPTOR", SType::SharedTextureMemoryAHardwareBufferDescriptor)    
    .value("SHARED_TEXTURE_MEMORY_DMA_BUF_DESCRIPTOR", SType::SharedTextureMemoryDmaBufDescriptor)    
    .value("SHARED_TEXTURE_MEMORY_OPAQUE_FD_DESCRIPTOR", SType::SharedTextureMemoryOpaqueFDDescriptor)    
    .value("SHARED_TEXTURE_MEMORY_ZIRCON_HANDLE_DESCRIPTOR", SType::SharedTextureMemoryZirconHandleDescriptor)    
    .value("SHARED_TEXTURE_MEMORY_DXGI_SHARED_HANDLE_DESCRIPTOR", SType::SharedTextureMemoryDXGISharedHandleDescriptor)    
    .value("SHARED_TEXTURE_MEMORY_D3D11_TEXTURE2D_DESCRIPTOR", SType::SharedTextureMemoryD3D11Texture2DDescriptor)    
    .value("SHARED_TEXTURE_MEMORY_IO_SURFACE_DESCRIPTOR", SType::SharedTextureMemoryIOSurfaceDescriptor)    
    .value("SHARED_TEXTURE_MEMORY_EGL_IMAGE_DESCRIPTOR", SType::SharedTextureMemoryEGLImageDescriptor)    
    .value("SHARED_TEXTURE_MEMORY_INITIALIZED_BEGIN_STATE", SType::SharedTextureMemoryInitializedBeginState)    
    .value("SHARED_TEXTURE_MEMORY_INITIALIZED_END_STATE", SType::SharedTextureMemoryInitializedEndState)    
    .value("SHARED_TEXTURE_MEMORY_VK_IMAGE_LAYOUT_BEGIN_STATE", SType::SharedTextureMemoryVkImageLayoutBeginState)    
    .value("SHARED_TEXTURE_MEMORY_VK_IMAGE_LAYOUT_END_STATE", SType::SharedTextureMemoryVkImageLayoutEndState)    
    .value("SHARED_TEXTURE_MEMORY_D3D_SWAPCHAIN_BEGIN_STATE", SType::SharedTextureMemoryD3DSwapchainBeginState)    
    .value("SHARED_FENCE_VK_SEMAPHORE_OPAQUE_FD_DESCRIPTOR", SType::SharedFenceVkSemaphoreOpaqueFDDescriptor)    
    .value("SHARED_FENCE_VK_SEMAPHORE_OPAQUE_FD_EXPORT_INFO", SType::SharedFenceVkSemaphoreOpaqueFDExportInfo)    
    .value("SHARED_FENCE_VK_SEMAPHORE_SYNC_FD_DESCRIPTOR", SType::SharedFenceVkSemaphoreSyncFDDescriptor)    
    .value("SHARED_FENCE_VK_SEMAPHORE_SYNC_FD_EXPORT_INFO", SType::SharedFenceVkSemaphoreSyncFDExportInfo)    
    .value("SHARED_FENCE_VK_SEMAPHORE_ZIRCON_HANDLE_DESCRIPTOR", SType::SharedFenceVkSemaphoreZirconHandleDescriptor)    
    .value("SHARED_FENCE_VK_SEMAPHORE_ZIRCON_HANDLE_EXPORT_INFO", SType::SharedFenceVkSemaphoreZirconHandleExportInfo)    
    .value("SHARED_FENCE_DXGI_SHARED_HANDLE_DESCRIPTOR", SType::SharedFenceDXGISharedHandleDescriptor)    
    .value("SHARED_FENCE_DXGI_SHARED_HANDLE_EXPORT_INFO", SType::SharedFenceDXGISharedHandleExportInfo)    
    .value("SHARED_FENCE_MTL_SHARED_EVENT_DESCRIPTOR", SType::SharedFenceMTLSharedEventDescriptor)    
    .value("SHARED_FENCE_MTL_SHARED_EVENT_EXPORT_INFO", SType::SharedFenceMTLSharedEventExportInfo)    
    .value("SHARED_BUFFER_MEMORY_D3D12_RESOURCE_DESCRIPTOR", SType::SharedBufferMemoryD3D12ResourceDescriptor)    
    .value("STATIC_SAMPLER_BINDING_LAYOUT", SType::StaticSamplerBindingLayout)    
    .value("Y_CB_CR_VK_DESCRIPTOR", SType::YCbCrVkDescriptor)    
    .value("SHARED_TEXTURE_MEMORY_A_HARDWARE_BUFFER_PROPERTIES", SType::SharedTextureMemoryAHardwareBufferProperties)    
    .value("A_HARDWARE_BUFFER_PROPERTIES", SType::AHardwareBufferProperties)    
;

py::enum_<SurfaceGetCurrentTextureStatus>(m, "SurfaceGetCurrentTextureStatus", py::arithmetic())
    .value("SUCCESS", SurfaceGetCurrentTextureStatus::Success)    
    .value("TIMEOUT", SurfaceGetCurrentTextureStatus::Timeout)    
    .value("OUTDATED", SurfaceGetCurrentTextureStatus::Outdated)    
    .value("LOST", SurfaceGetCurrentTextureStatus::Lost)    
    .value("OUT_OF_MEMORY", SurfaceGetCurrentTextureStatus::OutOfMemory)    
    .value("DEVICE_LOST", SurfaceGetCurrentTextureStatus::DeviceLost)    
    .value("ERROR", SurfaceGetCurrentTextureStatus::Error)    
;

py::enum_<TextureAspect>(m, "TextureAspect", py::arithmetic())
    .value("UNDEFINED", TextureAspect::Undefined)    
    .value("ALL", TextureAspect::All)    
    .value("STENCIL_ONLY", TextureAspect::StencilOnly)    
    .value("DEPTH_ONLY", TextureAspect::DepthOnly)    
    .value("PLANE0_ONLY", TextureAspect::Plane0Only)    
    .value("PLANE1_ONLY", TextureAspect::Plane1Only)    
    .value("PLANE2_ONLY", TextureAspect::Plane2Only)    
;

py::enum_<TextureDimension>(m, "TextureDimension", py::arithmetic())
    .value("UNDEFINED", TextureDimension::Undefined)    
    .value("E1D", TextureDimension::e1D)    
    .value("E2D", TextureDimension::e2D)    
    .value("E3D", TextureDimension::e3D)    
;

py::enum_<TextureFormat>(m, "TextureFormat", py::arithmetic())
    .value("UNDEFINED", TextureFormat::Undefined)    
    .value("R8_UNORM", TextureFormat::R8Unorm)    
    .value("R8_SNORM", TextureFormat::R8Snorm)    
    .value("R8_UINT", TextureFormat::R8Uint)    
    .value("R8_SINT", TextureFormat::R8Sint)    
    .value("R16_UINT", TextureFormat::R16Uint)    
    .value("R16_SINT", TextureFormat::R16Sint)    
    .value("R16_FLOAT", TextureFormat::R16Float)    
    .value("RG8_UNORM", TextureFormat::RG8Unorm)    
    .value("RG8_SNORM", TextureFormat::RG8Snorm)    
    .value("RG8_UINT", TextureFormat::RG8Uint)    
    .value("RG8_SINT", TextureFormat::RG8Sint)    
    .value("R32_FLOAT", TextureFormat::R32Float)    
    .value("R32_UINT", TextureFormat::R32Uint)    
    .value("R32_SINT", TextureFormat::R32Sint)    
    .value("RG16_UINT", TextureFormat::RG16Uint)    
    .value("RG16_SINT", TextureFormat::RG16Sint)    
    .value("RG16_FLOAT", TextureFormat::RG16Float)    
    .value("RGBA8_UNORM", TextureFormat::RGBA8Unorm)    
    .value("RGBA8_UNORM_SRGB", TextureFormat::RGBA8UnormSrgb)    
    .value("RGBA8_SNORM", TextureFormat::RGBA8Snorm)    
    .value("RGBA8_UINT", TextureFormat::RGBA8Uint)    
    .value("RGBA8_SINT", TextureFormat::RGBA8Sint)    
    .value("BGRA8_UNORM", TextureFormat::BGRA8Unorm)    
    .value("BGRA8_UNORM_SRGB", TextureFormat::BGRA8UnormSrgb)    
    .value("RGB10A2_UINT", TextureFormat::RGB10A2Uint)    
    .value("RGB10A2_UNORM", TextureFormat::RGB10A2Unorm)    
    .value("RG11B10_UFLOAT", TextureFormat::RG11B10Ufloat)    
    .value("RGB9E5_UFLOAT", TextureFormat::RGB9E5Ufloat)    
    .value("RG32_FLOAT", TextureFormat::RG32Float)    
    .value("RG32_UINT", TextureFormat::RG32Uint)    
    .value("RG32_SINT", TextureFormat::RG32Sint)    
    .value("RGBA16_UINT", TextureFormat::RGBA16Uint)    
    .value("RGBA16_SINT", TextureFormat::RGBA16Sint)    
    .value("RGBA16_FLOAT", TextureFormat::RGBA16Float)    
    .value("RGBA32_FLOAT", TextureFormat::RGBA32Float)    
    .value("RGBA32_UINT", TextureFormat::RGBA32Uint)    
    .value("RGBA32_SINT", TextureFormat::RGBA32Sint)    
    .value("STENCIL8", TextureFormat::Stencil8)    
    .value("DEPTH16_UNORM", TextureFormat::Depth16Unorm)    
    .value("DEPTH24_PLUS", TextureFormat::Depth24Plus)    
    .value("DEPTH24_PLUS_STENCIL8", TextureFormat::Depth24PlusStencil8)    
    .value("DEPTH32_FLOAT", TextureFormat::Depth32Float)    
    .value("DEPTH32_FLOAT_STENCIL8", TextureFormat::Depth32FloatStencil8)    
    .value("BC1RGBA_UNORM", TextureFormat::BC1RGBAUnorm)    
    .value("BC1RGBA_UNORM_SRGB", TextureFormat::BC1RGBAUnormSrgb)    
    .value("BC2RGBA_UNORM", TextureFormat::BC2RGBAUnorm)    
    .value("BC2RGBA_UNORM_SRGB", TextureFormat::BC2RGBAUnormSrgb)    
    .value("BC3RGBA_UNORM", TextureFormat::BC3RGBAUnorm)    
    .value("BC3RGBA_UNORM_SRGB", TextureFormat::BC3RGBAUnormSrgb)    
    .value("BC4R_UNORM", TextureFormat::BC4RUnorm)    
    .value("BC4R_SNORM", TextureFormat::BC4RSnorm)    
    .value("BC5RG_UNORM", TextureFormat::BC5RGUnorm)    
    .value("BC5RG_SNORM", TextureFormat::BC5RGSnorm)    
    .value("BC6HRGB_UFLOAT", TextureFormat::BC6HRGBUfloat)    
    .value("BC6HRGB_FLOAT", TextureFormat::BC6HRGBFloat)    
    .value("BC7RGBA_UNORM", TextureFormat::BC7RGBAUnorm)    
    .value("BC7RGBA_UNORM_SRGB", TextureFormat::BC7RGBAUnormSrgb)    
    .value("ETC2RGB8_UNORM", TextureFormat::ETC2RGB8Unorm)    
    .value("ETC2RGB8_UNORM_SRGB", TextureFormat::ETC2RGB8UnormSrgb)    
    .value("ETC2RGB8A1_UNORM", TextureFormat::ETC2RGB8A1Unorm)    
    .value("ETC2RGB8A1_UNORM_SRGB", TextureFormat::ETC2RGB8A1UnormSrgb)    
    .value("ETC2RGBA8_UNORM", TextureFormat::ETC2RGBA8Unorm)    
    .value("ETC2RGBA8_UNORM_SRGB", TextureFormat::ETC2RGBA8UnormSrgb)    
    .value("EACR11_UNORM", TextureFormat::EACR11Unorm)    
    .value("EACR11_SNORM", TextureFormat::EACR11Snorm)    
    .value("EACRG11_UNORM", TextureFormat::EACRG11Unorm)    
    .value("EACRG11_SNORM", TextureFormat::EACRG11Snorm)    
    .value("ASTC4X4_UNORM", TextureFormat::ASTC4x4Unorm)    
    .value("ASTC4X4_UNORM_SRGB", TextureFormat::ASTC4x4UnormSrgb)    
    .value("ASTC5X4_UNORM", TextureFormat::ASTC5x4Unorm)    
    .value("ASTC5X4_UNORM_SRGB", TextureFormat::ASTC5x4UnormSrgb)    
    .value("ASTC5X5_UNORM", TextureFormat::ASTC5x5Unorm)    
    .value("ASTC5X5_UNORM_SRGB", TextureFormat::ASTC5x5UnormSrgb)    
    .value("ASTC6X5_UNORM", TextureFormat::ASTC6x5Unorm)    
    .value("ASTC6X5_UNORM_SRGB", TextureFormat::ASTC6x5UnormSrgb)    
    .value("ASTC6X6_UNORM", TextureFormat::ASTC6x6Unorm)    
    .value("ASTC6X6_UNORM_SRGB", TextureFormat::ASTC6x6UnormSrgb)    
    .value("ASTC8X5_UNORM", TextureFormat::ASTC8x5Unorm)    
    .value("ASTC8X5_UNORM_SRGB", TextureFormat::ASTC8x5UnormSrgb)    
    .value("ASTC8X6_UNORM", TextureFormat::ASTC8x6Unorm)    
    .value("ASTC8X6_UNORM_SRGB", TextureFormat::ASTC8x6UnormSrgb)    
    .value("ASTC8X8_UNORM", TextureFormat::ASTC8x8Unorm)    
    .value("ASTC8X8_UNORM_SRGB", TextureFormat::ASTC8x8UnormSrgb)    
    .value("ASTC10X5_UNORM", TextureFormat::ASTC10x5Unorm)    
    .value("ASTC10X5_UNORM_SRGB", TextureFormat::ASTC10x5UnormSrgb)    
    .value("ASTC10X6_UNORM", TextureFormat::ASTC10x6Unorm)    
    .value("ASTC10X6_UNORM_SRGB", TextureFormat::ASTC10x6UnormSrgb)    
    .value("ASTC10X8_UNORM", TextureFormat::ASTC10x8Unorm)    
    .value("ASTC10X8_UNORM_SRGB", TextureFormat::ASTC10x8UnormSrgb)    
    .value("ASTC10X10_UNORM", TextureFormat::ASTC10x10Unorm)    
    .value("ASTC10X10_UNORM_SRGB", TextureFormat::ASTC10x10UnormSrgb)    
    .value("ASTC12X10_UNORM", TextureFormat::ASTC12x10Unorm)    
    .value("ASTC12X10_UNORM_SRGB", TextureFormat::ASTC12x10UnormSrgb)    
    .value("ASTC12X12_UNORM", TextureFormat::ASTC12x12Unorm)    
    .value("ASTC12X12_UNORM_SRGB", TextureFormat::ASTC12x12UnormSrgb)    
    .value("R16_UNORM", TextureFormat::R16Unorm)    
    .value("RG16_UNORM", TextureFormat::RG16Unorm)    
    .value("RGBA16_UNORM", TextureFormat::RGBA16Unorm)    
    .value("R16_SNORM", TextureFormat::R16Snorm)    
    .value("RG16_SNORM", TextureFormat::RG16Snorm)    
    .value("RGBA16_SNORM", TextureFormat::RGBA16Snorm)    
    .value("R8BG8_BIPLANAR420_UNORM", TextureFormat::R8BG8Biplanar420Unorm)    
    .value("R10X6BG10X6_BIPLANAR420_UNORM", TextureFormat::R10X6BG10X6Biplanar420Unorm)    
    .value("R8BG8A8_TRIPLANAR420_UNORM", TextureFormat::R8BG8A8Triplanar420Unorm)    
    .value("R8BG8_BIPLANAR422_UNORM", TextureFormat::R8BG8Biplanar422Unorm)    
    .value("R8BG8_BIPLANAR444_UNORM", TextureFormat::R8BG8Biplanar444Unorm)    
    .value("R10X6BG10X6_BIPLANAR422_UNORM", TextureFormat::R10X6BG10X6Biplanar422Unorm)    
    .value("R10X6BG10X6_BIPLANAR444_UNORM", TextureFormat::R10X6BG10X6Biplanar444Unorm)    
    .value("EXTERNAL", TextureFormat::External)    
;

py::enum_<TextureViewDimension>(m, "TextureViewDimension", py::arithmetic())
    .value("UNDEFINED", TextureViewDimension::Undefined)    
    .value("E1D", TextureViewDimension::e1D)    
    .value("E2D", TextureViewDimension::e2D)    
    .value("E2D_ARRAY", TextureViewDimension::e2DArray)    
    .value("CUBE", TextureViewDimension::Cube)    
    .value("CUBE_ARRAY", TextureViewDimension::CubeArray)    
    .value("E3D", TextureViewDimension::e3D)    
;

py::enum_<VertexFormat>(m, "VertexFormat", py::arithmetic())
    .value("UINT8X2", VertexFormat::Uint8x2)    
    .value("UINT8X4", VertexFormat::Uint8x4)    
    .value("SINT8X2", VertexFormat::Sint8x2)    
    .value("SINT8X4", VertexFormat::Sint8x4)    
    .value("UNORM8X2", VertexFormat::Unorm8x2)    
    .value("UNORM8X4", VertexFormat::Unorm8x4)    
    .value("SNORM8X2", VertexFormat::Snorm8x2)    
    .value("SNORM8X4", VertexFormat::Snorm8x4)    
    .value("UINT16X2", VertexFormat::Uint16x2)    
    .value("UINT16X4", VertexFormat::Uint16x4)    
    .value("SINT16X2", VertexFormat::Sint16x2)    
    .value("SINT16X4", VertexFormat::Sint16x4)    
    .value("UNORM16X2", VertexFormat::Unorm16x2)    
    .value("UNORM16X4", VertexFormat::Unorm16x4)    
    .value("SNORM16X2", VertexFormat::Snorm16x2)    
    .value("SNORM16X4", VertexFormat::Snorm16x4)    
    .value("FLOAT16X2", VertexFormat::Float16x2)    
    .value("FLOAT16X4", VertexFormat::Float16x4)    
    .value("FLOAT32", VertexFormat::Float32)    
    .value("FLOAT32X2", VertexFormat::Float32x2)    
    .value("FLOAT32X3", VertexFormat::Float32x3)    
    .value("FLOAT32X4", VertexFormat::Float32x4)    
    .value("UINT32", VertexFormat::Uint32)    
    .value("UINT32X2", VertexFormat::Uint32x2)    
    .value("UINT32X3", VertexFormat::Uint32x3)    
    .value("UINT32X4", VertexFormat::Uint32x4)    
    .value("SINT32", VertexFormat::Sint32)    
    .value("SINT32X2", VertexFormat::Sint32x2)    
    .value("SINT32X3", VertexFormat::Sint32x3)    
    .value("SINT32X4", VertexFormat::Sint32x4)    
    .value("UNORM10_10_10_2", VertexFormat::Unorm10_10_10_2)    
;

py::enum_<WGSLFeatureName>(m, "WGSLFeatureName", py::arithmetic())
    .value("READONLY_AND_READWRITE_STORAGE_TEXTURES", WGSLFeatureName::ReadonlyAndReadwriteStorageTextures)    
    .value("PACKED4X8_INTEGER_DOT_PRODUCT", WGSLFeatureName::Packed4x8IntegerDotProduct)    
    .value("UNRESTRICTED_POINTER_PARAMETERS", WGSLFeatureName::UnrestrictedPointerParameters)    
    .value("POINTER_COMPOSITE_ACCESS", WGSLFeatureName::PointerCompositeAccess)    
    .value("CHROMIUM_TESTING_UNIMPLEMENTED", WGSLFeatureName::ChromiumTestingUnimplemented)    
    .value("CHROMIUM_TESTING_UNSAFE_EXPERIMENTAL", WGSLFeatureName::ChromiumTestingUnsafeExperimental)    
    .value("CHROMIUM_TESTING_EXPERIMENTAL", WGSLFeatureName::ChromiumTestingExperimental)    
    .value("CHROMIUM_TESTING_SHIPPED_WITH_KILLSWITCH", WGSLFeatureName::ChromiumTestingShippedWithKillswitch)    
    .value("CHROMIUM_TESTING_SHIPPED", WGSLFeatureName::ChromiumTestingShipped)    
;

py::enum_<BufferUsage>(m, "BufferUsage", py::arithmetic())
    .value("NONE", BufferUsage::None)    
    .value("MAP_READ", BufferUsage::MapRead)    
    .value("MAP_WRITE", BufferUsage::MapWrite)    
    .value("COPY_SRC", BufferUsage::CopySrc)    
    .value("COPY_DST", BufferUsage::CopyDst)    
    .value("INDEX", BufferUsage::Index)    
    .value("VERTEX", BufferUsage::Vertex)    
    .value("UNIFORM", BufferUsage::Uniform)    
    .value("STORAGE", BufferUsage::Storage)    
    .value("INDIRECT", BufferUsage::Indirect)    
    .value("QUERY_RESOLVE", BufferUsage::QueryResolve)    
    
    .def("__or__", [](wgpu::BufferUsage& a, wgpu::BufferUsage& b) {
        return (wgpu::BufferUsage)(a | b);
    }, py::is_operator());
    

py::enum_<ColorWriteMask>(m, "ColorWriteMask", py::arithmetic())
    .value("NONE", ColorWriteMask::None)    
    .value("RED", ColorWriteMask::Red)    
    .value("GREEN", ColorWriteMask::Green)    
    .value("BLUE", ColorWriteMask::Blue)    
    .value("ALPHA", ColorWriteMask::Alpha)    
    .value("ALL", ColorWriteMask::All)    
    
    .def("__or__", [](wgpu::ColorWriteMask& a, wgpu::ColorWriteMask& b) {
        return (wgpu::ColorWriteMask)(a | b);
    }, py::is_operator());
    

py::enum_<MapMode>(m, "MapMode", py::arithmetic())
    .value("NONE", MapMode::None)    
    .value("READ", MapMode::Read)    
    .value("WRITE", MapMode::Write)    
    
    .def("__or__", [](wgpu::MapMode& a, wgpu::MapMode& b) {
        return (wgpu::MapMode)(a | b);
    }, py::is_operator());
    

py::enum_<ShaderStage>(m, "ShaderStage", py::arithmetic())
    .value("NONE", ShaderStage::None)    
    .value("VERTEX", ShaderStage::Vertex)    
    .value("FRAGMENT", ShaderStage::Fragment)    
    .value("COMPUTE", ShaderStage::Compute)    
    
    .def("__or__", [](wgpu::ShaderStage& a, wgpu::ShaderStage& b) {
        return (wgpu::ShaderStage)(a | b);
    }, py::is_operator());
    

py::enum_<TextureUsage>(m, "TextureUsage", py::arithmetic())
    .value("NONE", TextureUsage::None)    
    .value("COPY_SRC", TextureUsage::CopySrc)    
    .value("COPY_DST", TextureUsage::CopyDst)    
    .value("TEXTURE_BINDING", TextureUsage::TextureBinding)    
    .value("STORAGE_BINDING", TextureUsage::StorageBinding)    
    .value("RENDER_ATTACHMENT", TextureUsage::RenderAttachment)    
    .value("TRANSIENT_ATTACHMENT", TextureUsage::TransientAttachment)    
    .value("STORAGE_ATTACHMENT", TextureUsage::StorageAttachment)    
    
    .def("__or__", [](wgpu::TextureUsage& a, wgpu::TextureUsage& b) {
        return (wgpu::TextureUsage)(a | b);
    }, py::is_operator());
    

py::enum_<HeapProperty>(m, "HeapProperty", py::arithmetic())
    .value("DEVICE_LOCAL", HeapProperty::DeviceLocal)    
    .value("HOST_VISIBLE", HeapProperty::HostVisible)    
    .value("HOST_COHERENT", HeapProperty::HostCoherent)    
    .value("HOST_UNCACHED", HeapProperty::HostUncached)    
    .value("HOST_CACHED", HeapProperty::HostCached)    
    
    .def("__or__", [](wgpu::HeapProperty& a, wgpu::HeapProperty& b) {
        return (wgpu::HeapProperty)(a | b);
    }, py::is_operator());
    

PYCLASS_BEGIN(m, wgpu::Adapter, Adapter) Adapter
    .def("get_instance", &wgpu::Adapter::GetInstance
        , py::return_value_policy::automatic_reference)
    
    .def("get_limits", &wgpu::Adapter::GetLimits
        , py::arg("limits")
        , py::return_value_policy::automatic_reference)
    
    .def("get_info", &wgpu::Adapter::GetInfo
        , py::arg("info")
        , py::return_value_policy::automatic_reference)
    
    .def("get_properties", &wgpu::Adapter::GetProperties
        , py::arg("properties")
        , py::return_value_policy::automatic_reference)
    
    .def("has_feature", &wgpu::Adapter::HasFeature
        , py::arg("feature")
        , py::return_value_policy::automatic_reference)
    
    .def("enumerate_features", &wgpu::Adapter::EnumerateFeatures
        , py::arg("features")
        , py::return_value_policy::automatic_reference)
    
    .def("request_device", &wgpu::Adapter::RequestDevice
        , py::arg("descriptor"), py::arg("callback"), py::arg("userdata")
        , py::return_value_policy::automatic_reference)
    
    .def("create_device", &wgpu::Adapter::CreateDevice
        , py::arg("descriptor") = nullptr
        , py::return_value_policy::automatic_reference)
    
    .def("get_format_capabilities", &wgpu::Adapter::GetFormatCapabilities
        , py::arg("format"), py::arg("capabilities")
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::Adapter, Adapter)

PYCLASS_BEGIN(m, wgpu::BindGroup, BindGroup) BindGroup
    .def("set_label", &wgpu::BindGroup::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label_2", &wgpu::BindGroup::SetLabel2
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::BindGroup, BindGroup)

PYCLASS_BEGIN(m, wgpu::BindGroupLayout, BindGroupLayout) BindGroupLayout
    .def("set_label", &wgpu::BindGroupLayout::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label_2", &wgpu::BindGroupLayout::SetLabel2
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::BindGroupLayout, BindGroupLayout)

PYCLASS_BEGIN(m, wgpu::Buffer, Buffer) Buffer
    .def("map_async", &wgpu::Buffer::MapAsync
        , py::arg("mode"), py::arg("offset"), py::arg("size"), py::arg("callback"), py::arg("userdata")
        , py::return_value_policy::automatic_reference)
    
    .def("get_mapped_range", &wgpu::Buffer::GetMappedRange
        , py::arg("offset") = 0, py::arg("size") = WGPU_WHOLE_MAP_SIZE
        , py::return_value_policy::automatic_reference)
    
    .def("get_const_mapped_range", &wgpu::Buffer::GetConstMappedRange
        , py::arg("offset") = 0, py::arg("size") = WGPU_WHOLE_MAP_SIZE
        , py::return_value_policy::automatic_reference)
    
    .def("set_label", &wgpu::Buffer::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label_2", &wgpu::Buffer::SetLabel2
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("get_usage", &wgpu::Buffer::GetUsage
        , py::return_value_policy::automatic_reference)
    
    .def("get_size", &wgpu::Buffer::GetSize
        , py::return_value_policy::automatic_reference)
    
    .def("get_map_state", &wgpu::Buffer::GetMapState
        , py::return_value_policy::automatic_reference)
    
    .def("unmap", &wgpu::Buffer::Unmap
        , py::return_value_policy::automatic_reference)
    
    .def("destroy", &wgpu::Buffer::Destroy
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::Buffer, Buffer)

PYCLASS_BEGIN(m, wgpu::CommandBuffer, CommandBuffer) CommandBuffer
    .def("set_label", &wgpu::CommandBuffer::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label_2", &wgpu::CommandBuffer::SetLabel2
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::CommandBuffer, CommandBuffer)

PYCLASS_BEGIN(m, wgpu::CommandEncoder, CommandEncoder) CommandEncoder
    .def("finish", &wgpu::CommandEncoder::Finish
        , py::arg("descriptor") = nullptr
        , py::return_value_policy::automatic_reference)
    
    .def("begin_compute_pass", &wgpu::CommandEncoder::BeginComputePass
        , py::arg("descriptor") = nullptr
        , py::return_value_policy::automatic_reference)
    
    .def("begin_render_pass", &wgpu::CommandEncoder::BeginRenderPass
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference)
    
    .def("copy_buffer_to_buffer", &wgpu::CommandEncoder::CopyBufferToBuffer
        , py::arg("source"), py::arg("source_offset"), py::arg("destination"), py::arg("destination_offset"), py::arg("size")
        , py::return_value_policy::automatic_reference)
    
    .def("copy_buffer_to_texture", &wgpu::CommandEncoder::CopyBufferToTexture
        , py::arg("source"), py::arg("destination"), py::arg("copy_size")
        , py::return_value_policy::automatic_reference)
    
    .def("copy_texture_to_buffer", &wgpu::CommandEncoder::CopyTextureToBuffer
        , py::arg("source"), py::arg("destination"), py::arg("copy_size")
        , py::return_value_policy::automatic_reference)
    
    .def("copy_texture_to_texture", &wgpu::CommandEncoder::CopyTextureToTexture
        , py::arg("source"), py::arg("destination"), py::arg("copy_size")
        , py::return_value_policy::automatic_reference)
    
    .def("clear_buffer", &wgpu::CommandEncoder::ClearBuffer
        , py::arg("buffer"), py::arg("offset") = 0, py::arg("size") = WGPU_WHOLE_SIZE
        , py::return_value_policy::automatic_reference)
    
    .def("inject_validation_error", &wgpu::CommandEncoder::InjectValidationError
        , py::arg("message")
        , py::return_value_policy::automatic_reference)
    
    .def("inject_validation_error_2", &wgpu::CommandEncoder::InjectValidationError2
        , py::arg("message")
        , py::return_value_policy::automatic_reference)
    
    .def("insert_debug_marker", &wgpu::CommandEncoder::InsertDebugMarker
        , py::arg("marker_label")
        , py::return_value_policy::automatic_reference)
    
    .def("insert_debug_marker_2", &wgpu::CommandEncoder::InsertDebugMarker2
        , py::arg("marker_label")
        , py::return_value_policy::automatic_reference)
    
    .def("pop_debug_group", &wgpu::CommandEncoder::PopDebugGroup
        , py::return_value_policy::automatic_reference)
    
    .def("push_debug_group", &wgpu::CommandEncoder::PushDebugGroup
        , py::arg("group_label")
        , py::return_value_policy::automatic_reference)
    
    .def("push_debug_group_2", &wgpu::CommandEncoder::PushDebugGroup2
        , py::arg("group_label")
        , py::return_value_policy::automatic_reference)
    
    .def("resolve_query_set", &wgpu::CommandEncoder::ResolveQuerySet
        , py::arg("query_set"), py::arg("first_query"), py::arg("query_count"), py::arg("destination"), py::arg("destination_offset")
        , py::return_value_policy::automatic_reference)
    
    .def("write_buffer", &wgpu::CommandEncoder::WriteBuffer
        , py::arg("buffer"), py::arg("buffer_offset"), py::arg("data"), py::arg("size")
        , py::return_value_policy::automatic_reference)
    
    .def("write_timestamp", &wgpu::CommandEncoder::WriteTimestamp
        , py::arg("query_set"), py::arg("query_index")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label", &wgpu::CommandEncoder::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label_2", &wgpu::CommandEncoder::SetLabel2
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::CommandEncoder, CommandEncoder)

PYCLASS_BEGIN(m, wgpu::ComputePassEncoder, ComputePassEncoder) ComputePassEncoder
    .def("insert_debug_marker", &wgpu::ComputePassEncoder::InsertDebugMarker
        , py::arg("marker_label")
        , py::return_value_policy::automatic_reference)
    
    .def("insert_debug_marker_2", &wgpu::ComputePassEncoder::InsertDebugMarker2
        , py::arg("marker_label")
        , py::return_value_policy::automatic_reference)
    
    .def("pop_debug_group", &wgpu::ComputePassEncoder::PopDebugGroup
        , py::return_value_policy::automatic_reference)
    
    .def("push_debug_group", &wgpu::ComputePassEncoder::PushDebugGroup
        , py::arg("group_label")
        , py::return_value_policy::automatic_reference)
    
    .def("push_debug_group_2", &wgpu::ComputePassEncoder::PushDebugGroup2
        , py::arg("group_label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_pipeline", &wgpu::ComputePassEncoder::SetPipeline
        , py::arg("pipeline")
        , py::return_value_policy::automatic_reference)
    
    .def("set_bind_group", &wgpu::ComputePassEncoder::SetBindGroup
        , py::arg("group_index"), py::arg("group"), py::arg("dynamic_offset_count") = 0, py::arg("dynamic_offsets") = nullptr
        , py::return_value_policy::automatic_reference)
    
    .def("write_timestamp", &wgpu::ComputePassEncoder::WriteTimestamp
        , py::arg("query_set"), py::arg("query_index")
        , py::return_value_policy::automatic_reference)
    
    .def("dispatch_workgroups", &wgpu::ComputePassEncoder::DispatchWorkgroups
        , py::arg("workgroupCountX"), py::arg("workgroupCountY") = 1, py::arg("workgroupCountZ") = 1
        , py::return_value_policy::automatic_reference)
    
    .def("dispatch_workgroups_indirect", &wgpu::ComputePassEncoder::DispatchWorkgroupsIndirect
        , py::arg("indirect_buffer"), py::arg("indirect_offset")
        , py::return_value_policy::automatic_reference)
    
    .def("end", &wgpu::ComputePassEncoder::End
        , py::return_value_policy::automatic_reference)
    
    .def("set_label", &wgpu::ComputePassEncoder::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label_2", &wgpu::ComputePassEncoder::SetLabel2
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::ComputePassEncoder, ComputePassEncoder)

PYCLASS_BEGIN(m, wgpu::ComputePipeline, ComputePipeline) ComputePipeline
    .def("get_bind_group_layout", &wgpu::ComputePipeline::GetBindGroupLayout
        , py::arg("group_index")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label", &wgpu::ComputePipeline::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label_2", &wgpu::ComputePipeline::SetLabel2
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::ComputePipeline, ComputePipeline)

PYCLASS_BEGIN(m, wgpu::Device, Device) Device
    .def("create_bind_group", &wgpu::Device::CreateBindGroup
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference)
    
    .def("create_bind_group_layout", &wgpu::Device::CreateBindGroupLayout
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference)
    
    .def("create_buffer", &wgpu::Device::CreateBuffer
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference)
    
    .def("create_error_buffer", &wgpu::Device::CreateErrorBuffer
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference)
    
    .def("create_command_encoder", &wgpu::Device::CreateCommandEncoder
        , py::arg("descriptor") = nullptr
        , py::return_value_policy::automatic_reference)
    
    .def("create_compute_pipeline", &wgpu::Device::CreateComputePipeline
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference)
    
    .def("create_compute_pipeline_async", &wgpu::Device::CreateComputePipelineAsync
        , py::arg("descriptor"), py::arg("callback"), py::arg("userdata")
        , py::return_value_policy::automatic_reference)
    
    .def("create_external_texture", &wgpu::Device::CreateExternalTexture
        , py::arg("external_texture_descriptor")
        , py::return_value_policy::automatic_reference)
    
    .def("create_error_external_texture", &wgpu::Device::CreateErrorExternalTexture
        , py::return_value_policy::automatic_reference)
    
    .def("create_pipeline_layout", &wgpu::Device::CreatePipelineLayout
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference)
    
    .def("create_query_set", &wgpu::Device::CreateQuerySet
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference)
    
    .def("create_render_pipeline_async", &wgpu::Device::CreateRenderPipelineAsync
        , py::arg("descriptor"), py::arg("callback"), py::arg("userdata")
        , py::return_value_policy::automatic_reference)
    
    .def("create_render_bundle_encoder", &wgpu::Device::CreateRenderBundleEncoder
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference)
    
    .def("create_render_pipeline", &wgpu::Device::CreateRenderPipeline
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference)
    
    .def("create_sampler", &wgpu::Device::CreateSampler
        , py::arg("descriptor") = nullptr
        , py::return_value_policy::automatic_reference)
    
    .def("create_shader_module", &wgpu::Device::CreateShaderModule
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference)
    
    .def("create_error_shader_module", &wgpu::Device::CreateErrorShaderModule
        , py::arg("descriptor"), py::arg("error_message")
        , py::return_value_policy::automatic_reference)
    
    .def("create_error_shader_module_2", &wgpu::Device::CreateErrorShaderModule2
        , py::arg("descriptor"), py::arg("error_message")
        , py::return_value_policy::automatic_reference)
    
    .def("create_swap_chain", &wgpu::Device::CreateSwapChain
        , py::arg("surface"), py::arg("descriptor")
        , py::return_value_policy::automatic_reference)
    
    .def("create_texture", &wgpu::Device::CreateTexture
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference)
    
    .def("import_shared_buffer_memory", &wgpu::Device::ImportSharedBufferMemory
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference)
    
    .def("import_shared_texture_memory", &wgpu::Device::ImportSharedTextureMemory
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference)
    
    .def("import_shared_fence", &wgpu::Device::ImportSharedFence
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference)
    
    .def("create_error_texture", &wgpu::Device::CreateErrorTexture
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference)
    
    .def("destroy", &wgpu::Device::Destroy
        , py::return_value_policy::automatic_reference)
    
    .def("get_a_hardware_buffer_properties", &wgpu::Device::GetAHardwareBufferProperties
        , py::arg("handle"), py::arg("properties")
        , py::return_value_policy::automatic_reference)
    
    .def("get_limits", &wgpu::Device::GetLimits
        , py::arg("limits")
        , py::return_value_policy::automatic_reference)
    
    .def("has_feature", &wgpu::Device::HasFeature
        , py::arg("feature")
        , py::return_value_policy::automatic_reference)
    
    .def("enumerate_features", &wgpu::Device::EnumerateFeatures
        , py::arg("features")
        , py::return_value_policy::automatic_reference)
    
    .def("get_adapter", &wgpu::Device::GetAdapter
        , py::return_value_policy::automatic_reference)
    
    .def("get_queue", &wgpu::Device::GetQueue
        , py::return_value_policy::automatic_reference)
    
    .def("inject_error", &wgpu::Device::InjectError
        , py::arg("type"), py::arg("message")
        , py::return_value_policy::automatic_reference)
    
    .def("inject_error_2", &wgpu::Device::InjectError2
        , py::arg("type"), py::arg("message")
        , py::return_value_policy::automatic_reference)
    
    .def("force_loss", &wgpu::Device::ForceLoss
        , py::arg("type"), py::arg("message")
        , py::return_value_policy::automatic_reference)
    
    .def("force_loss_2", &wgpu::Device::ForceLoss2
        , py::arg("type"), py::arg("message")
        , py::return_value_policy::automatic_reference)
    
    .def("tick", &wgpu::Device::Tick
        , py::return_value_policy::automatic_reference)
    
    .def("set_uncaptured_error_callback", &wgpu::Device::SetUncapturedErrorCallback
        , py::arg("callback"), py::arg("userdata")
        , py::return_value_policy::automatic_reference)
    
    .def("set_logging_callback", &wgpu::Device::SetLoggingCallback
        , py::arg("callback"), py::arg("userdata")
        , py::return_value_policy::automatic_reference)
    
    .def("set_device_lost_callback", &wgpu::Device::SetDeviceLostCallback
        , py::arg("callback"), py::arg("userdata")
        , py::return_value_policy::automatic_reference)
    
    .def("push_error_scope", &wgpu::Device::PushErrorScope
        , py::arg("filter")
        , py::return_value_policy::automatic_reference)
    
    .def("pop_error_scope", &wgpu::Device::PopErrorScope
        , py::arg("old_callback"), py::arg("userdata")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label", &wgpu::Device::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label_2", &wgpu::Device::SetLabel2
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("validate_texture_descriptor", &wgpu::Device::ValidateTextureDescriptor
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference)
    
    .def("get_supported_surface_usage", &wgpu::Device::GetSupportedSurfaceUsage
        , py::arg("surface")
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::Device, Device)

PYCLASS_BEGIN(m, wgpu::ExternalTexture, ExternalTexture) ExternalTexture
    .def("set_label", &wgpu::ExternalTexture::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label_2", &wgpu::ExternalTexture::SetLabel2
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("destroy", &wgpu::ExternalTexture::Destroy
        , py::return_value_policy::automatic_reference)
    
    .def("expire", &wgpu::ExternalTexture::Expire
        , py::return_value_policy::automatic_reference)
    
    .def("refresh", &wgpu::ExternalTexture::Refresh
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::ExternalTexture, ExternalTexture)

PYCLASS_BEGIN(m, wgpu::SharedBufferMemory, SharedBufferMemory) SharedBufferMemory
    .def("set_label", &wgpu::SharedBufferMemory::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label_2", &wgpu::SharedBufferMemory::SetLabel2
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("get_properties", &wgpu::SharedBufferMemory::GetProperties
        , py::arg("properties")
        , py::return_value_policy::automatic_reference)
    
    .def("create_buffer", &wgpu::SharedBufferMemory::CreateBuffer
        , py::arg("descriptor") = nullptr
        , py::return_value_policy::automatic_reference)
    
    .def("begin_access", &wgpu::SharedBufferMemory::BeginAccess
        , py::arg("buffer"), py::arg("descriptor")
        , py::return_value_policy::automatic_reference)
    
    .def("end_access", &wgpu::SharedBufferMemory::EndAccess
        , py::arg("buffer"), py::arg("descriptor")
        , py::return_value_policy::automatic_reference)
    
    .def("is_device_lost", &wgpu::SharedBufferMemory::IsDeviceLost
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::SharedBufferMemory, SharedBufferMemory)

PYCLASS_BEGIN(m, wgpu::SharedTextureMemory, SharedTextureMemory) SharedTextureMemory
    .def("set_label", &wgpu::SharedTextureMemory::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label_2", &wgpu::SharedTextureMemory::SetLabel2
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("get_properties", &wgpu::SharedTextureMemory::GetProperties
        , py::arg("properties")
        , py::return_value_policy::automatic_reference)
    
    .def("create_texture", &wgpu::SharedTextureMemory::CreateTexture
        , py::arg("descriptor") = nullptr
        , py::return_value_policy::automatic_reference)
    
    .def("begin_access", &wgpu::SharedTextureMemory::BeginAccess
        , py::arg("texture"), py::arg("descriptor")
        , py::return_value_policy::automatic_reference)
    
    .def("end_access", &wgpu::SharedTextureMemory::EndAccess
        , py::arg("texture"), py::arg("descriptor")
        , py::return_value_policy::automatic_reference)
    
    .def("is_device_lost", &wgpu::SharedTextureMemory::IsDeviceLost
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::SharedTextureMemory, SharedTextureMemory)

PYCLASS_BEGIN(m, wgpu::SharedFence, SharedFence) SharedFence
    .def("export_info", &wgpu::SharedFence::ExportInfo
        , py::arg("info")
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::SharedFence, SharedFence)

PYCLASS_BEGIN(m, wgpu::Instance, Instance) Instance
    .def("create_surface", &wgpu::Instance::CreateSurface
        , py::arg("descriptor")
        , py::return_value_policy::automatic_reference)
    
    .def("process_events", &wgpu::Instance::ProcessEvents
        , py::return_value_policy::automatic_reference)
    
    .def("wait_any", &wgpu::Instance::WaitAny
        , py::arg("future_count"), py::arg("futures"), py::arg("timeout_NS")
        , py::return_value_policy::automatic_reference)
    
    .def("has_WGSL_language_feature", &wgpu::Instance::HasWGSLLanguageFeature
        , py::arg("feature")
        , py::return_value_policy::automatic_reference)
    
    .def("enumerate_WGSL_language_features", &wgpu::Instance::EnumerateWGSLLanguageFeatures
        , py::arg("features")
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::Instance, Instance)

PYCLASS_BEGIN(m, wgpu::PipelineLayout, PipelineLayout) PipelineLayout
    .def("set_label", &wgpu::PipelineLayout::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label_2", &wgpu::PipelineLayout::SetLabel2
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::PipelineLayout, PipelineLayout)

PYCLASS_BEGIN(m, wgpu::QuerySet, QuerySet) QuerySet
    .def("set_label", &wgpu::QuerySet::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label_2", &wgpu::QuerySet::SetLabel2
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("get_type", &wgpu::QuerySet::GetType
        , py::return_value_policy::automatic_reference)
    
    .def("get_count", &wgpu::QuerySet::GetCount
        , py::return_value_policy::automatic_reference)
    
    .def("destroy", &wgpu::QuerySet::Destroy
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::QuerySet, QuerySet)

PYCLASS_BEGIN(m, wgpu::Queue, Queue) Queue
    .def("submit", &wgpu::Queue::Submit
        , py::arg("command_count"), py::arg("commands")
        , py::return_value_policy::automatic_reference)
    
    .def("write_buffer", &wgpu::Queue::WriteBuffer
        , py::arg("buffer"), py::arg("buffer_offset"), py::arg("data"), py::arg("size")
        , py::return_value_policy::automatic_reference)
    
    .def("write_texture", &wgpu::Queue::WriteTexture
        , py::arg("destination"), py::arg("data"), py::arg("data_size"), py::arg("data_layout"), py::arg("write_size")
        , py::return_value_policy::automatic_reference)
    
    .def("copy_texture_for_browser", &wgpu::Queue::CopyTextureForBrowser
        , py::arg("source"), py::arg("destination"), py::arg("copy_size"), py::arg("options")
        , py::return_value_policy::automatic_reference)
    
    .def("copy_external_texture_for_browser", &wgpu::Queue::CopyExternalTextureForBrowser
        , py::arg("source"), py::arg("destination"), py::arg("copy_size"), py::arg("options")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label", &wgpu::Queue::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label_2", &wgpu::Queue::SetLabel2
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::Queue, Queue)

PYCLASS_BEGIN(m, wgpu::RenderBundle, RenderBundle) RenderBundle
    .def("set_label", &wgpu::RenderBundle::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label_2", &wgpu::RenderBundle::SetLabel2
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::RenderBundle, RenderBundle)

PYCLASS_BEGIN(m, wgpu::RenderBundleEncoder, RenderBundleEncoder) RenderBundleEncoder
    .def("set_pipeline", &wgpu::RenderBundleEncoder::SetPipeline
        , py::arg("pipeline")
        , py::return_value_policy::automatic_reference)
    
    .def("set_bind_group", &wgpu::RenderBundleEncoder::SetBindGroup
        , py::arg("group_index"), py::arg("group"), py::arg("dynamic_offset_count") = 0, py::arg("dynamic_offsets") = nullptr
        , py::return_value_policy::automatic_reference)
    
    .def("draw", &wgpu::RenderBundleEncoder::Draw
        , py::arg("vertex_count"), py::arg("instance_count") = 1, py::arg("first_vertex") = 0, py::arg("first_instance") = 0
        , py::return_value_policy::automatic_reference)
    
    .def("draw_indexed", &wgpu::RenderBundleEncoder::DrawIndexed
        , py::arg("index_count"), py::arg("instance_count") = 1, py::arg("first_index") = 0, py::arg("base_vertex") = 0, py::arg("first_instance") = 0
        , py::return_value_policy::automatic_reference)
    
    .def("draw_indirect", &wgpu::RenderBundleEncoder::DrawIndirect
        , py::arg("indirect_buffer"), py::arg("indirect_offset")
        , py::return_value_policy::automatic_reference)
    
    .def("draw_indexed_indirect", &wgpu::RenderBundleEncoder::DrawIndexedIndirect
        , py::arg("indirect_buffer"), py::arg("indirect_offset")
        , py::return_value_policy::automatic_reference)
    
    .def("insert_debug_marker", &wgpu::RenderBundleEncoder::InsertDebugMarker
        , py::arg("marker_label")
        , py::return_value_policy::automatic_reference)
    
    .def("insert_debug_marker_2", &wgpu::RenderBundleEncoder::InsertDebugMarker2
        , py::arg("marker_label")
        , py::return_value_policy::automatic_reference)
    
    .def("pop_debug_group", &wgpu::RenderBundleEncoder::PopDebugGroup
        , py::return_value_policy::automatic_reference)
    
    .def("push_debug_group", &wgpu::RenderBundleEncoder::PushDebugGroup
        , py::arg("group_label")
        , py::return_value_policy::automatic_reference)
    
    .def("push_debug_group_2", &wgpu::RenderBundleEncoder::PushDebugGroup2
        , py::arg("group_label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_vertex_buffer", &wgpu::RenderBundleEncoder::SetVertexBuffer
        , py::arg("slot"), py::arg("buffer"), py::arg("offset") = 0, py::arg("size") = WGPU_WHOLE_SIZE
        , py::return_value_policy::automatic_reference)
    
    .def("set_index_buffer", &wgpu::RenderBundleEncoder::SetIndexBuffer
        , py::arg("buffer"), py::arg("format"), py::arg("offset") = 0, py::arg("size") = WGPU_WHOLE_SIZE
        , py::return_value_policy::automatic_reference)
    
    .def("finish", &wgpu::RenderBundleEncoder::Finish
        , py::arg("descriptor") = nullptr
        , py::return_value_policy::automatic_reference)
    
    .def("set_label", &wgpu::RenderBundleEncoder::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label_2", &wgpu::RenderBundleEncoder::SetLabel2
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::RenderBundleEncoder, RenderBundleEncoder)

PYCLASS_BEGIN(m, wgpu::RenderPassEncoder, RenderPassEncoder) RenderPassEncoder
    .def("set_pipeline", &wgpu::RenderPassEncoder::SetPipeline
        , py::arg("pipeline")
        , py::return_value_policy::automatic_reference)
    
    .def("set_bind_group", &wgpu::RenderPassEncoder::SetBindGroup
        , py::arg("group_index"), py::arg("group"), py::arg("dynamic_offset_count") = 0, py::arg("dynamic_offsets") = nullptr
        , py::return_value_policy::automatic_reference)
    
    .def("draw", &wgpu::RenderPassEncoder::Draw
        , py::arg("vertex_count"), py::arg("instance_count") = 1, py::arg("first_vertex") = 0, py::arg("first_instance") = 0
        , py::return_value_policy::automatic_reference)
    
    .def("draw_indexed", &wgpu::RenderPassEncoder::DrawIndexed
        , py::arg("index_count"), py::arg("instance_count") = 1, py::arg("first_index") = 0, py::arg("base_vertex") = 0, py::arg("first_instance") = 0
        , py::return_value_policy::automatic_reference)
    
    .def("draw_indirect", &wgpu::RenderPassEncoder::DrawIndirect
        , py::arg("indirect_buffer"), py::arg("indirect_offset")
        , py::return_value_policy::automatic_reference)
    
    .def("draw_indexed_indirect", &wgpu::RenderPassEncoder::DrawIndexedIndirect
        , py::arg("indirect_buffer"), py::arg("indirect_offset")
        , py::return_value_policy::automatic_reference)
    
    .def("execute_bundles", &wgpu::RenderPassEncoder::ExecuteBundles
        , py::arg("bundle_count"), py::arg("bundles")
        , py::return_value_policy::automatic_reference)
    
    .def("insert_debug_marker", &wgpu::RenderPassEncoder::InsertDebugMarker
        , py::arg("marker_label")
        , py::return_value_policy::automatic_reference)
    
    .def("insert_debug_marker_2", &wgpu::RenderPassEncoder::InsertDebugMarker2
        , py::arg("marker_label")
        , py::return_value_policy::automatic_reference)
    
    .def("pop_debug_group", &wgpu::RenderPassEncoder::PopDebugGroup
        , py::return_value_policy::automatic_reference)
    
    .def("push_debug_group", &wgpu::RenderPassEncoder::PushDebugGroup
        , py::arg("group_label")
        , py::return_value_policy::automatic_reference)
    
    .def("push_debug_group_2", &wgpu::RenderPassEncoder::PushDebugGroup2
        , py::arg("group_label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_stencil_reference", &wgpu::RenderPassEncoder::SetStencilReference
        , py::arg("reference")
        , py::return_value_policy::automatic_reference)
    
    .def("set_blend_constant", &wgpu::RenderPassEncoder::SetBlendConstant
        , py::arg("color")
        , py::return_value_policy::automatic_reference)
    
    .def("set_viewport", &wgpu::RenderPassEncoder::SetViewport
        , py::arg("x"), py::arg("y"), py::arg("width"), py::arg("height"), py::arg("min_depth"), py::arg("max_depth")
        , py::return_value_policy::automatic_reference)
    
    .def("set_scissor_rect", &wgpu::RenderPassEncoder::SetScissorRect
        , py::arg("x"), py::arg("y"), py::arg("width"), py::arg("height")
        , py::return_value_policy::automatic_reference)
    
    .def("set_vertex_buffer", &wgpu::RenderPassEncoder::SetVertexBuffer
        , py::arg("slot"), py::arg("buffer"), py::arg("offset") = 0, py::arg("size") = WGPU_WHOLE_SIZE
        , py::return_value_policy::automatic_reference)
    
    .def("set_index_buffer", &wgpu::RenderPassEncoder::SetIndexBuffer
        , py::arg("buffer"), py::arg("format"), py::arg("offset") = 0, py::arg("size") = WGPU_WHOLE_SIZE
        , py::return_value_policy::automatic_reference)
    
    .def("begin_occlusion_query", &wgpu::RenderPassEncoder::BeginOcclusionQuery
        , py::arg("query_index")
        , py::return_value_policy::automatic_reference)
    
    .def("end_occlusion_query", &wgpu::RenderPassEncoder::EndOcclusionQuery
        , py::return_value_policy::automatic_reference)
    
    .def("write_timestamp", &wgpu::RenderPassEncoder::WriteTimestamp
        , py::arg("query_set"), py::arg("query_index")
        , py::return_value_policy::automatic_reference)
    
    .def("pixel_local_storage_barrier", &wgpu::RenderPassEncoder::PixelLocalStorageBarrier
        , py::return_value_policy::automatic_reference)
    
    .def("end", &wgpu::RenderPassEncoder::End
        , py::return_value_policy::automatic_reference)
    
    .def("set_label", &wgpu::RenderPassEncoder::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label_2", &wgpu::RenderPassEncoder::SetLabel2
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::RenderPassEncoder, RenderPassEncoder)

PYCLASS_BEGIN(m, wgpu::RenderPipeline, RenderPipeline) RenderPipeline
    .def("get_bind_group_layout", &wgpu::RenderPipeline::GetBindGroupLayout
        , py::arg("group_index")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label", &wgpu::RenderPipeline::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label_2", &wgpu::RenderPipeline::SetLabel2
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::RenderPipeline, RenderPipeline)

PYCLASS_BEGIN(m, wgpu::Sampler, Sampler) Sampler
    .def("set_label", &wgpu::Sampler::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label_2", &wgpu::Sampler::SetLabel2
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::Sampler, Sampler)

PYCLASS_BEGIN(m, wgpu::ShaderModule, ShaderModule) ShaderModule
    .def("get_compilation_info", &wgpu::ShaderModule::GetCompilationInfo
        , py::arg("callback"), py::arg("userdata")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label", &wgpu::ShaderModule::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label_2", &wgpu::ShaderModule::SetLabel2
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::ShaderModule, ShaderModule)

PYCLASS_BEGIN(m, wgpu::Surface, Surface) Surface
    .def("configure", &wgpu::Surface::Configure
        , py::arg("config")
        , py::return_value_policy::automatic_reference)
    
    .def("get_capabilities", &wgpu::Surface::GetCapabilities
        , py::arg("adapter"), py::arg("capabilities")
        , py::return_value_policy::automatic_reference)
    
    .def("get_current_texture", &wgpu::Surface::GetCurrentTexture
        , py::arg("surface_texture")
        , py::return_value_policy::automatic_reference)
    
    .def("get_preferred_format", &wgpu::Surface::GetPreferredFormat
        , py::arg("adapter")
        , py::return_value_policy::automatic_reference)
    
    .def("present", &wgpu::Surface::Present
        , py::return_value_policy::automatic_reference)
    
    .def("unconfigure", &wgpu::Surface::Unconfigure
        , py::return_value_policy::automatic_reference)
    
    .def("set_label", &wgpu::Surface::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label_2", &wgpu::Surface::SetLabel2
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::Surface, Surface)

PYCLASS_BEGIN(m, wgpu::SwapChain, SwapChain) SwapChain
    .def("get_current_texture_view", &wgpu::SwapChain::GetCurrentTextureView
        , py::return_value_policy::automatic_reference)
    
    .def("get_current_texture", &wgpu::SwapChain::GetCurrentTexture
        , py::return_value_policy::automatic_reference)
    
    .def("present", &wgpu::SwapChain::Present
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::SwapChain, SwapChain)

PYCLASS_BEGIN(m, wgpu::Texture, Texture) Texture
    .def("create_view", &wgpu::Texture::CreateView
        , py::arg("descriptor") = nullptr
        , py::return_value_policy::automatic_reference)
    
    .def("create_error_view", &wgpu::Texture::CreateErrorView
        , py::arg("descriptor") = nullptr
        , py::return_value_policy::automatic_reference)
    
    .def("set_label", &wgpu::Texture::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label_2", &wgpu::Texture::SetLabel2
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("get_width", &wgpu::Texture::GetWidth
        , py::return_value_policy::automatic_reference)
    
    .def("get_height", &wgpu::Texture::GetHeight
        , py::return_value_policy::automatic_reference)
    
    .def("get_depth_or_array_layers", &wgpu::Texture::GetDepthOrArrayLayers
        , py::return_value_policy::automatic_reference)
    
    .def("get_mip_level_count", &wgpu::Texture::GetMipLevelCount
        , py::return_value_policy::automatic_reference)
    
    .def("get_sample_count", &wgpu::Texture::GetSampleCount
        , py::return_value_policy::automatic_reference)
    
    .def("get_dimension", &wgpu::Texture::GetDimension
        , py::return_value_policy::automatic_reference)
    
    .def("get_format", &wgpu::Texture::GetFormat
        , py::return_value_policy::automatic_reference)
    
    .def("get_usage", &wgpu::Texture::GetUsage
        , py::return_value_policy::automatic_reference)
    
    .def("destroy", &wgpu::Texture::Destroy
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::Texture, Texture)

PYCLASS_BEGIN(m, wgpu::TextureView, TextureView) TextureView
    .def("set_label", &wgpu::TextureView::SetLabel
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
    .def("set_label_2", &wgpu::TextureView::SetLabel2
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    
        ;
PYCLASS_END(m, wgpu::TextureView, TextureView)

PYCLASS_BEGIN(m, wgpu::INTERNAL__HAVE_EMDAWNWEBGPU_HEADER, INTERNAL__HAVE_EMDAWNWEBGPU_HEADER) INTERNAL__HAVE_EMDAWNWEBGPU_HEADER
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::INTERNAL__HAVE_EMDAWNWEBGPU_HEADER obj{};        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::INTERNAL__HAVE_EMDAWNWEBGPU_HEADER, INTERNAL__HAVE_EMDAWNWEBGPU_HEADER)

PYCLASS_BEGIN(m, wgpu::RequestAdapterOptions, RequestAdapterOptions) RequestAdapterOptions
    .def_readwrite("next_in_chain", &wgpu::RequestAdapterOptions::nextInChain)    
    .def_readwrite("compatible_surface", &wgpu::RequestAdapterOptions::compatibleSurface)    
    .def_readwrite("power_preference", &wgpu::RequestAdapterOptions::powerPreference)    
    .def_readwrite("backend_type", &wgpu::RequestAdapterOptions::backendType)    
    .def_readwrite("force_fallback_adapter", &wgpu::RequestAdapterOptions::forceFallbackAdapter)    
    .def_readwrite("compatibility_mode", &wgpu::RequestAdapterOptions::compatibilityMode)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::RequestAdapterOptions obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("compatible_surface"))        
        {        
            auto value = kwargs["compatible_surface"].cast<wgpu::Surface>();            
            obj.compatibleSurface = value;            
        }        
        if (kwargs.contains("power_preference"))        
        {        
            auto value = kwargs["power_preference"].cast<wgpu::PowerPreference>();            
            obj.powerPreference = value;            
        }        
        if (kwargs.contains("backend_type"))        
        {        
            auto value = kwargs["backend_type"].cast<wgpu::BackendType>();            
            obj.backendType = value;            
        }        
        if (kwargs.contains("force_fallback_adapter"))        
        {        
            auto value = kwargs["force_fallback_adapter"].cast<wgpu::Bool>();            
            obj.forceFallbackAdapter = value;            
        }        
        if (kwargs.contains("compatibility_mode"))        
        {        
            auto value = kwargs["compatibility_mode"].cast<wgpu::Bool>();            
            obj.compatibilityMode = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::RequestAdapterOptions, RequestAdapterOptions)

PYCLASS_BEGIN(m, wgpu::RequestAdapterCallbackInfo, RequestAdapterCallbackInfo) RequestAdapterCallbackInfo
    .def_readwrite("next_in_chain", &wgpu::RequestAdapterCallbackInfo::nextInChain)    
    .def_readwrite("mode", &wgpu::RequestAdapterCallbackInfo::mode)    
    .def_readwrite("userdata", &wgpu::RequestAdapterCallbackInfo::userdata)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::RequestAdapterCallbackInfo obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("mode"))        
        {        
            auto value = kwargs["mode"].cast<wgpu::CallbackMode>();            
            obj.mode = value;            
        }        
        if (kwargs.contains("userdata"))        
        {        
            auto value = kwargs["userdata"].cast<void *>();            
            obj.userdata = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::RequestAdapterCallbackInfo, RequestAdapterCallbackInfo)

PYCLASS_BEGIN(m, wgpu::AdapterInfo, AdapterInfo) AdapterInfo
    .def_readonly("next_in_chain", &wgpu::AdapterInfo::nextInChain)    
    .def_readonly("vendor", &wgpu::AdapterInfo::vendor)    
    .def_readonly("architecture", &wgpu::AdapterInfo::architecture)    
    .def_readonly("device", &wgpu::AdapterInfo::device)    
    .def_readonly("description", &wgpu::AdapterInfo::description)    
    .def_readonly("backend_type", &wgpu::AdapterInfo::backendType)    
    .def_readonly("adapter_type", &wgpu::AdapterInfo::adapterType)    
    .def_readonly("vendor_id", &wgpu::AdapterInfo::vendorID)    
    .def_readonly("device_id", &wgpu::AdapterInfo::deviceID)    
    .def_readonly("compatibility_mode", &wgpu::AdapterInfo::compatibilityMode)    
;
PYCLASS_END(m, wgpu::AdapterInfo, AdapterInfo)

PYCLASS_BEGIN(m, wgpu::AdapterProperties, AdapterProperties) AdapterProperties
    .def_readonly("next_in_chain", &wgpu::AdapterProperties::nextInChain)    
    .def_readonly("vendor_id", &wgpu::AdapterProperties::vendorID)    
    .def_readonly("vendor_name", &wgpu::AdapterProperties::vendorName)    
    .def_readonly("architecture", &wgpu::AdapterProperties::architecture)    
    .def_readonly("device_id", &wgpu::AdapterProperties::deviceID)    
    .def_readonly("name", &wgpu::AdapterProperties::name)    
    .def_readonly("driver_description", &wgpu::AdapterProperties::driverDescription)    
    .def_readonly("adapter_type", &wgpu::AdapterProperties::adapterType)    
    .def_readonly("backend_type", &wgpu::AdapterProperties::backendType)    
    .def_readonly("compatibility_mode", &wgpu::AdapterProperties::compatibilityMode)    
;
PYCLASS_END(m, wgpu::AdapterProperties, AdapterProperties)

PYCLASS_BEGIN(m, wgpu::DeviceDescriptor, DeviceDescriptor) DeviceDescriptor
    .def_readwrite("next_in_chain", &wgpu::DeviceDescriptor::nextInChain)    
    .def_property("label",    
        [](const wgpu::DeviceDescriptor& self) {        
            return self.label;            
        },        
        [](wgpu::DeviceDescriptor& self, char const *  source) {        
            self.label = strdup(source);            
        }        
    )    
    .def_readwrite("required_feature_count", &wgpu::DeviceDescriptor::requiredFeatureCount)    
    .def_readwrite("required_features", &wgpu::DeviceDescriptor::requiredFeatures)    
    .def_readwrite("required_limits", &wgpu::DeviceDescriptor::requiredLimits)    
    .def_readwrite("default_queue", &wgpu::DeviceDescriptor::defaultQueue)    
    .def_readwrite("device_lost_userdata", &wgpu::DeviceDescriptor::deviceLostUserdata)    
    .def_readwrite("device_lost_callback_info", &wgpu::DeviceDescriptor::deviceLostCallbackInfo)    
    .def_readwrite("uncaptured_error_callback_info", &wgpu::DeviceDescriptor::uncapturedErrorCallbackInfo)    
    .def_readwrite("device_lost_callback_info_2", &wgpu::DeviceDescriptor::deviceLostCallbackInfo2)    
    .def_readwrite("uncaptured_error_callback_info_2", &wgpu::DeviceDescriptor::uncapturedErrorCallbackInfo2)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::DeviceDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("label"))        
        {        
            auto value = kwargs["label"].cast<std::string>();            
            obj.label = strdup(value.c_str());            
        }        
        if (kwargs.contains("required_feature_count"))        
        {        
            auto value = kwargs["required_feature_count"].cast<size_t>();            
            obj.requiredFeatureCount = value;            
        }        
        if (kwargs.contains("required_features"))        
        {        
            auto _value = kwargs["required_features"].cast<std::vector<wgpu::FeatureName>>();            
            auto count = _value.size();            
            auto value = new wgpu::FeatureName[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.requiredFeatures = value;            
        }        
        if (kwargs.contains("required_limits"))        
        {        
            auto value = kwargs["required_limits"].cast<wgpu::RequiredLimits const *>();            
            obj.requiredLimits = value;            
        }        
        if (kwargs.contains("default_queue"))        
        {        
            auto value = kwargs["default_queue"].cast<wgpu::QueueDescriptor>();            
            obj.defaultQueue = value;            
        }        
        if (kwargs.contains("device_lost_userdata"))        
        {        
            auto value = kwargs["device_lost_userdata"].cast<void *>();            
            obj.deviceLostUserdata = value;            
        }        
        if (kwargs.contains("device_lost_callback_info"))        
        {        
            auto value = kwargs["device_lost_callback_info"].cast<wgpu::DeviceLostCallbackInfo>();            
            obj.deviceLostCallbackInfo = value;            
        }        
        if (kwargs.contains("uncaptured_error_callback_info"))        
        {        
            auto value = kwargs["uncaptured_error_callback_info"].cast<wgpu::UncapturedErrorCallbackInfo>();            
            obj.uncapturedErrorCallbackInfo = value;            
        }        
        if (kwargs.contains("device_lost_callback_info_2"))        
        {        
            auto value = kwargs["device_lost_callback_info_2"].cast<wgpu::DeviceLostCallbackInfo2>();            
            obj.deviceLostCallbackInfo2 = value;            
        }        
        if (kwargs.contains("uncaptured_error_callback_info_2"))        
        {        
            auto value = kwargs["uncaptured_error_callback_info_2"].cast<wgpu::UncapturedErrorCallbackInfo2>();            
            obj.uncapturedErrorCallbackInfo2 = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::DeviceDescriptor, DeviceDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::DawnTogglesDescriptor, ChainedStruct, DawnTogglesDescriptor) DawnTogglesDescriptor
    .def_readwrite("next_in_chain", &wgpu::DawnTogglesDescriptor::nextInChain)    
    .def_readwrite("enabled_toggle_count", &wgpu::DawnTogglesDescriptor::enabledToggleCount)    
    .def_readwrite("disabled_toggle_count", &wgpu::DawnTogglesDescriptor::disabledToggleCount)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::DawnTogglesDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("enabled_toggle_count"))        
        {        
            auto value = kwargs["enabled_toggle_count"].cast<size_t>();            
            obj.enabledToggleCount = value;            
        }        
        if (kwargs.contains("disabled_toggle_count"))        
        {        
            auto value = kwargs["disabled_toggle_count"].cast<size_t>();            
            obj.disabledToggleCount = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::DawnTogglesDescriptor, DawnTogglesDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::DawnCacheDeviceDescriptor, ChainedStruct, DawnCacheDeviceDescriptor) DawnCacheDeviceDescriptor
    .def_readwrite("next_in_chain", &wgpu::DawnCacheDeviceDescriptor::nextInChain)    
    .def_property("isolation_key",    
        [](const wgpu::DawnCacheDeviceDescriptor& self) {        
            return self.isolationKey;            
        },        
        [](wgpu::DawnCacheDeviceDescriptor& self, char const *  source) {        
            self.isolationKey = strdup(source);            
        }        
    )    
    .def_readwrite("function_userdata", &wgpu::DawnCacheDeviceDescriptor::functionUserdata)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::DawnCacheDeviceDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("isolation_key"))        
        {        
            auto value = kwargs["isolation_key"].cast<std::string>();            
            obj.isolationKey = strdup(value.c_str());            
        }        
        if (kwargs.contains("function_userdata"))        
        {        
            auto value = kwargs["function_userdata"].cast<void *>();            
            obj.functionUserdata = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::DawnCacheDeviceDescriptor, DawnCacheDeviceDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::DawnWGSLBlocklist, ChainedStruct, DawnWGSLBlocklist) DawnWGSLBlocklist
    .def_readwrite("next_in_chain", &wgpu::DawnWGSLBlocklist::nextInChain)    
    .def_readwrite("blocklisted_feature_count", &wgpu::DawnWGSLBlocklist::blocklistedFeatureCount)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::DawnWGSLBlocklist obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("blocklisted_feature_count"))        
        {        
            auto value = kwargs["blocklisted_feature_count"].cast<size_t>();            
            obj.blocklistedFeatureCount = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::DawnWGSLBlocklist, DawnWGSLBlocklist)

PYCLASS_BEGIN(m, wgpu::BindGroupEntry, BindGroupEntry) BindGroupEntry
    .def_readwrite("next_in_chain", &wgpu::BindGroupEntry::nextInChain)    
    .def_readwrite("binding", &wgpu::BindGroupEntry::binding)    
    .def_readwrite("buffer", &wgpu::BindGroupEntry::buffer)    
    .def_readwrite("offset", &wgpu::BindGroupEntry::offset)    
    .def_readwrite("size", &wgpu::BindGroupEntry::size)    
    .def_readwrite("sampler", &wgpu::BindGroupEntry::sampler)    
    .def_readwrite("texture_view", &wgpu::BindGroupEntry::textureView)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::BindGroupEntry obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
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
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::BindGroupEntry, BindGroupEntry)

PYCLASS_BEGIN(m, wgpu::BindGroupDescriptor, BindGroupDescriptor) BindGroupDescriptor
    .def_readwrite("next_in_chain", &wgpu::BindGroupDescriptor::nextInChain)    
    .def_property("label",    
        [](const wgpu::BindGroupDescriptor& self) {        
            return self.label;            
        },        
        [](wgpu::BindGroupDescriptor& self, char const *  source) {        
            self.label = strdup(source);            
        }        
    )    
    .def_readwrite("layout", &wgpu::BindGroupDescriptor::layout)    
    .def_readwrite("entry_count", &wgpu::BindGroupDescriptor::entryCount)    
    .def_readwrite("entries", &wgpu::BindGroupDescriptor::entries)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::BindGroupDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("label"))        
        {        
            auto value = kwargs["label"].cast<std::string>();            
            obj.label = strdup(value.c_str());            
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
            auto _value = kwargs["entries"].cast<std::vector<wgpu::BindGroupEntry>>();            
            auto count = _value.size();            
            auto value = new wgpu::BindGroupEntry[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.entries = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::BindGroupDescriptor, BindGroupDescriptor)

PYCLASS_BEGIN(m, wgpu::BufferBindingLayout, BufferBindingLayout) BufferBindingLayout
    .def_readwrite("next_in_chain", &wgpu::BufferBindingLayout::nextInChain)    
    .def_readwrite("type", &wgpu::BufferBindingLayout::type)    
    .def_readwrite("has_dynamic_offset", &wgpu::BufferBindingLayout::hasDynamicOffset)    
    .def_readwrite("min_binding_size", &wgpu::BufferBindingLayout::minBindingSize)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::BufferBindingLayout obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
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
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::BufferBindingLayout, BufferBindingLayout)

PYCLASS_BEGIN(m, wgpu::SamplerBindingLayout, SamplerBindingLayout) SamplerBindingLayout
    .def_readwrite("next_in_chain", &wgpu::SamplerBindingLayout::nextInChain)    
    .def_readwrite("type", &wgpu::SamplerBindingLayout::type)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SamplerBindingLayout obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("type"))        
        {        
            auto value = kwargs["type"].cast<wgpu::SamplerBindingType>();            
            obj.type = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SamplerBindingLayout, SamplerBindingLayout)

PYSUBCLASS_BEGIN(m, wgpu::StaticSamplerBindingLayout, ChainedStruct, StaticSamplerBindingLayout) StaticSamplerBindingLayout
    .def_readwrite("next_in_chain", &wgpu::StaticSamplerBindingLayout::nextInChain)    
    .def_readwrite("sampler", &wgpu::StaticSamplerBindingLayout::sampler)    
    .def_readwrite("sampled_texture_binding", &wgpu::StaticSamplerBindingLayout::sampledTextureBinding)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::StaticSamplerBindingLayout obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("sampler"))        
        {        
            auto value = kwargs["sampler"].cast<wgpu::Sampler>();            
            obj.sampler = value;            
        }        
        if (kwargs.contains("sampled_texture_binding"))        
        {        
            auto value = kwargs["sampled_texture_binding"].cast<uint32_t>();            
            obj.sampledTextureBinding = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::StaticSamplerBindingLayout, StaticSamplerBindingLayout)

PYCLASS_BEGIN(m, wgpu::TextureBindingLayout, TextureBindingLayout) TextureBindingLayout
    .def_readwrite("next_in_chain", &wgpu::TextureBindingLayout::nextInChain)    
    .def_readwrite("sample_type", &wgpu::TextureBindingLayout::sampleType)    
    .def_readwrite("view_dimension", &wgpu::TextureBindingLayout::viewDimension)    
    .def_readwrite("multisampled", &wgpu::TextureBindingLayout::multisampled)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::TextureBindingLayout obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
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
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::TextureBindingLayout, TextureBindingLayout)

PYCLASS_BEGIN(m, wgpu::SurfaceCapabilities, SurfaceCapabilities) SurfaceCapabilities
    .def_readonly("next_in_chain", &wgpu::SurfaceCapabilities::nextInChain)    
    .def_readonly("usages", &wgpu::SurfaceCapabilities::usages)    
    .def_readonly("format_count", &wgpu::SurfaceCapabilities::formatCount)    
    .def_readonly("formats", &wgpu::SurfaceCapabilities::formats)    
    .def_readonly("present_mode_count", &wgpu::SurfaceCapabilities::presentModeCount)    
    .def_readonly("present_modes", &wgpu::SurfaceCapabilities::presentModes)    
    .def_readonly("alpha_mode_count", &wgpu::SurfaceCapabilities::alphaModeCount)    
    .def_readonly("alpha_modes", &wgpu::SurfaceCapabilities::alphaModes)    
;
PYCLASS_END(m, wgpu::SurfaceCapabilities, SurfaceCapabilities)

PYCLASS_BEGIN(m, wgpu::SurfaceConfiguration, SurfaceConfiguration) SurfaceConfiguration
    .def_readwrite("next_in_chain", &wgpu::SurfaceConfiguration::nextInChain)    
    .def_readwrite("device", &wgpu::SurfaceConfiguration::device)    
    .def_readwrite("format", &wgpu::SurfaceConfiguration::format)    
    .def_readwrite("usage", &wgpu::SurfaceConfiguration::usage)    
    .def_readwrite("view_format_count", &wgpu::SurfaceConfiguration::viewFormatCount)    
    .def_readwrite("view_formats", &wgpu::SurfaceConfiguration::viewFormats)    
    .def_readwrite("alpha_mode", &wgpu::SurfaceConfiguration::alphaMode)    
    .def_readwrite("width", &wgpu::SurfaceConfiguration::width)    
    .def_readwrite("height", &wgpu::SurfaceConfiguration::height)    
    .def_readwrite("present_mode", &wgpu::SurfaceConfiguration::presentMode)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SurfaceConfiguration obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("device"))        
        {        
            auto value = kwargs["device"].cast<wgpu::Device>();            
            obj.device = value;            
        }        
        if (kwargs.contains("format"))        
        {        
            auto value = kwargs["format"].cast<wgpu::TextureFormat>();            
            obj.format = value;            
        }        
        if (kwargs.contains("usage"))        
        {        
            auto value = kwargs["usage"].cast<wgpu::TextureUsage>();            
            obj.usage = value;            
        }        
        if (kwargs.contains("view_format_count"))        
        {        
            auto value = kwargs["view_format_count"].cast<size_t>();            
            obj.viewFormatCount = value;            
        }        
        if (kwargs.contains("view_formats"))        
        {        
            auto _value = kwargs["view_formats"].cast<std::vector<wgpu::TextureFormat>>();            
            auto count = _value.size();            
            auto value = new wgpu::TextureFormat[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.viewFormats = value;            
        }        
        if (kwargs.contains("alpha_mode"))        
        {        
            auto value = kwargs["alpha_mode"].cast<wgpu::CompositeAlphaMode>();            
            obj.alphaMode = value;            
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
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SurfaceConfiguration, SurfaceConfiguration)

PYSUBCLASS_BEGIN(m, wgpu::ExternalTextureBindingEntry, ChainedStruct, ExternalTextureBindingEntry) ExternalTextureBindingEntry
    .def_readwrite("next_in_chain", &wgpu::ExternalTextureBindingEntry::nextInChain)    
    .def_readwrite("external_texture", &wgpu::ExternalTextureBindingEntry::externalTexture)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::ExternalTextureBindingEntry obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("external_texture"))        
        {        
            auto value = kwargs["external_texture"].cast<wgpu::ExternalTexture>();            
            obj.externalTexture = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::ExternalTextureBindingEntry, ExternalTextureBindingEntry)

PYSUBCLASS_BEGIN(m, wgpu::ExternalTextureBindingLayout, ChainedStruct, ExternalTextureBindingLayout) ExternalTextureBindingLayout
    .def_readwrite("next_in_chain", &wgpu::ExternalTextureBindingLayout::nextInChain)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::ExternalTextureBindingLayout obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::ExternalTextureBindingLayout, ExternalTextureBindingLayout)

PYCLASS_BEGIN(m, wgpu::StorageTextureBindingLayout, StorageTextureBindingLayout) StorageTextureBindingLayout
    .def_readwrite("next_in_chain", &wgpu::StorageTextureBindingLayout::nextInChain)    
    .def_readwrite("access", &wgpu::StorageTextureBindingLayout::access)    
    .def_readwrite("format", &wgpu::StorageTextureBindingLayout::format)    
    .def_readwrite("view_dimension", &wgpu::StorageTextureBindingLayout::viewDimension)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::StorageTextureBindingLayout obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("access"))        
        {        
            auto value = kwargs["access"].cast<wgpu::StorageTextureAccess>();            
            obj.access = value;            
        }        
        if (kwargs.contains("format"))        
        {        
            auto value = kwargs["format"].cast<wgpu::TextureFormat>();            
            obj.format = value;            
        }        
        if (kwargs.contains("view_dimension"))        
        {        
            auto value = kwargs["view_dimension"].cast<wgpu::TextureViewDimension>();            
            obj.viewDimension = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::StorageTextureBindingLayout, StorageTextureBindingLayout)

PYCLASS_BEGIN(m, wgpu::BindGroupLayoutEntry, BindGroupLayoutEntry) BindGroupLayoutEntry
    .def_readwrite("next_in_chain", &wgpu::BindGroupLayoutEntry::nextInChain)    
    .def_readwrite("binding", &wgpu::BindGroupLayoutEntry::binding)    
    .def_readwrite("visibility", &wgpu::BindGroupLayoutEntry::visibility)    
    .def_readwrite("buffer", &wgpu::BindGroupLayoutEntry::buffer)    
    .def_readwrite("sampler", &wgpu::BindGroupLayoutEntry::sampler)    
    .def_readwrite("texture", &wgpu::BindGroupLayoutEntry::texture)    
    .def_readwrite("storage_texture", &wgpu::BindGroupLayoutEntry::storageTexture)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::BindGroupLayoutEntry obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
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
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::BindGroupLayoutEntry, BindGroupLayoutEntry)

PYCLASS_BEGIN(m, wgpu::BindGroupLayoutDescriptor, BindGroupLayoutDescriptor) BindGroupLayoutDescriptor
    .def_readwrite("next_in_chain", &wgpu::BindGroupLayoutDescriptor::nextInChain)    
    .def_property("label",    
        [](const wgpu::BindGroupLayoutDescriptor& self) {        
            return self.label;            
        },        
        [](wgpu::BindGroupLayoutDescriptor& self, char const *  source) {        
            self.label = strdup(source);            
        }        
    )    
    .def_readwrite("entry_count", &wgpu::BindGroupLayoutDescriptor::entryCount)    
    .def_readwrite("entries", &wgpu::BindGroupLayoutDescriptor::entries)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::BindGroupLayoutDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("label"))        
        {        
            auto value = kwargs["label"].cast<std::string>();            
            obj.label = strdup(value.c_str());            
        }        
        if (kwargs.contains("entry_count"))        
        {        
            auto value = kwargs["entry_count"].cast<size_t>();            
            obj.entryCount = value;            
        }        
        if (kwargs.contains("entries"))        
        {        
            auto _value = kwargs["entries"].cast<std::vector<wgpu::BindGroupLayoutEntry>>();            
            auto count = _value.size();            
            auto value = new wgpu::BindGroupLayoutEntry[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.entries = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::BindGroupLayoutDescriptor, BindGroupLayoutDescriptor)

PYCLASS_BEGIN(m, wgpu::BlendComponent, BlendComponent) BlendComponent
    .def_readwrite("operation", &wgpu::BlendComponent::operation)    
    .def_readwrite("src_factor", &wgpu::BlendComponent::srcFactor)    
    .def_readwrite("dst_factor", &wgpu::BlendComponent::dstFactor)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::BlendComponent obj{};        
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
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::BlendComponent, BlendComponent)

PYCLASS_BEGIN(m, wgpu::BufferDescriptor, BufferDescriptor) BufferDescriptor
    .def_readwrite("next_in_chain", &wgpu::BufferDescriptor::nextInChain)    
    .def_property("label",    
        [](const wgpu::BufferDescriptor& self) {        
            return self.label;            
        },        
        [](wgpu::BufferDescriptor& self, char const *  source) {        
            self.label = strdup(source);            
        }        
    )    
    .def_readwrite("usage", &wgpu::BufferDescriptor::usage)    
    .def_readwrite("size", &wgpu::BufferDescriptor::size)    
    .def_readwrite("mapped_at_creation", &wgpu::BufferDescriptor::mappedAtCreation)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::BufferDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("label"))        
        {        
            auto value = kwargs["label"].cast<std::string>();            
            obj.label = strdup(value.c_str());            
        }        
        if (kwargs.contains("usage"))        
        {        
            auto value = kwargs["usage"].cast<wgpu::BufferUsage>();            
            obj.usage = value;            
        }        
        if (kwargs.contains("size"))        
        {        
            auto value = kwargs["size"].cast<uint64_t>();            
            obj.size = value;            
        }        
        if (kwargs.contains("mapped_at_creation"))        
        {        
            auto value = kwargs["mapped_at_creation"].cast<wgpu::Bool>();            
            obj.mappedAtCreation = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::BufferDescriptor, BufferDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::BufferHostMappedPointer, ChainedStruct, BufferHostMappedPointer) BufferHostMappedPointer
    .def_readwrite("next_in_chain", &wgpu::BufferHostMappedPointer::nextInChain)    
    .def_readwrite("pointer", &wgpu::BufferHostMappedPointer::pointer)    
    .def_readwrite("userdata", &wgpu::BufferHostMappedPointer::userdata)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::BufferHostMappedPointer obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("pointer"))        
        {        
            auto value = kwargs["pointer"].cast<void *>();            
            obj.pointer = value;            
        }        
        if (kwargs.contains("userdata"))        
        {        
            auto value = kwargs["userdata"].cast<void *>();            
            obj.userdata = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::BufferHostMappedPointer, BufferHostMappedPointer)

PYCLASS_BEGIN(m, wgpu::BufferMapCallbackInfo, BufferMapCallbackInfo) BufferMapCallbackInfo
    .def_readwrite("next_in_chain", &wgpu::BufferMapCallbackInfo::nextInChain)    
    .def_readwrite("mode", &wgpu::BufferMapCallbackInfo::mode)    
    .def_readwrite("userdata", &wgpu::BufferMapCallbackInfo::userdata)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::BufferMapCallbackInfo obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("mode"))        
        {        
            auto value = kwargs["mode"].cast<wgpu::CallbackMode>();            
            obj.mode = value;            
        }        
        if (kwargs.contains("userdata"))        
        {        
            auto value = kwargs["userdata"].cast<void *>();            
            obj.userdata = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::BufferMapCallbackInfo, BufferMapCallbackInfo)

PYCLASS_BEGIN(m, wgpu::Color, Color) Color
    .def_readwrite("r", &wgpu::Color::r)    
    .def_readwrite("g", &wgpu::Color::g)    
    .def_readwrite("b", &wgpu::Color::b)    
    .def_readwrite("a", &wgpu::Color::a)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::Color obj{};        
        if (kwargs.contains("r"))        
        {        
            auto value = kwargs["r"].cast<double>();            
            obj.r = value;            
        }        
        if (kwargs.contains("g"))        
        {        
            auto value = kwargs["g"].cast<double>();            
            obj.g = value;            
        }        
        if (kwargs.contains("b"))        
        {        
            auto value = kwargs["b"].cast<double>();            
            obj.b = value;            
        }        
        if (kwargs.contains("a"))        
        {        
            auto value = kwargs["a"].cast<double>();            
            obj.a = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::Color, Color)

PYCLASS_BEGIN(m, wgpu::ConstantEntry, ConstantEntry) ConstantEntry
    .def_readwrite("next_in_chain", &wgpu::ConstantEntry::nextInChain)    
    .def_property("key",    
        [](const wgpu::ConstantEntry& self) {        
            return self.key;            
        },        
        [](wgpu::ConstantEntry& self, char const *  source) {        
            self.key = strdup(source);            
        }        
    )    
    .def_readwrite("value", &wgpu::ConstantEntry::value)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::ConstantEntry obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("key"))        
        {        
            auto value = kwargs["key"].cast<std::string>();            
            obj.key = strdup(value.c_str());            
        }        
        if (kwargs.contains("value"))        
        {        
            auto value = kwargs["value"].cast<double>();            
            obj.value = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::ConstantEntry, ConstantEntry)

PYCLASS_BEGIN(m, wgpu::CommandBufferDescriptor, CommandBufferDescriptor) CommandBufferDescriptor
    .def_readwrite("next_in_chain", &wgpu::CommandBufferDescriptor::nextInChain)    
    .def_property("label",    
        [](const wgpu::CommandBufferDescriptor& self) {        
            return self.label;            
        },        
        [](wgpu::CommandBufferDescriptor& self, char const *  source) {        
            self.label = strdup(source);            
        }        
    )    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::CommandBufferDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("label"))        
        {        
            auto value = kwargs["label"].cast<std::string>();            
            obj.label = strdup(value.c_str());            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::CommandBufferDescriptor, CommandBufferDescriptor)

PYCLASS_BEGIN(m, wgpu::CommandEncoderDescriptor, CommandEncoderDescriptor) CommandEncoderDescriptor
    .def_readwrite("next_in_chain", &wgpu::CommandEncoderDescriptor::nextInChain)    
    .def_property("label",    
        [](const wgpu::CommandEncoderDescriptor& self) {        
            return self.label;            
        },        
        [](wgpu::CommandEncoderDescriptor& self, char const *  source) {        
            self.label = strdup(source);            
        }        
    )    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::CommandEncoderDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("label"))        
        {        
            auto value = kwargs["label"].cast<std::string>();            
            obj.label = strdup(value.c_str());            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::CommandEncoderDescriptor, CommandEncoderDescriptor)

PYCLASS_BEGIN(m, wgpu::CompilationInfo, CompilationInfo) CompilationInfo
    .def_readwrite("next_in_chain", &wgpu::CompilationInfo::nextInChain)    
    .def_readwrite("message_count", &wgpu::CompilationInfo::messageCount)    
    .def_readwrite("messages", &wgpu::CompilationInfo::messages)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::CompilationInfo obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("message_count"))        
        {        
            auto value = kwargs["message_count"].cast<size_t>();            
            obj.messageCount = value;            
        }        
        if (kwargs.contains("messages"))        
        {        
            auto _value = kwargs["messages"].cast<std::vector<wgpu::CompilationMessage>>();            
            auto count = _value.size();            
            auto value = new wgpu::CompilationMessage[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.messages = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::CompilationInfo, CompilationInfo)

PYCLASS_BEGIN(m, wgpu::CompilationInfoCallbackInfo, CompilationInfoCallbackInfo) CompilationInfoCallbackInfo
    .def_readwrite("next_in_chain", &wgpu::CompilationInfoCallbackInfo::nextInChain)    
    .def_readwrite("mode", &wgpu::CompilationInfoCallbackInfo::mode)    
    .def_readwrite("userdata", &wgpu::CompilationInfoCallbackInfo::userdata)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::CompilationInfoCallbackInfo obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("mode"))        
        {        
            auto value = kwargs["mode"].cast<wgpu::CallbackMode>();            
            obj.mode = value;            
        }        
        if (kwargs.contains("userdata"))        
        {        
            auto value = kwargs["userdata"].cast<void *>();            
            obj.userdata = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::CompilationInfoCallbackInfo, CompilationInfoCallbackInfo)

PYCLASS_BEGIN(m, wgpu::CompilationMessage, CompilationMessage) CompilationMessage
    .def_readwrite("next_in_chain", &wgpu::CompilationMessage::nextInChain)    
    .def_property("message",    
        [](const wgpu::CompilationMessage& self) {        
            return self.message;            
        },        
        [](wgpu::CompilationMessage& self, char const *  source) {        
            self.message = strdup(source);            
        }        
    )    
    .def_readwrite("type", &wgpu::CompilationMessage::type)    
    .def_readwrite("line_num", &wgpu::CompilationMessage::lineNum)    
    .def_readwrite("line_pos", &wgpu::CompilationMessage::linePos)    
    .def_readwrite("offset", &wgpu::CompilationMessage::offset)    
    .def_readwrite("length", &wgpu::CompilationMessage::length)    
    .def_readwrite("utf16_line_pos", &wgpu::CompilationMessage::utf16LinePos)    
    .def_readwrite("utf16_offset", &wgpu::CompilationMessage::utf16Offset)    
    .def_readwrite("utf16_length", &wgpu::CompilationMessage::utf16Length)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::CompilationMessage obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("message"))        
        {        
            auto value = kwargs["message"].cast<std::string>();            
            obj.message = strdup(value.c_str());            
        }        
        if (kwargs.contains("type"))        
        {        
            auto value = kwargs["type"].cast<wgpu::CompilationMessageType>();            
            obj.type = value;            
        }        
        if (kwargs.contains("line_num"))        
        {        
            auto value = kwargs["line_num"].cast<uint64_t>();            
            obj.lineNum = value;            
        }        
        if (kwargs.contains("line_pos"))        
        {        
            auto value = kwargs["line_pos"].cast<uint64_t>();            
            obj.linePos = value;            
        }        
        if (kwargs.contains("offset"))        
        {        
            auto value = kwargs["offset"].cast<uint64_t>();            
            obj.offset = value;            
        }        
        if (kwargs.contains("length"))        
        {        
            auto value = kwargs["length"].cast<uint64_t>();            
            obj.length = value;            
        }        
        if (kwargs.contains("utf16_line_pos"))        
        {        
            auto value = kwargs["utf16_line_pos"].cast<uint64_t>();            
            obj.utf16LinePos = value;            
        }        
        if (kwargs.contains("utf16_offset"))        
        {        
            auto value = kwargs["utf16_offset"].cast<uint64_t>();            
            obj.utf16Offset = value;            
        }        
        if (kwargs.contains("utf16_length"))        
        {        
            auto value = kwargs["utf16_length"].cast<uint64_t>();            
            obj.utf16Length = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::CompilationMessage, CompilationMessage)

PYCLASS_BEGIN(m, wgpu::ComputePassDescriptor, ComputePassDescriptor) ComputePassDescriptor
    .def_readwrite("next_in_chain", &wgpu::ComputePassDescriptor::nextInChain)    
    .def_property("label",    
        [](const wgpu::ComputePassDescriptor& self) {        
            return self.label;            
        },        
        [](wgpu::ComputePassDescriptor& self, char const *  source) {        
            self.label = strdup(source);            
        }        
    )    
    .def_readwrite("timestamp_writes", &wgpu::ComputePassDescriptor::timestampWrites)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::ComputePassDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("label"))        
        {        
            auto value = kwargs["label"].cast<std::string>();            
            obj.label = strdup(value.c_str());            
        }        
        if (kwargs.contains("timestamp_writes"))        
        {        
            auto value = kwargs["timestamp_writes"].cast<wgpu::ComputePassTimestampWrites const *>();            
            obj.timestampWrites = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::ComputePassDescriptor, ComputePassDescriptor)

PYCLASS_BEGIN(m, wgpu::ComputePassTimestampWrites, ComputePassTimestampWrites) ComputePassTimestampWrites
    .def_readwrite("query_set", &wgpu::ComputePassTimestampWrites::querySet)    
    .def_readwrite("beginning_of_pass_write_index", &wgpu::ComputePassTimestampWrites::beginningOfPassWriteIndex)    
    .def_readwrite("end_of_pass_write_index", &wgpu::ComputePassTimestampWrites::endOfPassWriteIndex)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::ComputePassTimestampWrites obj{};        
        if (kwargs.contains("query_set"))        
        {        
            auto value = kwargs["query_set"].cast<wgpu::QuerySet>();            
            obj.querySet = value;            
        }        
        if (kwargs.contains("beginning_of_pass_write_index"))        
        {        
            auto value = kwargs["beginning_of_pass_write_index"].cast<uint32_t>();            
            obj.beginningOfPassWriteIndex = value;            
        }        
        if (kwargs.contains("end_of_pass_write_index"))        
        {        
            auto value = kwargs["end_of_pass_write_index"].cast<uint32_t>();            
            obj.endOfPassWriteIndex = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::ComputePassTimestampWrites, ComputePassTimestampWrites)

PYCLASS_BEGIN(m, wgpu::ComputePipelineDescriptor, ComputePipelineDescriptor) ComputePipelineDescriptor
    .def_readwrite("next_in_chain", &wgpu::ComputePipelineDescriptor::nextInChain)    
    .def_property("label",    
        [](const wgpu::ComputePipelineDescriptor& self) {        
            return self.label;            
        },        
        [](wgpu::ComputePipelineDescriptor& self, char const *  source) {        
            self.label = strdup(source);            
        }        
    )    
    .def_readwrite("layout", &wgpu::ComputePipelineDescriptor::layout)    
    .def_readwrite("compute", &wgpu::ComputePipelineDescriptor::compute)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::ComputePipelineDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("label"))        
        {        
            auto value = kwargs["label"].cast<std::string>();            
            obj.label = strdup(value.c_str());            
        }        
        if (kwargs.contains("layout"))        
        {        
            auto value = kwargs["layout"].cast<wgpu::PipelineLayout>();            
            obj.layout = value;            
        }        
        if (kwargs.contains("compute"))        
        {        
            auto value = kwargs["compute"].cast<wgpu::ProgrammableStageDescriptor>();            
            obj.compute = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::ComputePipelineDescriptor, ComputePipelineDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::DawnComputePipelineFullSubgroups, ChainedStruct, DawnComputePipelineFullSubgroups) DawnComputePipelineFullSubgroups
    .def_readwrite("next_in_chain", &wgpu::DawnComputePipelineFullSubgroups::nextInChain)    
    .def_readwrite("requires_full_subgroups", &wgpu::DawnComputePipelineFullSubgroups::requiresFullSubgroups)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::DawnComputePipelineFullSubgroups obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("requires_full_subgroups"))        
        {        
            auto value = kwargs["requires_full_subgroups"].cast<wgpu::Bool>();            
            obj.requiresFullSubgroups = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::DawnComputePipelineFullSubgroups, DawnComputePipelineFullSubgroups)

PYCLASS_BEGIN(m, wgpu::CopyTextureForBrowserOptions, CopyTextureForBrowserOptions) CopyTextureForBrowserOptions
    .def_readwrite("next_in_chain", &wgpu::CopyTextureForBrowserOptions::nextInChain)    
    .def_readwrite("flip_y", &wgpu::CopyTextureForBrowserOptions::flipY)    
    .def_readwrite("needs_color_space_conversion", &wgpu::CopyTextureForBrowserOptions::needsColorSpaceConversion)    
    .def_readwrite("src_alpha_mode", &wgpu::CopyTextureForBrowserOptions::srcAlphaMode)    
    .def_readwrite("src_transfer_function_parameters", &wgpu::CopyTextureForBrowserOptions::srcTransferFunctionParameters)    
    .def_readwrite("conversion_matrix", &wgpu::CopyTextureForBrowserOptions::conversionMatrix)    
    .def_readwrite("dst_transfer_function_parameters", &wgpu::CopyTextureForBrowserOptions::dstTransferFunctionParameters)    
    .def_readwrite("dst_alpha_mode", &wgpu::CopyTextureForBrowserOptions::dstAlphaMode)    
    .def_readwrite("internal_usage", &wgpu::CopyTextureForBrowserOptions::internalUsage)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::CopyTextureForBrowserOptions obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("flip_y"))        
        {        
            auto value = kwargs["flip_y"].cast<wgpu::Bool>();            
            obj.flipY = value;            
        }        
        if (kwargs.contains("needs_color_space_conversion"))        
        {        
            auto value = kwargs["needs_color_space_conversion"].cast<wgpu::Bool>();            
            obj.needsColorSpaceConversion = value;            
        }        
        if (kwargs.contains("src_alpha_mode"))        
        {        
            auto value = kwargs["src_alpha_mode"].cast<wgpu::AlphaMode>();            
            obj.srcAlphaMode = value;            
        }        
        if (kwargs.contains("src_transfer_function_parameters"))        
        {        
            auto _value = kwargs["src_transfer_function_parameters"].cast<std::vector<float>>();            
            auto count = _value.size();            
            auto value = new float[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.srcTransferFunctionParameters = value;            
        }        
        if (kwargs.contains("conversion_matrix"))        
        {        
            auto _value = kwargs["conversion_matrix"].cast<std::vector<float>>();            
            auto count = _value.size();            
            auto value = new float[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.conversionMatrix = value;            
        }        
        if (kwargs.contains("dst_transfer_function_parameters"))        
        {        
            auto _value = kwargs["dst_transfer_function_parameters"].cast<std::vector<float>>();            
            auto count = _value.size();            
            auto value = new float[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.dstTransferFunctionParameters = value;            
        }        
        if (kwargs.contains("dst_alpha_mode"))        
        {        
            auto value = kwargs["dst_alpha_mode"].cast<wgpu::AlphaMode>();            
            obj.dstAlphaMode = value;            
        }        
        if (kwargs.contains("internal_usage"))        
        {        
            auto value = kwargs["internal_usage"].cast<wgpu::Bool>();            
            obj.internalUsage = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::CopyTextureForBrowserOptions, CopyTextureForBrowserOptions)

PYCLASS_BEGIN(m, wgpu::CreateComputePipelineAsyncCallbackInfo, CreateComputePipelineAsyncCallbackInfo) CreateComputePipelineAsyncCallbackInfo
    .def_readwrite("next_in_chain", &wgpu::CreateComputePipelineAsyncCallbackInfo::nextInChain)    
    .def_readwrite("mode", &wgpu::CreateComputePipelineAsyncCallbackInfo::mode)    
    .def_readwrite("userdata", &wgpu::CreateComputePipelineAsyncCallbackInfo::userdata)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::CreateComputePipelineAsyncCallbackInfo obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("mode"))        
        {        
            auto value = kwargs["mode"].cast<wgpu::CallbackMode>();            
            obj.mode = value;            
        }        
        if (kwargs.contains("userdata"))        
        {        
            auto value = kwargs["userdata"].cast<void *>();            
            obj.userdata = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::CreateComputePipelineAsyncCallbackInfo, CreateComputePipelineAsyncCallbackInfo)

PYCLASS_BEGIN(m, wgpu::CreateRenderPipelineAsyncCallbackInfo, CreateRenderPipelineAsyncCallbackInfo) CreateRenderPipelineAsyncCallbackInfo
    .def_readwrite("next_in_chain", &wgpu::CreateRenderPipelineAsyncCallbackInfo::nextInChain)    
    .def_readwrite("mode", &wgpu::CreateRenderPipelineAsyncCallbackInfo::mode)    
    .def_readwrite("userdata", &wgpu::CreateRenderPipelineAsyncCallbackInfo::userdata)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::CreateRenderPipelineAsyncCallbackInfo obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("mode"))        
        {        
            auto value = kwargs["mode"].cast<wgpu::CallbackMode>();            
            obj.mode = value;            
        }        
        if (kwargs.contains("userdata"))        
        {        
            auto value = kwargs["userdata"].cast<void *>();            
            obj.userdata = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::CreateRenderPipelineAsyncCallbackInfo, CreateRenderPipelineAsyncCallbackInfo)

PYCLASS_BEGIN(m, wgpu::AHardwareBufferProperties, AHardwareBufferProperties) AHardwareBufferProperties
    .def_readwrite("y_cb_cr_info", &wgpu::AHardwareBufferProperties::yCbCrInfo)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::AHardwareBufferProperties obj{};        
        if (kwargs.contains("y_cb_cr_info"))        
        {        
            auto value = kwargs["y_cb_cr_info"].cast<wgpu::YCbCrVkDescriptor>();            
            obj.yCbCrInfo = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::AHardwareBufferProperties, AHardwareBufferProperties)

PYCLASS_BEGIN(m, wgpu::DeviceLostCallbackInfo, DeviceLostCallbackInfo) DeviceLostCallbackInfo
    .def_readwrite("next_in_chain", &wgpu::DeviceLostCallbackInfo::nextInChain)    
    .def_readwrite("mode", &wgpu::DeviceLostCallbackInfo::mode)    
    .def_readwrite("userdata", &wgpu::DeviceLostCallbackInfo::userdata)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::DeviceLostCallbackInfo obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("mode"))        
        {        
            auto value = kwargs["mode"].cast<wgpu::CallbackMode>();            
            obj.mode = value;            
        }        
        if (kwargs.contains("userdata"))        
        {        
            auto value = kwargs["userdata"].cast<void *>();            
            obj.userdata = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::DeviceLostCallbackInfo, DeviceLostCallbackInfo)

PYCLASS_BEGIN(m, wgpu::UncapturedErrorCallbackInfo, UncapturedErrorCallbackInfo) UncapturedErrorCallbackInfo
    .def_readwrite("next_in_chain", &wgpu::UncapturedErrorCallbackInfo::nextInChain)    
    .def_readwrite("userdata", &wgpu::UncapturedErrorCallbackInfo::userdata)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::UncapturedErrorCallbackInfo obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("userdata"))        
        {        
            auto value = kwargs["userdata"].cast<void *>();            
            obj.userdata = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::UncapturedErrorCallbackInfo, UncapturedErrorCallbackInfo)

PYCLASS_BEGIN(m, wgpu::PopErrorScopeCallbackInfo, PopErrorScopeCallbackInfo) PopErrorScopeCallbackInfo
    .def_readwrite("next_in_chain", &wgpu::PopErrorScopeCallbackInfo::nextInChain)    
    .def_readwrite("mode", &wgpu::PopErrorScopeCallbackInfo::mode)    
    .def_readwrite("userdata", &wgpu::PopErrorScopeCallbackInfo::userdata)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::PopErrorScopeCallbackInfo obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("mode"))        
        {        
            auto value = kwargs["mode"].cast<wgpu::CallbackMode>();            
            obj.mode = value;            
        }        
        if (kwargs.contains("userdata"))        
        {        
            auto value = kwargs["userdata"].cast<void *>();            
            obj.userdata = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::PopErrorScopeCallbackInfo, PopErrorScopeCallbackInfo)

PYCLASS_BEGIN(m, wgpu::Limits, Limits) Limits
    .def_readwrite("max_texture_dimension_1d", &wgpu::Limits::maxTextureDimension1D)    
    .def_readwrite("max_texture_dimension_2d", &wgpu::Limits::maxTextureDimension2D)    
    .def_readwrite("max_texture_dimension_3d", &wgpu::Limits::maxTextureDimension3D)    
    .def_readwrite("max_texture_array_layers", &wgpu::Limits::maxTextureArrayLayers)    
    .def_readwrite("max_bind_groups", &wgpu::Limits::maxBindGroups)    
    .def_readwrite("max_bind_groups_plus_vertex_buffers", &wgpu::Limits::maxBindGroupsPlusVertexBuffers)    
    .def_readwrite("max_bindings_per_bind_group", &wgpu::Limits::maxBindingsPerBindGroup)    
    .def_readwrite("max_dynamic_uniform_buffers_per_pipeline_layout", &wgpu::Limits::maxDynamicUniformBuffersPerPipelineLayout)    
    .def_readwrite("max_dynamic_storage_buffers_per_pipeline_layout", &wgpu::Limits::maxDynamicStorageBuffersPerPipelineLayout)    
    .def_readwrite("max_sampled_textures_per_shader_stage", &wgpu::Limits::maxSampledTexturesPerShaderStage)    
    .def_readwrite("max_samplers_per_shader_stage", &wgpu::Limits::maxSamplersPerShaderStage)    
    .def_readwrite("max_storage_buffers_per_shader_stage", &wgpu::Limits::maxStorageBuffersPerShaderStage)    
    .def_readwrite("max_storage_textures_per_shader_stage", &wgpu::Limits::maxStorageTexturesPerShaderStage)    
    .def_readwrite("max_uniform_buffers_per_shader_stage", &wgpu::Limits::maxUniformBuffersPerShaderStage)    
    .def_readwrite("max_uniform_buffer_binding_size", &wgpu::Limits::maxUniformBufferBindingSize)    
    .def_readwrite("max_storage_buffer_binding_size", &wgpu::Limits::maxStorageBufferBindingSize)    
    .def_readwrite("min_uniform_buffer_offset_alignment", &wgpu::Limits::minUniformBufferOffsetAlignment)    
    .def_readwrite("min_storage_buffer_offset_alignment", &wgpu::Limits::minStorageBufferOffsetAlignment)    
    .def_readwrite("max_vertex_buffers", &wgpu::Limits::maxVertexBuffers)    
    .def_readwrite("max_buffer_size", &wgpu::Limits::maxBufferSize)    
    .def_readwrite("max_vertex_attributes", &wgpu::Limits::maxVertexAttributes)    
    .def_readwrite("max_vertex_buffer_array_stride", &wgpu::Limits::maxVertexBufferArrayStride)    
    .def_readwrite("max_inter_stage_shader_components", &wgpu::Limits::maxInterStageShaderComponents)    
    .def_readwrite("max_inter_stage_shader_variables", &wgpu::Limits::maxInterStageShaderVariables)    
    .def_readwrite("max_color_attachments", &wgpu::Limits::maxColorAttachments)    
    .def_readwrite("max_color_attachment_bytes_per_sample", &wgpu::Limits::maxColorAttachmentBytesPerSample)    
    .def_readwrite("max_compute_workgroup_storage_size", &wgpu::Limits::maxComputeWorkgroupStorageSize)    
    .def_readwrite("max_compute_invocations_per_workgroup", &wgpu::Limits::maxComputeInvocationsPerWorkgroup)    
    .def_readwrite("max_compute_workgroup_size_x", &wgpu::Limits::maxComputeWorkgroupSizeX)    
    .def_readwrite("max_compute_workgroup_size_y", &wgpu::Limits::maxComputeWorkgroupSizeY)    
    .def_readwrite("max_compute_workgroup_size_z", &wgpu::Limits::maxComputeWorkgroupSizeZ)    
    .def_readwrite("max_compute_workgroups_per_dimension", &wgpu::Limits::maxComputeWorkgroupsPerDimension)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::Limits obj{};        
        if (kwargs.contains("max_texture_dimension_1d"))        
        {        
            auto value = kwargs["max_texture_dimension_1d"].cast<uint32_t>();            
            obj.maxTextureDimension1D = value;            
        }        
        if (kwargs.contains("max_texture_dimension_2d"))        
        {        
            auto value = kwargs["max_texture_dimension_2d"].cast<uint32_t>();            
            obj.maxTextureDimension2D = value;            
        }        
        if (kwargs.contains("max_texture_dimension_3d"))        
        {        
            auto value = kwargs["max_texture_dimension_3d"].cast<uint32_t>();            
            obj.maxTextureDimension3D = value;            
        }        
        if (kwargs.contains("max_texture_array_layers"))        
        {        
            auto value = kwargs["max_texture_array_layers"].cast<uint32_t>();            
            obj.maxTextureArrayLayers = value;            
        }        
        if (kwargs.contains("max_bind_groups"))        
        {        
            auto value = kwargs["max_bind_groups"].cast<uint32_t>();            
            obj.maxBindGroups = value;            
        }        
        if (kwargs.contains("max_bind_groups_plus_vertex_buffers"))        
        {        
            auto value = kwargs["max_bind_groups_plus_vertex_buffers"].cast<uint32_t>();            
            obj.maxBindGroupsPlusVertexBuffers = value;            
        }        
        if (kwargs.contains("max_bindings_per_bind_group"))        
        {        
            auto value = kwargs["max_bindings_per_bind_group"].cast<uint32_t>();            
            obj.maxBindingsPerBindGroup = value;            
        }        
        if (kwargs.contains("max_dynamic_uniform_buffers_per_pipeline_layout"))        
        {        
            auto value = kwargs["max_dynamic_uniform_buffers_per_pipeline_layout"].cast<uint32_t>();            
            obj.maxDynamicUniformBuffersPerPipelineLayout = value;            
        }        
        if (kwargs.contains("max_dynamic_storage_buffers_per_pipeline_layout"))        
        {        
            auto value = kwargs["max_dynamic_storage_buffers_per_pipeline_layout"].cast<uint32_t>();            
            obj.maxDynamicStorageBuffersPerPipelineLayout = value;            
        }        
        if (kwargs.contains("max_sampled_textures_per_shader_stage"))        
        {        
            auto value = kwargs["max_sampled_textures_per_shader_stage"].cast<uint32_t>();            
            obj.maxSampledTexturesPerShaderStage = value;            
        }        
        if (kwargs.contains("max_samplers_per_shader_stage"))        
        {        
            auto value = kwargs["max_samplers_per_shader_stage"].cast<uint32_t>();            
            obj.maxSamplersPerShaderStage = value;            
        }        
        if (kwargs.contains("max_storage_buffers_per_shader_stage"))        
        {        
            auto value = kwargs["max_storage_buffers_per_shader_stage"].cast<uint32_t>();            
            obj.maxStorageBuffersPerShaderStage = value;            
        }        
        if (kwargs.contains("max_storage_textures_per_shader_stage"))        
        {        
            auto value = kwargs["max_storage_textures_per_shader_stage"].cast<uint32_t>();            
            obj.maxStorageTexturesPerShaderStage = value;            
        }        
        if (kwargs.contains("max_uniform_buffers_per_shader_stage"))        
        {        
            auto value = kwargs["max_uniform_buffers_per_shader_stage"].cast<uint32_t>();            
            obj.maxUniformBuffersPerShaderStage = value;            
        }        
        if (kwargs.contains("max_uniform_buffer_binding_size"))        
        {        
            auto value = kwargs["max_uniform_buffer_binding_size"].cast<uint64_t>();            
            obj.maxUniformBufferBindingSize = value;            
        }        
        if (kwargs.contains("max_storage_buffer_binding_size"))        
        {        
            auto value = kwargs["max_storage_buffer_binding_size"].cast<uint64_t>();            
            obj.maxStorageBufferBindingSize = value;            
        }        
        if (kwargs.contains("min_uniform_buffer_offset_alignment"))        
        {        
            auto value = kwargs["min_uniform_buffer_offset_alignment"].cast<uint32_t>();            
            obj.minUniformBufferOffsetAlignment = value;            
        }        
        if (kwargs.contains("min_storage_buffer_offset_alignment"))        
        {        
            auto value = kwargs["min_storage_buffer_offset_alignment"].cast<uint32_t>();            
            obj.minStorageBufferOffsetAlignment = value;            
        }        
        if (kwargs.contains("max_vertex_buffers"))        
        {        
            auto value = kwargs["max_vertex_buffers"].cast<uint32_t>();            
            obj.maxVertexBuffers = value;            
        }        
        if (kwargs.contains("max_buffer_size"))        
        {        
            auto value = kwargs["max_buffer_size"].cast<uint64_t>();            
            obj.maxBufferSize = value;            
        }        
        if (kwargs.contains("max_vertex_attributes"))        
        {        
            auto value = kwargs["max_vertex_attributes"].cast<uint32_t>();            
            obj.maxVertexAttributes = value;            
        }        
        if (kwargs.contains("max_vertex_buffer_array_stride"))        
        {        
            auto value = kwargs["max_vertex_buffer_array_stride"].cast<uint32_t>();            
            obj.maxVertexBufferArrayStride = value;            
        }        
        if (kwargs.contains("max_inter_stage_shader_components"))        
        {        
            auto value = kwargs["max_inter_stage_shader_components"].cast<uint32_t>();            
            obj.maxInterStageShaderComponents = value;            
        }        
        if (kwargs.contains("max_inter_stage_shader_variables"))        
        {        
            auto value = kwargs["max_inter_stage_shader_variables"].cast<uint32_t>();            
            obj.maxInterStageShaderVariables = value;            
        }        
        if (kwargs.contains("max_color_attachments"))        
        {        
            auto value = kwargs["max_color_attachments"].cast<uint32_t>();            
            obj.maxColorAttachments = value;            
        }        
        if (kwargs.contains("max_color_attachment_bytes_per_sample"))        
        {        
            auto value = kwargs["max_color_attachment_bytes_per_sample"].cast<uint32_t>();            
            obj.maxColorAttachmentBytesPerSample = value;            
        }        
        if (kwargs.contains("max_compute_workgroup_storage_size"))        
        {        
            auto value = kwargs["max_compute_workgroup_storage_size"].cast<uint32_t>();            
            obj.maxComputeWorkgroupStorageSize = value;            
        }        
        if (kwargs.contains("max_compute_invocations_per_workgroup"))        
        {        
            auto value = kwargs["max_compute_invocations_per_workgroup"].cast<uint32_t>();            
            obj.maxComputeInvocationsPerWorkgroup = value;            
        }        
        if (kwargs.contains("max_compute_workgroup_size_x"))        
        {        
            auto value = kwargs["max_compute_workgroup_size_x"].cast<uint32_t>();            
            obj.maxComputeWorkgroupSizeX = value;            
        }        
        if (kwargs.contains("max_compute_workgroup_size_y"))        
        {        
            auto value = kwargs["max_compute_workgroup_size_y"].cast<uint32_t>();            
            obj.maxComputeWorkgroupSizeY = value;            
        }        
        if (kwargs.contains("max_compute_workgroup_size_z"))        
        {        
            auto value = kwargs["max_compute_workgroup_size_z"].cast<uint32_t>();            
            obj.maxComputeWorkgroupSizeZ = value;            
        }        
        if (kwargs.contains("max_compute_workgroups_per_dimension"))        
        {        
            auto value = kwargs["max_compute_workgroups_per_dimension"].cast<uint32_t>();            
            obj.maxComputeWorkgroupsPerDimension = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::Limits, Limits)

PYSUBCLASS_BEGIN(m, wgpu::DawnExperimentalSubgroupLimits, ChainedStructOut, DawnExperimentalSubgroupLimits) DawnExperimentalSubgroupLimits
    .def_readonly("next_in_chain", &wgpu::DawnExperimentalSubgroupLimits::nextInChain)    
    .def_readonly("min_subgroup_size", &wgpu::DawnExperimentalSubgroupLimits::minSubgroupSize)    
    .def_readonly("max_subgroup_size", &wgpu::DawnExperimentalSubgroupLimits::maxSubgroupSize)    
;
PYCLASS_END(m, wgpu::DawnExperimentalSubgroupLimits, DawnExperimentalSubgroupLimits)

PYCLASS_BEGIN(m, wgpu::RequiredLimits, RequiredLimits) RequiredLimits
    .def_readwrite("next_in_chain", &wgpu::RequiredLimits::nextInChain)    
    .def_readwrite("limits", &wgpu::RequiredLimits::limits)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::RequiredLimits obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("limits"))        
        {        
            auto value = kwargs["limits"].cast<wgpu::Limits>();            
            obj.limits = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::RequiredLimits, RequiredLimits)

PYCLASS_BEGIN(m, wgpu::SupportedLimits, SupportedLimits) SupportedLimits
    .def_readonly("next_in_chain", &wgpu::SupportedLimits::nextInChain)    
    .def_readonly("limits", &wgpu::SupportedLimits::limits)    
;
PYCLASS_END(m, wgpu::SupportedLimits, SupportedLimits)

PYCLASS_BEGIN(m, wgpu::Extent2D, Extent2D) Extent2D
    .def_readwrite("width", &wgpu::Extent2D::width)    
    .def_readwrite("height", &wgpu::Extent2D::height)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::Extent2D obj{};        
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
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::Extent2D, Extent2D)

PYCLASS_BEGIN(m, wgpu::Extent3D, Extent3D) Extent3D
    .def_readwrite("width", &wgpu::Extent3D::width)    
    .def_readwrite("height", &wgpu::Extent3D::height)    
    .def_readwrite("depth_or_array_layers", &wgpu::Extent3D::depthOrArrayLayers)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::Extent3D obj{};        
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
        if (kwargs.contains("depth_or_array_layers"))        
        {        
            auto value = kwargs["depth_or_array_layers"].cast<uint32_t>();            
            obj.depthOrArrayLayers = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::Extent3D, Extent3D)

PYCLASS_BEGIN(m, wgpu::ExternalTextureDescriptor, ExternalTextureDescriptor) ExternalTextureDescriptor
    .def_readwrite("next_in_chain", &wgpu::ExternalTextureDescriptor::nextInChain)    
    .def_property("label",    
        [](const wgpu::ExternalTextureDescriptor& self) {        
            return self.label;            
        },        
        [](wgpu::ExternalTextureDescriptor& self, char const *  source) {        
            self.label = strdup(source);            
        }        
    )    
    .def_readwrite("plane_0", &wgpu::ExternalTextureDescriptor::plane0)    
    .def_readwrite("plane_1", &wgpu::ExternalTextureDescriptor::plane1)    
    .def_readwrite("visible_origin", &wgpu::ExternalTextureDescriptor::visibleOrigin)    
    .def_readwrite("visible_size", &wgpu::ExternalTextureDescriptor::visibleSize)    
    .def_readwrite("do_yuv_to_rgb_conversion_only", &wgpu::ExternalTextureDescriptor::doYuvToRgbConversionOnly)    
    .def_readwrite("yuv_to_rgb_conversion_matrix", &wgpu::ExternalTextureDescriptor::yuvToRgbConversionMatrix)    
    .def_readwrite("src_transfer_function_parameters", &wgpu::ExternalTextureDescriptor::srcTransferFunctionParameters)    
    .def_readwrite("dst_transfer_function_parameters", &wgpu::ExternalTextureDescriptor::dstTransferFunctionParameters)    
    .def_readwrite("gamut_conversion_matrix", &wgpu::ExternalTextureDescriptor::gamutConversionMatrix)    
    .def_readwrite("mirrored", &wgpu::ExternalTextureDescriptor::mirrored)    
    .def_readwrite("rotation", &wgpu::ExternalTextureDescriptor::rotation)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::ExternalTextureDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("label"))        
        {        
            auto value = kwargs["label"].cast<std::string>();            
            obj.label = strdup(value.c_str());            
        }        
        if (kwargs.contains("plane_0"))        
        {        
            auto value = kwargs["plane_0"].cast<wgpu::TextureView>();            
            obj.plane0 = value;            
        }        
        if (kwargs.contains("plane_1"))        
        {        
            auto value = kwargs["plane_1"].cast<wgpu::TextureView>();            
            obj.plane1 = value;            
        }        
        if (kwargs.contains("visible_origin"))        
        {        
            auto value = kwargs["visible_origin"].cast<wgpu::Origin2D>();            
            obj.visibleOrigin = value;            
        }        
        if (kwargs.contains("visible_size"))        
        {        
            auto value = kwargs["visible_size"].cast<wgpu::Extent2D>();            
            obj.visibleSize = value;            
        }        
        if (kwargs.contains("do_yuv_to_rgb_conversion_only"))        
        {        
            auto value = kwargs["do_yuv_to_rgb_conversion_only"].cast<wgpu::Bool>();            
            obj.doYuvToRgbConversionOnly = value;            
        }        
        if (kwargs.contains("yuv_to_rgb_conversion_matrix"))        
        {        
            auto _value = kwargs["yuv_to_rgb_conversion_matrix"].cast<std::vector<float>>();            
            auto count = _value.size();            
            auto value = new float[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.yuvToRgbConversionMatrix = value;            
        }        
        if (kwargs.contains("src_transfer_function_parameters"))        
        {        
            auto _value = kwargs["src_transfer_function_parameters"].cast<std::vector<float>>();            
            auto count = _value.size();            
            auto value = new float[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.srcTransferFunctionParameters = value;            
        }        
        if (kwargs.contains("dst_transfer_function_parameters"))        
        {        
            auto _value = kwargs["dst_transfer_function_parameters"].cast<std::vector<float>>();            
            auto count = _value.size();            
            auto value = new float[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.dstTransferFunctionParameters = value;            
        }        
        if (kwargs.contains("gamut_conversion_matrix"))        
        {        
            auto _value = kwargs["gamut_conversion_matrix"].cast<std::vector<float>>();            
            auto count = _value.size();            
            auto value = new float[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.gamutConversionMatrix = value;            
        }        
        if (kwargs.contains("mirrored"))        
        {        
            auto value = kwargs["mirrored"].cast<wgpu::Bool>();            
            obj.mirrored = value;            
        }        
        if (kwargs.contains("rotation"))        
        {        
            auto value = kwargs["rotation"].cast<wgpu::ExternalTextureRotation>();            
            obj.rotation = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::ExternalTextureDescriptor, ExternalTextureDescriptor)

PYCLASS_BEGIN(m, wgpu::SharedBufferMemoryProperties, SharedBufferMemoryProperties) SharedBufferMemoryProperties
    .def_readonly("next_in_chain", &wgpu::SharedBufferMemoryProperties::nextInChain)    
    .def_readonly("usage", &wgpu::SharedBufferMemoryProperties::usage)    
    .def_readonly("size", &wgpu::SharedBufferMemoryProperties::size)    
;
PYCLASS_END(m, wgpu::SharedBufferMemoryProperties, SharedBufferMemoryProperties)

PYCLASS_BEGIN(m, wgpu::SharedBufferMemoryDescriptor, SharedBufferMemoryDescriptor) SharedBufferMemoryDescriptor
    .def_readwrite("next_in_chain", &wgpu::SharedBufferMemoryDescriptor::nextInChain)    
    .def_property("label",    
        [](const wgpu::SharedBufferMemoryDescriptor& self) {        
            return self.label;            
        },        
        [](wgpu::SharedBufferMemoryDescriptor& self, char const *  source) {        
            self.label = strdup(source);            
        }        
    )    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SharedBufferMemoryDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("label"))        
        {        
            auto value = kwargs["label"].cast<std::string>();            
            obj.label = strdup(value.c_str());            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SharedBufferMemoryDescriptor, SharedBufferMemoryDescriptor)

PYCLASS_BEGIN(m, wgpu::SharedTextureMemoryProperties, SharedTextureMemoryProperties) SharedTextureMemoryProperties
    .def_readonly("next_in_chain", &wgpu::SharedTextureMemoryProperties::nextInChain)    
    .def_readonly("usage", &wgpu::SharedTextureMemoryProperties::usage)    
    .def_readonly("size", &wgpu::SharedTextureMemoryProperties::size)    
    .def_readonly("format", &wgpu::SharedTextureMemoryProperties::format)    
;
PYCLASS_END(m, wgpu::SharedTextureMemoryProperties, SharedTextureMemoryProperties)

PYSUBCLASS_BEGIN(m, wgpu::SharedTextureMemoryAHardwareBufferProperties, ChainedStructOut, SharedTextureMemoryAHardwareBufferProperties) SharedTextureMemoryAHardwareBufferProperties
    .def_readonly("next_in_chain", &wgpu::SharedTextureMemoryAHardwareBufferProperties::nextInChain)    
    .def_readonly("y_cb_cr_info", &wgpu::SharedTextureMemoryAHardwareBufferProperties::yCbCrInfo)    
;
PYCLASS_END(m, wgpu::SharedTextureMemoryAHardwareBufferProperties, SharedTextureMemoryAHardwareBufferProperties)

PYCLASS_BEGIN(m, wgpu::SharedTextureMemoryDescriptor, SharedTextureMemoryDescriptor) SharedTextureMemoryDescriptor
    .def_readwrite("next_in_chain", &wgpu::SharedTextureMemoryDescriptor::nextInChain)    
    .def_property("label",    
        [](const wgpu::SharedTextureMemoryDescriptor& self) {        
            return self.label;            
        },        
        [](wgpu::SharedTextureMemoryDescriptor& self, char const *  source) {        
            self.label = strdup(source);            
        }        
    )    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SharedTextureMemoryDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("label"))        
        {        
            auto value = kwargs["label"].cast<std::string>();            
            obj.label = strdup(value.c_str());            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SharedTextureMemoryDescriptor, SharedTextureMemoryDescriptor)

PYCLASS_BEGIN(m, wgpu::SharedBufferMemoryBeginAccessDescriptor, SharedBufferMemoryBeginAccessDescriptor) SharedBufferMemoryBeginAccessDescriptor
    .def_readwrite("next_in_chain", &wgpu::SharedBufferMemoryBeginAccessDescriptor::nextInChain)    
    .def_readwrite("initialized", &wgpu::SharedBufferMemoryBeginAccessDescriptor::initialized)    
    .def_readwrite("fence_count", &wgpu::SharedBufferMemoryBeginAccessDescriptor::fenceCount)    
    .def_readwrite("fences", &wgpu::SharedBufferMemoryBeginAccessDescriptor::fences)    
    .def_readwrite("signaled_values", &wgpu::SharedBufferMemoryBeginAccessDescriptor::signaledValues)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SharedBufferMemoryBeginAccessDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("initialized"))        
        {        
            auto value = kwargs["initialized"].cast<wgpu::Bool>();            
            obj.initialized = value;            
        }        
        if (kwargs.contains("fence_count"))        
        {        
            auto value = kwargs["fence_count"].cast<size_t>();            
            obj.fenceCount = value;            
        }        
        if (kwargs.contains("fences"))        
        {        
            auto _value = kwargs["fences"].cast<std::vector<wgpu::SharedFence>>();            
            auto count = _value.size();            
            auto value = new wgpu::SharedFence[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.fences = value;            
        }        
        if (kwargs.contains("signaled_values"))        
        {        
            auto _value = kwargs["signaled_values"].cast<std::vector<uint64_t>>();            
            auto count = _value.size();            
            auto value = new uint64_t[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.signaledValues = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SharedBufferMemoryBeginAccessDescriptor, SharedBufferMemoryBeginAccessDescriptor)

PYCLASS_BEGIN(m, wgpu::SharedBufferMemoryEndAccessState, SharedBufferMemoryEndAccessState) SharedBufferMemoryEndAccessState
    .def_readonly("next_in_chain", &wgpu::SharedBufferMemoryEndAccessState::nextInChain)    
    .def_readonly("initialized", &wgpu::SharedBufferMemoryEndAccessState::initialized)    
    .def_readonly("fence_count", &wgpu::SharedBufferMemoryEndAccessState::fenceCount)    
    .def_readonly("fences", &wgpu::SharedBufferMemoryEndAccessState::fences)    
    .def_readonly("signaled_values", &wgpu::SharedBufferMemoryEndAccessState::signaledValues)    
;
PYCLASS_END(m, wgpu::SharedBufferMemoryEndAccessState, SharedBufferMemoryEndAccessState)

PYSUBCLASS_BEGIN(m, wgpu::SharedTextureMemoryVkDedicatedAllocationDescriptor, ChainedStruct, SharedTextureMemoryVkDedicatedAllocationDescriptor) SharedTextureMemoryVkDedicatedAllocationDescriptor
    .def_readwrite("next_in_chain", &wgpu::SharedTextureMemoryVkDedicatedAllocationDescriptor::nextInChain)    
    .def_readwrite("dedicated_allocation", &wgpu::SharedTextureMemoryVkDedicatedAllocationDescriptor::dedicatedAllocation)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SharedTextureMemoryVkDedicatedAllocationDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("dedicated_allocation"))        
        {        
            auto value = kwargs["dedicated_allocation"].cast<wgpu::Bool>();            
            obj.dedicatedAllocation = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SharedTextureMemoryVkDedicatedAllocationDescriptor, SharedTextureMemoryVkDedicatedAllocationDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::SharedTextureMemoryAHardwareBufferDescriptor, ChainedStruct, SharedTextureMemoryAHardwareBufferDescriptor) SharedTextureMemoryAHardwareBufferDescriptor
    .def_readwrite("next_in_chain", &wgpu::SharedTextureMemoryAHardwareBufferDescriptor::nextInChain)    
    .def_readwrite("handle", &wgpu::SharedTextureMemoryAHardwareBufferDescriptor::handle)    
    .def_readwrite("use_external_format", &wgpu::SharedTextureMemoryAHardwareBufferDescriptor::useExternalFormat)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SharedTextureMemoryAHardwareBufferDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("handle"))        
        {        
            auto value = kwargs["handle"].cast<void *>();            
            obj.handle = value;            
        }        
        if (kwargs.contains("use_external_format"))        
        {        
            auto value = kwargs["use_external_format"].cast<wgpu::Bool>();            
            obj.useExternalFormat = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SharedTextureMemoryAHardwareBufferDescriptor, SharedTextureMemoryAHardwareBufferDescriptor)

PYCLASS_BEGIN(m, wgpu::SharedTextureMemoryDmaBufPlane, SharedTextureMemoryDmaBufPlane) SharedTextureMemoryDmaBufPlane
    .def_readwrite("fd", &wgpu::SharedTextureMemoryDmaBufPlane::fd)    
    .def_readwrite("offset", &wgpu::SharedTextureMemoryDmaBufPlane::offset)    
    .def_readwrite("stride", &wgpu::SharedTextureMemoryDmaBufPlane::stride)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SharedTextureMemoryDmaBufPlane obj{};        
        if (kwargs.contains("fd"))        
        {        
            auto value = kwargs["fd"].cast<int>();            
            obj.fd = value;            
        }        
        if (kwargs.contains("offset"))        
        {        
            auto value = kwargs["offset"].cast<uint64_t>();            
            obj.offset = value;            
        }        
        if (kwargs.contains("stride"))        
        {        
            auto value = kwargs["stride"].cast<uint32_t>();            
            obj.stride = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SharedTextureMemoryDmaBufPlane, SharedTextureMemoryDmaBufPlane)

PYSUBCLASS_BEGIN(m, wgpu::SharedTextureMemoryDmaBufDescriptor, ChainedStruct, SharedTextureMemoryDmaBufDescriptor) SharedTextureMemoryDmaBufDescriptor
    .def_readwrite("next_in_chain", &wgpu::SharedTextureMemoryDmaBufDescriptor::nextInChain)    
    .def_readwrite("size", &wgpu::SharedTextureMemoryDmaBufDescriptor::size)    
    .def_readwrite("drm_format", &wgpu::SharedTextureMemoryDmaBufDescriptor::drmFormat)    
    .def_readwrite("drm_modifier", &wgpu::SharedTextureMemoryDmaBufDescriptor::drmModifier)    
    .def_readwrite("plane_count", &wgpu::SharedTextureMemoryDmaBufDescriptor::planeCount)    
    .def_readwrite("planes", &wgpu::SharedTextureMemoryDmaBufDescriptor::planes)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SharedTextureMemoryDmaBufDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("size"))        
        {        
            auto value = kwargs["size"].cast<wgpu::Extent3D>();            
            obj.size = value;            
        }        
        if (kwargs.contains("drm_format"))        
        {        
            auto value = kwargs["drm_format"].cast<uint32_t>();            
            obj.drmFormat = value;            
        }        
        if (kwargs.contains("drm_modifier"))        
        {        
            auto value = kwargs["drm_modifier"].cast<uint64_t>();            
            obj.drmModifier = value;            
        }        
        if (kwargs.contains("plane_count"))        
        {        
            auto value = kwargs["plane_count"].cast<size_t>();            
            obj.planeCount = value;            
        }        
        if (kwargs.contains("planes"))        
        {        
            auto _value = kwargs["planes"].cast<std::vector<wgpu::SharedTextureMemoryDmaBufPlane>>();            
            auto count = _value.size();            
            auto value = new wgpu::SharedTextureMemoryDmaBufPlane[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.planes = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SharedTextureMemoryDmaBufDescriptor, SharedTextureMemoryDmaBufDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::SharedTextureMemoryOpaqueFDDescriptor, ChainedStruct, SharedTextureMemoryOpaqueFDDescriptor) SharedTextureMemoryOpaqueFDDescriptor
    .def_readwrite("next_in_chain", &wgpu::SharedTextureMemoryOpaqueFDDescriptor::nextInChain)    
    .def_readwrite("vk_image_create_info", &wgpu::SharedTextureMemoryOpaqueFDDescriptor::vkImageCreateInfo)    
    .def_readwrite("memory_fd", &wgpu::SharedTextureMemoryOpaqueFDDescriptor::memoryFD)    
    .def_readwrite("memory_type_index", &wgpu::SharedTextureMemoryOpaqueFDDescriptor::memoryTypeIndex)    
    .def_readwrite("allocation_size", &wgpu::SharedTextureMemoryOpaqueFDDescriptor::allocationSize)    
    .def_readwrite("dedicated_allocation", &wgpu::SharedTextureMemoryOpaqueFDDescriptor::dedicatedAllocation)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SharedTextureMemoryOpaqueFDDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("vk_image_create_info"))        
        {        
            auto value = kwargs["vk_image_create_info"].cast<void const *>();            
            obj.vkImageCreateInfo = value;            
        }        
        if (kwargs.contains("memory_fd"))        
        {        
            auto value = kwargs["memory_fd"].cast<int>();            
            obj.memoryFD = value;            
        }        
        if (kwargs.contains("memory_type_index"))        
        {        
            auto value = kwargs["memory_type_index"].cast<uint32_t>();            
            obj.memoryTypeIndex = value;            
        }        
        if (kwargs.contains("allocation_size"))        
        {        
            auto value = kwargs["allocation_size"].cast<uint64_t>();            
            obj.allocationSize = value;            
        }        
        if (kwargs.contains("dedicated_allocation"))        
        {        
            auto value = kwargs["dedicated_allocation"].cast<wgpu::Bool>();            
            obj.dedicatedAllocation = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SharedTextureMemoryOpaqueFDDescriptor, SharedTextureMemoryOpaqueFDDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::SharedTextureMemoryZirconHandleDescriptor, ChainedStruct, SharedTextureMemoryZirconHandleDescriptor) SharedTextureMemoryZirconHandleDescriptor
    .def_readwrite("next_in_chain", &wgpu::SharedTextureMemoryZirconHandleDescriptor::nextInChain)    
    .def_readwrite("memory_fd", &wgpu::SharedTextureMemoryZirconHandleDescriptor::memoryFD)    
    .def_readwrite("allocation_size", &wgpu::SharedTextureMemoryZirconHandleDescriptor::allocationSize)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SharedTextureMemoryZirconHandleDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("memory_fd"))        
        {        
            auto value = kwargs["memory_fd"].cast<uint32_t>();            
            obj.memoryFD = value;            
        }        
        if (kwargs.contains("allocation_size"))        
        {        
            auto value = kwargs["allocation_size"].cast<uint64_t>();            
            obj.allocationSize = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SharedTextureMemoryZirconHandleDescriptor, SharedTextureMemoryZirconHandleDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::SharedTextureMemoryDXGISharedHandleDescriptor, ChainedStruct, SharedTextureMemoryDXGISharedHandleDescriptor) SharedTextureMemoryDXGISharedHandleDescriptor
    .def_readwrite("next_in_chain", &wgpu::SharedTextureMemoryDXGISharedHandleDescriptor::nextInChain)    
    .def_readwrite("handle", &wgpu::SharedTextureMemoryDXGISharedHandleDescriptor::handle)    
    .def_readwrite("use_keyed_mutex", &wgpu::SharedTextureMemoryDXGISharedHandleDescriptor::useKeyedMutex)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SharedTextureMemoryDXGISharedHandleDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("handle"))        
        {        
            auto value = kwargs["handle"].cast<void *>();            
            obj.handle = value;            
        }        
        if (kwargs.contains("use_keyed_mutex"))        
        {        
            auto value = kwargs["use_keyed_mutex"].cast<wgpu::Bool>();            
            obj.useKeyedMutex = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SharedTextureMemoryDXGISharedHandleDescriptor, SharedTextureMemoryDXGISharedHandleDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::SharedTextureMemoryIOSurfaceDescriptor, ChainedStruct, SharedTextureMemoryIOSurfaceDescriptor) SharedTextureMemoryIOSurfaceDescriptor
    .def_readwrite("next_in_chain", &wgpu::SharedTextureMemoryIOSurfaceDescriptor::nextInChain)    
    .def_readwrite("io_surface", &wgpu::SharedTextureMemoryIOSurfaceDescriptor::ioSurface)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SharedTextureMemoryIOSurfaceDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("io_surface"))        
        {        
            auto value = kwargs["io_surface"].cast<void *>();            
            obj.ioSurface = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SharedTextureMemoryIOSurfaceDescriptor, SharedTextureMemoryIOSurfaceDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::SharedTextureMemoryEGLImageDescriptor, ChainedStruct, SharedTextureMemoryEGLImageDescriptor) SharedTextureMemoryEGLImageDescriptor
    .def_readwrite("next_in_chain", &wgpu::SharedTextureMemoryEGLImageDescriptor::nextInChain)    
    .def_readwrite("image", &wgpu::SharedTextureMemoryEGLImageDescriptor::image)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SharedTextureMemoryEGLImageDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("image"))        
        {        
            auto value = kwargs["image"].cast<void *>();            
            obj.image = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SharedTextureMemoryEGLImageDescriptor, SharedTextureMemoryEGLImageDescriptor)

PYCLASS_BEGIN(m, wgpu::SharedTextureMemoryBeginAccessDescriptor, SharedTextureMemoryBeginAccessDescriptor) SharedTextureMemoryBeginAccessDescriptor
    .def_readwrite("next_in_chain", &wgpu::SharedTextureMemoryBeginAccessDescriptor::nextInChain)    
    .def_readwrite("concurrent_read", &wgpu::SharedTextureMemoryBeginAccessDescriptor::concurrentRead)    
    .def_readwrite("initialized", &wgpu::SharedTextureMemoryBeginAccessDescriptor::initialized)    
    .def_readwrite("fence_count", &wgpu::SharedTextureMemoryBeginAccessDescriptor::fenceCount)    
    .def_readwrite("fences", &wgpu::SharedTextureMemoryBeginAccessDescriptor::fences)    
    .def_readwrite("signaled_values", &wgpu::SharedTextureMemoryBeginAccessDescriptor::signaledValues)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SharedTextureMemoryBeginAccessDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("concurrent_read"))        
        {        
            auto value = kwargs["concurrent_read"].cast<wgpu::Bool>();            
            obj.concurrentRead = value;            
        }        
        if (kwargs.contains("initialized"))        
        {        
            auto value = kwargs["initialized"].cast<wgpu::Bool>();            
            obj.initialized = value;            
        }        
        if (kwargs.contains("fence_count"))        
        {        
            auto value = kwargs["fence_count"].cast<size_t>();            
            obj.fenceCount = value;            
        }        
        if (kwargs.contains("fences"))        
        {        
            auto _value = kwargs["fences"].cast<std::vector<wgpu::SharedFence>>();            
            auto count = _value.size();            
            auto value = new wgpu::SharedFence[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.fences = value;            
        }        
        if (kwargs.contains("signaled_values"))        
        {        
            auto _value = kwargs["signaled_values"].cast<std::vector<uint64_t>>();            
            auto count = _value.size();            
            auto value = new uint64_t[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.signaledValues = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SharedTextureMemoryBeginAccessDescriptor, SharedTextureMemoryBeginAccessDescriptor)

PYCLASS_BEGIN(m, wgpu::SharedTextureMemoryEndAccessState, SharedTextureMemoryEndAccessState) SharedTextureMemoryEndAccessState
    .def_readonly("next_in_chain", &wgpu::SharedTextureMemoryEndAccessState::nextInChain)    
    .def_readonly("initialized", &wgpu::SharedTextureMemoryEndAccessState::initialized)    
    .def_readonly("fence_count", &wgpu::SharedTextureMemoryEndAccessState::fenceCount)    
    .def_readonly("fences", &wgpu::SharedTextureMemoryEndAccessState::fences)    
    .def_readonly("signaled_values", &wgpu::SharedTextureMemoryEndAccessState::signaledValues)    
;
PYCLASS_END(m, wgpu::SharedTextureMemoryEndAccessState, SharedTextureMemoryEndAccessState)

PYSUBCLASS_BEGIN(m, wgpu::SharedTextureMemoryVkImageLayoutBeginState, ChainedStruct, SharedTextureMemoryVkImageLayoutBeginState) SharedTextureMemoryVkImageLayoutBeginState
    .def_readwrite("next_in_chain", &wgpu::SharedTextureMemoryVkImageLayoutBeginState::nextInChain)    
    .def_readwrite("old_layout", &wgpu::SharedTextureMemoryVkImageLayoutBeginState::oldLayout)    
    .def_readwrite("new_layout", &wgpu::SharedTextureMemoryVkImageLayoutBeginState::newLayout)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SharedTextureMemoryVkImageLayoutBeginState obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("old_layout"))        
        {        
            auto value = kwargs["old_layout"].cast<int32_t>();            
            obj.oldLayout = value;            
        }        
        if (kwargs.contains("new_layout"))        
        {        
            auto value = kwargs["new_layout"].cast<int32_t>();            
            obj.newLayout = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SharedTextureMemoryVkImageLayoutBeginState, SharedTextureMemoryVkImageLayoutBeginState)

PYSUBCLASS_BEGIN(m, wgpu::SharedTextureMemoryVkImageLayoutEndState, ChainedStructOut, SharedTextureMemoryVkImageLayoutEndState) SharedTextureMemoryVkImageLayoutEndState
    .def_readonly("next_in_chain", &wgpu::SharedTextureMemoryVkImageLayoutEndState::nextInChain)    
    .def_readonly("old_layout", &wgpu::SharedTextureMemoryVkImageLayoutEndState::oldLayout)    
    .def_readonly("new_layout", &wgpu::SharedTextureMemoryVkImageLayoutEndState::newLayout)    
;
PYCLASS_END(m, wgpu::SharedTextureMemoryVkImageLayoutEndState, SharedTextureMemoryVkImageLayoutEndState)

PYSUBCLASS_BEGIN(m, wgpu::SharedTextureMemoryD3DSwapchainBeginState, ChainedStruct, SharedTextureMemoryD3DSwapchainBeginState) SharedTextureMemoryD3DSwapchainBeginState
    .def_readwrite("next_in_chain", &wgpu::SharedTextureMemoryD3DSwapchainBeginState::nextInChain)    
    .def_readwrite("is_swapchain", &wgpu::SharedTextureMemoryD3DSwapchainBeginState::isSwapchain)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SharedTextureMemoryD3DSwapchainBeginState obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("is_swapchain"))        
        {        
            auto value = kwargs["is_swapchain"].cast<wgpu::Bool>();            
            obj.isSwapchain = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SharedTextureMemoryD3DSwapchainBeginState, SharedTextureMemoryD3DSwapchainBeginState)

PYCLASS_BEGIN(m, wgpu::SharedFenceDescriptor, SharedFenceDescriptor) SharedFenceDescriptor
    .def_readwrite("next_in_chain", &wgpu::SharedFenceDescriptor::nextInChain)    
    .def_property("label",    
        [](const wgpu::SharedFenceDescriptor& self) {        
            return self.label;            
        },        
        [](wgpu::SharedFenceDescriptor& self, char const *  source) {        
            self.label = strdup(source);            
        }        
    )    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SharedFenceDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("label"))        
        {        
            auto value = kwargs["label"].cast<std::string>();            
            obj.label = strdup(value.c_str());            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SharedFenceDescriptor, SharedFenceDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::SharedFenceVkSemaphoreOpaqueFDDescriptor, ChainedStruct, SharedFenceVkSemaphoreOpaqueFDDescriptor) SharedFenceVkSemaphoreOpaqueFDDescriptor
    .def_readwrite("next_in_chain", &wgpu::SharedFenceVkSemaphoreOpaqueFDDescriptor::nextInChain)    
    .def_readwrite("handle", &wgpu::SharedFenceVkSemaphoreOpaqueFDDescriptor::handle)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SharedFenceVkSemaphoreOpaqueFDDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("handle"))        
        {        
            auto value = kwargs["handle"].cast<int>();            
            obj.handle = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SharedFenceVkSemaphoreOpaqueFDDescriptor, SharedFenceVkSemaphoreOpaqueFDDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::SharedFenceVkSemaphoreSyncFDDescriptor, ChainedStruct, SharedFenceVkSemaphoreSyncFDDescriptor) SharedFenceVkSemaphoreSyncFDDescriptor
    .def_readwrite("next_in_chain", &wgpu::SharedFenceVkSemaphoreSyncFDDescriptor::nextInChain)    
    .def_readwrite("handle", &wgpu::SharedFenceVkSemaphoreSyncFDDescriptor::handle)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SharedFenceVkSemaphoreSyncFDDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("handle"))        
        {        
            auto value = kwargs["handle"].cast<int>();            
            obj.handle = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SharedFenceVkSemaphoreSyncFDDescriptor, SharedFenceVkSemaphoreSyncFDDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::SharedFenceVkSemaphoreZirconHandleDescriptor, ChainedStruct, SharedFenceVkSemaphoreZirconHandleDescriptor) SharedFenceVkSemaphoreZirconHandleDescriptor
    .def_readwrite("next_in_chain", &wgpu::SharedFenceVkSemaphoreZirconHandleDescriptor::nextInChain)    
    .def_readwrite("handle", &wgpu::SharedFenceVkSemaphoreZirconHandleDescriptor::handle)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SharedFenceVkSemaphoreZirconHandleDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("handle"))        
        {        
            auto value = kwargs["handle"].cast<uint32_t>();            
            obj.handle = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SharedFenceVkSemaphoreZirconHandleDescriptor, SharedFenceVkSemaphoreZirconHandleDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::SharedFenceDXGISharedHandleDescriptor, ChainedStruct, SharedFenceDXGISharedHandleDescriptor) SharedFenceDXGISharedHandleDescriptor
    .def_readwrite("next_in_chain", &wgpu::SharedFenceDXGISharedHandleDescriptor::nextInChain)    
    .def_readwrite("handle", &wgpu::SharedFenceDXGISharedHandleDescriptor::handle)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SharedFenceDXGISharedHandleDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("handle"))        
        {        
            auto value = kwargs["handle"].cast<void *>();            
            obj.handle = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SharedFenceDXGISharedHandleDescriptor, SharedFenceDXGISharedHandleDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::SharedFenceMTLSharedEventDescriptor, ChainedStruct, SharedFenceMTLSharedEventDescriptor) SharedFenceMTLSharedEventDescriptor
    .def_readwrite("next_in_chain", &wgpu::SharedFenceMTLSharedEventDescriptor::nextInChain)    
    .def_readwrite("shared_event", &wgpu::SharedFenceMTLSharedEventDescriptor::sharedEvent)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SharedFenceMTLSharedEventDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("shared_event"))        
        {        
            auto value = kwargs["shared_event"].cast<void *>();            
            obj.sharedEvent = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SharedFenceMTLSharedEventDescriptor, SharedFenceMTLSharedEventDescriptor)

PYCLASS_BEGIN(m, wgpu::SharedFenceExportInfo, SharedFenceExportInfo) SharedFenceExportInfo
    .def_readonly("next_in_chain", &wgpu::SharedFenceExportInfo::nextInChain)    
    .def_readonly("type", &wgpu::SharedFenceExportInfo::type)    
;
PYCLASS_END(m, wgpu::SharedFenceExportInfo, SharedFenceExportInfo)

PYSUBCLASS_BEGIN(m, wgpu::SharedFenceVkSemaphoreOpaqueFDExportInfo, ChainedStructOut, SharedFenceVkSemaphoreOpaqueFDExportInfo) SharedFenceVkSemaphoreOpaqueFDExportInfo
    .def_readonly("next_in_chain", &wgpu::SharedFenceVkSemaphoreOpaqueFDExportInfo::nextInChain)    
    .def_readonly("handle", &wgpu::SharedFenceVkSemaphoreOpaqueFDExportInfo::handle)    
;
PYCLASS_END(m, wgpu::SharedFenceVkSemaphoreOpaqueFDExportInfo, SharedFenceVkSemaphoreOpaqueFDExportInfo)

PYSUBCLASS_BEGIN(m, wgpu::SharedFenceVkSemaphoreSyncFDExportInfo, ChainedStructOut, SharedFenceVkSemaphoreSyncFDExportInfo) SharedFenceVkSemaphoreSyncFDExportInfo
    .def_readonly("next_in_chain", &wgpu::SharedFenceVkSemaphoreSyncFDExportInfo::nextInChain)    
    .def_readonly("handle", &wgpu::SharedFenceVkSemaphoreSyncFDExportInfo::handle)    
;
PYCLASS_END(m, wgpu::SharedFenceVkSemaphoreSyncFDExportInfo, SharedFenceVkSemaphoreSyncFDExportInfo)

PYSUBCLASS_BEGIN(m, wgpu::SharedFenceVkSemaphoreZirconHandleExportInfo, ChainedStructOut, SharedFenceVkSemaphoreZirconHandleExportInfo) SharedFenceVkSemaphoreZirconHandleExportInfo
    .def_readonly("next_in_chain", &wgpu::SharedFenceVkSemaphoreZirconHandleExportInfo::nextInChain)    
    .def_readonly("handle", &wgpu::SharedFenceVkSemaphoreZirconHandleExportInfo::handle)    
;
PYCLASS_END(m, wgpu::SharedFenceVkSemaphoreZirconHandleExportInfo, SharedFenceVkSemaphoreZirconHandleExportInfo)

PYSUBCLASS_BEGIN(m, wgpu::SharedFenceDXGISharedHandleExportInfo, ChainedStructOut, SharedFenceDXGISharedHandleExportInfo) SharedFenceDXGISharedHandleExportInfo
    .def_readonly("next_in_chain", &wgpu::SharedFenceDXGISharedHandleExportInfo::nextInChain)    
    .def_readonly("handle", &wgpu::SharedFenceDXGISharedHandleExportInfo::handle)    
;
PYCLASS_END(m, wgpu::SharedFenceDXGISharedHandleExportInfo, SharedFenceDXGISharedHandleExportInfo)

PYSUBCLASS_BEGIN(m, wgpu::SharedFenceMTLSharedEventExportInfo, ChainedStructOut, SharedFenceMTLSharedEventExportInfo) SharedFenceMTLSharedEventExportInfo
    .def_readonly("next_in_chain", &wgpu::SharedFenceMTLSharedEventExportInfo::nextInChain)    
    .def_readonly("shared_event", &wgpu::SharedFenceMTLSharedEventExportInfo::sharedEvent)    
;
PYCLASS_END(m, wgpu::SharedFenceMTLSharedEventExportInfo, SharedFenceMTLSharedEventExportInfo)

PYCLASS_BEGIN(m, wgpu::FormatCapabilities, FormatCapabilities) FormatCapabilities
    .def_readonly("next_in_chain", &wgpu::FormatCapabilities::nextInChain)    
;
PYCLASS_END(m, wgpu::FormatCapabilities, FormatCapabilities)

PYSUBCLASS_BEGIN(m, wgpu::DrmFormatCapabilities, ChainedStructOut, DrmFormatCapabilities) DrmFormatCapabilities
    .def_readonly("next_in_chain", &wgpu::DrmFormatCapabilities::nextInChain)    
    .def_readonly("properties_count", &wgpu::DrmFormatCapabilities::propertiesCount)    
    .def_readonly("properties", &wgpu::DrmFormatCapabilities::properties)    
;
PYCLASS_END(m, wgpu::DrmFormatCapabilities, DrmFormatCapabilities)

PYCLASS_BEGIN(m, wgpu::DrmFormatProperties, DrmFormatProperties) DrmFormatProperties
    .def_readwrite("modifier", &wgpu::DrmFormatProperties::modifier)    
    .def_readwrite("modifier_plane_count", &wgpu::DrmFormatProperties::modifierPlaneCount)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::DrmFormatProperties obj{};        
        if (kwargs.contains("modifier"))        
        {        
            auto value = kwargs["modifier"].cast<uint64_t>();            
            obj.modifier = value;            
        }        
        if (kwargs.contains("modifier_plane_count"))        
        {        
            auto value = kwargs["modifier_plane_count"].cast<uint32_t>();            
            obj.modifierPlaneCount = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::DrmFormatProperties, DrmFormatProperties)

PYCLASS_BEGIN(m, wgpu::ImageCopyBuffer, ImageCopyBuffer) ImageCopyBuffer
    .def_readwrite("layout", &wgpu::ImageCopyBuffer::layout)    
    .def_readwrite("buffer", &wgpu::ImageCopyBuffer::buffer)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::ImageCopyBuffer obj{};        
        if (kwargs.contains("layout"))        
        {        
            auto value = kwargs["layout"].cast<wgpu::TextureDataLayout>();            
            obj.layout = value;            
        }        
        if (kwargs.contains("buffer"))        
        {        
            auto value = kwargs["buffer"].cast<wgpu::Buffer>();            
            obj.buffer = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::ImageCopyBuffer, ImageCopyBuffer)

PYCLASS_BEGIN(m, wgpu::ImageCopyTexture, ImageCopyTexture) ImageCopyTexture
    .def_readwrite("texture", &wgpu::ImageCopyTexture::texture)    
    .def_readwrite("mip_level", &wgpu::ImageCopyTexture::mipLevel)    
    .def_readwrite("origin", &wgpu::ImageCopyTexture::origin)    
    .def_readwrite("aspect", &wgpu::ImageCopyTexture::aspect)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::ImageCopyTexture obj{};        
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
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::ImageCopyTexture, ImageCopyTexture)

PYCLASS_BEGIN(m, wgpu::ImageCopyExternalTexture, ImageCopyExternalTexture) ImageCopyExternalTexture
    .def_readwrite("next_in_chain", &wgpu::ImageCopyExternalTexture::nextInChain)    
    .def_readwrite("external_texture", &wgpu::ImageCopyExternalTexture::externalTexture)    
    .def_readwrite("origin", &wgpu::ImageCopyExternalTexture::origin)    
    .def_readwrite("natural_size", &wgpu::ImageCopyExternalTexture::naturalSize)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::ImageCopyExternalTexture obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("external_texture"))        
        {        
            auto value = kwargs["external_texture"].cast<wgpu::ExternalTexture>();            
            obj.externalTexture = value;            
        }        
        if (kwargs.contains("origin"))        
        {        
            auto value = kwargs["origin"].cast<wgpu::Origin3D>();            
            obj.origin = value;            
        }        
        if (kwargs.contains("natural_size"))        
        {        
            auto value = kwargs["natural_size"].cast<wgpu::Extent2D>();            
            obj.naturalSize = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::ImageCopyExternalTexture, ImageCopyExternalTexture)

PYCLASS_BEGIN(m, wgpu::Future, Future) Future
    .def_readwrite("id", &wgpu::Future::id)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::Future obj{};        
        if (kwargs.contains("id"))        
        {        
            auto value = kwargs["id"].cast<uint64_t>();            
            obj.id = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::Future, Future)

PYCLASS_BEGIN(m, wgpu::FutureWaitInfo, FutureWaitInfo) FutureWaitInfo
    .def_readwrite("future", &wgpu::FutureWaitInfo::future)    
    .def_readwrite("completed", &wgpu::FutureWaitInfo::completed)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::FutureWaitInfo obj{};        
        if (kwargs.contains("future"))        
        {        
            auto value = kwargs["future"].cast<wgpu::Future>();            
            obj.future = value;            
        }        
        if (kwargs.contains("completed"))        
        {        
            auto value = kwargs["completed"].cast<wgpu::Bool>();            
            obj.completed = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::FutureWaitInfo, FutureWaitInfo)

PYCLASS_BEGIN(m, wgpu::InstanceFeatures, InstanceFeatures) InstanceFeatures
    .def_readwrite("next_in_chain", &wgpu::InstanceFeatures::nextInChain)    
    .def_readwrite("timed_wait_any_enable", &wgpu::InstanceFeatures::timedWaitAnyEnable)    
    .def_readwrite("timed_wait_any_max_count", &wgpu::InstanceFeatures::timedWaitAnyMaxCount)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::InstanceFeatures obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("timed_wait_any_enable"))        
        {        
            auto value = kwargs["timed_wait_any_enable"].cast<wgpu::Bool>();            
            obj.timedWaitAnyEnable = value;            
        }        
        if (kwargs.contains("timed_wait_any_max_count"))        
        {        
            auto value = kwargs["timed_wait_any_max_count"].cast<size_t>();            
            obj.timedWaitAnyMaxCount = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::InstanceFeatures, InstanceFeatures)

PYCLASS_BEGIN(m, wgpu::InstanceDescriptor, InstanceDescriptor) InstanceDescriptor
    .def_readwrite("next_in_chain", &wgpu::InstanceDescriptor::nextInChain)    
    .def_readwrite("features", &wgpu::InstanceDescriptor::features)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::InstanceDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("features"))        
        {        
            auto value = kwargs["features"].cast<wgpu::InstanceFeatures>();            
            obj.features = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::InstanceDescriptor, InstanceDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::DawnWireWGSLControl, ChainedStruct, DawnWireWGSLControl) DawnWireWGSLControl
    .def_readwrite("next_in_chain", &wgpu::DawnWireWGSLControl::nextInChain)    
    .def_readwrite("enable_experimental", &wgpu::DawnWireWGSLControl::enableExperimental)    
    .def_readwrite("enable_unsafe", &wgpu::DawnWireWGSLControl::enableUnsafe)    
    .def_readwrite("enable_testing", &wgpu::DawnWireWGSLControl::enableTesting)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::DawnWireWGSLControl obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("enable_experimental"))        
        {        
            auto value = kwargs["enable_experimental"].cast<wgpu::Bool>();            
            obj.enableExperimental = value;            
        }        
        if (kwargs.contains("enable_unsafe"))        
        {        
            auto value = kwargs["enable_unsafe"].cast<wgpu::Bool>();            
            obj.enableUnsafe = value;            
        }        
        if (kwargs.contains("enable_testing"))        
        {        
            auto value = kwargs["enable_testing"].cast<wgpu::Bool>();            
            obj.enableTesting = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::DawnWireWGSLControl, DawnWireWGSLControl)

PYCLASS_BEGIN(m, wgpu::VertexAttribute, VertexAttribute) VertexAttribute
    .def_readwrite("format", &wgpu::VertexAttribute::format)    
    .def_readwrite("offset", &wgpu::VertexAttribute::offset)    
    .def_readwrite("shader_location", &wgpu::VertexAttribute::shaderLocation)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::VertexAttribute obj{};        
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
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::VertexAttribute, VertexAttribute)

PYCLASS_BEGIN(m, wgpu::VertexBufferLayout, VertexBufferLayout) VertexBufferLayout
    .def_readwrite("array_stride", &wgpu::VertexBufferLayout::arrayStride)    
    .def_readwrite("step_mode", &wgpu::VertexBufferLayout::stepMode)    
    .def_readwrite("attribute_count", &wgpu::VertexBufferLayout::attributeCount)    
    .def_readwrite("attributes", &wgpu::VertexBufferLayout::attributes)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::VertexBufferLayout obj{};        
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
            auto _value = kwargs["attributes"].cast<std::vector<wgpu::VertexAttribute>>();            
            auto count = _value.size();            
            auto value = new wgpu::VertexAttribute[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.attributes = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::VertexBufferLayout, VertexBufferLayout)

PYCLASS_BEGIN(m, wgpu::Origin3D, Origin3D) Origin3D
    .def_readwrite("x", &wgpu::Origin3D::x)    
    .def_readwrite("y", &wgpu::Origin3D::y)    
    .def_readwrite("z", &wgpu::Origin3D::z)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::Origin3D obj{};        
        if (kwargs.contains("x"))        
        {        
            auto value = kwargs["x"].cast<uint32_t>();            
            obj.x = value;            
        }        
        if (kwargs.contains("y"))        
        {        
            auto value = kwargs["y"].cast<uint32_t>();            
            obj.y = value;            
        }        
        if (kwargs.contains("z"))        
        {        
            auto value = kwargs["z"].cast<uint32_t>();            
            obj.z = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::Origin3D, Origin3D)

PYCLASS_BEGIN(m, wgpu::Origin2D, Origin2D) Origin2D
    .def_readwrite("x", &wgpu::Origin2D::x)    
    .def_readwrite("y", &wgpu::Origin2D::y)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::Origin2D obj{};        
        if (kwargs.contains("x"))        
        {        
            auto value = kwargs["x"].cast<uint32_t>();            
            obj.x = value;            
        }        
        if (kwargs.contains("y"))        
        {        
            auto value = kwargs["y"].cast<uint32_t>();            
            obj.y = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::Origin2D, Origin2D)

PYCLASS_BEGIN(m, wgpu::PipelineLayoutDescriptor, PipelineLayoutDescriptor) PipelineLayoutDescriptor
    .def_readwrite("next_in_chain", &wgpu::PipelineLayoutDescriptor::nextInChain)    
    .def_property("label",    
        [](const wgpu::PipelineLayoutDescriptor& self) {        
            return self.label;            
        },        
        [](wgpu::PipelineLayoutDescriptor& self, char const *  source) {        
            self.label = strdup(source);            
        }        
    )    
    .def_readwrite("bind_group_layout_count", &wgpu::PipelineLayoutDescriptor::bindGroupLayoutCount)    
    .def_readwrite("bind_group_layouts", &wgpu::PipelineLayoutDescriptor::bindGroupLayouts)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::PipelineLayoutDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("label"))        
        {        
            auto value = kwargs["label"].cast<std::string>();            
            obj.label = strdup(value.c_str());            
        }        
        if (kwargs.contains("bind_group_layout_count"))        
        {        
            auto value = kwargs["bind_group_layout_count"].cast<size_t>();            
            obj.bindGroupLayoutCount = value;            
        }        
        if (kwargs.contains("bind_group_layouts"))        
        {        
            auto _value = kwargs["bind_group_layouts"].cast<std::vector<wgpu::BindGroupLayout>>();            
            auto count = _value.size();            
            auto value = new wgpu::BindGroupLayout[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.bindGroupLayouts = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::PipelineLayoutDescriptor, PipelineLayoutDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::PipelineLayoutPixelLocalStorage, ChainedStruct, PipelineLayoutPixelLocalStorage) PipelineLayoutPixelLocalStorage
    .def_readwrite("next_in_chain", &wgpu::PipelineLayoutPixelLocalStorage::nextInChain)    
    .def_readwrite("total_pixel_local_storage_size", &wgpu::PipelineLayoutPixelLocalStorage::totalPixelLocalStorageSize)    
    .def_readwrite("storage_attachment_count", &wgpu::PipelineLayoutPixelLocalStorage::storageAttachmentCount)    
    .def_readwrite("storage_attachments", &wgpu::PipelineLayoutPixelLocalStorage::storageAttachments)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::PipelineLayoutPixelLocalStorage obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("total_pixel_local_storage_size"))        
        {        
            auto value = kwargs["total_pixel_local_storage_size"].cast<uint64_t>();            
            obj.totalPixelLocalStorageSize = value;            
        }        
        if (kwargs.contains("storage_attachment_count"))        
        {        
            auto value = kwargs["storage_attachment_count"].cast<size_t>();            
            obj.storageAttachmentCount = value;            
        }        
        if (kwargs.contains("storage_attachments"))        
        {        
            auto _value = kwargs["storage_attachments"].cast<std::vector<wgpu::PipelineLayoutStorageAttachment>>();            
            auto count = _value.size();            
            auto value = new wgpu::PipelineLayoutStorageAttachment[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.storageAttachments = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::PipelineLayoutPixelLocalStorage, PipelineLayoutPixelLocalStorage)

PYCLASS_BEGIN(m, wgpu::PipelineLayoutStorageAttachment, PipelineLayoutStorageAttachment) PipelineLayoutStorageAttachment
    .def_readwrite("next_in_chain", &wgpu::PipelineLayoutStorageAttachment::nextInChain)    
    .def_readwrite("offset", &wgpu::PipelineLayoutStorageAttachment::offset)    
    .def_readwrite("format", &wgpu::PipelineLayoutStorageAttachment::format)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::PipelineLayoutStorageAttachment obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("offset"))        
        {        
            auto value = kwargs["offset"].cast<uint64_t>();            
            obj.offset = value;            
        }        
        if (kwargs.contains("format"))        
        {        
            auto value = kwargs["format"].cast<wgpu::TextureFormat>();            
            obj.format = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::PipelineLayoutStorageAttachment, PipelineLayoutStorageAttachment)

PYCLASS_BEGIN(m, wgpu::ProgrammableStageDescriptor, ProgrammableStageDescriptor) ProgrammableStageDescriptor
    .def_readwrite("next_in_chain", &wgpu::ProgrammableStageDescriptor::nextInChain)    
    .def_readwrite("module", &wgpu::ProgrammableStageDescriptor::module)    
    .def_property("entry_point",    
        [](const wgpu::ProgrammableStageDescriptor& self) {        
            return self.entryPoint;            
        },        
        [](wgpu::ProgrammableStageDescriptor& self, char const *  source) {        
            self.entryPoint = strdup(source);            
        }        
    )    
    .def_readwrite("constant_count", &wgpu::ProgrammableStageDescriptor::constantCount)    
    .def_readwrite("constants", &wgpu::ProgrammableStageDescriptor::constants)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::ProgrammableStageDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("module"))        
        {        
            auto value = kwargs["module"].cast<wgpu::ShaderModule>();            
            obj.module = value;            
        }        
        if (kwargs.contains("entry_point"))        
        {        
            auto value = kwargs["entry_point"].cast<std::string>();            
            obj.entryPoint = strdup(value.c_str());            
        }        
        if (kwargs.contains("constant_count"))        
        {        
            auto value = kwargs["constant_count"].cast<size_t>();            
            obj.constantCount = value;            
        }        
        if (kwargs.contains("constants"))        
        {        
            auto _value = kwargs["constants"].cast<std::vector<wgpu::ConstantEntry>>();            
            auto count = _value.size();            
            auto value = new wgpu::ConstantEntry[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.constants = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::ProgrammableStageDescriptor, ProgrammableStageDescriptor)

PYCLASS_BEGIN(m, wgpu::QuerySetDescriptor, QuerySetDescriptor) QuerySetDescriptor
    .def_readwrite("next_in_chain", &wgpu::QuerySetDescriptor::nextInChain)    
    .def_property("label",    
        [](const wgpu::QuerySetDescriptor& self) {        
            return self.label;            
        },        
        [](wgpu::QuerySetDescriptor& self, char const *  source) {        
            self.label = strdup(source);            
        }        
    )    
    .def_readwrite("type", &wgpu::QuerySetDescriptor::type)    
    .def_readwrite("count", &wgpu::QuerySetDescriptor::count)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::QuerySetDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("label"))        
        {        
            auto value = kwargs["label"].cast<std::string>();            
            obj.label = strdup(value.c_str());            
        }        
        if (kwargs.contains("type"))        
        {        
            auto value = kwargs["type"].cast<wgpu::QueryType>();            
            obj.type = value;            
        }        
        if (kwargs.contains("count"))        
        {        
            auto value = kwargs["count"].cast<uint32_t>();            
            obj.count = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::QuerySetDescriptor, QuerySetDescriptor)

PYCLASS_BEGIN(m, wgpu::QueueDescriptor, QueueDescriptor) QueueDescriptor
    .def_readwrite("next_in_chain", &wgpu::QueueDescriptor::nextInChain)    
    .def_property("label",    
        [](const wgpu::QueueDescriptor& self) {        
            return self.label;            
        },        
        [](wgpu::QueueDescriptor& self, char const *  source) {        
            self.label = strdup(source);            
        }        
    )    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::QueueDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("label"))        
        {        
            auto value = kwargs["label"].cast<std::string>();            
            obj.label = strdup(value.c_str());            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::QueueDescriptor, QueueDescriptor)

PYCLASS_BEGIN(m, wgpu::QueueWorkDoneCallbackInfo, QueueWorkDoneCallbackInfo) QueueWorkDoneCallbackInfo
    .def_readwrite("next_in_chain", &wgpu::QueueWorkDoneCallbackInfo::nextInChain)    
    .def_readwrite("mode", &wgpu::QueueWorkDoneCallbackInfo::mode)    
    .def_readwrite("userdata", &wgpu::QueueWorkDoneCallbackInfo::userdata)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::QueueWorkDoneCallbackInfo obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("mode"))        
        {        
            auto value = kwargs["mode"].cast<wgpu::CallbackMode>();            
            obj.mode = value;            
        }        
        if (kwargs.contains("userdata"))        
        {        
            auto value = kwargs["userdata"].cast<void *>();            
            obj.userdata = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::QueueWorkDoneCallbackInfo, QueueWorkDoneCallbackInfo)

PYCLASS_BEGIN(m, wgpu::RenderBundleDescriptor, RenderBundleDescriptor) RenderBundleDescriptor
    .def_readwrite("next_in_chain", &wgpu::RenderBundleDescriptor::nextInChain)    
    .def_property("label",    
        [](const wgpu::RenderBundleDescriptor& self) {        
            return self.label;            
        },        
        [](wgpu::RenderBundleDescriptor& self, char const *  source) {        
            self.label = strdup(source);            
        }        
    )    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::RenderBundleDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("label"))        
        {        
            auto value = kwargs["label"].cast<std::string>();            
            obj.label = strdup(value.c_str());            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::RenderBundleDescriptor, RenderBundleDescriptor)

PYCLASS_BEGIN(m, wgpu::RenderBundleEncoderDescriptor, RenderBundleEncoderDescriptor) RenderBundleEncoderDescriptor
    .def_readwrite("next_in_chain", &wgpu::RenderBundleEncoderDescriptor::nextInChain)    
    .def_property("label",    
        [](const wgpu::RenderBundleEncoderDescriptor& self) {        
            return self.label;            
        },        
        [](wgpu::RenderBundleEncoderDescriptor& self, char const *  source) {        
            self.label = strdup(source);            
        }        
    )    
    .def_readwrite("color_format_count", &wgpu::RenderBundleEncoderDescriptor::colorFormatCount)    
    .def_readwrite("color_formats", &wgpu::RenderBundleEncoderDescriptor::colorFormats)    
    .def_readwrite("depth_stencil_format", &wgpu::RenderBundleEncoderDescriptor::depthStencilFormat)    
    .def_readwrite("sample_count", &wgpu::RenderBundleEncoderDescriptor::sampleCount)    
    .def_readwrite("depth_read_only", &wgpu::RenderBundleEncoderDescriptor::depthReadOnly)    
    .def_readwrite("stencil_read_only", &wgpu::RenderBundleEncoderDescriptor::stencilReadOnly)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::RenderBundleEncoderDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("label"))        
        {        
            auto value = kwargs["label"].cast<std::string>();            
            obj.label = strdup(value.c_str());            
        }        
        if (kwargs.contains("color_format_count"))        
        {        
            auto value = kwargs["color_format_count"].cast<size_t>();            
            obj.colorFormatCount = value;            
        }        
        if (kwargs.contains("color_formats"))        
        {        
            auto _value = kwargs["color_formats"].cast<std::vector<wgpu::TextureFormat>>();            
            auto count = _value.size();            
            auto value = new wgpu::TextureFormat[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.colorFormats = value;            
        }        
        if (kwargs.contains("depth_stencil_format"))        
        {        
            auto value = kwargs["depth_stencil_format"].cast<wgpu::TextureFormat>();            
            obj.depthStencilFormat = value;            
        }        
        if (kwargs.contains("sample_count"))        
        {        
            auto value = kwargs["sample_count"].cast<uint32_t>();            
            obj.sampleCount = value;            
        }        
        if (kwargs.contains("depth_read_only"))        
        {        
            auto value = kwargs["depth_read_only"].cast<wgpu::Bool>();            
            obj.depthReadOnly = value;            
        }        
        if (kwargs.contains("stencil_read_only"))        
        {        
            auto value = kwargs["stencil_read_only"].cast<wgpu::Bool>();            
            obj.stencilReadOnly = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::RenderBundleEncoderDescriptor, RenderBundleEncoderDescriptor)

PYCLASS_BEGIN(m, wgpu::RenderPassColorAttachment, RenderPassColorAttachment) RenderPassColorAttachment
    .def_readwrite("next_in_chain", &wgpu::RenderPassColorAttachment::nextInChain)    
    .def_readwrite("view", &wgpu::RenderPassColorAttachment::view)    
    .def_readwrite("depth_slice", &wgpu::RenderPassColorAttachment::depthSlice)    
    .def_readwrite("resolve_target", &wgpu::RenderPassColorAttachment::resolveTarget)    
    .def_readwrite("load_op", &wgpu::RenderPassColorAttachment::loadOp)    
    .def_readwrite("store_op", &wgpu::RenderPassColorAttachment::storeOp)    
    .def_readwrite("clear_value", &wgpu::RenderPassColorAttachment::clearValue)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::RenderPassColorAttachment obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
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
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::RenderPassColorAttachment, RenderPassColorAttachment)

PYSUBCLASS_BEGIN(m, wgpu::DawnRenderPassColorAttachmentRenderToSingleSampled, ChainedStruct, DawnRenderPassColorAttachmentRenderToSingleSampled) DawnRenderPassColorAttachmentRenderToSingleSampled
    .def_readwrite("next_in_chain", &wgpu::DawnRenderPassColorAttachmentRenderToSingleSampled::nextInChain)    
    .def_readwrite("implicit_sample_count", &wgpu::DawnRenderPassColorAttachmentRenderToSingleSampled::implicitSampleCount)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::DawnRenderPassColorAttachmentRenderToSingleSampled obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("implicit_sample_count"))        
        {        
            auto value = kwargs["implicit_sample_count"].cast<uint32_t>();            
            obj.implicitSampleCount = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::DawnRenderPassColorAttachmentRenderToSingleSampled, DawnRenderPassColorAttachmentRenderToSingleSampled)

PYCLASS_BEGIN(m, wgpu::RenderPassDepthStencilAttachment, RenderPassDepthStencilAttachment) RenderPassDepthStencilAttachment
    .def_readwrite("view", &wgpu::RenderPassDepthStencilAttachment::view)    
    .def_readwrite("depth_load_op", &wgpu::RenderPassDepthStencilAttachment::depthLoadOp)    
    .def_readwrite("depth_store_op", &wgpu::RenderPassDepthStencilAttachment::depthStoreOp)    
    .def_readwrite("depth_clear_value", &wgpu::RenderPassDepthStencilAttachment::depthClearValue)    
    .def_readwrite("depth_read_only", &wgpu::RenderPassDepthStencilAttachment::depthReadOnly)    
    .def_readwrite("stencil_load_op", &wgpu::RenderPassDepthStencilAttachment::stencilLoadOp)    
    .def_readwrite("stencil_store_op", &wgpu::RenderPassDepthStencilAttachment::stencilStoreOp)    
    .def_readwrite("stencil_clear_value", &wgpu::RenderPassDepthStencilAttachment::stencilClearValue)    
    .def_readwrite("stencil_read_only", &wgpu::RenderPassDepthStencilAttachment::stencilReadOnly)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::RenderPassDepthStencilAttachment obj{};        
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
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::RenderPassDepthStencilAttachment, RenderPassDepthStencilAttachment)

PYCLASS_BEGIN(m, wgpu::RenderPassDescriptor, RenderPassDescriptor) RenderPassDescriptor
    .def_readwrite("next_in_chain", &wgpu::RenderPassDescriptor::nextInChain)    
    .def_property("label",    
        [](const wgpu::RenderPassDescriptor& self) {        
            return self.label;            
        },        
        [](wgpu::RenderPassDescriptor& self, char const *  source) {        
            self.label = strdup(source);            
        }        
    )    
    .def_readwrite("color_attachment_count", &wgpu::RenderPassDescriptor::colorAttachmentCount)    
    .def_readwrite("color_attachments", &wgpu::RenderPassDescriptor::colorAttachments)    
    .def_readwrite("depth_stencil_attachment", &wgpu::RenderPassDescriptor::depthStencilAttachment)    
    .def_readwrite("occlusion_query_set", &wgpu::RenderPassDescriptor::occlusionQuerySet)    
    .def_readwrite("timestamp_writes", &wgpu::RenderPassDescriptor::timestampWrites)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::RenderPassDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("label"))        
        {        
            auto value = kwargs["label"].cast<std::string>();            
            obj.label = strdup(value.c_str());            
        }        
        if (kwargs.contains("color_attachment_count"))        
        {        
            auto value = kwargs["color_attachment_count"].cast<size_t>();            
            obj.colorAttachmentCount = value;            
        }        
        if (kwargs.contains("color_attachments"))        
        {        
            auto _value = kwargs["color_attachments"].cast<std::vector<wgpu::RenderPassColorAttachment>>();            
            auto count = _value.size();            
            auto value = new wgpu::RenderPassColorAttachment[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.colorAttachments = value;            
        }        
        if (kwargs.contains("depth_stencil_attachment"))        
        {        
            auto value = kwargs["depth_stencil_attachment"].cast<wgpu::RenderPassDepthStencilAttachment const *>();            
            obj.depthStencilAttachment = value;            
        }        
        if (kwargs.contains("occlusion_query_set"))        
        {        
            auto value = kwargs["occlusion_query_set"].cast<wgpu::QuerySet>();            
            obj.occlusionQuerySet = value;            
        }        
        if (kwargs.contains("timestamp_writes"))        
        {        
            auto value = kwargs["timestamp_writes"].cast<wgpu::RenderPassTimestampWrites const *>();            
            obj.timestampWrites = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::RenderPassDescriptor, RenderPassDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::RenderPassDescriptorMaxDrawCount, ChainedStruct, RenderPassDescriptorMaxDrawCount) RenderPassDescriptorMaxDrawCount
    .def_readwrite("next_in_chain", &wgpu::RenderPassDescriptorMaxDrawCount::nextInChain)    
    .def_readwrite("max_draw_count", &wgpu::RenderPassDescriptorMaxDrawCount::maxDrawCount)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::RenderPassDescriptorMaxDrawCount obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("max_draw_count"))        
        {        
            auto value = kwargs["max_draw_count"].cast<uint64_t>();            
            obj.maxDrawCount = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::RenderPassDescriptorMaxDrawCount, RenderPassDescriptorMaxDrawCount)

PYSUBCLASS_BEGIN(m, wgpu::RenderPassPixelLocalStorage, ChainedStruct, RenderPassPixelLocalStorage) RenderPassPixelLocalStorage
    .def_readwrite("next_in_chain", &wgpu::RenderPassPixelLocalStorage::nextInChain)    
    .def_readwrite("total_pixel_local_storage_size", &wgpu::RenderPassPixelLocalStorage::totalPixelLocalStorageSize)    
    .def_readwrite("storage_attachment_count", &wgpu::RenderPassPixelLocalStorage::storageAttachmentCount)    
    .def_readwrite("storage_attachments", &wgpu::RenderPassPixelLocalStorage::storageAttachments)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::RenderPassPixelLocalStorage obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("total_pixel_local_storage_size"))        
        {        
            auto value = kwargs["total_pixel_local_storage_size"].cast<uint64_t>();            
            obj.totalPixelLocalStorageSize = value;            
        }        
        if (kwargs.contains("storage_attachment_count"))        
        {        
            auto value = kwargs["storage_attachment_count"].cast<size_t>();            
            obj.storageAttachmentCount = value;            
        }        
        if (kwargs.contains("storage_attachments"))        
        {        
            auto _value = kwargs["storage_attachments"].cast<std::vector<wgpu::RenderPassStorageAttachment>>();            
            auto count = _value.size();            
            auto value = new wgpu::RenderPassStorageAttachment[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.storageAttachments = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::RenderPassPixelLocalStorage, RenderPassPixelLocalStorage)

PYCLASS_BEGIN(m, wgpu::RenderPassStorageAttachment, RenderPassStorageAttachment) RenderPassStorageAttachment
    .def_readwrite("next_in_chain", &wgpu::RenderPassStorageAttachment::nextInChain)    
    .def_readwrite("offset", &wgpu::RenderPassStorageAttachment::offset)    
    .def_readwrite("storage", &wgpu::RenderPassStorageAttachment::storage)    
    .def_readwrite("load_op", &wgpu::RenderPassStorageAttachment::loadOp)    
    .def_readwrite("store_op", &wgpu::RenderPassStorageAttachment::storeOp)    
    .def_readwrite("clear_value", &wgpu::RenderPassStorageAttachment::clearValue)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::RenderPassStorageAttachment obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("offset"))        
        {        
            auto value = kwargs["offset"].cast<uint64_t>();            
            obj.offset = value;            
        }        
        if (kwargs.contains("storage"))        
        {        
            auto value = kwargs["storage"].cast<wgpu::TextureView>();            
            obj.storage = value;            
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
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::RenderPassStorageAttachment, RenderPassStorageAttachment)

PYCLASS_BEGIN(m, wgpu::RenderPassTimestampWrites, RenderPassTimestampWrites) RenderPassTimestampWrites
    .def_readwrite("query_set", &wgpu::RenderPassTimestampWrites::querySet)    
    .def_readwrite("beginning_of_pass_write_index", &wgpu::RenderPassTimestampWrites::beginningOfPassWriteIndex)    
    .def_readwrite("end_of_pass_write_index", &wgpu::RenderPassTimestampWrites::endOfPassWriteIndex)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::RenderPassTimestampWrites obj{};        
        if (kwargs.contains("query_set"))        
        {        
            auto value = kwargs["query_set"].cast<wgpu::QuerySet>();            
            obj.querySet = value;            
        }        
        if (kwargs.contains("beginning_of_pass_write_index"))        
        {        
            auto value = kwargs["beginning_of_pass_write_index"].cast<uint32_t>();            
            obj.beginningOfPassWriteIndex = value;            
        }        
        if (kwargs.contains("end_of_pass_write_index"))        
        {        
            auto value = kwargs["end_of_pass_write_index"].cast<uint32_t>();            
            obj.endOfPassWriteIndex = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::RenderPassTimestampWrites, RenderPassTimestampWrites)

PYCLASS_BEGIN(m, wgpu::RequestDeviceCallbackInfo, RequestDeviceCallbackInfo) RequestDeviceCallbackInfo
    .def_readwrite("next_in_chain", &wgpu::RequestDeviceCallbackInfo::nextInChain)    
    .def_readwrite("mode", &wgpu::RequestDeviceCallbackInfo::mode)    
    .def_readwrite("userdata", &wgpu::RequestDeviceCallbackInfo::userdata)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::RequestDeviceCallbackInfo obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("mode"))        
        {        
            auto value = kwargs["mode"].cast<wgpu::CallbackMode>();            
            obj.mode = value;            
        }        
        if (kwargs.contains("userdata"))        
        {        
            auto value = kwargs["userdata"].cast<void *>();            
            obj.userdata = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::RequestDeviceCallbackInfo, RequestDeviceCallbackInfo)

PYCLASS_BEGIN(m, wgpu::VertexState, VertexState) VertexState
    .def_readwrite("next_in_chain", &wgpu::VertexState::nextInChain)    
    .def_readwrite("module", &wgpu::VertexState::module)    
    .def_property("entry_point",    
        [](const wgpu::VertexState& self) {        
            return self.entryPoint;            
        },        
        [](wgpu::VertexState& self, char const *  source) {        
            self.entryPoint = strdup(source);            
        }        
    )    
    .def_readwrite("constant_count", &wgpu::VertexState::constantCount)    
    .def_readwrite("constants", &wgpu::VertexState::constants)    
    .def_readwrite("buffer_count", &wgpu::VertexState::bufferCount)    
    .def_readwrite("buffers", &wgpu::VertexState::buffers)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::VertexState obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("module"))        
        {        
            auto value = kwargs["module"].cast<wgpu::ShaderModule>();            
            obj.module = value;            
        }        
        if (kwargs.contains("entry_point"))        
        {        
            auto value = kwargs["entry_point"].cast<std::string>();            
            obj.entryPoint = strdup(value.c_str());            
        }        
        if (kwargs.contains("constant_count"))        
        {        
            auto value = kwargs["constant_count"].cast<size_t>();            
            obj.constantCount = value;            
        }        
        if (kwargs.contains("constants"))        
        {        
            auto _value = kwargs["constants"].cast<std::vector<wgpu::ConstantEntry>>();            
            auto count = _value.size();            
            auto value = new wgpu::ConstantEntry[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.constants = value;            
        }        
        if (kwargs.contains("buffer_count"))        
        {        
            auto value = kwargs["buffer_count"].cast<size_t>();            
            obj.bufferCount = value;            
        }        
        if (kwargs.contains("buffers"))        
        {        
            auto _value = kwargs["buffers"].cast<std::vector<wgpu::VertexBufferLayout>>();            
            auto count = _value.size();            
            auto value = new wgpu::VertexBufferLayout[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.buffers = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::VertexState, VertexState)

PYCLASS_BEGIN(m, wgpu::PrimitiveState, PrimitiveState) PrimitiveState
    .def_readwrite("next_in_chain", &wgpu::PrimitiveState::nextInChain)    
    .def_readwrite("topology", &wgpu::PrimitiveState::topology)    
    .def_readwrite("strip_index_format", &wgpu::PrimitiveState::stripIndexFormat)    
    .def_readwrite("front_face", &wgpu::PrimitiveState::frontFace)    
    .def_readwrite("cull_mode", &wgpu::PrimitiveState::cullMode)    
    .def_readwrite("unclipped_depth", &wgpu::PrimitiveState::unclippedDepth)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::PrimitiveState obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
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
        if (kwargs.contains("unclipped_depth"))        
        {        
            auto value = kwargs["unclipped_depth"].cast<wgpu::Bool>();            
            obj.unclippedDepth = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::PrimitiveState, PrimitiveState)

PYSUBCLASS_BEGIN(m, wgpu::PrimitiveDepthClipControl, ChainedStruct, PrimitiveDepthClipControl) PrimitiveDepthClipControl
    .def_readwrite("next_in_chain", &wgpu::PrimitiveDepthClipControl::nextInChain)    
    .def_readwrite("unclipped_depth", &wgpu::PrimitiveDepthClipControl::unclippedDepth)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::PrimitiveDepthClipControl obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("unclipped_depth"))        
        {        
            auto value = kwargs["unclipped_depth"].cast<wgpu::Bool>();            
            obj.unclippedDepth = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::PrimitiveDepthClipControl, PrimitiveDepthClipControl)

PYCLASS_BEGIN(m, wgpu::DepthStencilState, DepthStencilState) DepthStencilState
    .def_readwrite("next_in_chain", &wgpu::DepthStencilState::nextInChain)    
    .def_readwrite("format", &wgpu::DepthStencilState::format)    
    .def_readwrite("depth_write_enabled", &wgpu::DepthStencilState::depthWriteEnabled)    
    .def_readwrite("depth_compare", &wgpu::DepthStencilState::depthCompare)    
    .def_readwrite("stencil_front", &wgpu::DepthStencilState::stencilFront)    
    .def_readwrite("stencil_back", &wgpu::DepthStencilState::stencilBack)    
    .def_readwrite("stencil_read_mask", &wgpu::DepthStencilState::stencilReadMask)    
    .def_readwrite("stencil_write_mask", &wgpu::DepthStencilState::stencilWriteMask)    
    .def_readwrite("depth_bias", &wgpu::DepthStencilState::depthBias)    
    .def_readwrite("depth_bias_slope_scale", &wgpu::DepthStencilState::depthBiasSlopeScale)    
    .def_readwrite("depth_bias_clamp", &wgpu::DepthStencilState::depthBiasClamp)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::DepthStencilState obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
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
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::DepthStencilState, DepthStencilState)

PYSUBCLASS_BEGIN(m, wgpu::DepthStencilStateDepthWriteDefinedDawn, ChainedStruct, DepthStencilStateDepthWriteDefinedDawn) DepthStencilStateDepthWriteDefinedDawn
    .def_readwrite("next_in_chain", &wgpu::DepthStencilStateDepthWriteDefinedDawn::nextInChain)    
    .def_readwrite("depth_write_defined", &wgpu::DepthStencilStateDepthWriteDefinedDawn::depthWriteDefined)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::DepthStencilStateDepthWriteDefinedDawn obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("depth_write_defined"))        
        {        
            auto value = kwargs["depth_write_defined"].cast<wgpu::Bool>();            
            obj.depthWriteDefined = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::DepthStencilStateDepthWriteDefinedDawn, DepthStencilStateDepthWriteDefinedDawn)

PYCLASS_BEGIN(m, wgpu::MultisampleState, MultisampleState) MultisampleState
    .def_readwrite("next_in_chain", &wgpu::MultisampleState::nextInChain)    
    .def_readwrite("count", &wgpu::MultisampleState::count)    
    .def_readwrite("mask", &wgpu::MultisampleState::mask)    
    .def_readwrite("alpha_to_coverage_enabled", &wgpu::MultisampleState::alphaToCoverageEnabled)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::MultisampleState obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("count"))        
        {        
            auto value = kwargs["count"].cast<uint32_t>();            
            obj.count = value;            
        }        
        if (kwargs.contains("mask"))        
        {        
            auto value = kwargs["mask"].cast<uint32_t>();            
            obj.mask = value;            
        }        
        if (kwargs.contains("alpha_to_coverage_enabled"))        
        {        
            auto value = kwargs["alpha_to_coverage_enabled"].cast<wgpu::Bool>();            
            obj.alphaToCoverageEnabled = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::MultisampleState, MultisampleState)

PYCLASS_BEGIN(m, wgpu::FragmentState, FragmentState) FragmentState
    .def_readwrite("next_in_chain", &wgpu::FragmentState::nextInChain)    
    .def_readwrite("module", &wgpu::FragmentState::module)    
    .def_property("entry_point",    
        [](const wgpu::FragmentState& self) {        
            return self.entryPoint;            
        },        
        [](wgpu::FragmentState& self, char const *  source) {        
            self.entryPoint = strdup(source);            
        }        
    )    
    .def_readwrite("constant_count", &wgpu::FragmentState::constantCount)    
    .def_readwrite("constants", &wgpu::FragmentState::constants)    
    .def_readwrite("target_count", &wgpu::FragmentState::targetCount)    
    .def_readwrite("targets", &wgpu::FragmentState::targets)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::FragmentState obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("module"))        
        {        
            auto value = kwargs["module"].cast<wgpu::ShaderModule>();            
            obj.module = value;            
        }        
        if (kwargs.contains("entry_point"))        
        {        
            auto value = kwargs["entry_point"].cast<std::string>();            
            obj.entryPoint = strdup(value.c_str());            
        }        
        if (kwargs.contains("constant_count"))        
        {        
            auto value = kwargs["constant_count"].cast<size_t>();            
            obj.constantCount = value;            
        }        
        if (kwargs.contains("constants"))        
        {        
            auto _value = kwargs["constants"].cast<std::vector<wgpu::ConstantEntry>>();            
            auto count = _value.size();            
            auto value = new wgpu::ConstantEntry[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.constants = value;            
        }        
        if (kwargs.contains("target_count"))        
        {        
            auto value = kwargs["target_count"].cast<size_t>();            
            obj.targetCount = value;            
        }        
        if (kwargs.contains("targets"))        
        {        
            auto _value = kwargs["targets"].cast<std::vector<wgpu::ColorTargetState>>();            
            auto count = _value.size();            
            auto value = new wgpu::ColorTargetState[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.targets = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::FragmentState, FragmentState)

PYCLASS_BEGIN(m, wgpu::ColorTargetState, ColorTargetState) ColorTargetState
    .def_readwrite("next_in_chain", &wgpu::ColorTargetState::nextInChain)    
    .def_readwrite("format", &wgpu::ColorTargetState::format)    
    .def_readwrite("blend", &wgpu::ColorTargetState::blend)    
    .def_readwrite("write_mask", &wgpu::ColorTargetState::writeMask)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::ColorTargetState obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("format"))        
        {        
            auto value = kwargs["format"].cast<wgpu::TextureFormat>();            
            obj.format = value;            
        }        
        if (kwargs.contains("blend"))        
        {        
            auto value = kwargs["blend"].cast<wgpu::BlendState const *>();            
            obj.blend = value;            
        }        
        if (kwargs.contains("write_mask"))        
        {        
            auto value = kwargs["write_mask"].cast<wgpu::ColorWriteMask>();            
            obj.writeMask = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::ColorTargetState, ColorTargetState)

PYSUBCLASS_BEGIN(m, wgpu::ColorTargetStateExpandResolveTextureDawn, ChainedStruct, ColorTargetStateExpandResolveTextureDawn) ColorTargetStateExpandResolveTextureDawn
    .def_readwrite("next_in_chain", &wgpu::ColorTargetStateExpandResolveTextureDawn::nextInChain)    
    .def_readwrite("enabled", &wgpu::ColorTargetStateExpandResolveTextureDawn::enabled)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::ColorTargetStateExpandResolveTextureDawn obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("enabled"))        
        {        
            auto value = kwargs["enabled"].cast<wgpu::Bool>();            
            obj.enabled = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::ColorTargetStateExpandResolveTextureDawn, ColorTargetStateExpandResolveTextureDawn)

PYCLASS_BEGIN(m, wgpu::BlendState, BlendState) BlendState
    .def_readwrite("color", &wgpu::BlendState::color)    
    .def_readwrite("alpha", &wgpu::BlendState::alpha)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::BlendState obj{};        
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
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::BlendState, BlendState)

PYCLASS_BEGIN(m, wgpu::RenderPipelineDescriptor, RenderPipelineDescriptor) RenderPipelineDescriptor
    .def_readwrite("next_in_chain", &wgpu::RenderPipelineDescriptor::nextInChain)    
    .def_property("label",    
        [](const wgpu::RenderPipelineDescriptor& self) {        
            return self.label;            
        },        
        [](wgpu::RenderPipelineDescriptor& self, char const *  source) {        
            self.label = strdup(source);            
        }        
    )    
    .def_readwrite("layout", &wgpu::RenderPipelineDescriptor::layout)    
    .def_readwrite("vertex", &wgpu::RenderPipelineDescriptor::vertex)    
    .def_readwrite("primitive", &wgpu::RenderPipelineDescriptor::primitive)    
    .def_readwrite("depth_stencil", &wgpu::RenderPipelineDescriptor::depthStencil)    
    .def_readwrite("multisample", &wgpu::RenderPipelineDescriptor::multisample)    
    .def_readwrite("fragment", &wgpu::RenderPipelineDescriptor::fragment)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::RenderPipelineDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("label"))        
        {        
            auto value = kwargs["label"].cast<std::string>();            
            obj.label = strdup(value.c_str());            
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
            auto value = kwargs["depth_stencil"].cast<wgpu::DepthStencilState const *>();            
            obj.depthStencil = value;            
        }        
        if (kwargs.contains("multisample"))        
        {        
            auto value = kwargs["multisample"].cast<wgpu::MultisampleState>();            
            obj.multisample = value;            
        }        
        if (kwargs.contains("fragment"))        
        {        
            auto value = kwargs["fragment"].cast<wgpu::FragmentState const *>();            
            obj.fragment = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::RenderPipelineDescriptor, RenderPipelineDescriptor)

PYCLASS_BEGIN(m, wgpu::SamplerDescriptor, SamplerDescriptor) SamplerDescriptor
    .def_readwrite("next_in_chain", &wgpu::SamplerDescriptor::nextInChain)    
    .def_property("label",    
        [](const wgpu::SamplerDescriptor& self) {        
            return self.label;            
        },        
        [](wgpu::SamplerDescriptor& self, char const *  source) {        
            self.label = strdup(source);            
        }        
    )    
    .def_readwrite("address_mode_u", &wgpu::SamplerDescriptor::addressModeU)    
    .def_readwrite("address_mode_v", &wgpu::SamplerDescriptor::addressModeV)    
    .def_readwrite("address_mode_w", &wgpu::SamplerDescriptor::addressModeW)    
    .def_readwrite("mag_filter", &wgpu::SamplerDescriptor::magFilter)    
    .def_readwrite("min_filter", &wgpu::SamplerDescriptor::minFilter)    
    .def_readwrite("mipmap_filter", &wgpu::SamplerDescriptor::mipmapFilter)    
    .def_readwrite("lod_min_clamp", &wgpu::SamplerDescriptor::lodMinClamp)    
    .def_readwrite("lod_max_clamp", &wgpu::SamplerDescriptor::lodMaxClamp)    
    .def_readwrite("compare", &wgpu::SamplerDescriptor::compare)    
    .def_readwrite("max_anisotropy", &wgpu::SamplerDescriptor::maxAnisotropy)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SamplerDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("label"))        
        {        
            auto value = kwargs["label"].cast<std::string>();            
            obj.label = strdup(value.c_str());            
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
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SamplerDescriptor, SamplerDescriptor)

PYCLASS_BEGIN(m, wgpu::ShaderModuleDescriptor, ShaderModuleDescriptor) ShaderModuleDescriptor
    .def_readwrite("next_in_chain", &wgpu::ShaderModuleDescriptor::nextInChain)    
    .def_property("label",    
        [](const wgpu::ShaderModuleDescriptor& self) {        
            return self.label;            
        },        
        [](wgpu::ShaderModuleDescriptor& self, char const *  source) {        
            self.label = strdup(source);            
        }        
    )    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::ShaderModuleDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("label"))        
        {        
            auto value = kwargs["label"].cast<std::string>();            
            obj.label = strdup(value.c_str());            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::ShaderModuleDescriptor, ShaderModuleDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::ShaderModuleSPIRVDescriptor, ChainedStruct, ShaderModuleSPIRVDescriptor) ShaderModuleSPIRVDescriptor
    .def_readwrite("next_in_chain", &wgpu::ShaderModuleSPIRVDescriptor::nextInChain)    
    .def_readwrite("code_size", &wgpu::ShaderModuleSPIRVDescriptor::codeSize)    
    .def_readwrite("code", &wgpu::ShaderModuleSPIRVDescriptor::code)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::ShaderModuleSPIRVDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("code_size"))        
        {        
            auto value = kwargs["code_size"].cast<uint32_t>();            
            obj.codeSize = value;            
        }        
        if (kwargs.contains("code"))        
        {        
            auto _value = kwargs["code"].cast<std::vector<uint32_t>>();            
            auto count = _value.size();            
            auto value = new uint32_t[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.code = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::ShaderModuleSPIRVDescriptor, ShaderModuleSPIRVDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::ShaderModuleWGSLDescriptor, ChainedStruct, ShaderModuleWGSLDescriptor) ShaderModuleWGSLDescriptor
    .def_readwrite("next_in_chain", &wgpu::ShaderModuleWGSLDescriptor::nextInChain)    
    .def_property("code",    
        [](const wgpu::ShaderModuleWGSLDescriptor& self) {        
            return self.code;            
        },        
        [](wgpu::ShaderModuleWGSLDescriptor& self, char const *  source) {        
            self.code = strdup(source);            
        }        
    )    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::ShaderModuleWGSLDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("code"))        
        {        
            auto value = kwargs["code"].cast<std::string>();            
            obj.code = strdup(value.c_str());            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::ShaderModuleWGSLDescriptor, ShaderModuleWGSLDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::DawnShaderModuleSPIRVOptionsDescriptor, ChainedStruct, DawnShaderModuleSPIRVOptionsDescriptor) DawnShaderModuleSPIRVOptionsDescriptor
    .def_readwrite("next_in_chain", &wgpu::DawnShaderModuleSPIRVOptionsDescriptor::nextInChain)    
    .def_readwrite("allow_non_uniform_derivatives", &wgpu::DawnShaderModuleSPIRVOptionsDescriptor::allowNonUniformDerivatives)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::DawnShaderModuleSPIRVOptionsDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("allow_non_uniform_derivatives"))        
        {        
            auto value = kwargs["allow_non_uniform_derivatives"].cast<wgpu::Bool>();            
            obj.allowNonUniformDerivatives = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::DawnShaderModuleSPIRVOptionsDescriptor, DawnShaderModuleSPIRVOptionsDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::ShaderModuleCompilationOptions, ChainedStruct, ShaderModuleCompilationOptions) ShaderModuleCompilationOptions
    .def_readwrite("next_in_chain", &wgpu::ShaderModuleCompilationOptions::nextInChain)    
    .def_readwrite("strict_math", &wgpu::ShaderModuleCompilationOptions::strictMath)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::ShaderModuleCompilationOptions obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("strict_math"))        
        {        
            auto value = kwargs["strict_math"].cast<wgpu::Bool>();            
            obj.strictMath = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::ShaderModuleCompilationOptions, ShaderModuleCompilationOptions)

PYCLASS_BEGIN(m, wgpu::StencilFaceState, StencilFaceState) StencilFaceState
    .def_readwrite("compare", &wgpu::StencilFaceState::compare)    
    .def_readwrite("fail_op", &wgpu::StencilFaceState::failOp)    
    .def_readwrite("depth_fail_op", &wgpu::StencilFaceState::depthFailOp)    
    .def_readwrite("pass_op", &wgpu::StencilFaceState::passOp)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::StencilFaceState obj{};        
        if (kwargs.contains("compare"))        
        {        
            auto value = kwargs["compare"].cast<wgpu::CompareFunction>();            
            obj.compare = value;            
        }        
        if (kwargs.contains("fail_op"))        
        {        
            auto value = kwargs["fail_op"].cast<wgpu::StencilOperation>();            
            obj.failOp = value;            
        }        
        if (kwargs.contains("depth_fail_op"))        
        {        
            auto value = kwargs["depth_fail_op"].cast<wgpu::StencilOperation>();            
            obj.depthFailOp = value;            
        }        
        if (kwargs.contains("pass_op"))        
        {        
            auto value = kwargs["pass_op"].cast<wgpu::StencilOperation>();            
            obj.passOp = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::StencilFaceState, StencilFaceState)

PYCLASS_BEGIN(m, wgpu::SurfaceDescriptor, SurfaceDescriptor) SurfaceDescriptor
    .def_readwrite("next_in_chain", &wgpu::SurfaceDescriptor::nextInChain)    
    .def_property("label",    
        [](const wgpu::SurfaceDescriptor& self) {        
            return self.label;            
        },        
        [](wgpu::SurfaceDescriptor& self, char const *  source) {        
            self.label = strdup(source);            
        }        
    )    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SurfaceDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("label"))        
        {        
            auto value = kwargs["label"].cast<std::string>();            
            obj.label = strdup(value.c_str());            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SurfaceDescriptor, SurfaceDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::SurfaceDescriptorFromAndroidNativeWindow, ChainedStruct, SurfaceDescriptorFromAndroidNativeWindow) SurfaceDescriptorFromAndroidNativeWindow
    .def_readwrite("next_in_chain", &wgpu::SurfaceDescriptorFromAndroidNativeWindow::nextInChain)    
    .def_readwrite("window", &wgpu::SurfaceDescriptorFromAndroidNativeWindow::window)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SurfaceDescriptorFromAndroidNativeWindow obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("window"))        
        {        
            auto value = kwargs["window"].cast<void *>();            
            obj.window = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SurfaceDescriptorFromAndroidNativeWindow, SurfaceDescriptorFromAndroidNativeWindow)

PYSUBCLASS_BEGIN(m, wgpu::SurfaceDescriptorFromCanvasHTMLSelector, ChainedStruct, SurfaceDescriptorFromCanvasHTMLSelector) SurfaceDescriptorFromCanvasHTMLSelector
    .def_readwrite("next_in_chain", &wgpu::SurfaceDescriptorFromCanvasHTMLSelector::nextInChain)    
    .def_property("selector",    
        [](const wgpu::SurfaceDescriptorFromCanvasHTMLSelector& self) {        
            return self.selector;            
        },        
        [](wgpu::SurfaceDescriptorFromCanvasHTMLSelector& self, char const *  source) {        
            self.selector = strdup(source);            
        }        
    )    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SurfaceDescriptorFromCanvasHTMLSelector obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("selector"))        
        {        
            auto value = kwargs["selector"].cast<std::string>();            
            obj.selector = strdup(value.c_str());            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SurfaceDescriptorFromCanvasHTMLSelector, SurfaceDescriptorFromCanvasHTMLSelector)

PYSUBCLASS_BEGIN(m, wgpu::SurfaceDescriptorFromMetalLayer, ChainedStruct, SurfaceDescriptorFromMetalLayer) SurfaceDescriptorFromMetalLayer
    .def_readwrite("next_in_chain", &wgpu::SurfaceDescriptorFromMetalLayer::nextInChain)    
    .def_readwrite("layer", &wgpu::SurfaceDescriptorFromMetalLayer::layer)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SurfaceDescriptorFromMetalLayer obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("layer"))        
        {        
            auto value = kwargs["layer"].cast<void *>();            
            obj.layer = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SurfaceDescriptorFromMetalLayer, SurfaceDescriptorFromMetalLayer)

PYSUBCLASS_BEGIN(m, wgpu::SurfaceDescriptorFromWindowsHWND, ChainedStruct, SurfaceDescriptorFromWindowsHWND) SurfaceDescriptorFromWindowsHWND
    .def_readwrite("next_in_chain", &wgpu::SurfaceDescriptorFromWindowsHWND::nextInChain)    
    .def_readwrite("hinstance", &wgpu::SurfaceDescriptorFromWindowsHWND::hinstance)    
    .def_readwrite("hwnd", &wgpu::SurfaceDescriptorFromWindowsHWND::hwnd)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SurfaceDescriptorFromWindowsHWND obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
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
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SurfaceDescriptorFromWindowsHWND, SurfaceDescriptorFromWindowsHWND)

PYSUBCLASS_BEGIN(m, wgpu::SurfaceDescriptorFromXcbWindow, ChainedStruct, SurfaceDescriptorFromXcbWindow) SurfaceDescriptorFromXcbWindow
    .def_readwrite("next_in_chain", &wgpu::SurfaceDescriptorFromXcbWindow::nextInChain)    
    .def_readwrite("connection", &wgpu::SurfaceDescriptorFromXcbWindow::connection)    
    .def_readwrite("window", &wgpu::SurfaceDescriptorFromXcbWindow::window)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SurfaceDescriptorFromXcbWindow obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("connection"))        
        {        
            auto value = kwargs["connection"].cast<void *>();            
            obj.connection = value;            
        }        
        if (kwargs.contains("window"))        
        {        
            auto value = kwargs["window"].cast<uint32_t>();            
            obj.window = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SurfaceDescriptorFromXcbWindow, SurfaceDescriptorFromXcbWindow)

PYSUBCLASS_BEGIN(m, wgpu::SurfaceDescriptorFromXlibWindow, ChainedStruct, SurfaceDescriptorFromXlibWindow) SurfaceDescriptorFromXlibWindow
    .def_readwrite("next_in_chain", &wgpu::SurfaceDescriptorFromXlibWindow::nextInChain)    
    .def_readwrite("display", &wgpu::SurfaceDescriptorFromXlibWindow::display)    
    .def_readwrite("window", &wgpu::SurfaceDescriptorFromXlibWindow::window)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SurfaceDescriptorFromXlibWindow obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("display"))        
        {        
            auto value = kwargs["display"].cast<void *>();            
            obj.display = value;            
        }        
        if (kwargs.contains("window"))        
        {        
            auto value = kwargs["window"].cast<uint64_t>();            
            obj.window = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SurfaceDescriptorFromXlibWindow, SurfaceDescriptorFromXlibWindow)

PYSUBCLASS_BEGIN(m, wgpu::SurfaceDescriptorFromWaylandSurface, ChainedStruct, SurfaceDescriptorFromWaylandSurface) SurfaceDescriptorFromWaylandSurface
    .def_readwrite("next_in_chain", &wgpu::SurfaceDescriptorFromWaylandSurface::nextInChain)    
    .def_readwrite("display", &wgpu::SurfaceDescriptorFromWaylandSurface::display)    
    .def_readwrite("surface", &wgpu::SurfaceDescriptorFromWaylandSurface::surface)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SurfaceDescriptorFromWaylandSurface obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("display"))        
        {        
            auto value = kwargs["display"].cast<void *>();            
            obj.display = value;            
        }        
        if (kwargs.contains("surface"))        
        {        
            auto value = kwargs["surface"].cast<void *>();            
            obj.surface = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SurfaceDescriptorFromWaylandSurface, SurfaceDescriptorFromWaylandSurface)

PYSUBCLASS_BEGIN(m, wgpu::SurfaceDescriptorFromWindowsCoreWindow, ChainedStruct, SurfaceDescriptorFromWindowsCoreWindow) SurfaceDescriptorFromWindowsCoreWindow
    .def_readwrite("next_in_chain", &wgpu::SurfaceDescriptorFromWindowsCoreWindow::nextInChain)    
    .def_readwrite("core_window", &wgpu::SurfaceDescriptorFromWindowsCoreWindow::coreWindow)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SurfaceDescriptorFromWindowsCoreWindow obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("core_window"))        
        {        
            auto value = kwargs["core_window"].cast<void *>();            
            obj.coreWindow = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SurfaceDescriptorFromWindowsCoreWindow, SurfaceDescriptorFromWindowsCoreWindow)

PYSUBCLASS_BEGIN(m, wgpu::SurfaceDescriptorFromWindowsSwapChainPanel, ChainedStruct, SurfaceDescriptorFromWindowsSwapChainPanel) SurfaceDescriptorFromWindowsSwapChainPanel
    .def_readwrite("next_in_chain", &wgpu::SurfaceDescriptorFromWindowsSwapChainPanel::nextInChain)    
    .def_readwrite("swap_chain_panel", &wgpu::SurfaceDescriptorFromWindowsSwapChainPanel::swapChainPanel)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SurfaceDescriptorFromWindowsSwapChainPanel obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("swap_chain_panel"))        
        {        
            auto value = kwargs["swap_chain_panel"].cast<void *>();            
            obj.swapChainPanel = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SurfaceDescriptorFromWindowsSwapChainPanel, SurfaceDescriptorFromWindowsSwapChainPanel)

PYCLASS_BEGIN(m, wgpu::SwapChainDescriptor, SwapChainDescriptor) SwapChainDescriptor
    .def_readwrite("next_in_chain", &wgpu::SwapChainDescriptor::nextInChain)    
    .def_property("label",    
        [](const wgpu::SwapChainDescriptor& self) {        
            return self.label;            
        },        
        [](wgpu::SwapChainDescriptor& self, char const *  source) {        
            self.label = strdup(source);            
        }        
    )    
    .def_readwrite("usage", &wgpu::SwapChainDescriptor::usage)    
    .def_readwrite("format", &wgpu::SwapChainDescriptor::format)    
    .def_readwrite("width", &wgpu::SwapChainDescriptor::width)    
    .def_readwrite("height", &wgpu::SwapChainDescriptor::height)    
    .def_readwrite("present_mode", &wgpu::SwapChainDescriptor::presentMode)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SwapChainDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("label"))        
        {        
            auto value = kwargs["label"].cast<std::string>();            
            obj.label = strdup(value.c_str());            
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
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SwapChainDescriptor, SwapChainDescriptor)

PYCLASS_BEGIN(m, wgpu::SurfaceTexture, SurfaceTexture) SurfaceTexture
    .def_readwrite("texture", &wgpu::SurfaceTexture::texture)    
    .def_readwrite("suboptimal", &wgpu::SurfaceTexture::suboptimal)    
    .def_readwrite("status", &wgpu::SurfaceTexture::status)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::SurfaceTexture obj{};        
        if (kwargs.contains("texture"))        
        {        
            auto value = kwargs["texture"].cast<wgpu::Texture>();            
            obj.texture = value;            
        }        
        if (kwargs.contains("suboptimal"))        
        {        
            auto value = kwargs["suboptimal"].cast<wgpu::Bool>();            
            obj.suboptimal = value;            
        }        
        if (kwargs.contains("status"))        
        {        
            auto value = kwargs["status"].cast<wgpu::SurfaceGetCurrentTextureStatus>();            
            obj.status = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::SurfaceTexture, SurfaceTexture)

PYCLASS_BEGIN(m, wgpu::TextureDataLayout, TextureDataLayout) TextureDataLayout
    .def_readwrite("next_in_chain", &wgpu::TextureDataLayout::nextInChain)    
    .def_readwrite("offset", &wgpu::TextureDataLayout::offset)    
    .def_readwrite("bytes_per_row", &wgpu::TextureDataLayout::bytesPerRow)    
    .def_readwrite("rows_per_image", &wgpu::TextureDataLayout::rowsPerImage)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::TextureDataLayout obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
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
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::TextureDataLayout, TextureDataLayout)

PYCLASS_BEGIN(m, wgpu::TextureDescriptor, TextureDescriptor) TextureDescriptor
    .def_readwrite("next_in_chain", &wgpu::TextureDescriptor::nextInChain)    
    .def_property("label",    
        [](const wgpu::TextureDescriptor& self) {        
            return self.label;            
        },        
        [](wgpu::TextureDescriptor& self, char const *  source) {        
            self.label = strdup(source);            
        }        
    )    
    .def_readwrite("usage", &wgpu::TextureDescriptor::usage)    
    .def_readwrite("dimension", &wgpu::TextureDescriptor::dimension)    
    .def_readwrite("size", &wgpu::TextureDescriptor::size)    
    .def_readwrite("format", &wgpu::TextureDescriptor::format)    
    .def_readwrite("mip_level_count", &wgpu::TextureDescriptor::mipLevelCount)    
    .def_readwrite("sample_count", &wgpu::TextureDescriptor::sampleCount)    
    .def_readwrite("view_format_count", &wgpu::TextureDescriptor::viewFormatCount)    
    .def_readwrite("view_formats", &wgpu::TextureDescriptor::viewFormats)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::TextureDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("label"))        
        {        
            auto value = kwargs["label"].cast<std::string>();            
            obj.label = strdup(value.c_str());            
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
            auto _value = kwargs["view_formats"].cast<std::vector<wgpu::TextureFormat>>();            
            auto count = _value.size();            
            auto value = new wgpu::TextureFormat[count];            
            std::copy(_value.begin(), _value.end(), value);            
            obj.viewFormats = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::TextureDescriptor, TextureDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::TextureBindingViewDimensionDescriptor, ChainedStruct, TextureBindingViewDimensionDescriptor) TextureBindingViewDimensionDescriptor
    .def_readwrite("next_in_chain", &wgpu::TextureBindingViewDimensionDescriptor::nextInChain)    
    .def_readwrite("texture_binding_view_dimension", &wgpu::TextureBindingViewDimensionDescriptor::textureBindingViewDimension)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::TextureBindingViewDimensionDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("texture_binding_view_dimension"))        
        {        
            auto value = kwargs["texture_binding_view_dimension"].cast<wgpu::TextureViewDimension>();            
            obj.textureBindingViewDimension = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::TextureBindingViewDimensionDescriptor, TextureBindingViewDimensionDescriptor)

PYCLASS_BEGIN(m, wgpu::TextureViewDescriptor, TextureViewDescriptor) TextureViewDescriptor
    .def_readwrite("next_in_chain", &wgpu::TextureViewDescriptor::nextInChain)    
    .def_property("label",    
        [](const wgpu::TextureViewDescriptor& self) {        
            return self.label;            
        },        
        [](wgpu::TextureViewDescriptor& self, char const *  source) {        
            self.label = strdup(source);            
        }        
    )    
    .def_readwrite("format", &wgpu::TextureViewDescriptor::format)    
    .def_readwrite("dimension", &wgpu::TextureViewDescriptor::dimension)    
    .def_readwrite("base_mip_level", &wgpu::TextureViewDescriptor::baseMipLevel)    
    .def_readwrite("mip_level_count", &wgpu::TextureViewDescriptor::mipLevelCount)    
    .def_readwrite("base_array_layer", &wgpu::TextureViewDescriptor::baseArrayLayer)    
    .def_readwrite("array_layer_count", &wgpu::TextureViewDescriptor::arrayLayerCount)    
    .def_readwrite("aspect", &wgpu::TextureViewDescriptor::aspect)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::TextureViewDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("label"))        
        {        
            auto value = kwargs["label"].cast<std::string>();            
            obj.label = strdup(value.c_str());            
        }        
        if (kwargs.contains("format"))        
        {        
            auto value = kwargs["format"].cast<wgpu::TextureFormat>();            
            obj.format = value;            
        }        
        if (kwargs.contains("dimension"))        
        {        
            auto value = kwargs["dimension"].cast<wgpu::TextureViewDimension>();            
            obj.dimension = value;            
        }        
        if (kwargs.contains("base_mip_level"))        
        {        
            auto value = kwargs["base_mip_level"].cast<uint32_t>();            
            obj.baseMipLevel = value;            
        }        
        if (kwargs.contains("mip_level_count"))        
        {        
            auto value = kwargs["mip_level_count"].cast<uint32_t>();            
            obj.mipLevelCount = value;            
        }        
        if (kwargs.contains("base_array_layer"))        
        {        
            auto value = kwargs["base_array_layer"].cast<uint32_t>();            
            obj.baseArrayLayer = value;            
        }        
        if (kwargs.contains("array_layer_count"))        
        {        
            auto value = kwargs["array_layer_count"].cast<uint32_t>();            
            obj.arrayLayerCount = value;            
        }        
        if (kwargs.contains("aspect"))        
        {        
            auto value = kwargs["aspect"].cast<wgpu::TextureAspect>();            
            obj.aspect = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::TextureViewDescriptor, TextureViewDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::YCbCrVkDescriptor, ChainedStruct, YCbCrVkDescriptor) YCbCrVkDescriptor
    .def_readwrite("next_in_chain", &wgpu::YCbCrVkDescriptor::nextInChain)    
    .def_readwrite("vk_format", &wgpu::YCbCrVkDescriptor::vkFormat)    
    .def_readwrite("vk_y_cb_cr_model", &wgpu::YCbCrVkDescriptor::vkYCbCrModel)    
    .def_readwrite("vk_y_cb_cr_range", &wgpu::YCbCrVkDescriptor::vkYCbCrRange)    
    .def_readwrite("vk_component_swizzle_red", &wgpu::YCbCrVkDescriptor::vkComponentSwizzleRed)    
    .def_readwrite("vk_component_swizzle_green", &wgpu::YCbCrVkDescriptor::vkComponentSwizzleGreen)    
    .def_readwrite("vk_component_swizzle_blue", &wgpu::YCbCrVkDescriptor::vkComponentSwizzleBlue)    
    .def_readwrite("vk_component_swizzle_alpha", &wgpu::YCbCrVkDescriptor::vkComponentSwizzleAlpha)    
    .def_readwrite("vk_x_chroma_offset", &wgpu::YCbCrVkDescriptor::vkXChromaOffset)    
    .def_readwrite("vk_y_chroma_offset", &wgpu::YCbCrVkDescriptor::vkYChromaOffset)    
    .def_readwrite("vk_chroma_filter", &wgpu::YCbCrVkDescriptor::vkChromaFilter)    
    .def_readwrite("force_explicit_reconstruction", &wgpu::YCbCrVkDescriptor::forceExplicitReconstruction)    
    .def_readwrite("external_format", &wgpu::YCbCrVkDescriptor::externalFormat)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::YCbCrVkDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("vk_format"))        
        {        
            auto value = kwargs["vk_format"].cast<uint32_t>();            
            obj.vkFormat = value;            
        }        
        if (kwargs.contains("vk_y_cb_cr_model"))        
        {        
            auto value = kwargs["vk_y_cb_cr_model"].cast<uint32_t>();            
            obj.vkYCbCrModel = value;            
        }        
        if (kwargs.contains("vk_y_cb_cr_range"))        
        {        
            auto value = kwargs["vk_y_cb_cr_range"].cast<uint32_t>();            
            obj.vkYCbCrRange = value;            
        }        
        if (kwargs.contains("vk_component_swizzle_red"))        
        {        
            auto value = kwargs["vk_component_swizzle_red"].cast<uint32_t>();            
            obj.vkComponentSwizzleRed = value;            
        }        
        if (kwargs.contains("vk_component_swizzle_green"))        
        {        
            auto value = kwargs["vk_component_swizzle_green"].cast<uint32_t>();            
            obj.vkComponentSwizzleGreen = value;            
        }        
        if (kwargs.contains("vk_component_swizzle_blue"))        
        {        
            auto value = kwargs["vk_component_swizzle_blue"].cast<uint32_t>();            
            obj.vkComponentSwizzleBlue = value;            
        }        
        if (kwargs.contains("vk_component_swizzle_alpha"))        
        {        
            auto value = kwargs["vk_component_swizzle_alpha"].cast<uint32_t>();            
            obj.vkComponentSwizzleAlpha = value;            
        }        
        if (kwargs.contains("vk_x_chroma_offset"))        
        {        
            auto value = kwargs["vk_x_chroma_offset"].cast<uint32_t>();            
            obj.vkXChromaOffset = value;            
        }        
        if (kwargs.contains("vk_y_chroma_offset"))        
        {        
            auto value = kwargs["vk_y_chroma_offset"].cast<uint32_t>();            
            obj.vkYChromaOffset = value;            
        }        
        if (kwargs.contains("vk_chroma_filter"))        
        {        
            auto value = kwargs["vk_chroma_filter"].cast<wgpu::FilterMode>();            
            obj.vkChromaFilter = value;            
        }        
        if (kwargs.contains("force_explicit_reconstruction"))        
        {        
            auto value = kwargs["force_explicit_reconstruction"].cast<wgpu::Bool>();            
            obj.forceExplicitReconstruction = value;            
        }        
        if (kwargs.contains("external_format"))        
        {        
            auto value = kwargs["external_format"].cast<uint64_t>();            
            obj.externalFormat = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::YCbCrVkDescriptor, YCbCrVkDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::DawnTextureInternalUsageDescriptor, ChainedStruct, DawnTextureInternalUsageDescriptor) DawnTextureInternalUsageDescriptor
    .def_readwrite("next_in_chain", &wgpu::DawnTextureInternalUsageDescriptor::nextInChain)    
    .def_readwrite("internal_usage", &wgpu::DawnTextureInternalUsageDescriptor::internalUsage)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::DawnTextureInternalUsageDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("internal_usage"))        
        {        
            auto value = kwargs["internal_usage"].cast<wgpu::TextureUsage>();            
            obj.internalUsage = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::DawnTextureInternalUsageDescriptor, DawnTextureInternalUsageDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::DawnEncoderInternalUsageDescriptor, ChainedStruct, DawnEncoderInternalUsageDescriptor) DawnEncoderInternalUsageDescriptor
    .def_readwrite("next_in_chain", &wgpu::DawnEncoderInternalUsageDescriptor::nextInChain)    
    .def_readwrite("use_internal_usages", &wgpu::DawnEncoderInternalUsageDescriptor::useInternalUsages)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::DawnEncoderInternalUsageDescriptor obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("use_internal_usages"))        
        {        
            auto value = kwargs["use_internal_usages"].cast<wgpu::Bool>();            
            obj.useInternalUsages = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::DawnEncoderInternalUsageDescriptor, DawnEncoderInternalUsageDescriptor)

PYSUBCLASS_BEGIN(m, wgpu::DawnAdapterPropertiesPowerPreference, ChainedStructOut, DawnAdapterPropertiesPowerPreference) DawnAdapterPropertiesPowerPreference
    .def_readonly("next_in_chain", &wgpu::DawnAdapterPropertiesPowerPreference::nextInChain)    
    .def_readonly("power_preference", &wgpu::DawnAdapterPropertiesPowerPreference::powerPreference)    
;
PYCLASS_END(m, wgpu::DawnAdapterPropertiesPowerPreference, DawnAdapterPropertiesPowerPreference)

PYCLASS_BEGIN(m, wgpu::MemoryHeapInfo, MemoryHeapInfo) MemoryHeapInfo
    .def_readwrite("properties", &wgpu::MemoryHeapInfo::properties)    
    .def_readwrite("size", &wgpu::MemoryHeapInfo::size)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::MemoryHeapInfo obj{};        
        if (kwargs.contains("properties"))        
        {        
            auto value = kwargs["properties"].cast<wgpu::HeapProperty>();            
            obj.properties = value;            
        }        
        if (kwargs.contains("size"))        
        {        
            auto value = kwargs["size"].cast<uint64_t>();            
            obj.size = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::MemoryHeapInfo, MemoryHeapInfo)

PYSUBCLASS_BEGIN(m, wgpu::AdapterPropertiesMemoryHeaps, ChainedStructOut, AdapterPropertiesMemoryHeaps) AdapterPropertiesMemoryHeaps
    .def_readonly("next_in_chain", &wgpu::AdapterPropertiesMemoryHeaps::nextInChain)    
    .def_readonly("heap_count", &wgpu::AdapterPropertiesMemoryHeaps::heapCount)    
    .def_readonly("heap_info", &wgpu::AdapterPropertiesMemoryHeaps::heapInfo)    
;
PYCLASS_END(m, wgpu::AdapterPropertiesMemoryHeaps, AdapterPropertiesMemoryHeaps)

PYSUBCLASS_BEGIN(m, wgpu::AdapterPropertiesD3D, ChainedStructOut, AdapterPropertiesD3D) AdapterPropertiesD3D
    .def_readonly("next_in_chain", &wgpu::AdapterPropertiesD3D::nextInChain)    
    .def_readonly("shader_model", &wgpu::AdapterPropertiesD3D::shaderModel)    
;
PYCLASS_END(m, wgpu::AdapterPropertiesD3D, AdapterPropertiesD3D)

PYSUBCLASS_BEGIN(m, wgpu::AdapterPropertiesVk, ChainedStructOut, AdapterPropertiesVk) AdapterPropertiesVk
    .def_readonly("next_in_chain", &wgpu::AdapterPropertiesVk::nextInChain)    
    .def_readonly("driver_version", &wgpu::AdapterPropertiesVk::driverVersion)    
;
PYCLASS_END(m, wgpu::AdapterPropertiesVk, AdapterPropertiesVk)

PYSUBCLASS_BEGIN(m, wgpu::DawnBufferDescriptorErrorInfoFromWireClient, ChainedStruct, DawnBufferDescriptorErrorInfoFromWireClient) DawnBufferDescriptorErrorInfoFromWireClient
    .def_readwrite("next_in_chain", &wgpu::DawnBufferDescriptorErrorInfoFromWireClient::nextInChain)    
    .def_readwrite("out_of_memory", &wgpu::DawnBufferDescriptorErrorInfoFromWireClient::outOfMemory)    
    .def(py::init([](const py::kwargs& kwargs) {    
        wgpu::DawnBufferDescriptorErrorInfoFromWireClient obj{};        
        if (kwargs.contains("next_in_chain"))        
        {        
            auto value = kwargs["next_in_chain"].cast<wgpu::ChainedStruct const *>();            
            obj.nextInChain = value;            
        }        
        if (kwargs.contains("out_of_memory"))        
        {        
            auto value = kwargs["out_of_memory"].cast<wgpu::Bool>();            
            obj.outOfMemory = value;            
        }        
        return obj;        
    }), py::return_value_policy::automatic_reference)    
;
PYCLASS_END(m, wgpu::DawnBufferDescriptorErrorInfoFromWireClient, DawnBufferDescriptorErrorInfoFromWireClient)


m.def("create_instance", &wgpu::CreateInstance
    , py::arg("descriptor") = nullptr
    , py::return_value_policy::automatic_reference)
    ;

m.def("get_instance_features", &wgpu::GetInstanceFeatures
    , py::arg("features")
    , py::return_value_policy::automatic_reference)
    ;

}