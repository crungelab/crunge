#ifndef WGPU_H
#define WGPU_H

#include <cassert>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <cstring>
#include <memory>
#include <functional>
#include <optional>

#include "webgpu/webgpu.h"
#include "webgpu/webgpu_cpp_chained_struct.h"
#include "webgpu/webgpu_enum_class_bitmasks.h"  // IWYU pragma: export

namespace wgpu {

namespace detail {
constexpr size_t ConstexprMax(size_t a, size_t b) {
    return a > b ? a : b;
}

template <typename T>
static T& AsNonConstReference(const T& value) {
    return const_cast<T&>(value);
}
}  // namespace detail


using BufferMapCallback = WGPUBufferMapCallback;
using Callback = WGPUCallback;
using CompilationInfoCallback = WGPUCompilationInfoCallback;
using CreateComputePipelineAsyncCallback = WGPUCreateComputePipelineAsyncCallback;
using CreateRenderPipelineAsyncCallback = WGPUCreateRenderPipelineAsyncCallback;
using DawnLoadCacheDataFunction = WGPUDawnLoadCacheDataFunction;
using DawnStoreCacheDataFunction = WGPUDawnStoreCacheDataFunction;
using DeviceLostCallback = WGPUDeviceLostCallback;
using DeviceLostCallbackNew = WGPUDeviceLostCallbackNew;
using ErrorCallback = WGPUErrorCallback;
using LoggingCallback = WGPULoggingCallback;
using PopErrorScopeCallback = WGPUPopErrorScopeCallback;
using Proc = WGPUProc;
using QueueWorkDoneCallback = WGPUQueueWorkDoneCallback;
using RequestAdapterCallback = WGPURequestAdapterCallback;
using RequestDeviceCallback = WGPURequestDeviceCallback;

using UncapturedErrorCallback = WGPUUncapturedErrorCallback;
using DeviceLostCallback2 = WGPUDeviceLostCallback2;
using RequestDeviceCallback2 = WGPURequestDeviceCallback2;
using QueueWorkDoneCallback2 = WGPUQueueWorkDoneCallback2;
using PopErrorScopeCallback2 = WGPUPopErrorScopeCallback2;
using CreateRenderPipelineAsyncCallback2 = WGPUCreateRenderPipelineAsyncCallback2;
using CreateComputePipelineAsyncCallback2 = WGPUCreateComputePipelineAsyncCallback2;
using CompilationInfoCallback2 = WGPUCompilationInfoCallback2;
using BufferMapCallback2 = WGPUBufferMapCallback2;
using RequestAdapterCallback2 = WGPURequestAdapterCallback2;

struct INTERNAL__HAVE_EMDAWNWEBGPU_HEADER;
struct RequestAdapterOptions;
struct RequestAdapterCallbackInfo;
struct RequestAdapterCallbackInfo2;
struct AdapterInfo;
struct AdapterProperties;
struct DeviceDescriptor;
struct DawnTogglesDescriptor;
struct DawnCacheDeviceDescriptor;
struct DawnWGSLBlocklist;
struct BindGroupEntry;
struct BindGroupDescriptor;
struct BufferBindingLayout;
struct SamplerBindingLayout;
struct StaticSamplerBindingLayout;
struct TextureBindingLayout;
struct SurfaceCapabilities;
struct SurfaceConfiguration;
struct ExternalTextureBindingEntry;
struct ExternalTextureBindingLayout;
struct StorageTextureBindingLayout;
struct BindGroupLayoutEntry;
struct BindGroupLayoutDescriptor;
struct BlendComponent;
struct StringView;
struct NullableStringView;
struct BufferDescriptor;
struct BufferHostMappedPointer;
struct BufferMapCallbackInfo;
struct BufferMapCallbackInfo2;
struct Color;
struct ConstantEntry;
struct CommandBufferDescriptor;
struct CommandEncoderDescriptor;
struct CompilationInfo;
struct CompilationInfoCallbackInfo;
struct CompilationInfoCallbackInfo2;
struct CompilationMessage;
struct ComputePassDescriptor;
struct ComputePassTimestampWrites;
struct ComputePipelineDescriptor;
struct DawnComputePipelineFullSubgroups;
struct CopyTextureForBrowserOptions;
struct CreateComputePipelineAsyncCallbackInfo;
struct CreateComputePipelineAsyncCallbackInfo2;
struct CreateRenderPipelineAsyncCallbackInfo;
struct CreateRenderPipelineAsyncCallbackInfo2;
struct AHardwareBufferProperties;
struct DeviceLostCallbackInfo;
struct DeviceLostCallbackInfo2;
struct UncapturedErrorCallbackInfo;
struct UncapturedErrorCallbackInfo2;
struct PopErrorScopeCallbackInfo;
struct PopErrorScopeCallbackInfo2;
struct Limits;
struct DawnExperimentalSubgroupLimits;
struct RequiredLimits;
struct SupportedLimits;
struct Extent2D;
struct Extent3D;
struct ExternalTextureDescriptor;
struct SharedBufferMemoryProperties;
struct SharedBufferMemoryDescriptor;
struct SharedTextureMemoryProperties;
struct SharedTextureMemoryAHardwareBufferProperties;
struct SharedTextureMemoryDescriptor;
struct SharedBufferMemoryBeginAccessDescriptor;
struct SharedBufferMemoryEndAccessState;
struct SharedTextureMemoryVkDedicatedAllocationDescriptor;
struct SharedTextureMemoryAHardwareBufferDescriptor;
struct SharedTextureMemoryDmaBufPlane;
struct SharedTextureMemoryDmaBufDescriptor;
struct SharedTextureMemoryOpaqueFDDescriptor;
struct SharedTextureMemoryZirconHandleDescriptor;
struct SharedTextureMemoryDXGISharedHandleDescriptor;
struct SharedTextureMemoryIOSurfaceDescriptor;
struct SharedTextureMemoryEGLImageDescriptor;
struct SharedTextureMemoryBeginAccessDescriptor;
struct SharedTextureMemoryEndAccessState;
struct SharedTextureMemoryVkImageLayoutBeginState;
struct SharedTextureMemoryVkImageLayoutEndState;
struct SharedTextureMemoryD3DSwapchainBeginState;
struct SharedFenceDescriptor;
struct SharedFenceVkSemaphoreOpaqueFDDescriptor;
struct SharedFenceVkSemaphoreSyncFDDescriptor;
struct SharedFenceVkSemaphoreZirconHandleDescriptor;
struct SharedFenceDXGISharedHandleDescriptor;
struct SharedFenceMTLSharedEventDescriptor;
struct SharedFenceExportInfo;
struct SharedFenceVkSemaphoreOpaqueFDExportInfo;
struct SharedFenceVkSemaphoreSyncFDExportInfo;
struct SharedFenceVkSemaphoreZirconHandleExportInfo;
struct SharedFenceDXGISharedHandleExportInfo;
struct SharedFenceMTLSharedEventExportInfo;
struct FormatCapabilities;
struct DrmFormatCapabilities;
struct DrmFormatProperties;
struct ImageCopyBuffer;
struct ImageCopyTexture;
struct ImageCopyExternalTexture;
struct Future;
struct FutureWaitInfo;
struct InstanceFeatures;
struct InstanceDescriptor;
struct DawnWireWGSLControl;
struct VertexAttribute;
struct VertexBufferLayout;
struct Origin3D;
struct Origin2D;
struct PipelineLayoutDescriptor;
struct PipelineLayoutPixelLocalStorage;
struct PipelineLayoutStorageAttachment;
struct ProgrammableStageDescriptor;
struct QuerySetDescriptor;
struct QueueDescriptor;
struct QueueWorkDoneCallbackInfo;
struct QueueWorkDoneCallbackInfo2;
struct RenderBundleDescriptor;
struct RenderBundleEncoderDescriptor;
struct RenderPassColorAttachment;
struct DawnRenderPassColorAttachmentRenderToSingleSampled;
struct RenderPassDepthStencilAttachment;
struct RenderPassDescriptor;
struct RenderPassDescriptorMaxDrawCount;
struct RenderPassPixelLocalStorage;
struct RenderPassStorageAttachment;
struct RenderPassTimestampWrites;
struct RequestDeviceCallbackInfo;
struct RequestDeviceCallbackInfo2;
struct VertexState;
struct PrimitiveState;
struct PrimitiveDepthClipControl;
struct DepthStencilState;
struct DepthStencilStateDepthWriteDefinedDawn;
struct MultisampleState;
struct FragmentState;
struct ColorTargetState;
struct ColorTargetStateExpandResolveTextureDawn;
struct BlendState;
struct RenderPipelineDescriptor;
struct SamplerDescriptor;
struct ShaderModuleDescriptor;
struct ShaderModuleSPIRVDescriptor;
struct ShaderModuleWGSLDescriptor;
struct DawnShaderModuleSPIRVOptionsDescriptor;
struct ShaderModuleCompilationOptions;
struct StencilFaceState;
struct SurfaceDescriptor;
struct SurfaceDescriptorFromAndroidNativeWindow;
struct SurfaceDescriptorFromCanvasHTMLSelector;
struct SurfaceDescriptorFromMetalLayer;
struct SurfaceDescriptorFromWindowsHWND;
struct SurfaceDescriptorFromXcbWindow;
struct SurfaceDescriptorFromXlibWindow;
struct SurfaceDescriptorFromWaylandSurface;
struct SurfaceDescriptorFromWindowsCoreWindow;
struct SurfaceDescriptorFromWindowsSwapChainPanel;
struct SwapChainDescriptor;
struct SurfaceTexture;
struct TextureDataLayout;
struct TextureDescriptor;
struct TextureBindingViewDimensionDescriptor;
struct TextureViewDescriptor;
struct YCbCrVkDescriptor;
struct DawnTextureInternalUsageDescriptor;
struct DawnEncoderInternalUsageDescriptor;
struct DawnAdapterPropertiesPowerPreference;
struct MemoryHeapInfo;
struct AdapterPropertiesMemoryHeaps;
struct AdapterPropertiesD3D;
struct AdapterPropertiesVk;
struct DawnBufferDescriptorErrorInfoFromWireClient;

class Adapter;
class BindGroup;
class BindGroupLayout;
class Buffer;
class CommandBuffer;
class CommandEncoder;
class ComputePassEncoder;
class ComputePipeline;
class Device;
class ExternalTexture;
class SharedBufferMemory;
class SharedTextureMemory;
class SharedFence;
class Instance;
class PipelineLayout;
class QuerySet;
class Queue;
class RenderBundle;
class RenderBundleEncoder;
class RenderPassEncoder;
class RenderPipeline;
class Sampler;
class ShaderModule;
class Surface;
class SwapChain;
class Texture;
class TextureView;

enum class RequestAdapterStatus : uint32_t {
    Success = WGPURequestAdapterStatus_Success,    
    InstanceDropped = WGPURequestAdapterStatus_InstanceDropped,    
    Unavailable = WGPURequestAdapterStatus_Unavailable,    
    Error = WGPURequestAdapterStatus_Error,    
    Unknown = WGPURequestAdapterStatus_Unknown,    
};

enum class AdapterType : uint32_t {
    DiscreteGPU = WGPUAdapterType_DiscreteGPU,    
    IntegratedGPU = WGPUAdapterType_IntegratedGPU,    
    CPU = WGPUAdapterType_CPU,    
    Unknown = WGPUAdapterType_Unknown,    
};

enum class AddressMode : uint32_t {
    Undefined = WGPUAddressMode_Undefined,    
    ClampToEdge = WGPUAddressMode_ClampToEdge,    
    Repeat = WGPUAddressMode_Repeat,    
    MirrorRepeat = WGPUAddressMode_MirrorRepeat,    
};

enum class BackendType : uint32_t {
    Undefined = WGPUBackendType_Undefined,    
    Null = WGPUBackendType_Null,    
    WebGPU = WGPUBackendType_WebGPU,    
    D3D11 = WGPUBackendType_D3D11,    
    D3D12 = WGPUBackendType_D3D12,    
    Metal = WGPUBackendType_Metal,    
    Vulkan = WGPUBackendType_Vulkan,    
    OpenGL = WGPUBackendType_OpenGL,    
    OpenGLES = WGPUBackendType_OpenGLES,    
};

enum class BufferBindingType : uint32_t {
    Undefined = WGPUBufferBindingType_Undefined,    
    Uniform = WGPUBufferBindingType_Uniform,    
    Storage = WGPUBufferBindingType_Storage,    
    ReadOnlyStorage = WGPUBufferBindingType_ReadOnlyStorage,    
};

enum class SamplerBindingType : uint32_t {
    Undefined = WGPUSamplerBindingType_Undefined,    
    Filtering = WGPUSamplerBindingType_Filtering,    
    NonFiltering = WGPUSamplerBindingType_NonFiltering,    
    Comparison = WGPUSamplerBindingType_Comparison,    
};

enum class TextureSampleType : uint32_t {
    Undefined = WGPUTextureSampleType_Undefined,    
    Float = WGPUTextureSampleType_Float,    
    UnfilterableFloat = WGPUTextureSampleType_UnfilterableFloat,    
    Depth = WGPUTextureSampleType_Depth,    
    Sint = WGPUTextureSampleType_Sint,    
    Uint = WGPUTextureSampleType_Uint,    
};

enum class StorageTextureAccess : uint32_t {
    Undefined = WGPUStorageTextureAccess_Undefined,    
    WriteOnly = WGPUStorageTextureAccess_WriteOnly,    
    ReadOnly = WGPUStorageTextureAccess_ReadOnly,    
    ReadWrite = WGPUStorageTextureAccess_ReadWrite,    
};

enum class BlendFactor : uint32_t {
    Undefined = WGPUBlendFactor_Undefined,    
    Zero = WGPUBlendFactor_Zero,    
    One = WGPUBlendFactor_One,    
    Src = WGPUBlendFactor_Src,    
    OneMinusSrc = WGPUBlendFactor_OneMinusSrc,    
    SrcAlpha = WGPUBlendFactor_SrcAlpha,    
    OneMinusSrcAlpha = WGPUBlendFactor_OneMinusSrcAlpha,    
    Dst = WGPUBlendFactor_Dst,    
    OneMinusDst = WGPUBlendFactor_OneMinusDst,    
    DstAlpha = WGPUBlendFactor_DstAlpha,    
    OneMinusDstAlpha = WGPUBlendFactor_OneMinusDstAlpha,    
    SrcAlphaSaturated = WGPUBlendFactor_SrcAlphaSaturated,    
    Constant = WGPUBlendFactor_Constant,    
    OneMinusConstant = WGPUBlendFactor_OneMinusConstant,    
    Src1 = WGPUBlendFactor_Src1,    
    OneMinusSrc1 = WGPUBlendFactor_OneMinusSrc1,    
    Src1Alpha = WGPUBlendFactor_Src1Alpha,    
    OneMinusSrc1Alpha = WGPUBlendFactor_OneMinusSrc1Alpha,    
};

enum class BlendOperation : uint32_t {
    Undefined = WGPUBlendOperation_Undefined,    
    Add = WGPUBlendOperation_Add,    
    Subtract = WGPUBlendOperation_Subtract,    
    ReverseSubtract = WGPUBlendOperation_ReverseSubtract,    
    Min = WGPUBlendOperation_Min,    
    Max = WGPUBlendOperation_Max,    
};

enum class BufferMapAsyncStatus : uint32_t {
    Success = WGPUBufferMapAsyncStatus_Success,    
    InstanceDropped = WGPUBufferMapAsyncStatus_InstanceDropped,    
    ValidationError = WGPUBufferMapAsyncStatus_ValidationError,    
    Unknown = WGPUBufferMapAsyncStatus_Unknown,    
    DeviceLost = WGPUBufferMapAsyncStatus_DeviceLost,    
    DestroyedBeforeCallback = WGPUBufferMapAsyncStatus_DestroyedBeforeCallback,    
    UnmappedBeforeCallback = WGPUBufferMapAsyncStatus_UnmappedBeforeCallback,    
    MappingAlreadyPending = WGPUBufferMapAsyncStatus_MappingAlreadyPending,    
    OffsetOutOfRange = WGPUBufferMapAsyncStatus_OffsetOutOfRange,    
    SizeOutOfRange = WGPUBufferMapAsyncStatus_SizeOutOfRange,    
};

enum class MapAsyncStatus : uint32_t {
    Success = WGPUMapAsyncStatus_Success,    
    InstanceDropped = WGPUMapAsyncStatus_InstanceDropped,    
    Error = WGPUMapAsyncStatus_Error,    
    Aborted = WGPUMapAsyncStatus_Aborted,    
    Unknown = WGPUMapAsyncStatus_Unknown,    
};

enum class BufferMapState : uint32_t {
    Unmapped = WGPUBufferMapState_Unmapped,    
    Pending = WGPUBufferMapState_Pending,    
    Mapped = WGPUBufferMapState_Mapped,    
};

enum class CompareFunction : uint32_t {
    Undefined = WGPUCompareFunction_Undefined,    
    Never = WGPUCompareFunction_Never,    
    Less = WGPUCompareFunction_Less,    
    Equal = WGPUCompareFunction_Equal,    
    LessEqual = WGPUCompareFunction_LessEqual,    
    Greater = WGPUCompareFunction_Greater,    
    NotEqual = WGPUCompareFunction_NotEqual,    
    GreaterEqual = WGPUCompareFunction_GreaterEqual,    
    Always = WGPUCompareFunction_Always,    
};

enum class CompilationInfoRequestStatus : uint32_t {
    Success = WGPUCompilationInfoRequestStatus_Success,    
    InstanceDropped = WGPUCompilationInfoRequestStatus_InstanceDropped,    
    Error = WGPUCompilationInfoRequestStatus_Error,    
    DeviceLost = WGPUCompilationInfoRequestStatus_DeviceLost,    
    Unknown = WGPUCompilationInfoRequestStatus_Unknown,    
};

enum class CompilationMessageType : uint32_t {
    Error = WGPUCompilationMessageType_Error,    
    Warning = WGPUCompilationMessageType_Warning,    
    Info = WGPUCompilationMessageType_Info,    
};

enum class CompositeAlphaMode : uint32_t {
    Auto = WGPUCompositeAlphaMode_Auto,    
    Opaque = WGPUCompositeAlphaMode_Opaque,    
    Premultiplied = WGPUCompositeAlphaMode_Premultiplied,    
    Unpremultiplied = WGPUCompositeAlphaMode_Unpremultiplied,    
    Inherit = WGPUCompositeAlphaMode_Inherit,    
};

enum class AlphaMode : uint32_t {
    Opaque = WGPUAlphaMode_Opaque,    
    Premultiplied = WGPUAlphaMode_Premultiplied,    
    Unpremultiplied = WGPUAlphaMode_Unpremultiplied,    
};

enum class CreatePipelineAsyncStatus : uint32_t {
    Success = WGPUCreatePipelineAsyncStatus_Success,    
    InstanceDropped = WGPUCreatePipelineAsyncStatus_InstanceDropped,    
    ValidationError = WGPUCreatePipelineAsyncStatus_ValidationError,    
    InternalError = WGPUCreatePipelineAsyncStatus_InternalError,    
    DeviceLost = WGPUCreatePipelineAsyncStatus_DeviceLost,    
    DeviceDestroyed = WGPUCreatePipelineAsyncStatus_DeviceDestroyed,    
    Unknown = WGPUCreatePipelineAsyncStatus_Unknown,    
};

enum class CullMode : uint32_t {
    Undefined = WGPUCullMode_Undefined,    
    None = WGPUCullMode_None,    
    Front = WGPUCullMode_Front,    
    Back = WGPUCullMode_Back,    
};

enum class DeviceLostReason : uint32_t {
    Unknown = WGPUDeviceLostReason_Unknown,    
    Destroyed = WGPUDeviceLostReason_Destroyed,    
    InstanceDropped = WGPUDeviceLostReason_InstanceDropped,    
    FailedCreation = WGPUDeviceLostReason_FailedCreation,    
};

enum class PopErrorScopeStatus : uint32_t {
    Success = WGPUPopErrorScopeStatus_Success,    
    InstanceDropped = WGPUPopErrorScopeStatus_InstanceDropped,    
};

enum class ErrorFilter : uint32_t {
    Validation = WGPUErrorFilter_Validation,    
    OutOfMemory = WGPUErrorFilter_OutOfMemory,    
    Internal = WGPUErrorFilter_Internal,    
};

enum class ErrorType : uint32_t {
    NoError = WGPUErrorType_NoError,    
    Validation = WGPUErrorType_Validation,    
    OutOfMemory = WGPUErrorType_OutOfMemory,    
    Internal = WGPUErrorType_Internal,    
    Unknown = WGPUErrorType_Unknown,    
    DeviceLost = WGPUErrorType_DeviceLost,    
};

enum class LoggingType : uint32_t {
    Verbose = WGPULoggingType_Verbose,    
    Info = WGPULoggingType_Info,    
    Warning = WGPULoggingType_Warning,    
    Error = WGPULoggingType_Error,    
};

enum class ExternalTextureRotation : uint32_t {
    Rotate0Degrees = WGPUExternalTextureRotation_Rotate0Degrees,    
    Rotate90Degrees = WGPUExternalTextureRotation_Rotate90Degrees,    
    Rotate180Degrees = WGPUExternalTextureRotation_Rotate180Degrees,    
    Rotate270Degrees = WGPUExternalTextureRotation_Rotate270Degrees,    
};

enum class Status : uint32_t {
    Success = WGPUStatus_Success,    
    Error = WGPUStatus_Error,    
};

enum class SharedFenceType : uint32_t {
    VkSemaphoreOpaqueFD = WGPUSharedFenceType_VkSemaphoreOpaqueFD,    
    VkSemaphoreSyncFD = WGPUSharedFenceType_VkSemaphoreSyncFD,    
    VkSemaphoreZirconHandle = WGPUSharedFenceType_VkSemaphoreZirconHandle,    
    DXGISharedHandle = WGPUSharedFenceType_DXGISharedHandle,    
    MTLSharedEvent = WGPUSharedFenceType_MTLSharedEvent,    
};

enum class FeatureName : uint32_t {
    DepthClipControl = WGPUFeatureName_DepthClipControl,    
    Depth32FloatStencil8 = WGPUFeatureName_Depth32FloatStencil8,    
    TimestampQuery = WGPUFeatureName_TimestampQuery,    
    TextureCompressionBC = WGPUFeatureName_TextureCompressionBC,    
    TextureCompressionETC2 = WGPUFeatureName_TextureCompressionETC2,    
    TextureCompressionASTC = WGPUFeatureName_TextureCompressionASTC,    
    IndirectFirstInstance = WGPUFeatureName_IndirectFirstInstance,    
    ShaderF16 = WGPUFeatureName_ShaderF16,    
    RG11B10UfloatRenderable = WGPUFeatureName_RG11B10UfloatRenderable,    
    BGRA8UnormStorage = WGPUFeatureName_BGRA8UnormStorage,    
    Float32Filterable = WGPUFeatureName_Float32Filterable,    
    Subgroups = WGPUFeatureName_Subgroups,    
    SubgroupsF16 = WGPUFeatureName_SubgroupsF16,    
    DawnInternalUsages = WGPUFeatureName_DawnInternalUsages,    
    DawnMultiPlanarFormats = WGPUFeatureName_DawnMultiPlanarFormats,    
    DawnNative = WGPUFeatureName_DawnNative,    
    ChromiumExperimentalTimestampQueryInsidePasses = WGPUFeatureName_ChromiumExperimentalTimestampQueryInsidePasses,    
    ImplicitDeviceSynchronization = WGPUFeatureName_ImplicitDeviceSynchronization,    
    SurfaceCapabilities = WGPUFeatureName_SurfaceCapabilities,    
    TransientAttachments = WGPUFeatureName_TransientAttachments,    
    MSAARenderToSingleSampled = WGPUFeatureName_MSAARenderToSingleSampled,    
    DualSourceBlending = WGPUFeatureName_DualSourceBlending,    
    D3D11MultithreadProtected = WGPUFeatureName_D3D11MultithreadProtected,    
    ANGLETextureSharing = WGPUFeatureName_ANGLETextureSharing,    
    ChromiumExperimentalSubgroups = WGPUFeatureName_ChromiumExperimentalSubgroups,    
    ChromiumExperimentalSubgroupUniformControlFlow = WGPUFeatureName_ChromiumExperimentalSubgroupUniformControlFlow,    
    PixelLocalStorageCoherent = WGPUFeatureName_PixelLocalStorageCoherent,    
    PixelLocalStorageNonCoherent = WGPUFeatureName_PixelLocalStorageNonCoherent,    
    Unorm16TextureFormats = WGPUFeatureName_Unorm16TextureFormats,    
    Snorm16TextureFormats = WGPUFeatureName_Snorm16TextureFormats,    
    MultiPlanarFormatExtendedUsages = WGPUFeatureName_MultiPlanarFormatExtendedUsages,    
    MultiPlanarFormatP010 = WGPUFeatureName_MultiPlanarFormatP010,    
    HostMappedPointer = WGPUFeatureName_HostMappedPointer,    
    MultiPlanarRenderTargets = WGPUFeatureName_MultiPlanarRenderTargets,    
    MultiPlanarFormatNv12a = WGPUFeatureName_MultiPlanarFormatNv12a,    
    FramebufferFetch = WGPUFeatureName_FramebufferFetch,    
    BufferMapExtendedUsages = WGPUFeatureName_BufferMapExtendedUsages,    
    AdapterPropertiesMemoryHeaps = WGPUFeatureName_AdapterPropertiesMemoryHeaps,    
    AdapterPropertiesD3D = WGPUFeatureName_AdapterPropertiesD3D,    
    AdapterPropertiesVk = WGPUFeatureName_AdapterPropertiesVk,    
    R8UnormStorage = WGPUFeatureName_R8UnormStorage,    
    FormatCapabilities = WGPUFeatureName_FormatCapabilities,    
    DrmFormatCapabilities = WGPUFeatureName_DrmFormatCapabilities,    
    Norm16TextureFormats = WGPUFeatureName_Norm16TextureFormats,    
    MultiPlanarFormatNv16 = WGPUFeatureName_MultiPlanarFormatNv16,    
    MultiPlanarFormatNv24 = WGPUFeatureName_MultiPlanarFormatNv24,    
    MultiPlanarFormatP210 = WGPUFeatureName_MultiPlanarFormatP210,    
    MultiPlanarFormatP410 = WGPUFeatureName_MultiPlanarFormatP410,    
    SharedTextureMemoryVkDedicatedAllocation = WGPUFeatureName_SharedTextureMemoryVkDedicatedAllocation,    
    SharedTextureMemoryAHardwareBuffer = WGPUFeatureName_SharedTextureMemoryAHardwareBuffer,    
    SharedTextureMemoryDmaBuf = WGPUFeatureName_SharedTextureMemoryDmaBuf,    
    SharedTextureMemoryOpaqueFD = WGPUFeatureName_SharedTextureMemoryOpaqueFD,    
    SharedTextureMemoryZirconHandle = WGPUFeatureName_SharedTextureMemoryZirconHandle,    
    SharedTextureMemoryDXGISharedHandle = WGPUFeatureName_SharedTextureMemoryDXGISharedHandle,    
    SharedTextureMemoryD3D11Texture2D = WGPUFeatureName_SharedTextureMemoryD3D11Texture2D,    
    SharedTextureMemoryIOSurface = WGPUFeatureName_SharedTextureMemoryIOSurface,    
    SharedTextureMemoryEGLImage = WGPUFeatureName_SharedTextureMemoryEGLImage,    
    SharedFenceVkSemaphoreOpaqueFD = WGPUFeatureName_SharedFenceVkSemaphoreOpaqueFD,    
    SharedFenceVkSemaphoreSyncFD = WGPUFeatureName_SharedFenceVkSemaphoreSyncFD,    
    SharedFenceVkSemaphoreZirconHandle = WGPUFeatureName_SharedFenceVkSemaphoreZirconHandle,    
    SharedFenceDXGISharedHandle = WGPUFeatureName_SharedFenceDXGISharedHandle,    
    SharedFenceMTLSharedEvent = WGPUFeatureName_SharedFenceMTLSharedEvent,    
    SharedBufferMemoryD3D12Resource = WGPUFeatureName_SharedBufferMemoryD3D12Resource,    
    StaticSamplers = WGPUFeatureName_StaticSamplers,    
    YCbCrVulkanSamplers = WGPUFeatureName_YCbCrVulkanSamplers,    
    ShaderModuleCompilationOptions = WGPUFeatureName_ShaderModuleCompilationOptions,    
    DawnLoadResolveTexture = WGPUFeatureName_DawnLoadResolveTexture,    
};

enum class FilterMode : uint32_t {
    Undefined = WGPUFilterMode_Undefined,    
    Nearest = WGPUFilterMode_Nearest,    
    Linear = WGPUFilterMode_Linear,    
};

enum class FrontFace : uint32_t {
    Undefined = WGPUFrontFace_Undefined,    
    CCW = WGPUFrontFace_CCW,    
    CW = WGPUFrontFace_CW,    
};

enum class IndexFormat : uint32_t {
    Undefined = WGPUIndexFormat_Undefined,    
    Uint16 = WGPUIndexFormat_Uint16,    
    Uint32 = WGPUIndexFormat_Uint32,    
};

enum class CallbackMode : uint32_t {
    WaitAnyOnly = WGPUCallbackMode_WaitAnyOnly,    
    AllowProcessEvents = WGPUCallbackMode_AllowProcessEvents,    
    AllowSpontaneous = WGPUCallbackMode_AllowSpontaneous,    
};

enum class WaitStatus : uint32_t {
    Success = WGPUWaitStatus_Success,    
    TimedOut = WGPUWaitStatus_TimedOut,    
    UnsupportedTimeout = WGPUWaitStatus_UnsupportedTimeout,    
    UnsupportedCount = WGPUWaitStatus_UnsupportedCount,    
    UnsupportedMixedSources = WGPUWaitStatus_UnsupportedMixedSources,    
    Unknown = WGPUWaitStatus_Unknown,    
};

enum class VertexStepMode : uint32_t {
    Undefined = WGPUVertexStepMode_Undefined,    
    VertexBufferNotUsed = WGPUVertexStepMode_VertexBufferNotUsed,    
    Vertex = WGPUVertexStepMode_Vertex,    
    Instance = WGPUVertexStepMode_Instance,    
};

enum class LoadOp : uint32_t {
    Undefined = WGPULoadOp_Undefined,    
    Clear = WGPULoadOp_Clear,    
    Load = WGPULoadOp_Load,    
    ExpandResolveTexture = WGPULoadOp_ExpandResolveTexture,    
};

enum class MipmapFilterMode : uint32_t {
    Undefined = WGPUMipmapFilterMode_Undefined,    
    Nearest = WGPUMipmapFilterMode_Nearest,    
    Linear = WGPUMipmapFilterMode_Linear,    
};

enum class StoreOp : uint32_t {
    Undefined = WGPUStoreOp_Undefined,    
    Store = WGPUStoreOp_Store,    
    Discard = WGPUStoreOp_Discard,    
};

enum class PowerPreference : uint32_t {
    Undefined = WGPUPowerPreference_Undefined,    
    LowPower = WGPUPowerPreference_LowPower,    
    HighPerformance = WGPUPowerPreference_HighPerformance,    
};

enum class PresentMode : uint32_t {
    Fifo = WGPUPresentMode_Fifo,    
    FifoRelaxed = WGPUPresentMode_FifoRelaxed,    
    Immediate = WGPUPresentMode_Immediate,    
    Mailbox = WGPUPresentMode_Mailbox,    
};

enum class PrimitiveTopology : uint32_t {
    Undefined = WGPUPrimitiveTopology_Undefined,    
    PointList = WGPUPrimitiveTopology_PointList,    
    LineList = WGPUPrimitiveTopology_LineList,    
    LineStrip = WGPUPrimitiveTopology_LineStrip,    
    TriangleList = WGPUPrimitiveTopology_TriangleList,    
    TriangleStrip = WGPUPrimitiveTopology_TriangleStrip,    
};

enum class QueryType : uint32_t {
    Occlusion = WGPUQueryType_Occlusion,    
    Timestamp = WGPUQueryType_Timestamp,    
};

enum class QueueWorkDoneStatus : uint32_t {
    Success = WGPUQueueWorkDoneStatus_Success,    
    InstanceDropped = WGPUQueueWorkDoneStatus_InstanceDropped,    
    Error = WGPUQueueWorkDoneStatus_Error,    
    Unknown = WGPUQueueWorkDoneStatus_Unknown,    
    DeviceLost = WGPUQueueWorkDoneStatus_DeviceLost,    
};

enum class RequestDeviceStatus : uint32_t {
    Success = WGPURequestDeviceStatus_Success,    
    InstanceDropped = WGPURequestDeviceStatus_InstanceDropped,    
    Error = WGPURequestDeviceStatus_Error,    
    Unknown = WGPURequestDeviceStatus_Unknown,    
};

enum class StencilOperation : uint32_t {
    Undefined = WGPUStencilOperation_Undefined,    
    Keep = WGPUStencilOperation_Keep,    
    Zero = WGPUStencilOperation_Zero,    
    Replace = WGPUStencilOperation_Replace,    
    Invert = WGPUStencilOperation_Invert,    
    IncrementClamp = WGPUStencilOperation_IncrementClamp,    
    DecrementClamp = WGPUStencilOperation_DecrementClamp,    
    IncrementWrap = WGPUStencilOperation_IncrementWrap,    
    DecrementWrap = WGPUStencilOperation_DecrementWrap,    
};

enum class SType : uint32_t {
    ShaderModuleSPIRVDescriptor = WGPUSType_ShaderModuleSPIRVDescriptor,    
    ShaderModuleWGSLDescriptor = WGPUSType_ShaderModuleWGSLDescriptor,    
    PrimitiveDepthClipControl = WGPUSType_PrimitiveDepthClipControl,    
    RenderPassDescriptorMaxDrawCount = WGPUSType_RenderPassDescriptorMaxDrawCount,    
    TextureBindingViewDimensionDescriptor = WGPUSType_TextureBindingViewDimensionDescriptor,    
    SurfaceDescriptorFromCanvasHTMLSelector = WGPUSType_SurfaceDescriptorFromCanvasHTMLSelector,    
    SurfaceDescriptorFromMetalLayer = WGPUSType_SurfaceDescriptorFromMetalLayer,    
    SurfaceDescriptorFromWindowsHWND = WGPUSType_SurfaceDescriptorFromWindowsHWND,    
    SurfaceDescriptorFromXlibWindow = WGPUSType_SurfaceDescriptorFromXlibWindow,    
    SurfaceDescriptorFromWaylandSurface = WGPUSType_SurfaceDescriptorFromWaylandSurface,    
    SurfaceDescriptorFromAndroidNativeWindow = WGPUSType_SurfaceDescriptorFromAndroidNativeWindow,    
    SurfaceDescriptorFromXcbWindow = WGPUSType_SurfaceDescriptorFromXcbWindow,    
    SurfaceDescriptorFromWindowsCoreWindow = WGPUSType_SurfaceDescriptorFromWindowsCoreWindow,    
    ExternalTextureBindingEntry = WGPUSType_ExternalTextureBindingEntry,    
    ExternalTextureBindingLayout = WGPUSType_ExternalTextureBindingLayout,    
    SurfaceDescriptorFromWindowsSwapChainPanel = WGPUSType_SurfaceDescriptorFromWindowsSwapChainPanel,    
    DepthStencilStateDepthWriteDefinedDawn = WGPUSType_DepthStencilStateDepthWriteDefinedDawn,    
    DawnTextureInternalUsageDescriptor = WGPUSType_DawnTextureInternalUsageDescriptor,    
    DawnEncoderInternalUsageDescriptor = WGPUSType_DawnEncoderInternalUsageDescriptor,    
    DawnInstanceDescriptor = WGPUSType_DawnInstanceDescriptor,    
    DawnCacheDeviceDescriptor = WGPUSType_DawnCacheDeviceDescriptor,    
    DawnAdapterPropertiesPowerPreference = WGPUSType_DawnAdapterPropertiesPowerPreference,    
    DawnBufferDescriptorErrorInfoFromWireClient = WGPUSType_DawnBufferDescriptorErrorInfoFromWireClient,    
    DawnTogglesDescriptor = WGPUSType_DawnTogglesDescriptor,    
    DawnShaderModuleSPIRVOptionsDescriptor = WGPUSType_DawnShaderModuleSPIRVOptionsDescriptor,    
    RequestAdapterOptionsLUID = WGPUSType_RequestAdapterOptionsLUID,    
    RequestAdapterOptionsGetGLProc = WGPUSType_RequestAdapterOptionsGetGLProc,    
    RequestAdapterOptionsD3D11Device = WGPUSType_RequestAdapterOptionsD3D11Device,    
    DawnRenderPassColorAttachmentRenderToSingleSampled = WGPUSType_DawnRenderPassColorAttachmentRenderToSingleSampled,    
    RenderPassPixelLocalStorage = WGPUSType_RenderPassPixelLocalStorage,    
    PipelineLayoutPixelLocalStorage = WGPUSType_PipelineLayoutPixelLocalStorage,    
    BufferHostMappedPointer = WGPUSType_BufferHostMappedPointer,    
    DawnExperimentalSubgroupLimits = WGPUSType_DawnExperimentalSubgroupLimits,    
    AdapterPropertiesMemoryHeaps = WGPUSType_AdapterPropertiesMemoryHeaps,    
    AdapterPropertiesD3D = WGPUSType_AdapterPropertiesD3D,    
    AdapterPropertiesVk = WGPUSType_AdapterPropertiesVk,    
    DawnComputePipelineFullSubgroups = WGPUSType_DawnComputePipelineFullSubgroups,    
    DawnWireWGSLControl = WGPUSType_DawnWireWGSLControl,    
    DawnWGSLBlocklist = WGPUSType_DawnWGSLBlocklist,    
    DrmFormatCapabilities = WGPUSType_DrmFormatCapabilities,    
    ShaderModuleCompilationOptions = WGPUSType_ShaderModuleCompilationOptions,    
    ColorTargetStateExpandResolveTextureDawn = WGPUSType_ColorTargetStateExpandResolveTextureDawn,    
    SharedTextureMemoryVkDedicatedAllocationDescriptor = WGPUSType_SharedTextureMemoryVkDedicatedAllocationDescriptor,    
    SharedTextureMemoryAHardwareBufferDescriptor = WGPUSType_SharedTextureMemoryAHardwareBufferDescriptor,    
    SharedTextureMemoryDmaBufDescriptor = WGPUSType_SharedTextureMemoryDmaBufDescriptor,    
    SharedTextureMemoryOpaqueFDDescriptor = WGPUSType_SharedTextureMemoryOpaqueFDDescriptor,    
    SharedTextureMemoryZirconHandleDescriptor = WGPUSType_SharedTextureMemoryZirconHandleDescriptor,    
    SharedTextureMemoryDXGISharedHandleDescriptor = WGPUSType_SharedTextureMemoryDXGISharedHandleDescriptor,    
    SharedTextureMemoryD3D11Texture2DDescriptor = WGPUSType_SharedTextureMemoryD3D11Texture2DDescriptor,    
    SharedTextureMemoryIOSurfaceDescriptor = WGPUSType_SharedTextureMemoryIOSurfaceDescriptor,    
    SharedTextureMemoryEGLImageDescriptor = WGPUSType_SharedTextureMemoryEGLImageDescriptor,    
    SharedTextureMemoryInitializedBeginState = WGPUSType_SharedTextureMemoryInitializedBeginState,    
    SharedTextureMemoryInitializedEndState = WGPUSType_SharedTextureMemoryInitializedEndState,    
    SharedTextureMemoryVkImageLayoutBeginState = WGPUSType_SharedTextureMemoryVkImageLayoutBeginState,    
    SharedTextureMemoryVkImageLayoutEndState = WGPUSType_SharedTextureMemoryVkImageLayoutEndState,    
    SharedTextureMemoryD3DSwapchainBeginState = WGPUSType_SharedTextureMemoryD3DSwapchainBeginState,    
    SharedFenceVkSemaphoreOpaqueFDDescriptor = WGPUSType_SharedFenceVkSemaphoreOpaqueFDDescriptor,    
    SharedFenceVkSemaphoreOpaqueFDExportInfo = WGPUSType_SharedFenceVkSemaphoreOpaqueFDExportInfo,    
    SharedFenceVkSemaphoreSyncFDDescriptor = WGPUSType_SharedFenceVkSemaphoreSyncFDDescriptor,    
    SharedFenceVkSemaphoreSyncFDExportInfo = WGPUSType_SharedFenceVkSemaphoreSyncFDExportInfo,    
    SharedFenceVkSemaphoreZirconHandleDescriptor = WGPUSType_SharedFenceVkSemaphoreZirconHandleDescriptor,    
    SharedFenceVkSemaphoreZirconHandleExportInfo = WGPUSType_SharedFenceVkSemaphoreZirconHandleExportInfo,    
    SharedFenceDXGISharedHandleDescriptor = WGPUSType_SharedFenceDXGISharedHandleDescriptor,    
    SharedFenceDXGISharedHandleExportInfo = WGPUSType_SharedFenceDXGISharedHandleExportInfo,    
    SharedFenceMTLSharedEventDescriptor = WGPUSType_SharedFenceMTLSharedEventDescriptor,    
    SharedFenceMTLSharedEventExportInfo = WGPUSType_SharedFenceMTLSharedEventExportInfo,    
    SharedBufferMemoryD3D12ResourceDescriptor = WGPUSType_SharedBufferMemoryD3D12ResourceDescriptor,    
    StaticSamplerBindingLayout = WGPUSType_StaticSamplerBindingLayout,    
    YCbCrVkDescriptor = WGPUSType_YCbCrVkDescriptor,    
    SharedTextureMemoryAHardwareBufferProperties = WGPUSType_SharedTextureMemoryAHardwareBufferProperties,    
    AHardwareBufferProperties = WGPUSType_AHardwareBufferProperties,    
};

enum class SurfaceGetCurrentTextureStatus : uint32_t {
    Success = WGPUSurfaceGetCurrentTextureStatus_Success,    
    Timeout = WGPUSurfaceGetCurrentTextureStatus_Timeout,    
    Outdated = WGPUSurfaceGetCurrentTextureStatus_Outdated,    
    Lost = WGPUSurfaceGetCurrentTextureStatus_Lost,    
    OutOfMemory = WGPUSurfaceGetCurrentTextureStatus_OutOfMemory,    
    DeviceLost = WGPUSurfaceGetCurrentTextureStatus_DeviceLost,    
    Error = WGPUSurfaceGetCurrentTextureStatus_Error,    
};

enum class TextureAspect : uint32_t {
    Undefined = WGPUTextureAspect_Undefined,    
    All = WGPUTextureAspect_All,    
    StencilOnly = WGPUTextureAspect_StencilOnly,    
    DepthOnly = WGPUTextureAspect_DepthOnly,    
    Plane0Only = WGPUTextureAspect_Plane0Only,    
    Plane1Only = WGPUTextureAspect_Plane1Only,    
    Plane2Only = WGPUTextureAspect_Plane2Only,    
};

enum class TextureDimension : uint32_t {
    Undefined = WGPUTextureDimension_Undefined,    
    e1D = WGPUTextureDimension_1D,    
    e2D = WGPUTextureDimension_2D,    
    e3D = WGPUTextureDimension_3D,    
};

enum class TextureFormat : uint32_t {
    Undefined = WGPUTextureFormat_Undefined,    
    R8Unorm = WGPUTextureFormat_R8Unorm,    
    R8Snorm = WGPUTextureFormat_R8Snorm,    
    R8Uint = WGPUTextureFormat_R8Uint,    
    R8Sint = WGPUTextureFormat_R8Sint,    
    R16Uint = WGPUTextureFormat_R16Uint,    
    R16Sint = WGPUTextureFormat_R16Sint,    
    R16Float = WGPUTextureFormat_R16Float,    
    RG8Unorm = WGPUTextureFormat_RG8Unorm,    
    RG8Snorm = WGPUTextureFormat_RG8Snorm,    
    RG8Uint = WGPUTextureFormat_RG8Uint,    
    RG8Sint = WGPUTextureFormat_RG8Sint,    
    R32Float = WGPUTextureFormat_R32Float,    
    R32Uint = WGPUTextureFormat_R32Uint,    
    R32Sint = WGPUTextureFormat_R32Sint,    
    RG16Uint = WGPUTextureFormat_RG16Uint,    
    RG16Sint = WGPUTextureFormat_RG16Sint,    
    RG16Float = WGPUTextureFormat_RG16Float,    
    RGBA8Unorm = WGPUTextureFormat_RGBA8Unorm,    
    RGBA8UnormSrgb = WGPUTextureFormat_RGBA8UnormSrgb,    
    RGBA8Snorm = WGPUTextureFormat_RGBA8Snorm,    
    RGBA8Uint = WGPUTextureFormat_RGBA8Uint,    
    RGBA8Sint = WGPUTextureFormat_RGBA8Sint,    
    BGRA8Unorm = WGPUTextureFormat_BGRA8Unorm,    
    BGRA8UnormSrgb = WGPUTextureFormat_BGRA8UnormSrgb,    
    RGB10A2Uint = WGPUTextureFormat_RGB10A2Uint,    
    RGB10A2Unorm = WGPUTextureFormat_RGB10A2Unorm,    
    RG11B10Ufloat = WGPUTextureFormat_RG11B10Ufloat,    
    RGB9E5Ufloat = WGPUTextureFormat_RGB9E5Ufloat,    
    RG32Float = WGPUTextureFormat_RG32Float,    
    RG32Uint = WGPUTextureFormat_RG32Uint,    
    RG32Sint = WGPUTextureFormat_RG32Sint,    
    RGBA16Uint = WGPUTextureFormat_RGBA16Uint,    
    RGBA16Sint = WGPUTextureFormat_RGBA16Sint,    
    RGBA16Float = WGPUTextureFormat_RGBA16Float,    
    RGBA32Float = WGPUTextureFormat_RGBA32Float,    
    RGBA32Uint = WGPUTextureFormat_RGBA32Uint,    
    RGBA32Sint = WGPUTextureFormat_RGBA32Sint,    
    Stencil8 = WGPUTextureFormat_Stencil8,    
    Depth16Unorm = WGPUTextureFormat_Depth16Unorm,    
    Depth24Plus = WGPUTextureFormat_Depth24Plus,    
    Depth24PlusStencil8 = WGPUTextureFormat_Depth24PlusStencil8,    
    Depth32Float = WGPUTextureFormat_Depth32Float,    
    Depth32FloatStencil8 = WGPUTextureFormat_Depth32FloatStencil8,    
    BC1RGBAUnorm = WGPUTextureFormat_BC1RGBAUnorm,    
    BC1RGBAUnormSrgb = WGPUTextureFormat_BC1RGBAUnormSrgb,    
    BC2RGBAUnorm = WGPUTextureFormat_BC2RGBAUnorm,    
    BC2RGBAUnormSrgb = WGPUTextureFormat_BC2RGBAUnormSrgb,    
    BC3RGBAUnorm = WGPUTextureFormat_BC3RGBAUnorm,    
    BC3RGBAUnormSrgb = WGPUTextureFormat_BC3RGBAUnormSrgb,    
    BC4RUnorm = WGPUTextureFormat_BC4RUnorm,    
    BC4RSnorm = WGPUTextureFormat_BC4RSnorm,    
    BC5RGUnorm = WGPUTextureFormat_BC5RGUnorm,    
    BC5RGSnorm = WGPUTextureFormat_BC5RGSnorm,    
    BC6HRGBUfloat = WGPUTextureFormat_BC6HRGBUfloat,    
    BC6HRGBFloat = WGPUTextureFormat_BC6HRGBFloat,    
    BC7RGBAUnorm = WGPUTextureFormat_BC7RGBAUnorm,    
    BC7RGBAUnormSrgb = WGPUTextureFormat_BC7RGBAUnormSrgb,    
    ETC2RGB8Unorm = WGPUTextureFormat_ETC2RGB8Unorm,    
    ETC2RGB8UnormSrgb = WGPUTextureFormat_ETC2RGB8UnormSrgb,    
    ETC2RGB8A1Unorm = WGPUTextureFormat_ETC2RGB8A1Unorm,    
    ETC2RGB8A1UnormSrgb = WGPUTextureFormat_ETC2RGB8A1UnormSrgb,    
    ETC2RGBA8Unorm = WGPUTextureFormat_ETC2RGBA8Unorm,    
    ETC2RGBA8UnormSrgb = WGPUTextureFormat_ETC2RGBA8UnormSrgb,    
    EACR11Unorm = WGPUTextureFormat_EACR11Unorm,    
    EACR11Snorm = WGPUTextureFormat_EACR11Snorm,    
    EACRG11Unorm = WGPUTextureFormat_EACRG11Unorm,    
    EACRG11Snorm = WGPUTextureFormat_EACRG11Snorm,    
    ASTC4x4Unorm = WGPUTextureFormat_ASTC4x4Unorm,    
    ASTC4x4UnormSrgb = WGPUTextureFormat_ASTC4x4UnormSrgb,    
    ASTC5x4Unorm = WGPUTextureFormat_ASTC5x4Unorm,    
    ASTC5x4UnormSrgb = WGPUTextureFormat_ASTC5x4UnormSrgb,    
    ASTC5x5Unorm = WGPUTextureFormat_ASTC5x5Unorm,    
    ASTC5x5UnormSrgb = WGPUTextureFormat_ASTC5x5UnormSrgb,    
    ASTC6x5Unorm = WGPUTextureFormat_ASTC6x5Unorm,    
    ASTC6x5UnormSrgb = WGPUTextureFormat_ASTC6x5UnormSrgb,    
    ASTC6x6Unorm = WGPUTextureFormat_ASTC6x6Unorm,    
    ASTC6x6UnormSrgb = WGPUTextureFormat_ASTC6x6UnormSrgb,    
    ASTC8x5Unorm = WGPUTextureFormat_ASTC8x5Unorm,    
    ASTC8x5UnormSrgb = WGPUTextureFormat_ASTC8x5UnormSrgb,    
    ASTC8x6Unorm = WGPUTextureFormat_ASTC8x6Unorm,    
    ASTC8x6UnormSrgb = WGPUTextureFormat_ASTC8x6UnormSrgb,    
    ASTC8x8Unorm = WGPUTextureFormat_ASTC8x8Unorm,    
    ASTC8x8UnormSrgb = WGPUTextureFormat_ASTC8x8UnormSrgb,    
    ASTC10x5Unorm = WGPUTextureFormat_ASTC10x5Unorm,    
    ASTC10x5UnormSrgb = WGPUTextureFormat_ASTC10x5UnormSrgb,    
    ASTC10x6Unorm = WGPUTextureFormat_ASTC10x6Unorm,    
    ASTC10x6UnormSrgb = WGPUTextureFormat_ASTC10x6UnormSrgb,    
    ASTC10x8Unorm = WGPUTextureFormat_ASTC10x8Unorm,    
    ASTC10x8UnormSrgb = WGPUTextureFormat_ASTC10x8UnormSrgb,    
    ASTC10x10Unorm = WGPUTextureFormat_ASTC10x10Unorm,    
    ASTC10x10UnormSrgb = WGPUTextureFormat_ASTC10x10UnormSrgb,    
    ASTC12x10Unorm = WGPUTextureFormat_ASTC12x10Unorm,    
    ASTC12x10UnormSrgb = WGPUTextureFormat_ASTC12x10UnormSrgb,    
    ASTC12x12Unorm = WGPUTextureFormat_ASTC12x12Unorm,    
    ASTC12x12UnormSrgb = WGPUTextureFormat_ASTC12x12UnormSrgb,    
    R16Unorm = WGPUTextureFormat_R16Unorm,    
    RG16Unorm = WGPUTextureFormat_RG16Unorm,    
    RGBA16Unorm = WGPUTextureFormat_RGBA16Unorm,    
    R16Snorm = WGPUTextureFormat_R16Snorm,    
    RG16Snorm = WGPUTextureFormat_RG16Snorm,    
    RGBA16Snorm = WGPUTextureFormat_RGBA16Snorm,    
    R8BG8Biplanar420Unorm = WGPUTextureFormat_R8BG8Biplanar420Unorm,    
    R10X6BG10X6Biplanar420Unorm = WGPUTextureFormat_R10X6BG10X6Biplanar420Unorm,    
    R8BG8A8Triplanar420Unorm = WGPUTextureFormat_R8BG8A8Triplanar420Unorm,    
    R8BG8Biplanar422Unorm = WGPUTextureFormat_R8BG8Biplanar422Unorm,    
    R8BG8Biplanar444Unorm = WGPUTextureFormat_R8BG8Biplanar444Unorm,    
    R10X6BG10X6Biplanar422Unorm = WGPUTextureFormat_R10X6BG10X6Biplanar422Unorm,    
    R10X6BG10X6Biplanar444Unorm = WGPUTextureFormat_R10X6BG10X6Biplanar444Unorm,    
    External = WGPUTextureFormat_External,    
};

enum class TextureViewDimension : uint32_t {
    Undefined = WGPUTextureViewDimension_Undefined,    
    e1D = WGPUTextureViewDimension_1D,    
    e2D = WGPUTextureViewDimension_2D,    
    e2DArray = WGPUTextureViewDimension_2DArray,    
    Cube = WGPUTextureViewDimension_Cube,    
    CubeArray = WGPUTextureViewDimension_CubeArray,    
    e3D = WGPUTextureViewDimension_3D,    
};

enum class VertexFormat : uint32_t {
    Uint8x2 = WGPUVertexFormat_Uint8x2,    
    Uint8x4 = WGPUVertexFormat_Uint8x4,    
    Sint8x2 = WGPUVertexFormat_Sint8x2,    
    Sint8x4 = WGPUVertexFormat_Sint8x4,    
    Unorm8x2 = WGPUVertexFormat_Unorm8x2,    
    Unorm8x4 = WGPUVertexFormat_Unorm8x4,    
    Snorm8x2 = WGPUVertexFormat_Snorm8x2,    
    Snorm8x4 = WGPUVertexFormat_Snorm8x4,    
    Uint16x2 = WGPUVertexFormat_Uint16x2,    
    Uint16x4 = WGPUVertexFormat_Uint16x4,    
    Sint16x2 = WGPUVertexFormat_Sint16x2,    
    Sint16x4 = WGPUVertexFormat_Sint16x4,    
    Unorm16x2 = WGPUVertexFormat_Unorm16x2,    
    Unorm16x4 = WGPUVertexFormat_Unorm16x4,    
    Snorm16x2 = WGPUVertexFormat_Snorm16x2,    
    Snorm16x4 = WGPUVertexFormat_Snorm16x4,    
    Float16x2 = WGPUVertexFormat_Float16x2,    
    Float16x4 = WGPUVertexFormat_Float16x4,    
    Float32 = WGPUVertexFormat_Float32,    
    Float32x2 = WGPUVertexFormat_Float32x2,    
    Float32x3 = WGPUVertexFormat_Float32x3,    
    Float32x4 = WGPUVertexFormat_Float32x4,    
    Uint32 = WGPUVertexFormat_Uint32,    
    Uint32x2 = WGPUVertexFormat_Uint32x2,    
    Uint32x3 = WGPUVertexFormat_Uint32x3,    
    Uint32x4 = WGPUVertexFormat_Uint32x4,    
    Sint32 = WGPUVertexFormat_Sint32,    
    Sint32x2 = WGPUVertexFormat_Sint32x2,    
    Sint32x3 = WGPUVertexFormat_Sint32x3,    
    Sint32x4 = WGPUVertexFormat_Sint32x4,    
    Unorm10_10_10_2 = WGPUVertexFormat_Unorm10_10_10_2,    
};

enum class WGSLFeatureName : uint32_t {
    ReadonlyAndReadwriteStorageTextures = WGPUWGSLFeatureName_ReadonlyAndReadwriteStorageTextures,    
    Packed4x8IntegerDotProduct = WGPUWGSLFeatureName_Packed4x8IntegerDotProduct,    
    UnrestrictedPointerParameters = WGPUWGSLFeatureName_UnrestrictedPointerParameters,    
    PointerCompositeAccess = WGPUWGSLFeatureName_PointerCompositeAccess,    
    ChromiumTestingUnimplemented = WGPUWGSLFeatureName_ChromiumTestingUnimplemented,    
    ChromiumTestingUnsafeExperimental = WGPUWGSLFeatureName_ChromiumTestingUnsafeExperimental,    
    ChromiumTestingExperimental = WGPUWGSLFeatureName_ChromiumTestingExperimental,    
    ChromiumTestingShippedWithKillswitch = WGPUWGSLFeatureName_ChromiumTestingShippedWithKillswitch,    
    ChromiumTestingShipped = WGPUWGSLFeatureName_ChromiumTestingShipped,    
};

enum class BufferUsage : uint64_t {
    None = WGPUBufferUsage_None,    
    MapRead = WGPUBufferUsage_MapRead,    
    MapWrite = WGPUBufferUsage_MapWrite,    
    CopySrc = WGPUBufferUsage_CopySrc,    
    CopyDst = WGPUBufferUsage_CopyDst,    
    Index = WGPUBufferUsage_Index,    
    Vertex = WGPUBufferUsage_Vertex,    
    Uniform = WGPUBufferUsage_Uniform,    
    Storage = WGPUBufferUsage_Storage,    
    Indirect = WGPUBufferUsage_Indirect,    
    QueryResolve = WGPUBufferUsage_QueryResolve,    
};

template<>
struct IsWGPUBitmask<wgpu::BufferUsage> {
    static constexpr bool enable = true;
};


enum class ColorWriteMask : uint64_t {
    None = WGPUColorWriteMask_None,    
    Red = WGPUColorWriteMask_Red,    
    Green = WGPUColorWriteMask_Green,    
    Blue = WGPUColorWriteMask_Blue,    
    Alpha = WGPUColorWriteMask_Alpha,    
    All = WGPUColorWriteMask_All,    
};

template<>
struct IsWGPUBitmask<wgpu::ColorWriteMask> {
    static constexpr bool enable = true;
};


enum class MapMode : uint64_t {
    None = WGPUMapMode_None,    
    Read = WGPUMapMode_Read,    
    Write = WGPUMapMode_Write,    
};

template<>
struct IsWGPUBitmask<wgpu::MapMode> {
    static constexpr bool enable = true;
};


enum class ShaderStage : uint64_t {
    None = WGPUShaderStage_None,    
    Vertex = WGPUShaderStage_Vertex,    
    Fragment = WGPUShaderStage_Fragment,    
    Compute = WGPUShaderStage_Compute,    
};

template<>
struct IsWGPUBitmask<wgpu::ShaderStage> {
    static constexpr bool enable = true;
};


enum class TextureUsage : uint64_t {
    None = WGPUTextureUsage_None,    
    CopySrc = WGPUTextureUsage_CopySrc,    
    CopyDst = WGPUTextureUsage_CopyDst,    
    TextureBinding = WGPUTextureUsage_TextureBinding,    
    StorageBinding = WGPUTextureUsage_StorageBinding,    
    RenderAttachment = WGPUTextureUsage_RenderAttachment,    
    TransientAttachment = WGPUTextureUsage_TransientAttachment,    
    StorageAttachment = WGPUTextureUsage_StorageAttachment,    
};

template<>
struct IsWGPUBitmask<wgpu::TextureUsage> {
    static constexpr bool enable = true;
};


enum class HeapProperty : uint64_t {
    DeviceLocal = WGPUHeapProperty_DeviceLocal,    
    HostVisible = WGPUHeapProperty_HostVisible,    
    HostCoherent = WGPUHeapProperty_HostCoherent,    
    HostUncached = WGPUHeapProperty_HostUncached,    
    HostCached = WGPUHeapProperty_HostCached,    
};

template<>
struct IsWGPUBitmask<wgpu::HeapProperty> {
    static constexpr bool enable = true;
};


// Special class for booleans in order to allow implicit conversions.
class Bool {
  public:
    constexpr Bool() = default;
    // NOLINTNEXTLINE(runtime/explicit) allow implicit construction
    constexpr Bool(bool value) : mValue(static_cast<WGPUBool>(value)) {}
    // NOLINTNEXTLINE(runtime/explicit) allow implicit construction
    Bool(WGPUBool value): mValue(value) {}

    constexpr operator bool() const { return static_cast<bool>(mValue); }

  private:
    friend struct std::hash<Bool>;
    // Default to false.
    WGPUBool mValue = static_cast<WGPUBool>(false);
};

// Helper class to wrap Status which allows implicit conversion to bool.
// Used while callers switch to checking the Status enum instead of booleans.
// TODO(crbug.com/42241199): Remove when all callers check the enum.
struct ConvertibleStatus {
    // NOLINTNEXTLINE(runtime/explicit) allow implicit construction
    constexpr ConvertibleStatus(Status status) : status(status) {}
    // NOLINTNEXTLINE(runtime/explicit) allow implicit conversion
    constexpr operator bool() const {
        return status == Status::Success;
    }
    // NOLINTNEXTLINE(runtime/explicit) allow implicit conversion
    constexpr operator Status() const {
        return status;
    }
    Status status;
};

template<typename Derived, typename CType>
class ObjectBase {
  public:
    ObjectBase() = default;
    ObjectBase(CType handle): mHandle(handle) {
        if (mHandle) Derived::WGPUAddRef(mHandle);
    }
    ~ObjectBase() {
        if (mHandle) Derived::WGPURelease(mHandle);
    }

    ObjectBase(ObjectBase const& other)
        : ObjectBase(other.Get()) {
    }
    Derived& operator=(ObjectBase const& other) {
        if (&other != this) {
            if (mHandle) Derived::WGPURelease(mHandle);
            mHandle = other.mHandle;
            if (mHandle) Derived::WGPUAddRef(mHandle);
        }

        return static_cast<Derived&>(*this);
    }

    ObjectBase(ObjectBase&& other) {
        mHandle = other.mHandle;
        other.mHandle = 0;
    }
    Derived& operator=(ObjectBase&& other) {
        if (&other != this) {
            if (mHandle) Derived::WGPURelease(mHandle);
            mHandle = other.mHandle;
            other.mHandle = 0;
        }

        return static_cast<Derived&>(*this);
    }

    ObjectBase(std::nullptr_t) {}
    Derived& operator=(std::nullptr_t) {
        if (mHandle != nullptr) {
            Derived::WGPURelease(mHandle);
            mHandle = nullptr;
        }
        return static_cast<Derived&>(*this);
    }

    bool operator==(std::nullptr_t) const {
        return mHandle == nullptr;
    }
    bool operator!=(std::nullptr_t) const {
        return mHandle != nullptr;
    }

    explicit operator bool() const {
        return mHandle != nullptr;
    }
    CType Get() const {
        return mHandle;
    }
    CType MoveToCHandle() {
        CType result = mHandle;
        mHandle = 0;
        return result;
    }
    static Derived Acquire(CType handle) {
        Derived result;
        result.mHandle = handle;
        return result;
    }

  protected:
    CType mHandle = nullptr;
};struct BlendComponent {
    operator const WGPUBlendComponent&() const noexcept;
    BlendOperation operation = BlendOperation::Add;
    BlendFactor srcFactor = BlendFactor::One;
    BlendFactor dstFactor = BlendFactor::Zero;
};

struct BlendState {
    operator const WGPUBlendState&() const noexcept;
    BlendComponent color = {};
    BlendComponent alpha = {};
};

struct VertexAttribute {
    operator const WGPUVertexAttribute&() const noexcept;
    VertexFormat format;
    uint64_t offset;
    uint32_t shaderLocation;
};

struct ColorTargetState {
    operator const WGPUColorTargetState&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    TextureFormat format;
    BlendState const * blend = nullptr;
    ColorWriteMask writeMask = ColorWriteMask::All;
};

struct ConstantEntry {
    operator const WGPUConstantEntry&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * key;
    double value;
};

class ShaderModule : public ObjectBase<ShaderModule, WGPUShaderModule> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    void GetCompilationInfo(CompilationInfoCallback callback, void * userdata) const;    
    void SetLabel(char const* label) const;    
    void SetLabel2(NullableStringView label) const;    
    
    friend ObjectBase<ShaderModule, WGPUShaderModule>;
    static void WGPUAddRef(WGPUShaderModule handle);
    static void WGPURelease(WGPUShaderModule handle);
};

struct StencilFaceState {
    operator const WGPUStencilFaceState&() const noexcept;
    CompareFunction compare = CompareFunction::Always;
    StencilOperation failOp = StencilOperation::Keep;
    StencilOperation depthFailOp = StencilOperation::Keep;
    StencilOperation passOp = StencilOperation::Keep;
};

struct VertexBufferLayout {
    operator const WGPUVertexBufferLayout&() const noexcept;
    uint64_t arrayStride;
    VertexStepMode stepMode = VertexStepMode::Vertex;
    size_t attributeCount;
    VertexAttribute const * attributes;
};

struct Color {
    operator const WGPUColor&() const noexcept;
    double r;
    double g;
    double b;
    double a;
};

class TextureView : public ObjectBase<TextureView, WGPUTextureView> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    void SetLabel(char const* label) const;    
    void SetLabel2(NullableStringView label) const;    
    
    friend ObjectBase<TextureView, WGPUTextureView>;
    static void WGPUAddRef(WGPUTextureView handle);
    static void WGPURelease(WGPUTextureView handle);
};

class QuerySet : public ObjectBase<QuerySet, WGPUQuerySet> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    void SetLabel(char const* label) const;    
    void SetLabel2(NullableStringView label) const;    
    QueryType GetType() const;    
    uint32_t GetCount() const;    
    void Destroy() const;    
    
    friend ObjectBase<QuerySet, WGPUQuerySet>;
    static void WGPUAddRef(WGPUQuerySet handle);
    static void WGPURelease(WGPUQuerySet handle);
};

struct StorageTextureBindingLayout {
    operator const WGPUStorageTextureBindingLayout&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    StorageTextureAccess access = StorageTextureAccess::Undefined;
    TextureFormat format = TextureFormat::Undefined;
    TextureViewDimension viewDimension = TextureViewDimension::e2D;
};

struct TextureBindingLayout {
    operator const WGPUTextureBindingLayout&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    TextureSampleType sampleType = TextureSampleType::Undefined;
    TextureViewDimension viewDimension = TextureViewDimension::e2D;
    Bool multisampled = false;
};

struct SamplerBindingLayout {
    operator const WGPUSamplerBindingLayout&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    SamplerBindingType type = SamplerBindingType::Undefined;
};

struct BufferBindingLayout {
    operator const WGPUBufferBindingLayout&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    BufferBindingType type = BufferBindingType::Undefined;
    Bool hasDynamicOffset = false;
    uint64_t minBindingSize = 0;
};

class Sampler : public ObjectBase<Sampler, WGPUSampler> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    void SetLabel(char const* label) const;    
    void SetLabel2(NullableStringView label) const;    
    
    friend ObjectBase<Sampler, WGPUSampler>;
    static void WGPUAddRef(WGPUSampler handle);
    static void WGPURelease(WGPUSampler handle);
};

class Buffer : public ObjectBase<Buffer, WGPUBuffer> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    void MapAsync(MapMode mode, size_t offset, size_t size, BufferMapCallback callback, void * userdata) const;    
    void * GetMappedRange(size_t offset, size_t size) const;    
    void const * GetConstMappedRange(size_t offset, size_t size) const;    
    void SetLabel(char const* label) const;    
    void SetLabel2(NullableStringView label) const;    
    BufferUsage GetUsage() const;    
    uint64_t GetSize() const;    
    BufferMapState GetMapState() const;    
    void Unmap() const;    
    void Destroy() const;    
    
    friend ObjectBase<Buffer, WGPUBuffer>;
    static void WGPUAddRef(WGPUBuffer handle);
    static void WGPURelease(WGPUBuffer handle);
};

struct Limits {
    operator const WGPULimits&() const noexcept;
    uint32_t maxTextureDimension1D = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t maxTextureDimension2D = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t maxTextureDimension3D = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t maxTextureArrayLayers = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t maxBindGroups = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t maxBindGroupsPlusVertexBuffers = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t maxBindingsPerBindGroup = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t maxDynamicUniformBuffersPerPipelineLayout = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t maxDynamicStorageBuffersPerPipelineLayout = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t maxSampledTexturesPerShaderStage = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t maxSamplersPerShaderStage = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t maxStorageBuffersPerShaderStage = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t maxStorageTexturesPerShaderStage = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t maxUniformBuffersPerShaderStage = WGPU_LIMIT_U32_UNDEFINED;
    uint64_t maxUniformBufferBindingSize = WGPU_LIMIT_U64_UNDEFINED;
    uint64_t maxStorageBufferBindingSize = WGPU_LIMIT_U64_UNDEFINED;
    uint32_t minUniformBufferOffsetAlignment = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t minStorageBufferOffsetAlignment = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t maxVertexBuffers = WGPU_LIMIT_U32_UNDEFINED;
    uint64_t maxBufferSize = WGPU_LIMIT_U64_UNDEFINED;
    uint32_t maxVertexAttributes = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t maxVertexBufferArrayStride = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t maxInterStageShaderComponents = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t maxInterStageShaderVariables = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t maxColorAttachments = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t maxColorAttachmentBytesPerSample = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t maxComputeWorkgroupStorageSize = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t maxComputeInvocationsPerWorkgroup = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t maxComputeWorkgroupSizeX = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t maxComputeWorkgroupSizeY = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t maxComputeWorkgroupSizeZ = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t maxComputeWorkgroupsPerDimension = WGPU_LIMIT_U32_UNDEFINED;
};

struct MemoryHeapInfo {
    operator const WGPUMemoryHeapInfo&() const noexcept;
    HeapProperty properties;
    uint64_t size;
};

struct Extent3D {
    operator const WGPUExtent3D&() const noexcept;
    uint32_t width;
    uint32_t height = 1;
    uint32_t depthOrArrayLayers = 1;
};

class Texture : public ObjectBase<Texture, WGPUTexture> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    TextureView CreateView(TextureViewDescriptor const* descriptor) const;    
    TextureView CreateErrorView(TextureViewDescriptor const* descriptor) const;    
    void SetLabel(char const* label) const;    
    void SetLabel2(NullableStringView label) const;    
    uint32_t GetWidth() const;    
    uint32_t GetHeight() const;    
    uint32_t GetDepthOrArrayLayers() const;    
    uint32_t GetMipLevelCount() const;    
    uint32_t GetSampleCount() const;    
    TextureDimension GetDimension() const;    
    TextureFormat GetFormat() const;    
    TextureUsage GetUsage() const;    
    void Destroy() const;    
    
    friend ObjectBase<Texture, WGPUTexture>;
    static void WGPUAddRef(WGPUTexture handle);
    static void WGPURelease(WGPUTexture handle);
};

struct FragmentState {
    operator const WGPUFragmentState&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    ShaderModule module;
    char const * entryPoint = nullptr;
    size_t constantCount = 0;
    ConstantEntry const * constants;
    size_t targetCount;
    ColorTargetState const * targets;
};

struct MultisampleState {
    operator const WGPUMultisampleState&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    uint32_t count = 1;
    uint32_t mask = 0xFFFFFFFF;
    Bool alphaToCoverageEnabled = false;
};

struct DepthStencilState {
    operator const WGPUDepthStencilState&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    TextureFormat format;
    Bool depthWriteEnabled = false;
    CompareFunction depthCompare = CompareFunction::Undefined;
    StencilFaceState stencilFront = {};
    StencilFaceState stencilBack = {};
    uint32_t stencilReadMask = 0xFFFFFFFF;
    uint32_t stencilWriteMask = 0xFFFFFFFF;
    int32_t depthBias = 0;
    float depthBiasSlopeScale = 0.0f;
    float depthBiasClamp = 0.0f;
};

struct PrimitiveState {
    operator const WGPUPrimitiveState&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    PrimitiveTopology topology = PrimitiveTopology::TriangleList;
    IndexFormat stripIndexFormat = IndexFormat::Undefined;
    FrontFace frontFace = FrontFace::CCW;
    CullMode cullMode = CullMode::None;
    Bool unclippedDepth = false;
};

struct VertexState {
    operator const WGPUVertexState&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    ShaderModule module;
    char const * entryPoint = nullptr;
    size_t constantCount = 0;
    ConstantEntry const * constants;
    size_t bufferCount = 0;
    VertexBufferLayout const * buffers;
};

class PipelineLayout : public ObjectBase<PipelineLayout, WGPUPipelineLayout> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    void SetLabel(char const* label) const;    
    void SetLabel2(NullableStringView label) const;    
    
    friend ObjectBase<PipelineLayout, WGPUPipelineLayout>;
    static void WGPUAddRef(WGPUPipelineLayout handle);
    static void WGPURelease(WGPUPipelineLayout handle);
};

struct RenderPassStorageAttachment {
    operator const WGPURenderPassStorageAttachment&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    uint64_t offset = 0;
    TextureView storage;
    LoadOp loadOp;
    StoreOp storeOp;
    Color clearValue = {};
};

struct RenderPassTimestampWrites {
    operator const WGPURenderPassTimestampWrites&() const noexcept;
    QuerySet querySet;
    uint32_t beginningOfPassWriteIndex = WGPU_QUERY_SET_INDEX_UNDEFINED;
    uint32_t endOfPassWriteIndex = WGPU_QUERY_SET_INDEX_UNDEFINED;
};

struct RenderPassDepthStencilAttachment {
    operator const WGPURenderPassDepthStencilAttachment&() const noexcept;
    TextureView view;
    LoadOp depthLoadOp = LoadOp::Undefined;
    StoreOp depthStoreOp = StoreOp::Undefined;
    float depthClearValue = NAN;
    Bool depthReadOnly = false;
    LoadOp stencilLoadOp = LoadOp::Undefined;
    StoreOp stencilStoreOp = StoreOp::Undefined;
    uint32_t stencilClearValue = 0;
    Bool stencilReadOnly = false;
};

struct RenderPassColorAttachment {
    operator const WGPURenderPassColorAttachment&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    TextureView view = nullptr;
    uint32_t depthSlice = WGPU_DEPTH_SLICE_UNDEFINED;
    TextureView resolveTarget = nullptr;
    LoadOp loadOp;
    StoreOp storeOp;
    Color clearValue = {};
};

struct PipelineLayoutStorageAttachment {
    operator const WGPUPipelineLayoutStorageAttachment&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    uint64_t offset = 0;
    TextureFormat format;
};

class BindGroupLayout : public ObjectBase<BindGroupLayout, WGPUBindGroupLayout> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    void SetLabel(char const* label) const;    
    void SetLabel2(NullableStringView label) const;    
    
    friend ObjectBase<BindGroupLayout, WGPUBindGroupLayout>;
    static void WGPUAddRef(WGPUBindGroupLayout handle);
    static void WGPURelease(WGPUBindGroupLayout handle);
};

struct InstanceFeatures {
    operator const WGPUInstanceFeatures&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    Bool timedWaitAnyEnable = false;
    size_t timedWaitAnyMaxCount = 0;
};

struct Future {
    operator const WGPUFuture&() const noexcept;
    uint64_t id;
};

struct Extent2D {
    operator const WGPUExtent2D&() const noexcept;
    uint32_t width;
    uint32_t height;
};

struct Origin3D {
    operator const WGPUOrigin3D&() const noexcept;
    uint32_t x = 0;
    uint32_t y = 0;
    uint32_t z = 0;
};

class ExternalTexture : public ObjectBase<ExternalTexture, WGPUExternalTexture> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    void SetLabel(char const* label) const;    
    void SetLabel2(NullableStringView label) const;    
    void Destroy() const;    
    void Expire() const;    
    void Refresh() const;    
    
    friend ObjectBase<ExternalTexture, WGPUExternalTexture>;
    static void WGPUAddRef(WGPUExternalTexture handle);
    static void WGPURelease(WGPUExternalTexture handle);
};

struct TextureDataLayout {
    operator const WGPUTextureDataLayout&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    uint64_t offset = 0;
    uint32_t bytesPerRow = WGPU_COPY_STRIDE_UNDEFINED;
    uint32_t rowsPerImage = WGPU_COPY_STRIDE_UNDEFINED;
};

struct DrmFormatProperties {
    operator const WGPUDrmFormatProperties&() const noexcept;
    uint64_t modifier;
    uint32_t modifierPlaneCount;
};

class SharedFence : public ObjectBase<SharedFence, WGPUSharedFence> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    void ExportInfo(SharedFenceExportInfo * info) const;    
    
    friend ObjectBase<SharedFence, WGPUSharedFence>;
    static void WGPUAddRef(WGPUSharedFence handle);
    static void WGPURelease(WGPUSharedFence handle);
};

struct SharedTextureMemoryDmaBufPlane {
    operator const WGPUSharedTextureMemoryDmaBufPlane&() const noexcept;
    int fd;
    uint64_t offset;
    uint32_t stride;
};

// Can be chained in SamplerDescriptor
// Can be chained in TextureViewDescriptor
struct YCbCrVkDescriptor : ChainedStruct {
    YCbCrVkDescriptor();

    struct Init;
    YCbCrVkDescriptor(Init&& init);
    operator const WGPUYCbCrVkDescriptor&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(uint32_t ));
    alignas(kFirstMemberAlignment) uint32_t vkFormat = 0;
    uint32_t vkYCbCrModel = 0;
    uint32_t vkYCbCrRange = 0;
    uint32_t vkComponentSwizzleRed = 0;
    uint32_t vkComponentSwizzleGreen = 0;
    uint32_t vkComponentSwizzleBlue = 0;
    uint32_t vkComponentSwizzleAlpha = 0;
    uint32_t vkXChromaOffset = 0;
    uint32_t vkYChromaOffset = 0;
    FilterMode vkChromaFilter = FilterMode::Nearest;
    Bool forceExplicitReconstruction = false;
    uint64_t externalFormat = 0;
};

struct Origin2D {
    operator const WGPUOrigin2D&() const noexcept;
    uint32_t x = 0;
    uint32_t y = 0;
};

struct ProgrammableStageDescriptor {
    operator const WGPUProgrammableStageDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    ShaderModule module;
    char const * entryPoint = nullptr;
    size_t constantCount = 0;
    ConstantEntry const * constants;
};

struct ComputePassTimestampWrites {
    operator const WGPUComputePassTimestampWrites&() const noexcept;
    QuerySet querySet;
    uint32_t beginningOfPassWriteIndex = WGPU_QUERY_SET_INDEX_UNDEFINED;
    uint32_t endOfPassWriteIndex = WGPU_QUERY_SET_INDEX_UNDEFINED;
};

struct CompilationMessage {
    operator const WGPUCompilationMessage&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * message = nullptr;
    CompilationMessageType type;
    uint64_t lineNum;
    uint64_t linePos;
    uint64_t offset;
    uint64_t length;
    uint64_t utf16LinePos;
    uint64_t utf16Offset;
    uint64_t utf16Length;
};

struct BindGroupLayoutEntry {
    operator const WGPUBindGroupLayoutEntry&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    uint32_t binding;
    ShaderStage visibility;
    BufferBindingLayout buffer = {};
    SamplerBindingLayout sampler = {};
    TextureBindingLayout texture = {};
    StorageTextureBindingLayout storageTexture = {};
};

class Device : public ObjectBase<Device, WGPUDevice> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    BindGroup CreateBindGroup(BindGroupDescriptor const* descriptor) const;    
    BindGroupLayout CreateBindGroupLayout(BindGroupLayoutDescriptor const* descriptor) const;    
    Buffer CreateBuffer(BufferDescriptor const* descriptor) const;    
    Buffer CreateErrorBuffer(BufferDescriptor const* descriptor) const;    
    CommandEncoder CreateCommandEncoder(CommandEncoderDescriptor const* descriptor) const;    
    ComputePipeline CreateComputePipeline(ComputePipelineDescriptor const* descriptor) const;    
    void CreateComputePipelineAsync(ComputePipelineDescriptor const* descriptor, CreateComputePipelineAsyncCallback callback, void * userdata) const;    
    ExternalTexture CreateExternalTexture(ExternalTextureDescriptor const* externalTextureDescriptor) const;    
    ExternalTexture CreateErrorExternalTexture() const;    
    PipelineLayout CreatePipelineLayout(PipelineLayoutDescriptor const* descriptor) const;    
    QuerySet CreateQuerySet(QuerySetDescriptor const* descriptor) const;    
    void CreateRenderPipelineAsync(RenderPipelineDescriptor const* descriptor, CreateRenderPipelineAsyncCallback callback, void * userdata) const;    
    RenderBundleEncoder CreateRenderBundleEncoder(RenderBundleEncoderDescriptor const* descriptor) const;    
    RenderPipeline CreateRenderPipeline(RenderPipelineDescriptor const* descriptor) const;    
    Sampler CreateSampler(SamplerDescriptor const* descriptor) const;    
    ShaderModule CreateShaderModule(ShaderModuleDescriptor const* descriptor) const;    
    ShaderModule CreateErrorShaderModule(ShaderModuleDescriptor const* descriptor, char const* errorMessage) const;    
    ShaderModule CreateErrorShaderModule2(ShaderModuleDescriptor const* descriptor, StringView errorMessage) const;    
    SwapChain CreateSwapChain(Surface surface, SwapChainDescriptor const* descriptor) const;    
    Texture CreateTexture(TextureDescriptor const* descriptor) const;    
    SharedBufferMemory ImportSharedBufferMemory(SharedBufferMemoryDescriptor const* descriptor) const;    
    SharedTextureMemory ImportSharedTextureMemory(SharedTextureMemoryDescriptor const* descriptor) const;    
    SharedFence ImportSharedFence(SharedFenceDescriptor const* descriptor) const;    
    Texture CreateErrorTexture(TextureDescriptor const* descriptor) const;    
    void Destroy() const;    
    Status GetAHardwareBufferProperties(void * handle, AHardwareBufferProperties * properties) const;    
    Status GetLimits(SupportedLimits * limits) const;    
    bool HasFeature(FeatureName feature) const;    
    size_t EnumerateFeatures(FeatureName * features) const;    
    Adapter GetAdapter() const;    
    Queue GetQueue() const;    
    void InjectError(ErrorType type, char const* message) const;    
    void InjectError2(ErrorType type, StringView message) const;    
    void ForceLoss(DeviceLostReason type, char const* message) const;    
    void ForceLoss2(DeviceLostReason type, StringView message) const;    
    void Tick() const;    
    void SetUncapturedErrorCallback(ErrorCallback callback, void * userdata) const;    
    void SetLoggingCallback(LoggingCallback callback, void * userdata) const;    
    void SetDeviceLostCallback(DeviceLostCallback callback, void * userdata) const;    
    void PushErrorScope(ErrorFilter filter) const;    
    void PopErrorScope(ErrorCallback oldCallback, void * userdata) const;    
    void SetLabel(char const* label) const;    
    void SetLabel2(NullableStringView label) const;    
    void ValidateTextureDescriptor(TextureDescriptor const* descriptor) const;    
    TextureUsage GetSupportedSurfaceUsage(Surface surface) const;    
    
    friend ObjectBase<Device, WGPUDevice>;
    static void WGPUAddRef(WGPUDevice handle);
    static void WGPURelease(WGPUDevice handle);
};

struct BindGroupEntry {
    operator const WGPUBindGroupEntry&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    uint32_t binding;
    Buffer buffer = nullptr;
    uint64_t offset = 0;
    uint64_t size = WGPU_WHOLE_SIZE;
    Sampler sampler = nullptr;
    TextureView textureView = nullptr;
};

struct UncapturedErrorCallbackInfo2 {
    operator const WGPUUncapturedErrorCallbackInfo2&() const noexcept;
    UncapturedErrorCallback callback = nullptr;
};

struct DeviceLostCallbackInfo2 {
    operator const WGPUDeviceLostCallbackInfo2&() const noexcept;
    CallbackMode mode;
    DeviceLostCallback2 callback = nullptr;
};

struct UncapturedErrorCallbackInfo {
    operator const WGPUUncapturedErrorCallbackInfo&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    ErrorCallback callback = nullptr;
    void * userdata = nullptr;
};

struct DeviceLostCallbackInfo {
    operator const WGPUDeviceLostCallbackInfo&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    CallbackMode mode = CallbackMode::WaitAnyOnly;
    DeviceLostCallbackNew callback = nullptr;
    void * userdata = nullptr;
};

struct QueueDescriptor {
    operator const WGPUQueueDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * label = nullptr;
};

struct RequiredLimits {
    operator const WGPURequiredLimits&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    Limits limits = {};
};

class Surface : public ObjectBase<Surface, WGPUSurface> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    void Configure(SurfaceConfiguration const* config) const;    
    Status GetCapabilities(Adapter adapter, SurfaceCapabilities * capabilities) const;    
    void GetCurrentTexture(SurfaceTexture * surfaceTexture) const;    
    TextureFormat GetPreferredFormat(Adapter adapter) const;    
    void Present() const;    
    void Unconfigure() const;    
    void SetLabel(char const* label) const;    
    void SetLabel2(NullableStringView label) const;    
    
    friend ObjectBase<Surface, WGPUSurface>;
    static void WGPUAddRef(WGPUSurface handle);
    static void WGPURelease(WGPUSurface handle);
};

// Can be chained in BufferDescriptor
struct DawnBufferDescriptorErrorInfoFromWireClient : ChainedStruct {
    DawnBufferDescriptorErrorInfoFromWireClient();

    struct Init;
    DawnBufferDescriptorErrorInfoFromWireClient(Init&& init);
    operator const WGPUDawnBufferDescriptorErrorInfoFromWireClient&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(Bool ));
    alignas(kFirstMemberAlignment) Bool outOfMemory = false;
};

// Can be chained in AdapterInfo
// Can be chained in AdapterProperties
struct AdapterPropertiesVk : ChainedStructOut {
    AdapterPropertiesVk();

    struct Init;
    AdapterPropertiesVk(Init&& init);
    ~AdapterPropertiesVk();
    AdapterPropertiesVk(const AdapterPropertiesVk&) = delete;
    void FreeMembers();
    AdapterPropertiesVk& operator=(const AdapterPropertiesVk&) = delete;
    AdapterPropertiesVk(AdapterPropertiesVk&&);
    AdapterPropertiesVk& operator=(AdapterPropertiesVk&&);
    
    operator const WGPUAdapterPropertiesVk&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStructOut), alignof(uint32_t ));
    alignas(kFirstMemberAlignment) uint32_t const driverVersion = {};
};

// Can be chained in AdapterInfo
// Can be chained in AdapterProperties
struct AdapterPropertiesD3D : ChainedStructOut {
    AdapterPropertiesD3D();

    struct Init;
    AdapterPropertiesD3D(Init&& init);
    ~AdapterPropertiesD3D();
    AdapterPropertiesD3D(const AdapterPropertiesD3D&) = delete;
    void FreeMembers();
    AdapterPropertiesD3D& operator=(const AdapterPropertiesD3D&) = delete;
    AdapterPropertiesD3D(AdapterPropertiesD3D&&);
    AdapterPropertiesD3D& operator=(AdapterPropertiesD3D&&);
    
    operator const WGPUAdapterPropertiesD3D&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStructOut), alignof(uint32_t ));
    alignas(kFirstMemberAlignment) uint32_t const shaderModel = {};
};

// Can be chained in AdapterInfo
// Can be chained in AdapterProperties
struct AdapterPropertiesMemoryHeaps : ChainedStructOut {
    AdapterPropertiesMemoryHeaps();

    struct Init;
    AdapterPropertiesMemoryHeaps(Init&& init);
    ~AdapterPropertiesMemoryHeaps();
    AdapterPropertiesMemoryHeaps(const AdapterPropertiesMemoryHeaps&) = delete;
    void FreeMembers();
    AdapterPropertiesMemoryHeaps& operator=(const AdapterPropertiesMemoryHeaps&) = delete;
    AdapterPropertiesMemoryHeaps(AdapterPropertiesMemoryHeaps&&);
    AdapterPropertiesMemoryHeaps& operator=(AdapterPropertiesMemoryHeaps&&);
    
    operator const WGPUAdapterPropertiesMemoryHeaps&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStructOut), alignof(size_t ));
    alignas(kFirstMemberAlignment) size_t const heapCount = {};
    MemoryHeapInfo const * const heapInfo = {};
};

// Can be chained in AdapterInfo
// Can be chained in AdapterProperties
struct DawnAdapterPropertiesPowerPreference : ChainedStructOut {
    DawnAdapterPropertiesPowerPreference();

    struct Init;
    DawnAdapterPropertiesPowerPreference(Init&& init);
    ~DawnAdapterPropertiesPowerPreference();
    DawnAdapterPropertiesPowerPreference(const DawnAdapterPropertiesPowerPreference&) = delete;
    void FreeMembers();
    DawnAdapterPropertiesPowerPreference& operator=(const DawnAdapterPropertiesPowerPreference&) = delete;
    DawnAdapterPropertiesPowerPreference(DawnAdapterPropertiesPowerPreference&&);
    DawnAdapterPropertiesPowerPreference& operator=(DawnAdapterPropertiesPowerPreference&&);
    
    operator const WGPUDawnAdapterPropertiesPowerPreference&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStructOut), alignof(PowerPreference ));
    alignas(kFirstMemberAlignment) PowerPreference const powerPreference = PowerPreference::Undefined;
};

// Can be chained in CommandEncoderDescriptor
struct DawnEncoderInternalUsageDescriptor : ChainedStruct {
    DawnEncoderInternalUsageDescriptor();

    struct Init;
    DawnEncoderInternalUsageDescriptor(Init&& init);
    operator const WGPUDawnEncoderInternalUsageDescriptor&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(Bool ));
    alignas(kFirstMemberAlignment) Bool useInternalUsages = false;
};

// Can be chained in TextureDescriptor
struct DawnTextureInternalUsageDescriptor : ChainedStruct {
    DawnTextureInternalUsageDescriptor();

    struct Init;
    DawnTextureInternalUsageDescriptor(Init&& init);
    operator const WGPUDawnTextureInternalUsageDescriptor&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(TextureUsage ));
    alignas(kFirstMemberAlignment) TextureUsage internalUsage = TextureUsage::None;
};

struct TextureViewDescriptor {
    operator const WGPUTextureViewDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * label = nullptr;
    TextureFormat format = TextureFormat::Undefined;
    TextureViewDimension dimension = TextureViewDimension::Undefined;
    uint32_t baseMipLevel = 0;
    uint32_t mipLevelCount = WGPU_MIP_LEVEL_COUNT_UNDEFINED;
    uint32_t baseArrayLayer = 0;
    uint32_t arrayLayerCount = WGPU_ARRAY_LAYER_COUNT_UNDEFINED;
    TextureAspect aspect = TextureAspect::All;
};

// Can be chained in TextureDescriptor
struct TextureBindingViewDimensionDescriptor : ChainedStruct {
    TextureBindingViewDimensionDescriptor();

    struct Init;
    TextureBindingViewDimensionDescriptor(Init&& init);
    operator const WGPUTextureBindingViewDimensionDescriptor&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(TextureViewDimension ));
    alignas(kFirstMemberAlignment) TextureViewDimension textureBindingViewDimension = TextureViewDimension::Undefined;
};

struct TextureDescriptor {
    operator const WGPUTextureDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * label = nullptr;
    TextureUsage usage;
    TextureDimension dimension = TextureDimension::e2D;
    Extent3D size = {};
    TextureFormat format;
    uint32_t mipLevelCount = 1;
    uint32_t sampleCount = 1;
    size_t viewFormatCount = 0;
    TextureFormat const * viewFormats;
};

struct SurfaceTexture {
    operator const WGPUSurfaceTexture&() const noexcept;
    Texture texture;
    Bool suboptimal;
    SurfaceGetCurrentTextureStatus status;
};

struct SwapChainDescriptor {
    operator const WGPUSwapChainDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * label = nullptr;
    TextureUsage usage;
    TextureFormat format;
    uint32_t width;
    uint32_t height;
    PresentMode presentMode;
};

// Can be chained in SurfaceDescriptor
struct SurfaceDescriptorFromWindowsSwapChainPanel : ChainedStruct {
    SurfaceDescriptorFromWindowsSwapChainPanel();

    struct Init;
    SurfaceDescriptorFromWindowsSwapChainPanel(Init&& init);
    operator const WGPUSurfaceDescriptorFromWindowsSwapChainPanel&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(void * ));
    alignas(kFirstMemberAlignment) void * swapChainPanel;
};

// Can be chained in SurfaceDescriptor
struct SurfaceDescriptorFromWindowsCoreWindow : ChainedStruct {
    SurfaceDescriptorFromWindowsCoreWindow();

    struct Init;
    SurfaceDescriptorFromWindowsCoreWindow(Init&& init);
    operator const WGPUSurfaceDescriptorFromWindowsCoreWindow&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(void * ));
    alignas(kFirstMemberAlignment) void * coreWindow;
};

// Can be chained in SurfaceDescriptor
struct SurfaceDescriptorFromWaylandSurface : ChainedStruct {
    SurfaceDescriptorFromWaylandSurface();

    struct Init;
    SurfaceDescriptorFromWaylandSurface(Init&& init);
    operator const WGPUSurfaceDescriptorFromWaylandSurface&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(void * ));
    alignas(kFirstMemberAlignment) void * display;
    void * surface;
};

// Can be chained in SurfaceDescriptor
struct SurfaceDescriptorFromXlibWindow : ChainedStruct {
    SurfaceDescriptorFromXlibWindow();

    struct Init;
    SurfaceDescriptorFromXlibWindow(Init&& init);
    operator const WGPUSurfaceDescriptorFromXlibWindow&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(void * ));
    alignas(kFirstMemberAlignment) void * display;
    uint64_t window;
};

// Can be chained in SurfaceDescriptor
struct SurfaceDescriptorFromXcbWindow : ChainedStruct {
    SurfaceDescriptorFromXcbWindow();

    struct Init;
    SurfaceDescriptorFromXcbWindow(Init&& init);
    operator const WGPUSurfaceDescriptorFromXcbWindow&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(void * ));
    alignas(kFirstMemberAlignment) void * connection;
    uint32_t window;
};

// Can be chained in SurfaceDescriptor
struct SurfaceDescriptorFromWindowsHWND : ChainedStruct {
    SurfaceDescriptorFromWindowsHWND();

    struct Init;
    SurfaceDescriptorFromWindowsHWND(Init&& init);
    operator const WGPUSurfaceDescriptorFromWindowsHWND&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(void * ));
    alignas(kFirstMemberAlignment) void * hinstance;
    void * hwnd;
};

// Can be chained in SurfaceDescriptor
struct SurfaceDescriptorFromMetalLayer : ChainedStruct {
    SurfaceDescriptorFromMetalLayer();

    struct Init;
    SurfaceDescriptorFromMetalLayer(Init&& init);
    operator const WGPUSurfaceDescriptorFromMetalLayer&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(void * ));
    alignas(kFirstMemberAlignment) void * layer;
};

// Can be chained in SurfaceDescriptor
struct SurfaceDescriptorFromCanvasHTMLSelector : ChainedStruct {
    SurfaceDescriptorFromCanvasHTMLSelector();

    struct Init;
    SurfaceDescriptorFromCanvasHTMLSelector(Init&& init);
    operator const WGPUSurfaceDescriptorFromCanvasHTMLSelector&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(char const * ));
    alignas(kFirstMemberAlignment) char const * selector;
};

// Can be chained in SurfaceDescriptor
struct SurfaceDescriptorFromAndroidNativeWindow : ChainedStruct {
    SurfaceDescriptorFromAndroidNativeWindow();

    struct Init;
    SurfaceDescriptorFromAndroidNativeWindow(Init&& init);
    operator const WGPUSurfaceDescriptorFromAndroidNativeWindow&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(void * ));
    alignas(kFirstMemberAlignment) void * window;
};

struct SurfaceDescriptor {
    operator const WGPUSurfaceDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * label = nullptr;
};

// Can be chained in ShaderModuleDescriptor
struct ShaderModuleCompilationOptions : ChainedStruct {
    ShaderModuleCompilationOptions();

    struct Init;
    ShaderModuleCompilationOptions(Init&& init);
    operator const WGPUShaderModuleCompilationOptions&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(Bool ));
    alignas(kFirstMemberAlignment) Bool strictMath;
};

// Can be chained in ShaderModuleDescriptor
struct DawnShaderModuleSPIRVOptionsDescriptor : ChainedStruct {
    DawnShaderModuleSPIRVOptionsDescriptor();

    struct Init;
    DawnShaderModuleSPIRVOptionsDescriptor(Init&& init);
    operator const WGPUDawnShaderModuleSPIRVOptionsDescriptor&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(Bool ));
    alignas(kFirstMemberAlignment) Bool allowNonUniformDerivatives = false;
};

// Can be chained in ShaderModuleDescriptor
struct ShaderModuleWGSLDescriptor : ChainedStruct {
    ShaderModuleWGSLDescriptor();

    struct Init;
    ShaderModuleWGSLDescriptor(Init&& init);
    operator const WGPUShaderModuleWGSLDescriptor&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(char const * ));
    alignas(kFirstMemberAlignment) char const * code;
};

// Can be chained in ShaderModuleDescriptor
struct ShaderModuleSPIRVDescriptor : ChainedStruct {
    ShaderModuleSPIRVDescriptor();

    struct Init;
    ShaderModuleSPIRVDescriptor(Init&& init);
    operator const WGPUShaderModuleSPIRVDescriptor&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(uint32_t ));
    alignas(kFirstMemberAlignment) uint32_t codeSize;
    uint32_t const * code;
};

struct ShaderModuleDescriptor {
    operator const WGPUShaderModuleDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * label = nullptr;
};

struct SamplerDescriptor {
    operator const WGPUSamplerDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * label = nullptr;
    AddressMode addressModeU = AddressMode::ClampToEdge;
    AddressMode addressModeV = AddressMode::ClampToEdge;
    AddressMode addressModeW = AddressMode::ClampToEdge;
    FilterMode magFilter = FilterMode::Nearest;
    FilterMode minFilter = FilterMode::Nearest;
    MipmapFilterMode mipmapFilter = MipmapFilterMode::Nearest;
    float lodMinClamp = 0.0f;
    float lodMaxClamp = 32.0f;
    CompareFunction compare = CompareFunction::Undefined;
    uint16_t maxAnisotropy = 1;
};

struct RenderPipelineDescriptor {
    operator const WGPURenderPipelineDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * label = nullptr;
    PipelineLayout layout = nullptr;
    VertexState vertex = {};
    PrimitiveState primitive = {};
    DepthStencilState const * depthStencil = nullptr;
    MultisampleState multisample = {};
    FragmentState const * fragment = nullptr;
};

// Can be chained in ColorTargetState
struct ColorTargetStateExpandResolveTextureDawn : ChainedStruct {
    ColorTargetStateExpandResolveTextureDawn();

    struct Init;
    ColorTargetStateExpandResolveTextureDawn(Init&& init);
    operator const WGPUColorTargetStateExpandResolveTextureDawn&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(Bool ));
    alignas(kFirstMemberAlignment) Bool enabled = false;
};

// Can be chained in DepthStencilState
struct DepthStencilStateDepthWriteDefinedDawn : ChainedStruct {
    DepthStencilStateDepthWriteDefinedDawn();

    struct Init;
    DepthStencilStateDepthWriteDefinedDawn(Init&& init);
    operator const WGPUDepthStencilStateDepthWriteDefinedDawn&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(Bool ));
    alignas(kFirstMemberAlignment) Bool depthWriteDefined;
};

// Can be chained in PrimitiveState
struct PrimitiveDepthClipControl : ChainedStruct {
    PrimitiveDepthClipControl();

    struct Init;
    PrimitiveDepthClipControl(Init&& init);
    operator const WGPUPrimitiveDepthClipControl&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(Bool ));
    alignas(kFirstMemberAlignment) Bool unclippedDepth = false;
};

struct RequestDeviceCallbackInfo2 {
    operator const WGPURequestDeviceCallbackInfo2&() const noexcept;
    CallbackMode mode;
    RequestDeviceCallback2 callback;
};

struct RequestDeviceCallbackInfo {
    operator const WGPURequestDeviceCallbackInfo&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    CallbackMode mode;
    RequestDeviceCallback callback;
    void * userdata;
};

// Can be chained in RenderPassDescriptor
struct RenderPassPixelLocalStorage : ChainedStruct {
    RenderPassPixelLocalStorage();

    struct Init;
    RenderPassPixelLocalStorage(Init&& init);
    operator const WGPURenderPassPixelLocalStorage&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(uint64_t ));
    alignas(kFirstMemberAlignment) uint64_t totalPixelLocalStorageSize;
    size_t storageAttachmentCount = 0;
    RenderPassStorageAttachment const * storageAttachments;
};

// Can be chained in RenderPassDescriptor
struct RenderPassDescriptorMaxDrawCount : ChainedStruct {
    RenderPassDescriptorMaxDrawCount();

    struct Init;
    RenderPassDescriptorMaxDrawCount(Init&& init);
    operator const WGPURenderPassDescriptorMaxDrawCount&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(uint64_t ));
    alignas(kFirstMemberAlignment) uint64_t maxDrawCount = 50000000;
};

struct RenderPassDescriptor {
    operator const WGPURenderPassDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * label = nullptr;
    size_t colorAttachmentCount;
    RenderPassColorAttachment const * colorAttachments;
    RenderPassDepthStencilAttachment const * depthStencilAttachment = nullptr;
    QuerySet occlusionQuerySet = nullptr;
    RenderPassTimestampWrites const * timestampWrites = nullptr;
};

// Can be chained in RenderPassColorAttachment
struct DawnRenderPassColorAttachmentRenderToSingleSampled : ChainedStruct {
    DawnRenderPassColorAttachmentRenderToSingleSampled();

    struct Init;
    DawnRenderPassColorAttachmentRenderToSingleSampled(Init&& init);
    operator const WGPUDawnRenderPassColorAttachmentRenderToSingleSampled&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(uint32_t ));
    alignas(kFirstMemberAlignment) uint32_t implicitSampleCount = 1;
};

struct RenderBundleEncoderDescriptor {
    operator const WGPURenderBundleEncoderDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * label = nullptr;
    size_t colorFormatCount;
    TextureFormat const * colorFormats;
    TextureFormat depthStencilFormat = TextureFormat::Undefined;
    uint32_t sampleCount = 1;
    Bool depthReadOnly = false;
    Bool stencilReadOnly = false;
};

struct RenderBundleDescriptor {
    operator const WGPURenderBundleDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * label = nullptr;
};

struct QueueWorkDoneCallbackInfo2 {
    operator const WGPUQueueWorkDoneCallbackInfo2&() const noexcept;
    CallbackMode mode;
    QueueWorkDoneCallback2 callback;
};

struct QueueWorkDoneCallbackInfo {
    operator const WGPUQueueWorkDoneCallbackInfo&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    CallbackMode mode;
    QueueWorkDoneCallback callback;
    void * userdata;
};

struct QuerySetDescriptor {
    operator const WGPUQuerySetDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * label = nullptr;
    QueryType type;
    uint32_t count;
};

// Can be chained in PipelineLayoutDescriptor
struct PipelineLayoutPixelLocalStorage : ChainedStruct {
    PipelineLayoutPixelLocalStorage();

    struct Init;
    PipelineLayoutPixelLocalStorage(Init&& init);
    operator const WGPUPipelineLayoutPixelLocalStorage&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(uint64_t ));
    alignas(kFirstMemberAlignment) uint64_t totalPixelLocalStorageSize;
    size_t storageAttachmentCount = 0;
    PipelineLayoutStorageAttachment const * storageAttachments;
};

struct PipelineLayoutDescriptor {
    operator const WGPUPipelineLayoutDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * label = nullptr;
    size_t bindGroupLayoutCount;
    BindGroupLayout const * bindGroupLayouts;
};

// Can be chained in InstanceDescriptor
struct DawnWireWGSLControl : ChainedStruct {
    DawnWireWGSLControl();

    struct Init;
    DawnWireWGSLControl(Init&& init);
    operator const WGPUDawnWireWGSLControl&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(Bool ));
    alignas(kFirstMemberAlignment) Bool enableExperimental = false;
    Bool enableUnsafe = false;
    Bool enableTesting = false;
};

struct InstanceDescriptor {
    operator const WGPUInstanceDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    InstanceFeatures features = {};
};

struct FutureWaitInfo {
    operator const WGPUFutureWaitInfo&() const noexcept;
    Future future = {};
    Bool completed = false;
};

struct ImageCopyExternalTexture {
    operator const WGPUImageCopyExternalTexture&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    ExternalTexture externalTexture;
    Origin3D origin = {};
    Extent2D naturalSize = {};
};

struct ImageCopyTexture {
    operator const WGPUImageCopyTexture&() const noexcept;
    Texture texture;
    uint32_t mipLevel = 0;
    Origin3D origin = {};
    TextureAspect aspect = TextureAspect::All;
};

struct ImageCopyBuffer {
    operator const WGPUImageCopyBuffer&() const noexcept;
    TextureDataLayout layout = {};
    Buffer buffer;
};

// Can be chained in FormatCapabilities
struct DrmFormatCapabilities : ChainedStructOut {
    DrmFormatCapabilities();

    struct Init;
    DrmFormatCapabilities(Init&& init);
    ~DrmFormatCapabilities();
    DrmFormatCapabilities(const DrmFormatCapabilities&) = delete;
    void FreeMembers();
    DrmFormatCapabilities& operator=(const DrmFormatCapabilities&) = delete;
    DrmFormatCapabilities(DrmFormatCapabilities&&);
    DrmFormatCapabilities& operator=(DrmFormatCapabilities&&);
    
    operator const WGPUDrmFormatCapabilities&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStructOut), alignof(size_t ));
    alignas(kFirstMemberAlignment) size_t const propertiesCount = {};
    DrmFormatProperties const * const properties = {};
};

struct FormatCapabilities {
FormatCapabilities() = default;
    ~FormatCapabilities();
    FormatCapabilities(const FormatCapabilities&) = delete;
    void FreeMembers();
    FormatCapabilities& operator=(const FormatCapabilities&) = delete;
    FormatCapabilities(FormatCapabilities&&);
    FormatCapabilities& operator=(FormatCapabilities&&);
    
    operator const WGPUFormatCapabilities&() const noexcept;
    ChainedStructOut * const nextInChain = nullptr;
};

// Can be chained in SharedFenceExportInfo
struct SharedFenceMTLSharedEventExportInfo : ChainedStructOut {
    SharedFenceMTLSharedEventExportInfo();

    struct Init;
    SharedFenceMTLSharedEventExportInfo(Init&& init);
    ~SharedFenceMTLSharedEventExportInfo();
    SharedFenceMTLSharedEventExportInfo(const SharedFenceMTLSharedEventExportInfo&) = delete;
    void FreeMembers();
    SharedFenceMTLSharedEventExportInfo& operator=(const SharedFenceMTLSharedEventExportInfo&) = delete;
    SharedFenceMTLSharedEventExportInfo(SharedFenceMTLSharedEventExportInfo&&);
    SharedFenceMTLSharedEventExportInfo& operator=(SharedFenceMTLSharedEventExportInfo&&);
    
    operator const WGPUSharedFenceMTLSharedEventExportInfo&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStructOut), alignof(void * ));
    alignas(kFirstMemberAlignment) void * const sharedEvent = {};
};

// Can be chained in SharedFenceExportInfo
struct SharedFenceDXGISharedHandleExportInfo : ChainedStructOut {
    SharedFenceDXGISharedHandleExportInfo();

    struct Init;
    SharedFenceDXGISharedHandleExportInfo(Init&& init);
    ~SharedFenceDXGISharedHandleExportInfo();
    SharedFenceDXGISharedHandleExportInfo(const SharedFenceDXGISharedHandleExportInfo&) = delete;
    void FreeMembers();
    SharedFenceDXGISharedHandleExportInfo& operator=(const SharedFenceDXGISharedHandleExportInfo&) = delete;
    SharedFenceDXGISharedHandleExportInfo(SharedFenceDXGISharedHandleExportInfo&&);
    SharedFenceDXGISharedHandleExportInfo& operator=(SharedFenceDXGISharedHandleExportInfo&&);
    
    operator const WGPUSharedFenceDXGISharedHandleExportInfo&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStructOut), alignof(void * ));
    alignas(kFirstMemberAlignment) void * const handle = {};
};

// Can be chained in SharedFenceExportInfo
struct SharedFenceVkSemaphoreZirconHandleExportInfo : ChainedStructOut {
    SharedFenceVkSemaphoreZirconHandleExportInfo();

    struct Init;
    SharedFenceVkSemaphoreZirconHandleExportInfo(Init&& init);
    ~SharedFenceVkSemaphoreZirconHandleExportInfo();
    SharedFenceVkSemaphoreZirconHandleExportInfo(const SharedFenceVkSemaphoreZirconHandleExportInfo&) = delete;
    void FreeMembers();
    SharedFenceVkSemaphoreZirconHandleExportInfo& operator=(const SharedFenceVkSemaphoreZirconHandleExportInfo&) = delete;
    SharedFenceVkSemaphoreZirconHandleExportInfo(SharedFenceVkSemaphoreZirconHandleExportInfo&&);
    SharedFenceVkSemaphoreZirconHandleExportInfo& operator=(SharedFenceVkSemaphoreZirconHandleExportInfo&&);
    
    operator const WGPUSharedFenceVkSemaphoreZirconHandleExportInfo&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStructOut), alignof(uint32_t ));
    alignas(kFirstMemberAlignment) uint32_t const handle = {};
};

// Can be chained in SharedFenceExportInfo
struct SharedFenceVkSemaphoreSyncFDExportInfo : ChainedStructOut {
    SharedFenceVkSemaphoreSyncFDExportInfo();

    struct Init;
    SharedFenceVkSemaphoreSyncFDExportInfo(Init&& init);
    ~SharedFenceVkSemaphoreSyncFDExportInfo();
    SharedFenceVkSemaphoreSyncFDExportInfo(const SharedFenceVkSemaphoreSyncFDExportInfo&) = delete;
    void FreeMembers();
    SharedFenceVkSemaphoreSyncFDExportInfo& operator=(const SharedFenceVkSemaphoreSyncFDExportInfo&) = delete;
    SharedFenceVkSemaphoreSyncFDExportInfo(SharedFenceVkSemaphoreSyncFDExportInfo&&);
    SharedFenceVkSemaphoreSyncFDExportInfo& operator=(SharedFenceVkSemaphoreSyncFDExportInfo&&);
    
    operator const WGPUSharedFenceVkSemaphoreSyncFDExportInfo&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStructOut), alignof(int ));
    alignas(kFirstMemberAlignment) int const handle = {};
};

// Can be chained in SharedFenceExportInfo
struct SharedFenceVkSemaphoreOpaqueFDExportInfo : ChainedStructOut {
    SharedFenceVkSemaphoreOpaqueFDExportInfo();

    struct Init;
    SharedFenceVkSemaphoreOpaqueFDExportInfo(Init&& init);
    ~SharedFenceVkSemaphoreOpaqueFDExportInfo();
    SharedFenceVkSemaphoreOpaqueFDExportInfo(const SharedFenceVkSemaphoreOpaqueFDExportInfo&) = delete;
    void FreeMembers();
    SharedFenceVkSemaphoreOpaqueFDExportInfo& operator=(const SharedFenceVkSemaphoreOpaqueFDExportInfo&) = delete;
    SharedFenceVkSemaphoreOpaqueFDExportInfo(SharedFenceVkSemaphoreOpaqueFDExportInfo&&);
    SharedFenceVkSemaphoreOpaqueFDExportInfo& operator=(SharedFenceVkSemaphoreOpaqueFDExportInfo&&);
    
    operator const WGPUSharedFenceVkSemaphoreOpaqueFDExportInfo&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStructOut), alignof(int ));
    alignas(kFirstMemberAlignment) int const handle = {};
};

struct SharedFenceExportInfo {
SharedFenceExportInfo() = default;
    ~SharedFenceExportInfo();
    SharedFenceExportInfo(const SharedFenceExportInfo&) = delete;
    void FreeMembers();
    SharedFenceExportInfo& operator=(const SharedFenceExportInfo&) = delete;
    SharedFenceExportInfo(SharedFenceExportInfo&&);
    SharedFenceExportInfo& operator=(SharedFenceExportInfo&&);
    
    operator const WGPUSharedFenceExportInfo&() const noexcept;
    ChainedStructOut * const nextInChain = nullptr;
    SharedFenceType const type = {};
};

// Can be chained in SharedFenceDescriptor
struct SharedFenceMTLSharedEventDescriptor : ChainedStruct {
    SharedFenceMTLSharedEventDescriptor();

    struct Init;
    SharedFenceMTLSharedEventDescriptor(Init&& init);
    operator const WGPUSharedFenceMTLSharedEventDescriptor&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(void * ));
    alignas(kFirstMemberAlignment) void * sharedEvent;
};

// Can be chained in SharedFenceDescriptor
struct SharedFenceDXGISharedHandleDescriptor : ChainedStruct {
    SharedFenceDXGISharedHandleDescriptor();

    struct Init;
    SharedFenceDXGISharedHandleDescriptor(Init&& init);
    operator const WGPUSharedFenceDXGISharedHandleDescriptor&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(void * ));
    alignas(kFirstMemberAlignment) void * handle;
};

// Can be chained in SharedFenceDescriptor
struct SharedFenceVkSemaphoreZirconHandleDescriptor : ChainedStruct {
    SharedFenceVkSemaphoreZirconHandleDescriptor();

    struct Init;
    SharedFenceVkSemaphoreZirconHandleDescriptor(Init&& init);
    operator const WGPUSharedFenceVkSemaphoreZirconHandleDescriptor&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(uint32_t ));
    alignas(kFirstMemberAlignment) uint32_t handle;
};

// Can be chained in SharedFenceDescriptor
struct SharedFenceVkSemaphoreSyncFDDescriptor : ChainedStruct {
    SharedFenceVkSemaphoreSyncFDDescriptor();

    struct Init;
    SharedFenceVkSemaphoreSyncFDDescriptor(Init&& init);
    operator const WGPUSharedFenceVkSemaphoreSyncFDDescriptor&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(int ));
    alignas(kFirstMemberAlignment) int handle;
};

// Can be chained in SharedFenceDescriptor
struct SharedFenceVkSemaphoreOpaqueFDDescriptor : ChainedStruct {
    SharedFenceVkSemaphoreOpaqueFDDescriptor();

    struct Init;
    SharedFenceVkSemaphoreOpaqueFDDescriptor(Init&& init);
    operator const WGPUSharedFenceVkSemaphoreOpaqueFDDescriptor&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(int ));
    alignas(kFirstMemberAlignment) int handle;
};

struct SharedFenceDescriptor {
    operator const WGPUSharedFenceDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * label = nullptr;
};

// Can be chained in SharedTextureMemoryBeginAccessDescriptor
struct SharedTextureMemoryD3DSwapchainBeginState : ChainedStruct {
    SharedTextureMemoryD3DSwapchainBeginState();

    struct Init;
    SharedTextureMemoryD3DSwapchainBeginState(Init&& init);
    operator const WGPUSharedTextureMemoryD3DSwapchainBeginState&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(Bool ));
    alignas(kFirstMemberAlignment) Bool isSwapchain = false;
};

// Can be chained in SharedTextureMemoryEndAccessState
struct SharedTextureMemoryVkImageLayoutEndState : ChainedStructOut {
    SharedTextureMemoryVkImageLayoutEndState();

    struct Init;
    SharedTextureMemoryVkImageLayoutEndState(Init&& init);
    ~SharedTextureMemoryVkImageLayoutEndState();
    SharedTextureMemoryVkImageLayoutEndState(const SharedTextureMemoryVkImageLayoutEndState&) = delete;
    void FreeMembers();
    SharedTextureMemoryVkImageLayoutEndState& operator=(const SharedTextureMemoryVkImageLayoutEndState&) = delete;
    SharedTextureMemoryVkImageLayoutEndState(SharedTextureMemoryVkImageLayoutEndState&&);
    SharedTextureMemoryVkImageLayoutEndState& operator=(SharedTextureMemoryVkImageLayoutEndState&&);
    
    operator const WGPUSharedTextureMemoryVkImageLayoutEndState&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStructOut), alignof(int32_t ));
    alignas(kFirstMemberAlignment) int32_t const oldLayout = {};
    int32_t const newLayout = {};
};

// Can be chained in SharedTextureMemoryBeginAccessDescriptor
struct SharedTextureMemoryVkImageLayoutBeginState : ChainedStruct {
    SharedTextureMemoryVkImageLayoutBeginState();

    struct Init;
    SharedTextureMemoryVkImageLayoutBeginState(Init&& init);
    operator const WGPUSharedTextureMemoryVkImageLayoutBeginState&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(int32_t ));
    alignas(kFirstMemberAlignment) int32_t oldLayout;
    int32_t newLayout;
};

struct SharedTextureMemoryEndAccessState {
SharedTextureMemoryEndAccessState() = default;
    ~SharedTextureMemoryEndAccessState();
    SharedTextureMemoryEndAccessState(const SharedTextureMemoryEndAccessState&) = delete;
    void FreeMembers();
    SharedTextureMemoryEndAccessState& operator=(const SharedTextureMemoryEndAccessState&) = delete;
    SharedTextureMemoryEndAccessState(SharedTextureMemoryEndAccessState&&);
    SharedTextureMemoryEndAccessState& operator=(SharedTextureMemoryEndAccessState&&);
    
    operator const WGPUSharedTextureMemoryEndAccessState&() const noexcept;
    ChainedStructOut * const nextInChain = nullptr;
    Bool const initialized = {};
    size_t const fenceCount = {};
    SharedFence const * const fences = {};
    uint64_t const * const signaledValues = {};
};

struct SharedTextureMemoryBeginAccessDescriptor {
    operator const WGPUSharedTextureMemoryBeginAccessDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    Bool concurrentRead;
    Bool initialized;
    size_t fenceCount;
    SharedFence const * fences;
    uint64_t const * signaledValues;
};

// Can be chained in SharedTextureMemoryDescriptor
struct SharedTextureMemoryEGLImageDescriptor : ChainedStruct {
    SharedTextureMemoryEGLImageDescriptor();

    struct Init;
    SharedTextureMemoryEGLImageDescriptor(Init&& init);
    operator const WGPUSharedTextureMemoryEGLImageDescriptor&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(void * ));
    alignas(kFirstMemberAlignment) void * image;
};

// Can be chained in SharedTextureMemoryDescriptor
struct SharedTextureMemoryIOSurfaceDescriptor : ChainedStruct {
    SharedTextureMemoryIOSurfaceDescriptor();

    struct Init;
    SharedTextureMemoryIOSurfaceDescriptor(Init&& init);
    operator const WGPUSharedTextureMemoryIOSurfaceDescriptor&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(void * ));
    alignas(kFirstMemberAlignment) void * ioSurface;
};

// Can be chained in SharedTextureMemoryDescriptor
struct SharedTextureMemoryDXGISharedHandleDescriptor : ChainedStruct {
    SharedTextureMemoryDXGISharedHandleDescriptor();

    struct Init;
    SharedTextureMemoryDXGISharedHandleDescriptor(Init&& init);
    operator const WGPUSharedTextureMemoryDXGISharedHandleDescriptor&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(void * ));
    alignas(kFirstMemberAlignment) void * handle;
    Bool useKeyedMutex;
};

// Can be chained in SharedTextureMemoryDescriptor
struct SharedTextureMemoryZirconHandleDescriptor : ChainedStruct {
    SharedTextureMemoryZirconHandleDescriptor();

    struct Init;
    SharedTextureMemoryZirconHandleDescriptor(Init&& init);
    operator const WGPUSharedTextureMemoryZirconHandleDescriptor&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(uint32_t ));
    alignas(kFirstMemberAlignment) uint32_t memoryFD;
    uint64_t allocationSize;
};

// Can be chained in SharedTextureMemoryDescriptor
struct SharedTextureMemoryOpaqueFDDescriptor : ChainedStruct {
    SharedTextureMemoryOpaqueFDDescriptor();

    struct Init;
    SharedTextureMemoryOpaqueFDDescriptor(Init&& init);
    operator const WGPUSharedTextureMemoryOpaqueFDDescriptor&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(void const * ));
    alignas(kFirstMemberAlignment) void const * vkImageCreateInfo;
    int memoryFD;
    uint32_t memoryTypeIndex;
    uint64_t allocationSize;
    Bool dedicatedAllocation;
};

// Can be chained in SharedTextureMemoryDescriptor
struct SharedTextureMemoryDmaBufDescriptor : ChainedStruct {
    SharedTextureMemoryDmaBufDescriptor();

    struct Init;
    SharedTextureMemoryDmaBufDescriptor(Init&& init);
    operator const WGPUSharedTextureMemoryDmaBufDescriptor&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(Extent3D ));
    alignas(kFirstMemberAlignment) Extent3D size = {};
    uint32_t drmFormat;
    uint64_t drmModifier;
    size_t planeCount;
    SharedTextureMemoryDmaBufPlane const * planes;
};

// Can be chained in SharedTextureMemoryDescriptor
struct SharedTextureMemoryAHardwareBufferDescriptor : ChainedStruct {
    SharedTextureMemoryAHardwareBufferDescriptor();

    struct Init;
    SharedTextureMemoryAHardwareBufferDescriptor(Init&& init);
    operator const WGPUSharedTextureMemoryAHardwareBufferDescriptor&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(void * ));
    alignas(kFirstMemberAlignment) void * handle;
    Bool useExternalFormat;
};

// Can be chained in SharedTextureMemoryDescriptor
struct SharedTextureMemoryVkDedicatedAllocationDescriptor : ChainedStruct {
    SharedTextureMemoryVkDedicatedAllocationDescriptor();

    struct Init;
    SharedTextureMemoryVkDedicatedAllocationDescriptor(Init&& init);
    operator const WGPUSharedTextureMemoryVkDedicatedAllocationDescriptor&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(Bool ));
    alignas(kFirstMemberAlignment) Bool dedicatedAllocation;
};

struct SharedBufferMemoryEndAccessState {
SharedBufferMemoryEndAccessState() = default;
    ~SharedBufferMemoryEndAccessState();
    SharedBufferMemoryEndAccessState(const SharedBufferMemoryEndAccessState&) = delete;
    void FreeMembers();
    SharedBufferMemoryEndAccessState& operator=(const SharedBufferMemoryEndAccessState&) = delete;
    SharedBufferMemoryEndAccessState(SharedBufferMemoryEndAccessState&&);
    SharedBufferMemoryEndAccessState& operator=(SharedBufferMemoryEndAccessState&&);
    
    operator const WGPUSharedBufferMemoryEndAccessState&() const noexcept;
    ChainedStructOut * const nextInChain = nullptr;
    Bool const initialized = {};
    size_t const fenceCount = 0;
    SharedFence const * const fences = {};
    uint64_t const * const signaledValues = {};
};

struct SharedBufferMemoryBeginAccessDescriptor {
    operator const WGPUSharedBufferMemoryBeginAccessDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    Bool initialized;
    size_t fenceCount = 0;
    SharedFence const * fences;
    uint64_t const * signaledValues;
};

struct SharedTextureMemoryDescriptor {
    operator const WGPUSharedTextureMemoryDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * label = nullptr;
};

// Can be chained in SharedTextureMemoryProperties
struct SharedTextureMemoryAHardwareBufferProperties : ChainedStructOut {
    SharedTextureMemoryAHardwareBufferProperties();

    struct Init;
    SharedTextureMemoryAHardwareBufferProperties(Init&& init);
    ~SharedTextureMemoryAHardwareBufferProperties();
    SharedTextureMemoryAHardwareBufferProperties(const SharedTextureMemoryAHardwareBufferProperties&) = delete;
    void FreeMembers();
    SharedTextureMemoryAHardwareBufferProperties& operator=(const SharedTextureMemoryAHardwareBufferProperties&) = delete;
    SharedTextureMemoryAHardwareBufferProperties(SharedTextureMemoryAHardwareBufferProperties&&);
    SharedTextureMemoryAHardwareBufferProperties& operator=(SharedTextureMemoryAHardwareBufferProperties&&);
    
    operator const WGPUSharedTextureMemoryAHardwareBufferProperties&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStructOut), alignof(YCbCrVkDescriptor ));
    alignas(kFirstMemberAlignment) YCbCrVkDescriptor const yCbCrInfo = {};
};

struct SharedTextureMemoryProperties {
SharedTextureMemoryProperties() = default;
    ~SharedTextureMemoryProperties();
    SharedTextureMemoryProperties(const SharedTextureMemoryProperties&) = delete;
    void FreeMembers();
    SharedTextureMemoryProperties& operator=(const SharedTextureMemoryProperties&) = delete;
    SharedTextureMemoryProperties(SharedTextureMemoryProperties&&);
    SharedTextureMemoryProperties& operator=(SharedTextureMemoryProperties&&);
    
    operator const WGPUSharedTextureMemoryProperties&() const noexcept;
    ChainedStructOut * const nextInChain = nullptr;
    TextureUsage const usage = {};
    Extent3D const size = {};
    TextureFormat const format = {};
};

struct SharedBufferMemoryDescriptor {
    operator const WGPUSharedBufferMemoryDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * label = nullptr;
};

struct SharedBufferMemoryProperties {
SharedBufferMemoryProperties() = default;
    ~SharedBufferMemoryProperties();
    SharedBufferMemoryProperties(const SharedBufferMemoryProperties&) = delete;
    void FreeMembers();
    SharedBufferMemoryProperties& operator=(const SharedBufferMemoryProperties&) = delete;
    SharedBufferMemoryProperties(SharedBufferMemoryProperties&&);
    SharedBufferMemoryProperties& operator=(SharedBufferMemoryProperties&&);
    
    operator const WGPUSharedBufferMemoryProperties&() const noexcept;
    ChainedStructOut * const nextInChain = nullptr;
    BufferUsage const usage = {};
    uint64_t const size = {};
};

struct ExternalTextureDescriptor {
    operator const WGPUExternalTextureDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * label = nullptr;
    TextureView plane0;
    TextureView plane1 = nullptr;
    Origin2D visibleOrigin = {};
    Extent2D visibleSize = {};
    Bool doYuvToRgbConversionOnly = false;
    float const * yuvToRgbConversionMatrix = nullptr;
    float const * srcTransferFunctionParameters;
    float const * dstTransferFunctionParameters;
    float const * gamutConversionMatrix;
    Bool mirrored = false;
    ExternalTextureRotation rotation = ExternalTextureRotation::Rotate0Degrees;
};

struct SupportedLimits {
SupportedLimits() = default;
    ~SupportedLimits();
    SupportedLimits(const SupportedLimits&) = delete;
    void FreeMembers();
    SupportedLimits& operator=(const SupportedLimits&) = delete;
    SupportedLimits(SupportedLimits&&);
    SupportedLimits& operator=(SupportedLimits&&);
    
    operator const WGPUSupportedLimits&() const noexcept;
    ChainedStructOut * const nextInChain = nullptr;
    Limits const limits = {};
};

// Can be chained in SupportedLimits
struct DawnExperimentalSubgroupLimits : ChainedStructOut {
    DawnExperimentalSubgroupLimits();

    struct Init;
    DawnExperimentalSubgroupLimits(Init&& init);
    ~DawnExperimentalSubgroupLimits();
    DawnExperimentalSubgroupLimits(const DawnExperimentalSubgroupLimits&) = delete;
    void FreeMembers();
    DawnExperimentalSubgroupLimits& operator=(const DawnExperimentalSubgroupLimits&) = delete;
    DawnExperimentalSubgroupLimits(DawnExperimentalSubgroupLimits&&);
    DawnExperimentalSubgroupLimits& operator=(DawnExperimentalSubgroupLimits&&);
    
    operator const WGPUDawnExperimentalSubgroupLimits&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStructOut), alignof(uint32_t ));
    alignas(kFirstMemberAlignment) uint32_t const minSubgroupSize = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t const maxSubgroupSize = WGPU_LIMIT_U32_UNDEFINED;
};

struct PopErrorScopeCallbackInfo2 {
    operator const WGPUPopErrorScopeCallbackInfo2&() const noexcept;
    CallbackMode mode;
    PopErrorScopeCallback2 callback;
};

struct PopErrorScopeCallbackInfo {
    operator const WGPUPopErrorScopeCallbackInfo&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    CallbackMode mode = CallbackMode::WaitAnyOnly;
    PopErrorScopeCallback callback;
    ErrorCallback oldCallback;
    void * userdata = nullptr;
};

struct AHardwareBufferProperties {
    operator const WGPUAHardwareBufferProperties&() const noexcept;
    YCbCrVkDescriptor yCbCrInfo = {};
};

struct CreateRenderPipelineAsyncCallbackInfo2 {
    operator const WGPUCreateRenderPipelineAsyncCallbackInfo2&() const noexcept;
    CallbackMode mode;
    CreateRenderPipelineAsyncCallback2 callback;
};

struct CreateRenderPipelineAsyncCallbackInfo {
    operator const WGPUCreateRenderPipelineAsyncCallbackInfo&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    CallbackMode mode;
    CreateRenderPipelineAsyncCallback callback;
    void * userdata;
};

struct CreateComputePipelineAsyncCallbackInfo2 {
    operator const WGPUCreateComputePipelineAsyncCallbackInfo2&() const noexcept;
    CallbackMode mode;
    CreateComputePipelineAsyncCallback2 callback;
};

struct CreateComputePipelineAsyncCallbackInfo {
    operator const WGPUCreateComputePipelineAsyncCallbackInfo&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    CallbackMode mode;
    CreateComputePipelineAsyncCallback callback;
    void * userdata;
};

struct CopyTextureForBrowserOptions {
    operator const WGPUCopyTextureForBrowserOptions&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    Bool flipY = false;
    Bool needsColorSpaceConversion = false;
    AlphaMode srcAlphaMode = AlphaMode::Unpremultiplied;
    float const * srcTransferFunctionParameters = nullptr;
    float const * conversionMatrix = nullptr;
    float const * dstTransferFunctionParameters = nullptr;
    AlphaMode dstAlphaMode = AlphaMode::Unpremultiplied;
    Bool internalUsage = false;
};

// Can be chained in ComputePipelineDescriptor
struct DawnComputePipelineFullSubgroups : ChainedStruct {
    DawnComputePipelineFullSubgroups();

    struct Init;
    DawnComputePipelineFullSubgroups(Init&& init);
    operator const WGPUDawnComputePipelineFullSubgroups&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(Bool ));
    alignas(kFirstMemberAlignment) Bool requiresFullSubgroups = false;
};

struct ComputePipelineDescriptor {
    operator const WGPUComputePipelineDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * label = nullptr;
    PipelineLayout layout = nullptr;
    ProgrammableStageDescriptor compute = {};
};

struct ComputePassDescriptor {
    operator const WGPUComputePassDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * label = nullptr;
    ComputePassTimestampWrites const * timestampWrites = nullptr;
};

struct CompilationInfoCallbackInfo2 {
    operator const WGPUCompilationInfoCallbackInfo2&() const noexcept;
    CallbackMode mode;
    CompilationInfoCallback2 callback;
};

struct CompilationInfoCallbackInfo {
    operator const WGPUCompilationInfoCallbackInfo&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    CallbackMode mode;
    CompilationInfoCallback callback;
    void * userdata = nullptr;
};

struct CompilationInfo {
    operator const WGPUCompilationInfo&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    size_t messageCount;
    CompilationMessage const * messages;
};

struct CommandEncoderDescriptor {
    operator const WGPUCommandEncoderDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * label = nullptr;
};

struct CommandBufferDescriptor {
    operator const WGPUCommandBufferDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * label = nullptr;
};

struct BufferMapCallbackInfo2 {
    operator const WGPUBufferMapCallbackInfo2&() const noexcept;
    CallbackMode mode;
    BufferMapCallback2 callback;
};

struct BufferMapCallbackInfo {
    operator const WGPUBufferMapCallbackInfo&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    CallbackMode mode;
    BufferMapCallback callback;
    void * userdata;
};

// Can be chained in BufferDescriptor
struct BufferHostMappedPointer : ChainedStruct {
    BufferHostMappedPointer();

    struct Init;
    BufferHostMappedPointer(Init&& init);
    operator const WGPUBufferHostMappedPointer&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(void * ));
    alignas(kFirstMemberAlignment) void * pointer;
    Callback disposeCallback;
    void * userdata;
};

struct BufferDescriptor {
    operator const WGPUBufferDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * label = nullptr;
    BufferUsage usage;
    uint64_t size;
    Bool mappedAtCreation = false;
};

struct NullableStringView {
    operator const WGPUStringView&() const noexcept;
    char const * data = nullptr;
    size_t length = SIZE_MAX;
    // NOLINTNEXTLINE(runtime/explicit) allow implicit construction
    inline constexpr NullableStringView(const std::string_view& sv) noexcept {
        this->data = sv.data();
        this->length = sv.length();
    }
    // NOLINTNEXTLINE(runtime/explicit) allow implicit construction
    inline constexpr NullableStringView(const char* s) {
        this->data = s;
        this->length = SIZE_MAX;  // use strlen
    }
    inline constexpr NullableStringView(const char* data, size_t length) {
        this->data = data;
        this->length = length;
    }
                inline constexpr NullableStringView() noexcept = default;
    
        // NOLINTNEXTLINE(runtime/explicit) allow implicit construction
        inline constexpr NullableStringView(std::nullptr_t) {
            this->data = nullptr;
            this->length = SIZE_MAX;
        }
        // NOLINTNEXTLINE(runtime/explicit) allow implicit construction
        inline constexpr NullableStringView(std::nullopt_t) {
            this->data = nullptr;
            this->length = SIZE_MAX;
        }
    
    operator std::optional<std::string_view>() const;
};

struct StringView {
    operator const WGPUStringView&() const noexcept;
    char const * data = nullptr;
    size_t length = SIZE_MAX;
    // NOLINTNEXTLINE(runtime/explicit) allow implicit construction
    inline constexpr StringView(const std::string_view& sv) noexcept {
        this->data = sv.data();
        this->length = sv.length();
    }
    // NOLINTNEXTLINE(runtime/explicit) allow implicit construction
    inline constexpr StringView(const char* s) {
        this->data = s;
        this->length = SIZE_MAX;  // use strlen
    }
    inline constexpr StringView(const char* data, size_t length) {
        this->data = data;
        this->length = length;
    }
    
    operator std::string_view() const;
};

struct BindGroupLayoutDescriptor {
    operator const WGPUBindGroupLayoutDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * label = nullptr;
    size_t entryCount;
    BindGroupLayoutEntry const * entries;
};

// Can be chained in BindGroupLayoutEntry
struct ExternalTextureBindingLayout : ChainedStruct {
    ExternalTextureBindingLayout();

    struct Init;
    ExternalTextureBindingLayout(Init&& init);
    operator const WGPUExternalTextureBindingLayout&() const noexcept;
};

// Can be chained in BindGroupEntry
struct ExternalTextureBindingEntry : ChainedStruct {
    ExternalTextureBindingEntry();

    struct Init;
    ExternalTextureBindingEntry(Init&& init);
    operator const WGPUExternalTextureBindingEntry&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(ExternalTexture ));
    alignas(kFirstMemberAlignment) ExternalTexture externalTexture;
};

struct SurfaceConfiguration {
    operator const WGPUSurfaceConfiguration&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    Device device;
    TextureFormat format;
    TextureUsage usage = TextureUsage::RenderAttachment;
    size_t viewFormatCount = 0;
    TextureFormat const * viewFormats;
    CompositeAlphaMode alphaMode = CompositeAlphaMode::Auto;
    uint32_t width;
    uint32_t height;
    PresentMode presentMode = PresentMode::Fifo;
};

struct SurfaceCapabilities {
SurfaceCapabilities() = default;
    ~SurfaceCapabilities();
    SurfaceCapabilities(const SurfaceCapabilities&) = delete;
    void FreeMembers();
    SurfaceCapabilities& operator=(const SurfaceCapabilities&) = delete;
    SurfaceCapabilities(SurfaceCapabilities&&);
    SurfaceCapabilities& operator=(SurfaceCapabilities&&);
    
    operator const WGPUSurfaceCapabilities&() const noexcept;
    ChainedStructOut * const nextInChain = nullptr;
    TextureUsage const usages = {};
    size_t const formatCount = {};
    TextureFormat const * const formats = {};
    size_t const presentModeCount = {};
    PresentMode const * const presentModes = {};
    size_t const alphaModeCount = {};
    CompositeAlphaMode const * const alphaModes = {};
};

// Can be chained in BindGroupLayoutEntry
struct StaticSamplerBindingLayout : ChainedStruct {
    StaticSamplerBindingLayout();

    struct Init;
    StaticSamplerBindingLayout(Init&& init);
    operator const WGPUStaticSamplerBindingLayout&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(Sampler ));
    alignas(kFirstMemberAlignment) Sampler sampler;
    uint32_t sampledTextureBinding = WGPU_LIMIT_U32_UNDEFINED;
};

struct BindGroupDescriptor {
    operator const WGPUBindGroupDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * label = nullptr;
    BindGroupLayout layout;
    size_t entryCount;
    BindGroupEntry const * entries;
};

// Can be chained in InstanceDescriptor
struct DawnWGSLBlocklist : ChainedStruct {
    DawnWGSLBlocklist();

    struct Init;
    DawnWGSLBlocklist(Init&& init);
    operator const WGPUDawnWGSLBlocklist&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(size_t ));
    alignas(kFirstMemberAlignment) size_t blocklistedFeatureCount = 0;
    const char* const * blocklistedFeatures;
};

// Can be chained in DeviceDescriptor
struct DawnCacheDeviceDescriptor : ChainedStruct {
    DawnCacheDeviceDescriptor();

    struct Init;
    DawnCacheDeviceDescriptor(Init&& init);
    operator const WGPUDawnCacheDeviceDescriptor&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(char const * ));
    alignas(kFirstMemberAlignment) char const * isolationKey = "";
    DawnLoadCacheDataFunction loadDataFunction = nullptr;
    DawnStoreCacheDataFunction storeDataFunction = nullptr;
    void * functionUserdata = nullptr;
};

// Can be chained in InstanceDescriptor
// Can be chained in RequestAdapterOptions
// Can be chained in DeviceDescriptor
struct DawnTogglesDescriptor : ChainedStruct {
    DawnTogglesDescriptor();

    struct Init;
    DawnTogglesDescriptor(Init&& init);
    operator const WGPUDawnTogglesDescriptor&() const noexcept;
    static constexpr size_t kFirstMemberAlignment = detail::ConstexprMax(alignof(ChainedStruct), alignof(size_t ));
    alignas(kFirstMemberAlignment) size_t enabledToggleCount = 0;
    const char* const * enabledToggles;
    size_t disabledToggleCount = 0;
    const char* const * disabledToggles;
};

struct DeviceDescriptor {
    operator const WGPUDeviceDescriptor&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    char const * label = nullptr;
    size_t requiredFeatureCount = 0;
    FeatureName const * requiredFeatures = nullptr;
    RequiredLimits const * requiredLimits = nullptr;
    QueueDescriptor defaultQueue = {};
    DeviceLostCallback deviceLostCallback = nullptr;
    void * deviceLostUserdata = nullptr;
    DeviceLostCallbackInfo deviceLostCallbackInfo = {};
    UncapturedErrorCallbackInfo uncapturedErrorCallbackInfo = {};
    DeviceLostCallbackInfo2 deviceLostCallbackInfo2;
    UncapturedErrorCallbackInfo2 uncapturedErrorCallbackInfo2;
};

struct AdapterProperties {
AdapterProperties() = default;
    ~AdapterProperties();
    AdapterProperties(const AdapterProperties&) = delete;
    void FreeMembers();
    AdapterProperties& operator=(const AdapterProperties&) = delete;
    AdapterProperties(AdapterProperties&&);
    AdapterProperties& operator=(AdapterProperties&&);
    
    operator const WGPUAdapterProperties&() const noexcept;
    ChainedStructOut * const nextInChain = nullptr;
    uint32_t const vendorID = {};
    char const * const vendorName = nullptr;
    char const * const architecture = nullptr;
    uint32_t const deviceID = {};
    char const * const name = nullptr;
    char const * const driverDescription = nullptr;
    AdapterType const adapterType = {};
    BackendType const backendType = {};
    Bool const compatibilityMode = false;
};

struct AdapterInfo {
AdapterInfo() = default;
    ~AdapterInfo();
    AdapterInfo(const AdapterInfo&) = delete;
    void FreeMembers();
    AdapterInfo& operator=(const AdapterInfo&) = delete;
    AdapterInfo(AdapterInfo&&);
    AdapterInfo& operator=(AdapterInfo&&);
    
    operator const WGPUAdapterInfo&() const noexcept;
    ChainedStructOut * const nextInChain = nullptr;
    char const * const vendor = nullptr;
    char const * const architecture = nullptr;
    char const * const device = nullptr;
    char const * const description = nullptr;
    BackendType const backendType = {};
    AdapterType const adapterType = {};
    uint32_t const vendorID = {};
    uint32_t const deviceID = {};
    Bool const compatibilityMode = false;
};

struct RequestAdapterCallbackInfo2 {
    operator const WGPURequestAdapterCallbackInfo2&() const noexcept;
    CallbackMode mode;
    RequestAdapterCallback2 callback;
};

struct RequestAdapterCallbackInfo {
    operator const WGPURequestAdapterCallbackInfo&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    CallbackMode mode;
    RequestAdapterCallback callback;
    void * userdata;
};

struct RequestAdapterOptions {
    operator const WGPURequestAdapterOptions&() const noexcept;
    ChainedStruct const * nextInChain = nullptr;
    Surface compatibleSurface = nullptr;
    PowerPreference powerPreference = PowerPreference::Undefined;
    BackendType backendType = BackendType::Undefined;
    Bool forceFallbackAdapter = false;
    Bool compatibilityMode = false;
};

struct INTERNAL__HAVE_EMDAWNWEBGPU_HEADER {
    operator const WGPUINTERNAL__HAVE_EMDAWNWEBGPU_HEADER&() const noexcept;
};

class SwapChain : public ObjectBase<SwapChain, WGPUSwapChain> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    TextureView GetCurrentTextureView() const;    
    Texture GetCurrentTexture() const;    
    void Present() const;    
    
    friend ObjectBase<SwapChain, WGPUSwapChain>;
    static void WGPUAddRef(WGPUSwapChain handle);
    static void WGPURelease(WGPUSwapChain handle);
};

class RenderPipeline : public ObjectBase<RenderPipeline, WGPURenderPipeline> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    BindGroupLayout GetBindGroupLayout(uint32_t groupIndex) const;    
    void SetLabel(char const* label) const;    
    void SetLabel2(NullableStringView label) const;    
    
    friend ObjectBase<RenderPipeline, WGPURenderPipeline>;
    static void WGPUAddRef(WGPURenderPipeline handle);
    static void WGPURelease(WGPURenderPipeline handle);
};

class RenderPassEncoder : public ObjectBase<RenderPassEncoder, WGPURenderPassEncoder> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    void SetPipeline(RenderPipeline pipeline) const;    
    void SetBindGroup(uint32_t groupIndex, BindGroup group, size_t dynamicOffsetCount, uint32_t const* dynamicOffsets) const;    
    void Draw(uint32_t vertexCount, uint32_t instanceCount, uint32_t firstVertex, uint32_t firstInstance) const;    
    void DrawIndexed(uint32_t indexCount, uint32_t instanceCount, uint32_t firstIndex, int32_t baseVertex, uint32_t firstInstance) const;    
    void DrawIndirect(Buffer indirectBuffer, uint64_t indirectOffset) const;    
    void DrawIndexedIndirect(Buffer indirectBuffer, uint64_t indirectOffset) const;    
    void ExecuteBundles(size_t bundleCount, RenderBundle const* bundles) const;    
    void InsertDebugMarker(char const* markerLabel) const;    
    void InsertDebugMarker2(StringView markerLabel) const;    
    void PopDebugGroup() const;    
    void PushDebugGroup(char const* groupLabel) const;    
    void PushDebugGroup2(StringView groupLabel) const;    
    void SetStencilReference(uint32_t reference) const;    
    void SetBlendConstant(Color const* color) const;    
    void SetViewport(float x, float y, float width, float height, float minDepth, float maxDepth) const;    
    void SetScissorRect(uint32_t x, uint32_t y, uint32_t width, uint32_t height) const;    
    void SetVertexBuffer(uint32_t slot, Buffer buffer, uint64_t offset, uint64_t size) const;    
    void SetIndexBuffer(Buffer buffer, IndexFormat format, uint64_t offset, uint64_t size) const;    
    void BeginOcclusionQuery(uint32_t queryIndex) const;    
    void EndOcclusionQuery() const;    
    void WriteTimestamp(QuerySet querySet, uint32_t queryIndex) const;    
    void PixelLocalStorageBarrier() const;    
    void End() const;    
    void SetLabel(char const* label) const;    
    void SetLabel2(NullableStringView label) const;    
    
    friend ObjectBase<RenderPassEncoder, WGPURenderPassEncoder>;
    static void WGPUAddRef(WGPURenderPassEncoder handle);
    static void WGPURelease(WGPURenderPassEncoder handle);
};

class RenderBundleEncoder : public ObjectBase<RenderBundleEncoder, WGPURenderBundleEncoder> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    void SetPipeline(RenderPipeline pipeline) const;    
    void SetBindGroup(uint32_t groupIndex, BindGroup group, size_t dynamicOffsetCount, uint32_t const* dynamicOffsets) const;    
    void Draw(uint32_t vertexCount, uint32_t instanceCount, uint32_t firstVertex, uint32_t firstInstance) const;    
    void DrawIndexed(uint32_t indexCount, uint32_t instanceCount, uint32_t firstIndex, int32_t baseVertex, uint32_t firstInstance) const;    
    void DrawIndirect(Buffer indirectBuffer, uint64_t indirectOffset) const;    
    void DrawIndexedIndirect(Buffer indirectBuffer, uint64_t indirectOffset) const;    
    void InsertDebugMarker(char const* markerLabel) const;    
    void InsertDebugMarker2(StringView markerLabel) const;    
    void PopDebugGroup() const;    
    void PushDebugGroup(char const* groupLabel) const;    
    void PushDebugGroup2(StringView groupLabel) const;    
    void SetVertexBuffer(uint32_t slot, Buffer buffer, uint64_t offset, uint64_t size) const;    
    void SetIndexBuffer(Buffer buffer, IndexFormat format, uint64_t offset, uint64_t size) const;    
    RenderBundle Finish(RenderBundleDescriptor const* descriptor) const;    
    void SetLabel(char const* label) const;    
    void SetLabel2(NullableStringView label) const;    
    
    friend ObjectBase<RenderBundleEncoder, WGPURenderBundleEncoder>;
    static void WGPUAddRef(WGPURenderBundleEncoder handle);
    static void WGPURelease(WGPURenderBundleEncoder handle);
};

class RenderBundle : public ObjectBase<RenderBundle, WGPURenderBundle> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    void SetLabel(char const* label) const;    
    void SetLabel2(NullableStringView label) const;    
    
    friend ObjectBase<RenderBundle, WGPURenderBundle>;
    static void WGPUAddRef(WGPURenderBundle handle);
    static void WGPURelease(WGPURenderBundle handle);
};

class Queue : public ObjectBase<Queue, WGPUQueue> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    void Submit(size_t commandCount, CommandBuffer const* commands) const;    
    void WriteBuffer(Buffer buffer, uint64_t bufferOffset, void const* data, size_t size) const;    
    void WriteTexture(ImageCopyTexture const* destination, void const* data, size_t dataSize, TextureDataLayout const* dataLayout, Extent3D const* writeSize) const;    
    void CopyTextureForBrowser(ImageCopyTexture const* source, ImageCopyTexture const* destination, Extent3D const* copySize, CopyTextureForBrowserOptions const* options) const;    
    void CopyExternalTextureForBrowser(ImageCopyExternalTexture const* source, ImageCopyTexture const* destination, Extent3D const* copySize, CopyTextureForBrowserOptions const* options) const;    
    void SetLabel(char const* label) const;    
    void SetLabel2(NullableStringView label) const;    
    
    friend ObjectBase<Queue, WGPUQueue>;
    static void WGPUAddRef(WGPUQueue handle);
    static void WGPURelease(WGPUQueue handle);
};

class Instance : public ObjectBase<Instance, WGPUInstance> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    Surface CreateSurface(SurfaceDescriptor const* descriptor) const;    
    void ProcessEvents() const;    
    WaitStatus WaitAny(size_t futureCount, FutureWaitInfo * futures, uint64_t timeoutNS) const;    
    void RequestAdapter(RequestAdapterOptions const* options, RequestAdapterCallback callback, void * userdata) const;    
    bool HasWGSLLanguageFeature(WGSLFeatureName feature) const;    
    size_t EnumerateWGSLLanguageFeatures(WGSLFeatureName * features) const;    
    
    friend ObjectBase<Instance, WGPUInstance>;
    static void WGPUAddRef(WGPUInstance handle);
    static void WGPURelease(WGPUInstance handle);
};

class SharedTextureMemory : public ObjectBase<SharedTextureMemory, WGPUSharedTextureMemory> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    void SetLabel(char const* label) const;    
    void SetLabel2(NullableStringView label) const;    
    Status GetProperties(SharedTextureMemoryProperties * properties) const;    
    Texture CreateTexture(TextureDescriptor const* descriptor) const;    
    Status BeginAccess(Texture texture, SharedTextureMemoryBeginAccessDescriptor const* descriptor) const;    
    Status EndAccess(Texture texture, SharedTextureMemoryEndAccessState * descriptor) const;    
    bool IsDeviceLost() const;    
    
    friend ObjectBase<SharedTextureMemory, WGPUSharedTextureMemory>;
    static void WGPUAddRef(WGPUSharedTextureMemory handle);
    static void WGPURelease(WGPUSharedTextureMemory handle);
};

class SharedBufferMemory : public ObjectBase<SharedBufferMemory, WGPUSharedBufferMemory> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    void SetLabel(char const* label) const;    
    void SetLabel2(NullableStringView label) const;    
    Status GetProperties(SharedBufferMemoryProperties * properties) const;    
    Buffer CreateBuffer(BufferDescriptor const* descriptor) const;    
    Status BeginAccess(Buffer buffer, SharedBufferMemoryBeginAccessDescriptor const* descriptor) const;    
    Status EndAccess(Buffer buffer, SharedBufferMemoryEndAccessState * descriptor) const;    
    bool IsDeviceLost() const;    
    
    friend ObjectBase<SharedBufferMemory, WGPUSharedBufferMemory>;
    static void WGPUAddRef(WGPUSharedBufferMemory handle);
    static void WGPURelease(WGPUSharedBufferMemory handle);
};

class ComputePipeline : public ObjectBase<ComputePipeline, WGPUComputePipeline> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    BindGroupLayout GetBindGroupLayout(uint32_t groupIndex) const;    
    void SetLabel(char const* label) const;    
    void SetLabel2(NullableStringView label) const;    
    
    friend ObjectBase<ComputePipeline, WGPUComputePipeline>;
    static void WGPUAddRef(WGPUComputePipeline handle);
    static void WGPURelease(WGPUComputePipeline handle);
};

class ComputePassEncoder : public ObjectBase<ComputePassEncoder, WGPUComputePassEncoder> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    void InsertDebugMarker(char const* markerLabel) const;    
    void InsertDebugMarker2(StringView markerLabel) const;    
    void PopDebugGroup() const;    
    void PushDebugGroup(char const* groupLabel) const;    
    void PushDebugGroup2(StringView groupLabel) const;    
    void SetPipeline(ComputePipeline pipeline) const;    
    void SetBindGroup(uint32_t groupIndex, BindGroup group, size_t dynamicOffsetCount, uint32_t const* dynamicOffsets) const;    
    void WriteTimestamp(QuerySet querySet, uint32_t queryIndex) const;    
    void DispatchWorkgroups(uint32_t workgroupCountX, uint32_t workgroupCountY, uint32_t workgroupCountZ) const;    
    void DispatchWorkgroupsIndirect(Buffer indirectBuffer, uint64_t indirectOffset) const;    
    void End() const;    
    void SetLabel(char const* label) const;    
    void SetLabel2(NullableStringView label) const;    
    
    friend ObjectBase<ComputePassEncoder, WGPUComputePassEncoder>;
    static void WGPUAddRef(WGPUComputePassEncoder handle);
    static void WGPURelease(WGPUComputePassEncoder handle);
};

class CommandEncoder : public ObjectBase<CommandEncoder, WGPUCommandEncoder> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    CommandBuffer Finish(CommandBufferDescriptor const* descriptor) const;    
    ComputePassEncoder BeginComputePass(ComputePassDescriptor const* descriptor) const;    
    RenderPassEncoder BeginRenderPass(RenderPassDescriptor const* descriptor) const;    
    void CopyBufferToBuffer(Buffer source, uint64_t sourceOffset, Buffer destination, uint64_t destinationOffset, uint64_t size) const;    
    void CopyBufferToTexture(ImageCopyBuffer const* source, ImageCopyTexture const* destination, Extent3D const* copySize) const;    
    void CopyTextureToBuffer(ImageCopyTexture const* source, ImageCopyBuffer const* destination, Extent3D const* copySize) const;    
    void CopyTextureToTexture(ImageCopyTexture const* source, ImageCopyTexture const* destination, Extent3D const* copySize) const;    
    void ClearBuffer(Buffer buffer, uint64_t offset, uint64_t size) const;    
    void InjectValidationError(char const* message) const;    
    void InjectValidationError2(StringView message) const;    
    void InsertDebugMarker(char const* markerLabel) const;    
    void InsertDebugMarker2(StringView markerLabel) const;    
    void PopDebugGroup() const;    
    void PushDebugGroup(char const* groupLabel) const;    
    void PushDebugGroup2(StringView groupLabel) const;    
    void ResolveQuerySet(QuerySet querySet, uint32_t firstQuery, uint32_t queryCount, Buffer destination, uint64_t destinationOffset) const;    
    void WriteBuffer(Buffer buffer, uint64_t bufferOffset, uint8_t const* data, uint64_t size) const;    
    void WriteTimestamp(QuerySet querySet, uint32_t queryIndex) const;    
    void SetLabel(char const* label) const;    
    void SetLabel2(NullableStringView label) const;    
    
    friend ObjectBase<CommandEncoder, WGPUCommandEncoder>;
    static void WGPUAddRef(WGPUCommandEncoder handle);
    static void WGPURelease(WGPUCommandEncoder handle);
};

class CommandBuffer : public ObjectBase<CommandBuffer, WGPUCommandBuffer> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    void SetLabel(char const* label) const;    
    void SetLabel2(NullableStringView label) const;    
    
    friend ObjectBase<CommandBuffer, WGPUCommandBuffer>;
    static void WGPUAddRef(WGPUCommandBuffer handle);
    static void WGPURelease(WGPUCommandBuffer handle);
};

class BindGroup : public ObjectBase<BindGroup, WGPUBindGroup> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    void SetLabel(char const* label) const;    
    void SetLabel2(NullableStringView label) const;    
    
    friend ObjectBase<BindGroup, WGPUBindGroup>;
    static void WGPUAddRef(WGPUBindGroup handle);
    static void WGPURelease(WGPUBindGroup handle);
};

class Adapter : public ObjectBase<Adapter, WGPUAdapter> {
public:
    using ObjectBase::ObjectBase;
    using ObjectBase::operator=;

    Instance GetInstance() const;    
    Status GetLimits(SupportedLimits * limits) const;    
    Status GetInfo(AdapterInfo * info) const;    
    Status GetProperties(AdapterProperties * properties) const;    
    bool HasFeature(FeatureName feature) const;    
    size_t EnumerateFeatures(FeatureName * features) const;    
    void RequestDevice(DeviceDescriptor const* descriptor, RequestDeviceCallback callback, void * userdata) const;    
    Device CreateDevice(DeviceDescriptor const* descriptor) const;    
    Status GetFormatCapabilities(TextureFormat format, FormatCapabilities * capabilities) const;    
    
    friend ObjectBase<Adapter, WGPUAdapter>;
    static void WGPUAddRef(WGPUAdapter handle);
    static void WGPURelease(WGPUAdapter handle);
};

Instance CreateInstance(InstanceDescriptor const* descriptor);
Status GetInstanceFeatures(InstanceFeatures * features);


} //namespace wgpu

#endif // WGPU_H