#include <dawn/webgpu_cpp.h>
//#include "wgpu.h"

namespace wgpu {
// INTERNAL__HAVE_EMDAWNWEBGPU_HEADER implementation

INTERNAL__HAVE_EMDAWNWEBGPU_HEADER::operator const WGPUINTERNAL__HAVE_EMDAWNWEBGPU_HEADER&() const noexcept {
    return *reinterpret_cast<const WGPUINTERNAL__HAVE_EMDAWNWEBGPU_HEADER*>(this);
}

// RequestAdapterOptions implementation

RequestAdapterOptions::operator const WGPURequestAdapterOptions&() const noexcept {
    return *reinterpret_cast<const WGPURequestAdapterOptions*>(this);
}

// RequestAdapterCallbackInfo implementation

RequestAdapterCallbackInfo::operator const WGPURequestAdapterCallbackInfo&() const noexcept {
    return *reinterpret_cast<const WGPURequestAdapterCallbackInfo*>(this);
}

// RequestAdapterCallbackInfo2 implementation

RequestAdapterCallbackInfo2::operator const WGPURequestAdapterCallbackInfo2&() const noexcept {
    return *reinterpret_cast<const WGPURequestAdapterCallbackInfo2*>(this);
}

// AdapterInfo implementation

AdapterInfo::operator const WGPUAdapterInfo&() const noexcept {
    return *reinterpret_cast<const WGPUAdapterInfo*>(this);
}

AdapterInfo::~AdapterInfo() {
    FreeMembers();
}
void AdapterInfo::FreeMembers() {
    // Free members here
}

AdapterInfo::AdapterInfo(AdapterInfo&& rhs) :
    nextInChain(rhs.nextInChain),    
    vendor(rhs.vendor),    
    architecture(rhs.architecture),    
    device(rhs.device),    
    description(rhs.description),    
    backendType(rhs.backendType),    
    adapterType(rhs.adapterType),    
    vendorID(rhs.vendorID),    
    deviceID(rhs.deviceID),    
    compatibilityMode(rhs.compatibilityMode)    
{}
AdapterInfo& AdapterInfo::operator=(AdapterInfo&& rhs) {
if (&rhs == this) {
    return *this;
}
FreeMembers();

    ::wgpu::detail::AsNonConstReference(this->nextInChain) = std::move(rhs.nextInChain);    
    ::wgpu::detail::AsNonConstReference(this->vendor) = std::move(rhs.vendor);    
    ::wgpu::detail::AsNonConstReference(this->architecture) = std::move(rhs.architecture);    
    ::wgpu::detail::AsNonConstReference(this->device) = std::move(rhs.device);    
    ::wgpu::detail::AsNonConstReference(this->description) = std::move(rhs.description);    
    ::wgpu::detail::AsNonConstReference(this->backendType) = std::move(rhs.backendType);    
    ::wgpu::detail::AsNonConstReference(this->adapterType) = std::move(rhs.adapterType);    
    ::wgpu::detail::AsNonConstReference(this->vendorID) = std::move(rhs.vendorID);    
    ::wgpu::detail::AsNonConstReference(this->deviceID) = std::move(rhs.deviceID);    
    ::wgpu::detail::AsNonConstReference(this->compatibilityMode) = std::move(rhs.compatibilityMode);    
    return *this;    
}
// AdapterProperties implementation

AdapterProperties::operator const WGPUAdapterProperties&() const noexcept {
    return *reinterpret_cast<const WGPUAdapterProperties*>(this);
}

AdapterProperties::~AdapterProperties() {
    FreeMembers();
}
void AdapterProperties::FreeMembers() {
    // Free members here
}

AdapterProperties::AdapterProperties(AdapterProperties&& rhs) :
    nextInChain(rhs.nextInChain),    
    vendorID(rhs.vendorID),    
    vendorName(rhs.vendorName),    
    architecture(rhs.architecture),    
    deviceID(rhs.deviceID),    
    name(rhs.name),    
    driverDescription(rhs.driverDescription),    
    adapterType(rhs.adapterType),    
    backendType(rhs.backendType),    
    compatibilityMode(rhs.compatibilityMode)    
{}
AdapterProperties& AdapterProperties::operator=(AdapterProperties&& rhs) {
if (&rhs == this) {
    return *this;
}
FreeMembers();

    ::wgpu::detail::AsNonConstReference(this->nextInChain) = std::move(rhs.nextInChain);    
    ::wgpu::detail::AsNonConstReference(this->vendorID) = std::move(rhs.vendorID);    
    ::wgpu::detail::AsNonConstReference(this->vendorName) = std::move(rhs.vendorName);    
    ::wgpu::detail::AsNonConstReference(this->architecture) = std::move(rhs.architecture);    
    ::wgpu::detail::AsNonConstReference(this->deviceID) = std::move(rhs.deviceID);    
    ::wgpu::detail::AsNonConstReference(this->name) = std::move(rhs.name);    
    ::wgpu::detail::AsNonConstReference(this->driverDescription) = std::move(rhs.driverDescription);    
    ::wgpu::detail::AsNonConstReference(this->adapterType) = std::move(rhs.adapterType);    
    ::wgpu::detail::AsNonConstReference(this->backendType) = std::move(rhs.backendType);    
    ::wgpu::detail::AsNonConstReference(this->compatibilityMode) = std::move(rhs.compatibilityMode);    
    return *this;    
}
// DeviceDescriptor implementation

DeviceDescriptor::operator const WGPUDeviceDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUDeviceDescriptor*>(this);
}

// DawnTogglesDescriptor implementation

DawnTogglesDescriptor::operator const WGPUDawnTogglesDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUDawnTogglesDescriptor*>(this);
}

DawnTogglesDescriptor::DawnTogglesDescriptor()
: ChainedStruct { nullptr, SType::DawnTogglesDescriptor } {}

struct DawnTogglesDescriptor::Init {
    ChainedStruct const * nextInChain = nullptr;
    size_t enabledToggleCount = 0;
    const char* const * enabledToggles;
    size_t disabledToggleCount = 0;
    const char* const * disabledToggles;
};
DawnTogglesDescriptor::DawnTogglesDescriptor(DawnTogglesDescriptor::Init&& init)
: ChainedStruct { init.nextInChain, SType::DawnTogglesDescriptor }
    ,enabledToggleCount(std::move(init.enabledToggleCount))
    ,enabledToggles(std::move(init.enabledToggles))
    ,disabledToggleCount(std::move(init.disabledToggleCount))
    ,disabledToggles(std::move(init.disabledToggles))
    {}
// DawnCacheDeviceDescriptor implementation

DawnCacheDeviceDescriptor::operator const WGPUDawnCacheDeviceDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUDawnCacheDeviceDescriptor*>(this);
}

DawnCacheDeviceDescriptor::DawnCacheDeviceDescriptor()
: ChainedStruct { nullptr, SType::DawnCacheDeviceDescriptor } {}

struct DawnCacheDeviceDescriptor::Init {
    ChainedStruct const * nextInChain = nullptr;
    char const * isolationKey = "";
    DawnLoadCacheDataFunction loadDataFunction = nullptr;
    DawnStoreCacheDataFunction storeDataFunction = nullptr;
    void * functionUserdata = nullptr;
};
DawnCacheDeviceDescriptor::DawnCacheDeviceDescriptor(DawnCacheDeviceDescriptor::Init&& init)
: ChainedStruct { init.nextInChain, SType::DawnCacheDeviceDescriptor }
    ,isolationKey(std::move(init.isolationKey))
    ,loadDataFunction(std::move(init.loadDataFunction))
    ,storeDataFunction(std::move(init.storeDataFunction))
    ,functionUserdata(std::move(init.functionUserdata))
    {}
// DawnWGSLBlocklist implementation

DawnWGSLBlocklist::operator const WGPUDawnWGSLBlocklist&() const noexcept {
    return *reinterpret_cast<const WGPUDawnWGSLBlocklist*>(this);
}

DawnWGSLBlocklist::DawnWGSLBlocklist()
: ChainedStruct { nullptr, SType::DawnWGSLBlocklist } {}

struct DawnWGSLBlocklist::Init {
    ChainedStruct const * nextInChain = nullptr;
    size_t blocklistedFeatureCount = 0;
    const char* const * blocklistedFeatures;
};
DawnWGSLBlocklist::DawnWGSLBlocklist(DawnWGSLBlocklist::Init&& init)
: ChainedStruct { init.nextInChain, SType::DawnWGSLBlocklist }
    ,blocklistedFeatureCount(std::move(init.blocklistedFeatureCount))
    ,blocklistedFeatures(std::move(init.blocklistedFeatures))
    {}
// BindGroupEntry implementation

BindGroupEntry::operator const WGPUBindGroupEntry&() const noexcept {
    return *reinterpret_cast<const WGPUBindGroupEntry*>(this);
}

// BindGroupDescriptor implementation

BindGroupDescriptor::operator const WGPUBindGroupDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUBindGroupDescriptor*>(this);
}

// BufferBindingLayout implementation

BufferBindingLayout::operator const WGPUBufferBindingLayout&() const noexcept {
    return *reinterpret_cast<const WGPUBufferBindingLayout*>(this);
}

// SamplerBindingLayout implementation

SamplerBindingLayout::operator const WGPUSamplerBindingLayout&() const noexcept {
    return *reinterpret_cast<const WGPUSamplerBindingLayout*>(this);
}

// StaticSamplerBindingLayout implementation

StaticSamplerBindingLayout::operator const WGPUStaticSamplerBindingLayout&() const noexcept {
    return *reinterpret_cast<const WGPUStaticSamplerBindingLayout*>(this);
}

StaticSamplerBindingLayout::StaticSamplerBindingLayout()
: ChainedStruct { nullptr, SType::StaticSamplerBindingLayout } {}

struct StaticSamplerBindingLayout::Init {
    ChainedStruct const * nextInChain = nullptr;
    Sampler sampler;
    uint32_t sampledTextureBinding = WGPU_LIMIT_U32_UNDEFINED;
};
StaticSamplerBindingLayout::StaticSamplerBindingLayout(StaticSamplerBindingLayout::Init&& init)
: ChainedStruct { init.nextInChain, SType::StaticSamplerBindingLayout }
    ,sampler(std::move(init.sampler))
    ,sampledTextureBinding(std::move(init.sampledTextureBinding))
    {}
// TextureBindingLayout implementation

TextureBindingLayout::operator const WGPUTextureBindingLayout&() const noexcept {
    return *reinterpret_cast<const WGPUTextureBindingLayout*>(this);
}

// SurfaceCapabilities implementation

SurfaceCapabilities::operator const WGPUSurfaceCapabilities&() const noexcept {
    return *reinterpret_cast<const WGPUSurfaceCapabilities*>(this);
}

SurfaceCapabilities::~SurfaceCapabilities() {
    FreeMembers();
}
void SurfaceCapabilities::FreeMembers() {
    // Free members here
}

SurfaceCapabilities::SurfaceCapabilities(SurfaceCapabilities&& rhs) :
    nextInChain(rhs.nextInChain),    
    usages(rhs.usages),    
    formatCount(rhs.formatCount),    
    formats(rhs.formats),    
    presentModeCount(rhs.presentModeCount),    
    presentModes(rhs.presentModes),    
    alphaModeCount(rhs.alphaModeCount),    
    alphaModes(rhs.alphaModes)    
{}
SurfaceCapabilities& SurfaceCapabilities::operator=(SurfaceCapabilities&& rhs) {
if (&rhs == this) {
    return *this;
}
FreeMembers();

    ::wgpu::detail::AsNonConstReference(this->nextInChain) = std::move(rhs.nextInChain);    
    ::wgpu::detail::AsNonConstReference(this->usages) = std::move(rhs.usages);    
    ::wgpu::detail::AsNonConstReference(this->formatCount) = std::move(rhs.formatCount);    
    ::wgpu::detail::AsNonConstReference(this->formats) = std::move(rhs.formats);    
    ::wgpu::detail::AsNonConstReference(this->presentModeCount) = std::move(rhs.presentModeCount);    
    ::wgpu::detail::AsNonConstReference(this->presentModes) = std::move(rhs.presentModes);    
    ::wgpu::detail::AsNonConstReference(this->alphaModeCount) = std::move(rhs.alphaModeCount);    
    ::wgpu::detail::AsNonConstReference(this->alphaModes) = std::move(rhs.alphaModes);    
    return *this;    
}
// SurfaceConfiguration implementation

SurfaceConfiguration::operator const WGPUSurfaceConfiguration&() const noexcept {
    return *reinterpret_cast<const WGPUSurfaceConfiguration*>(this);
}

// ExternalTextureBindingEntry implementation

ExternalTextureBindingEntry::operator const WGPUExternalTextureBindingEntry&() const noexcept {
    return *reinterpret_cast<const WGPUExternalTextureBindingEntry*>(this);
}

ExternalTextureBindingEntry::ExternalTextureBindingEntry()
: ChainedStruct { nullptr, SType::ExternalTextureBindingEntry } {}

struct ExternalTextureBindingEntry::Init {
    ChainedStruct const * nextInChain = nullptr;
    ExternalTexture externalTexture;
};
ExternalTextureBindingEntry::ExternalTextureBindingEntry(ExternalTextureBindingEntry::Init&& init)
: ChainedStruct { init.nextInChain, SType::ExternalTextureBindingEntry }
    ,externalTexture(std::move(init.externalTexture))
    {}
// ExternalTextureBindingLayout implementation

ExternalTextureBindingLayout::operator const WGPUExternalTextureBindingLayout&() const noexcept {
    return *reinterpret_cast<const WGPUExternalTextureBindingLayout*>(this);
}

ExternalTextureBindingLayout::ExternalTextureBindingLayout()
: ChainedStruct { nullptr, SType::ExternalTextureBindingLayout } {}

struct ExternalTextureBindingLayout::Init {
    ChainedStruct const * nextInChain = nullptr;
};
ExternalTextureBindingLayout::ExternalTextureBindingLayout(ExternalTextureBindingLayout::Init&& init)
: ChainedStruct { init.nextInChain, SType::ExternalTextureBindingLayout }
    {}
// StorageTextureBindingLayout implementation

StorageTextureBindingLayout::operator const WGPUStorageTextureBindingLayout&() const noexcept {
    return *reinterpret_cast<const WGPUStorageTextureBindingLayout*>(this);
}

// BindGroupLayoutEntry implementation

BindGroupLayoutEntry::operator const WGPUBindGroupLayoutEntry&() const noexcept {
    return *reinterpret_cast<const WGPUBindGroupLayoutEntry*>(this);
}

// BindGroupLayoutDescriptor implementation

BindGroupLayoutDescriptor::operator const WGPUBindGroupLayoutDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUBindGroupLayoutDescriptor*>(this);
}

// BlendComponent implementation

BlendComponent::operator const WGPUBlendComponent&() const noexcept {
    return *reinterpret_cast<const WGPUBlendComponent*>(this);
}

// StringView implementation

StringView::operator const WGPUStringView&() const noexcept {
    return *reinterpret_cast<const WGPUStringView*>(this);
}

// NullableStringView implementation

NullableStringView::operator const WGPUStringView&() const noexcept {
    return *reinterpret_cast<const WGPUStringView*>(this);
}

// BufferDescriptor implementation

BufferDescriptor::operator const WGPUBufferDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUBufferDescriptor*>(this);
}

// BufferHostMappedPointer implementation

BufferHostMappedPointer::operator const WGPUBufferHostMappedPointer&() const noexcept {
    return *reinterpret_cast<const WGPUBufferHostMappedPointer*>(this);
}

BufferHostMappedPointer::BufferHostMappedPointer()
: ChainedStruct { nullptr, SType::BufferHostMappedPointer } {}

struct BufferHostMappedPointer::Init {
    ChainedStruct const * nextInChain = nullptr;
    void * pointer;
    Callback disposeCallback;
    void * userdata;
};
BufferHostMappedPointer::BufferHostMappedPointer(BufferHostMappedPointer::Init&& init)
: ChainedStruct { init.nextInChain, SType::BufferHostMappedPointer }
    ,pointer(std::move(init.pointer))
    ,disposeCallback(std::move(init.disposeCallback))
    ,userdata(std::move(init.userdata))
    {}
// BufferMapCallbackInfo implementation

BufferMapCallbackInfo::operator const WGPUBufferMapCallbackInfo&() const noexcept {
    return *reinterpret_cast<const WGPUBufferMapCallbackInfo*>(this);
}

// BufferMapCallbackInfo2 implementation

BufferMapCallbackInfo2::operator const WGPUBufferMapCallbackInfo2&() const noexcept {
    return *reinterpret_cast<const WGPUBufferMapCallbackInfo2*>(this);
}

// Color implementation

Color::operator const WGPUColor&() const noexcept {
    return *reinterpret_cast<const WGPUColor*>(this);
}

// ConstantEntry implementation

ConstantEntry::operator const WGPUConstantEntry&() const noexcept {
    return *reinterpret_cast<const WGPUConstantEntry*>(this);
}

// CommandBufferDescriptor implementation

CommandBufferDescriptor::operator const WGPUCommandBufferDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUCommandBufferDescriptor*>(this);
}

// CommandEncoderDescriptor implementation

CommandEncoderDescriptor::operator const WGPUCommandEncoderDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUCommandEncoderDescriptor*>(this);
}

// CompilationInfo implementation

CompilationInfo::operator const WGPUCompilationInfo&() const noexcept {
    return *reinterpret_cast<const WGPUCompilationInfo*>(this);
}

// CompilationInfoCallbackInfo implementation

CompilationInfoCallbackInfo::operator const WGPUCompilationInfoCallbackInfo&() const noexcept {
    return *reinterpret_cast<const WGPUCompilationInfoCallbackInfo*>(this);
}

// CompilationInfoCallbackInfo2 implementation

CompilationInfoCallbackInfo2::operator const WGPUCompilationInfoCallbackInfo2&() const noexcept {
    return *reinterpret_cast<const WGPUCompilationInfoCallbackInfo2*>(this);
}

// CompilationMessage implementation

CompilationMessage::operator const WGPUCompilationMessage&() const noexcept {
    return *reinterpret_cast<const WGPUCompilationMessage*>(this);
}

// ComputePassDescriptor implementation

ComputePassDescriptor::operator const WGPUComputePassDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUComputePassDescriptor*>(this);
}

// ComputePassTimestampWrites implementation

ComputePassTimestampWrites::operator const WGPUComputePassTimestampWrites&() const noexcept {
    return *reinterpret_cast<const WGPUComputePassTimestampWrites*>(this);
}

// ComputePipelineDescriptor implementation

ComputePipelineDescriptor::operator const WGPUComputePipelineDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUComputePipelineDescriptor*>(this);
}

// DawnComputePipelineFullSubgroups implementation

DawnComputePipelineFullSubgroups::operator const WGPUDawnComputePipelineFullSubgroups&() const noexcept {
    return *reinterpret_cast<const WGPUDawnComputePipelineFullSubgroups*>(this);
}

DawnComputePipelineFullSubgroups::DawnComputePipelineFullSubgroups()
: ChainedStruct { nullptr, SType::DawnComputePipelineFullSubgroups } {}

struct DawnComputePipelineFullSubgroups::Init {
    ChainedStruct const * nextInChain = nullptr;
    Bool requiresFullSubgroups = false;
};
DawnComputePipelineFullSubgroups::DawnComputePipelineFullSubgroups(DawnComputePipelineFullSubgroups::Init&& init)
: ChainedStruct { init.nextInChain, SType::DawnComputePipelineFullSubgroups }
    ,requiresFullSubgroups(std::move(init.requiresFullSubgroups))
    {}
// CopyTextureForBrowserOptions implementation

CopyTextureForBrowserOptions::operator const WGPUCopyTextureForBrowserOptions&() const noexcept {
    return *reinterpret_cast<const WGPUCopyTextureForBrowserOptions*>(this);
}

// CreateComputePipelineAsyncCallbackInfo implementation

CreateComputePipelineAsyncCallbackInfo::operator const WGPUCreateComputePipelineAsyncCallbackInfo&() const noexcept {
    return *reinterpret_cast<const WGPUCreateComputePipelineAsyncCallbackInfo*>(this);
}

// CreateComputePipelineAsyncCallbackInfo2 implementation

CreateComputePipelineAsyncCallbackInfo2::operator const WGPUCreateComputePipelineAsyncCallbackInfo2&() const noexcept {
    return *reinterpret_cast<const WGPUCreateComputePipelineAsyncCallbackInfo2*>(this);
}

// CreateRenderPipelineAsyncCallbackInfo implementation

CreateRenderPipelineAsyncCallbackInfo::operator const WGPUCreateRenderPipelineAsyncCallbackInfo&() const noexcept {
    return *reinterpret_cast<const WGPUCreateRenderPipelineAsyncCallbackInfo*>(this);
}

// CreateRenderPipelineAsyncCallbackInfo2 implementation

CreateRenderPipelineAsyncCallbackInfo2::operator const WGPUCreateRenderPipelineAsyncCallbackInfo2&() const noexcept {
    return *reinterpret_cast<const WGPUCreateRenderPipelineAsyncCallbackInfo2*>(this);
}

// AHardwareBufferProperties implementation

AHardwareBufferProperties::operator const WGPUAHardwareBufferProperties&() const noexcept {
    return *reinterpret_cast<const WGPUAHardwareBufferProperties*>(this);
}

// DeviceLostCallbackInfo implementation

DeviceLostCallbackInfo::operator const WGPUDeviceLostCallbackInfo&() const noexcept {
    return *reinterpret_cast<const WGPUDeviceLostCallbackInfo*>(this);
}

// DeviceLostCallbackInfo2 implementation

DeviceLostCallbackInfo2::operator const WGPUDeviceLostCallbackInfo2&() const noexcept {
    return *reinterpret_cast<const WGPUDeviceLostCallbackInfo2*>(this);
}

// UncapturedErrorCallbackInfo implementation

UncapturedErrorCallbackInfo::operator const WGPUUncapturedErrorCallbackInfo&() const noexcept {
    return *reinterpret_cast<const WGPUUncapturedErrorCallbackInfo*>(this);
}

// UncapturedErrorCallbackInfo2 implementation

UncapturedErrorCallbackInfo2::operator const WGPUUncapturedErrorCallbackInfo2&() const noexcept {
    return *reinterpret_cast<const WGPUUncapturedErrorCallbackInfo2*>(this);
}

// PopErrorScopeCallbackInfo implementation

PopErrorScopeCallbackInfo::operator const WGPUPopErrorScopeCallbackInfo&() const noexcept {
    return *reinterpret_cast<const WGPUPopErrorScopeCallbackInfo*>(this);
}

// PopErrorScopeCallbackInfo2 implementation

PopErrorScopeCallbackInfo2::operator const WGPUPopErrorScopeCallbackInfo2&() const noexcept {
    return *reinterpret_cast<const WGPUPopErrorScopeCallbackInfo2*>(this);
}

// Limits implementation

Limits::operator const WGPULimits&() const noexcept {
    return *reinterpret_cast<const WGPULimits*>(this);
}

// DawnExperimentalSubgroupLimits implementation

DawnExperimentalSubgroupLimits::operator const WGPUDawnExperimentalSubgroupLimits&() const noexcept {
    return *reinterpret_cast<const WGPUDawnExperimentalSubgroupLimits*>(this);
}

DawnExperimentalSubgroupLimits::DawnExperimentalSubgroupLimits()
: ChainedStructOut { nullptr, SType::DawnExperimentalSubgroupLimits } {}

struct DawnExperimentalSubgroupLimits::Init {
    ChainedStructOut * const nextInChain = nullptr;
    uint32_t const minSubgroupSize = WGPU_LIMIT_U32_UNDEFINED;
    uint32_t const maxSubgroupSize = WGPU_LIMIT_U32_UNDEFINED;
};
DawnExperimentalSubgroupLimits::DawnExperimentalSubgroupLimits(DawnExperimentalSubgroupLimits::Init&& init)
: ChainedStructOut { init.nextInChain, SType::DawnExperimentalSubgroupLimits }
    ,minSubgroupSize(std::move(init.minSubgroupSize))
    ,maxSubgroupSize(std::move(init.maxSubgroupSize))
    {}
DawnExperimentalSubgroupLimits::~DawnExperimentalSubgroupLimits() {
    FreeMembers();
}
void DawnExperimentalSubgroupLimits::FreeMembers() {
    // Free members here
}

DawnExperimentalSubgroupLimits::DawnExperimentalSubgroupLimits(DawnExperimentalSubgroupLimits&& rhs) :
    minSubgroupSize(rhs.minSubgroupSize),    
    maxSubgroupSize(rhs.maxSubgroupSize)    
{}
DawnExperimentalSubgroupLimits& DawnExperimentalSubgroupLimits::operator=(DawnExperimentalSubgroupLimits&& rhs) {
if (&rhs == this) {
    return *this;
}
FreeMembers();

    ::wgpu::detail::AsNonConstReference(this->minSubgroupSize) = std::move(rhs.minSubgroupSize);    
    ::wgpu::detail::AsNonConstReference(this->maxSubgroupSize) = std::move(rhs.maxSubgroupSize);    
    return *this;    
}
// RequiredLimits implementation

RequiredLimits::operator const WGPURequiredLimits&() const noexcept {
    return *reinterpret_cast<const WGPURequiredLimits*>(this);
}

// SupportedLimits implementation

SupportedLimits::operator const WGPUSupportedLimits&() const noexcept {
    return *reinterpret_cast<const WGPUSupportedLimits*>(this);
}

SupportedLimits::~SupportedLimits() {
    FreeMembers();
}
void SupportedLimits::FreeMembers() {
    // Free members here
}

SupportedLimits::SupportedLimits(SupportedLimits&& rhs) :
    nextInChain(rhs.nextInChain),    
    limits(rhs.limits)    
{}
SupportedLimits& SupportedLimits::operator=(SupportedLimits&& rhs) {
if (&rhs == this) {
    return *this;
}
FreeMembers();

    ::wgpu::detail::AsNonConstReference(this->nextInChain) = std::move(rhs.nextInChain);    
    ::wgpu::detail::AsNonConstReference(this->limits) = std::move(rhs.limits);    
    return *this;    
}
// Extent2D implementation

Extent2D::operator const WGPUExtent2D&() const noexcept {
    return *reinterpret_cast<const WGPUExtent2D*>(this);
}

// Extent3D implementation

Extent3D::operator const WGPUExtent3D&() const noexcept {
    return *reinterpret_cast<const WGPUExtent3D*>(this);
}

// ExternalTextureDescriptor implementation

ExternalTextureDescriptor::operator const WGPUExternalTextureDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUExternalTextureDescriptor*>(this);
}

// SharedBufferMemoryProperties implementation

SharedBufferMemoryProperties::operator const WGPUSharedBufferMemoryProperties&() const noexcept {
    return *reinterpret_cast<const WGPUSharedBufferMemoryProperties*>(this);
}

SharedBufferMemoryProperties::~SharedBufferMemoryProperties() {
    FreeMembers();
}
void SharedBufferMemoryProperties::FreeMembers() {
    // Free members here
}

SharedBufferMemoryProperties::SharedBufferMemoryProperties(SharedBufferMemoryProperties&& rhs) :
    nextInChain(rhs.nextInChain),    
    usage(rhs.usage),    
    size(rhs.size)    
{}
SharedBufferMemoryProperties& SharedBufferMemoryProperties::operator=(SharedBufferMemoryProperties&& rhs) {
if (&rhs == this) {
    return *this;
}
FreeMembers();

    ::wgpu::detail::AsNonConstReference(this->nextInChain) = std::move(rhs.nextInChain);    
    ::wgpu::detail::AsNonConstReference(this->usage) = std::move(rhs.usage);    
    ::wgpu::detail::AsNonConstReference(this->size) = std::move(rhs.size);    
    return *this;    
}
// SharedBufferMemoryDescriptor implementation

SharedBufferMemoryDescriptor::operator const WGPUSharedBufferMemoryDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUSharedBufferMemoryDescriptor*>(this);
}

// SharedTextureMemoryProperties implementation

SharedTextureMemoryProperties::operator const WGPUSharedTextureMemoryProperties&() const noexcept {
    return *reinterpret_cast<const WGPUSharedTextureMemoryProperties*>(this);
}

SharedTextureMemoryProperties::~SharedTextureMemoryProperties() {
    FreeMembers();
}
void SharedTextureMemoryProperties::FreeMembers() {
    // Free members here
}

SharedTextureMemoryProperties::SharedTextureMemoryProperties(SharedTextureMemoryProperties&& rhs) :
    nextInChain(rhs.nextInChain),    
    usage(rhs.usage),    
    size(rhs.size),    
    format(rhs.format)    
{}
SharedTextureMemoryProperties& SharedTextureMemoryProperties::operator=(SharedTextureMemoryProperties&& rhs) {
if (&rhs == this) {
    return *this;
}
FreeMembers();

    ::wgpu::detail::AsNonConstReference(this->nextInChain) = std::move(rhs.nextInChain);    
    ::wgpu::detail::AsNonConstReference(this->usage) = std::move(rhs.usage);    
    ::wgpu::detail::AsNonConstReference(this->size) = std::move(rhs.size);    
    ::wgpu::detail::AsNonConstReference(this->format) = std::move(rhs.format);    
    return *this;    
}
// SharedTextureMemoryAHardwareBufferProperties implementation

SharedTextureMemoryAHardwareBufferProperties::operator const WGPUSharedTextureMemoryAHardwareBufferProperties&() const noexcept {
    return *reinterpret_cast<const WGPUSharedTextureMemoryAHardwareBufferProperties*>(this);
}

SharedTextureMemoryAHardwareBufferProperties::SharedTextureMemoryAHardwareBufferProperties()
: ChainedStructOut { nullptr, SType::SharedTextureMemoryAHardwareBufferProperties } {}

struct SharedTextureMemoryAHardwareBufferProperties::Init {
    ChainedStructOut * const nextInChain = nullptr;
    YCbCrVkDescriptor const yCbCrInfo = {};
};
SharedTextureMemoryAHardwareBufferProperties::SharedTextureMemoryAHardwareBufferProperties(SharedTextureMemoryAHardwareBufferProperties::Init&& init)
: ChainedStructOut { init.nextInChain, SType::SharedTextureMemoryAHardwareBufferProperties }
    ,yCbCrInfo(std::move(init.yCbCrInfo))
    {}
SharedTextureMemoryAHardwareBufferProperties::~SharedTextureMemoryAHardwareBufferProperties() {
    FreeMembers();
}
void SharedTextureMemoryAHardwareBufferProperties::FreeMembers() {
    // Free members here
}

SharedTextureMemoryAHardwareBufferProperties::SharedTextureMemoryAHardwareBufferProperties(SharedTextureMemoryAHardwareBufferProperties&& rhs) :
    yCbCrInfo(rhs.yCbCrInfo)    
{}
SharedTextureMemoryAHardwareBufferProperties& SharedTextureMemoryAHardwareBufferProperties::operator=(SharedTextureMemoryAHardwareBufferProperties&& rhs) {
if (&rhs == this) {
    return *this;
}
FreeMembers();

    ::wgpu::detail::AsNonConstReference(this->yCbCrInfo) = std::move(rhs.yCbCrInfo);    
    return *this;    
}
// SharedTextureMemoryDescriptor implementation

SharedTextureMemoryDescriptor::operator const WGPUSharedTextureMemoryDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUSharedTextureMemoryDescriptor*>(this);
}

// SharedBufferMemoryBeginAccessDescriptor implementation

SharedBufferMemoryBeginAccessDescriptor::operator const WGPUSharedBufferMemoryBeginAccessDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUSharedBufferMemoryBeginAccessDescriptor*>(this);
}

// SharedBufferMemoryEndAccessState implementation

SharedBufferMemoryEndAccessState::operator const WGPUSharedBufferMemoryEndAccessState&() const noexcept {
    return *reinterpret_cast<const WGPUSharedBufferMemoryEndAccessState*>(this);
}

SharedBufferMemoryEndAccessState::~SharedBufferMemoryEndAccessState() {
    FreeMembers();
}
void SharedBufferMemoryEndAccessState::FreeMembers() {
    // Free members here
}

SharedBufferMemoryEndAccessState::SharedBufferMemoryEndAccessState(SharedBufferMemoryEndAccessState&& rhs) :
    nextInChain(rhs.nextInChain),    
    initialized(rhs.initialized),    
    fenceCount(rhs.fenceCount),    
    fences(rhs.fences),    
    signaledValues(rhs.signaledValues)    
{}
SharedBufferMemoryEndAccessState& SharedBufferMemoryEndAccessState::operator=(SharedBufferMemoryEndAccessState&& rhs) {
if (&rhs == this) {
    return *this;
}
FreeMembers();

    ::wgpu::detail::AsNonConstReference(this->nextInChain) = std::move(rhs.nextInChain);    
    ::wgpu::detail::AsNonConstReference(this->initialized) = std::move(rhs.initialized);    
    ::wgpu::detail::AsNonConstReference(this->fenceCount) = std::move(rhs.fenceCount);    
    ::wgpu::detail::AsNonConstReference(this->fences) = std::move(rhs.fences);    
    ::wgpu::detail::AsNonConstReference(this->signaledValues) = std::move(rhs.signaledValues);    
    return *this;    
}
// SharedTextureMemoryVkDedicatedAllocationDescriptor implementation

SharedTextureMemoryVkDedicatedAllocationDescriptor::operator const WGPUSharedTextureMemoryVkDedicatedAllocationDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUSharedTextureMemoryVkDedicatedAllocationDescriptor*>(this);
}

SharedTextureMemoryVkDedicatedAllocationDescriptor::SharedTextureMemoryVkDedicatedAllocationDescriptor()
: ChainedStruct { nullptr, SType::SharedTextureMemoryVkDedicatedAllocationDescriptor } {}

struct SharedTextureMemoryVkDedicatedAllocationDescriptor::Init {
    ChainedStruct const * nextInChain = nullptr;
    Bool dedicatedAllocation;
};
SharedTextureMemoryVkDedicatedAllocationDescriptor::SharedTextureMemoryVkDedicatedAllocationDescriptor(SharedTextureMemoryVkDedicatedAllocationDescriptor::Init&& init)
: ChainedStruct { init.nextInChain, SType::SharedTextureMemoryVkDedicatedAllocationDescriptor }
    ,dedicatedAllocation(std::move(init.dedicatedAllocation))
    {}
// SharedTextureMemoryAHardwareBufferDescriptor implementation

SharedTextureMemoryAHardwareBufferDescriptor::operator const WGPUSharedTextureMemoryAHardwareBufferDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUSharedTextureMemoryAHardwareBufferDescriptor*>(this);
}

SharedTextureMemoryAHardwareBufferDescriptor::SharedTextureMemoryAHardwareBufferDescriptor()
: ChainedStruct { nullptr, SType::SharedTextureMemoryAHardwareBufferDescriptor } {}

struct SharedTextureMemoryAHardwareBufferDescriptor::Init {
    ChainedStruct const * nextInChain = nullptr;
    void * handle;
    Bool useExternalFormat;
};
SharedTextureMemoryAHardwareBufferDescriptor::SharedTextureMemoryAHardwareBufferDescriptor(SharedTextureMemoryAHardwareBufferDescriptor::Init&& init)
: ChainedStruct { init.nextInChain, SType::SharedTextureMemoryAHardwareBufferDescriptor }
    ,handle(std::move(init.handle))
    ,useExternalFormat(std::move(init.useExternalFormat))
    {}
// SharedTextureMemoryDmaBufPlane implementation

SharedTextureMemoryDmaBufPlane::operator const WGPUSharedTextureMemoryDmaBufPlane&() const noexcept {
    return *reinterpret_cast<const WGPUSharedTextureMemoryDmaBufPlane*>(this);
}

// SharedTextureMemoryDmaBufDescriptor implementation

SharedTextureMemoryDmaBufDescriptor::operator const WGPUSharedTextureMemoryDmaBufDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUSharedTextureMemoryDmaBufDescriptor*>(this);
}

SharedTextureMemoryDmaBufDescriptor::SharedTextureMemoryDmaBufDescriptor()
: ChainedStruct { nullptr, SType::SharedTextureMemoryDmaBufDescriptor } {}

struct SharedTextureMemoryDmaBufDescriptor::Init {
    ChainedStruct const * nextInChain = nullptr;
    Extent3D size = {};
    uint32_t drmFormat;
    uint64_t drmModifier;
    size_t planeCount;
    SharedTextureMemoryDmaBufPlane const * planes;
};
SharedTextureMemoryDmaBufDescriptor::SharedTextureMemoryDmaBufDescriptor(SharedTextureMemoryDmaBufDescriptor::Init&& init)
: ChainedStruct { init.nextInChain, SType::SharedTextureMemoryDmaBufDescriptor }
    ,size(std::move(init.size))
    ,drmFormat(std::move(init.drmFormat))
    ,drmModifier(std::move(init.drmModifier))
    ,planeCount(std::move(init.planeCount))
    ,planes(std::move(init.planes))
    {}
// SharedTextureMemoryOpaqueFDDescriptor implementation

SharedTextureMemoryOpaqueFDDescriptor::operator const WGPUSharedTextureMemoryOpaqueFDDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUSharedTextureMemoryOpaqueFDDescriptor*>(this);
}

SharedTextureMemoryOpaqueFDDescriptor::SharedTextureMemoryOpaqueFDDescriptor()
: ChainedStruct { nullptr, SType::SharedTextureMemoryOpaqueFDDescriptor } {}

struct SharedTextureMemoryOpaqueFDDescriptor::Init {
    ChainedStruct const * nextInChain = nullptr;
    void const * vkImageCreateInfo;
    int memoryFD;
    uint32_t memoryTypeIndex;
    uint64_t allocationSize;
    Bool dedicatedAllocation;
};
SharedTextureMemoryOpaqueFDDescriptor::SharedTextureMemoryOpaqueFDDescriptor(SharedTextureMemoryOpaqueFDDescriptor::Init&& init)
: ChainedStruct { init.nextInChain, SType::SharedTextureMemoryOpaqueFDDescriptor }
    ,vkImageCreateInfo(std::move(init.vkImageCreateInfo))
    ,memoryFD(std::move(init.memoryFD))
    ,memoryTypeIndex(std::move(init.memoryTypeIndex))
    ,allocationSize(std::move(init.allocationSize))
    ,dedicatedAllocation(std::move(init.dedicatedAllocation))
    {}
// SharedTextureMemoryZirconHandleDescriptor implementation

SharedTextureMemoryZirconHandleDescriptor::operator const WGPUSharedTextureMemoryZirconHandleDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUSharedTextureMemoryZirconHandleDescriptor*>(this);
}

SharedTextureMemoryZirconHandleDescriptor::SharedTextureMemoryZirconHandleDescriptor()
: ChainedStruct { nullptr, SType::SharedTextureMemoryZirconHandleDescriptor } {}

struct SharedTextureMemoryZirconHandleDescriptor::Init {
    ChainedStruct const * nextInChain = nullptr;
    uint32_t memoryFD;
    uint64_t allocationSize;
};
SharedTextureMemoryZirconHandleDescriptor::SharedTextureMemoryZirconHandleDescriptor(SharedTextureMemoryZirconHandleDescriptor::Init&& init)
: ChainedStruct { init.nextInChain, SType::SharedTextureMemoryZirconHandleDescriptor }
    ,memoryFD(std::move(init.memoryFD))
    ,allocationSize(std::move(init.allocationSize))
    {}
// SharedTextureMemoryDXGISharedHandleDescriptor implementation

SharedTextureMemoryDXGISharedHandleDescriptor::operator const WGPUSharedTextureMemoryDXGISharedHandleDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUSharedTextureMemoryDXGISharedHandleDescriptor*>(this);
}

SharedTextureMemoryDXGISharedHandleDescriptor::SharedTextureMemoryDXGISharedHandleDescriptor()
: ChainedStruct { nullptr, SType::SharedTextureMemoryDXGISharedHandleDescriptor } {}

struct SharedTextureMemoryDXGISharedHandleDescriptor::Init {
    ChainedStruct const * nextInChain = nullptr;
    void * handle;
    Bool useKeyedMutex;
};
SharedTextureMemoryDXGISharedHandleDescriptor::SharedTextureMemoryDXGISharedHandleDescriptor(SharedTextureMemoryDXGISharedHandleDescriptor::Init&& init)
: ChainedStruct { init.nextInChain, SType::SharedTextureMemoryDXGISharedHandleDescriptor }
    ,handle(std::move(init.handle))
    ,useKeyedMutex(std::move(init.useKeyedMutex))
    {}
// SharedTextureMemoryIOSurfaceDescriptor implementation

SharedTextureMemoryIOSurfaceDescriptor::operator const WGPUSharedTextureMemoryIOSurfaceDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUSharedTextureMemoryIOSurfaceDescriptor*>(this);
}

SharedTextureMemoryIOSurfaceDescriptor::SharedTextureMemoryIOSurfaceDescriptor()
: ChainedStruct { nullptr, SType::SharedTextureMemoryIOSurfaceDescriptor } {}

struct SharedTextureMemoryIOSurfaceDescriptor::Init {
    ChainedStruct const * nextInChain = nullptr;
    void * ioSurface;
};
SharedTextureMemoryIOSurfaceDescriptor::SharedTextureMemoryIOSurfaceDescriptor(SharedTextureMemoryIOSurfaceDescriptor::Init&& init)
: ChainedStruct { init.nextInChain, SType::SharedTextureMemoryIOSurfaceDescriptor }
    ,ioSurface(std::move(init.ioSurface))
    {}
// SharedTextureMemoryEGLImageDescriptor implementation

SharedTextureMemoryEGLImageDescriptor::operator const WGPUSharedTextureMemoryEGLImageDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUSharedTextureMemoryEGLImageDescriptor*>(this);
}

SharedTextureMemoryEGLImageDescriptor::SharedTextureMemoryEGLImageDescriptor()
: ChainedStruct { nullptr, SType::SharedTextureMemoryEGLImageDescriptor } {}

struct SharedTextureMemoryEGLImageDescriptor::Init {
    ChainedStruct const * nextInChain = nullptr;
    void * image;
};
SharedTextureMemoryEGLImageDescriptor::SharedTextureMemoryEGLImageDescriptor(SharedTextureMemoryEGLImageDescriptor::Init&& init)
: ChainedStruct { init.nextInChain, SType::SharedTextureMemoryEGLImageDescriptor }
    ,image(std::move(init.image))
    {}
// SharedTextureMemoryBeginAccessDescriptor implementation

SharedTextureMemoryBeginAccessDescriptor::operator const WGPUSharedTextureMemoryBeginAccessDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUSharedTextureMemoryBeginAccessDescriptor*>(this);
}

// SharedTextureMemoryEndAccessState implementation

SharedTextureMemoryEndAccessState::operator const WGPUSharedTextureMemoryEndAccessState&() const noexcept {
    return *reinterpret_cast<const WGPUSharedTextureMemoryEndAccessState*>(this);
}

SharedTextureMemoryEndAccessState::~SharedTextureMemoryEndAccessState() {
    FreeMembers();
}
void SharedTextureMemoryEndAccessState::FreeMembers() {
    // Free members here
}

SharedTextureMemoryEndAccessState::SharedTextureMemoryEndAccessState(SharedTextureMemoryEndAccessState&& rhs) :
    nextInChain(rhs.nextInChain),    
    initialized(rhs.initialized),    
    fenceCount(rhs.fenceCount),    
    fences(rhs.fences),    
    signaledValues(rhs.signaledValues)    
{}
SharedTextureMemoryEndAccessState& SharedTextureMemoryEndAccessState::operator=(SharedTextureMemoryEndAccessState&& rhs) {
if (&rhs == this) {
    return *this;
}
FreeMembers();

    ::wgpu::detail::AsNonConstReference(this->nextInChain) = std::move(rhs.nextInChain);    
    ::wgpu::detail::AsNonConstReference(this->initialized) = std::move(rhs.initialized);    
    ::wgpu::detail::AsNonConstReference(this->fenceCount) = std::move(rhs.fenceCount);    
    ::wgpu::detail::AsNonConstReference(this->fences) = std::move(rhs.fences);    
    ::wgpu::detail::AsNonConstReference(this->signaledValues) = std::move(rhs.signaledValues);    
    return *this;    
}
// SharedTextureMemoryVkImageLayoutBeginState implementation

SharedTextureMemoryVkImageLayoutBeginState::operator const WGPUSharedTextureMemoryVkImageLayoutBeginState&() const noexcept {
    return *reinterpret_cast<const WGPUSharedTextureMemoryVkImageLayoutBeginState*>(this);
}

SharedTextureMemoryVkImageLayoutBeginState::SharedTextureMemoryVkImageLayoutBeginState()
: ChainedStruct { nullptr, SType::SharedTextureMemoryVkImageLayoutBeginState } {}

struct SharedTextureMemoryVkImageLayoutBeginState::Init {
    ChainedStruct const * nextInChain = nullptr;
    int32_t oldLayout;
    int32_t newLayout;
};
SharedTextureMemoryVkImageLayoutBeginState::SharedTextureMemoryVkImageLayoutBeginState(SharedTextureMemoryVkImageLayoutBeginState::Init&& init)
: ChainedStruct { init.nextInChain, SType::SharedTextureMemoryVkImageLayoutBeginState }
    ,oldLayout(std::move(init.oldLayout))
    ,newLayout(std::move(init.newLayout))
    {}
// SharedTextureMemoryVkImageLayoutEndState implementation

SharedTextureMemoryVkImageLayoutEndState::operator const WGPUSharedTextureMemoryVkImageLayoutEndState&() const noexcept {
    return *reinterpret_cast<const WGPUSharedTextureMemoryVkImageLayoutEndState*>(this);
}

SharedTextureMemoryVkImageLayoutEndState::SharedTextureMemoryVkImageLayoutEndState()
: ChainedStructOut { nullptr, SType::SharedTextureMemoryVkImageLayoutEndState } {}

struct SharedTextureMemoryVkImageLayoutEndState::Init {
    ChainedStructOut * const nextInChain = nullptr;
    int32_t const oldLayout = {};
    int32_t const newLayout = {};
};
SharedTextureMemoryVkImageLayoutEndState::SharedTextureMemoryVkImageLayoutEndState(SharedTextureMemoryVkImageLayoutEndState::Init&& init)
: ChainedStructOut { init.nextInChain, SType::SharedTextureMemoryVkImageLayoutEndState }
    ,oldLayout(std::move(init.oldLayout))
    ,newLayout(std::move(init.newLayout))
    {}
SharedTextureMemoryVkImageLayoutEndState::~SharedTextureMemoryVkImageLayoutEndState() {
    FreeMembers();
}
void SharedTextureMemoryVkImageLayoutEndState::FreeMembers() {
    // Free members here
}

SharedTextureMemoryVkImageLayoutEndState::SharedTextureMemoryVkImageLayoutEndState(SharedTextureMemoryVkImageLayoutEndState&& rhs) :
    oldLayout(rhs.oldLayout),    
    newLayout(rhs.newLayout)    
{}
SharedTextureMemoryVkImageLayoutEndState& SharedTextureMemoryVkImageLayoutEndState::operator=(SharedTextureMemoryVkImageLayoutEndState&& rhs) {
if (&rhs == this) {
    return *this;
}
FreeMembers();

    ::wgpu::detail::AsNonConstReference(this->oldLayout) = std::move(rhs.oldLayout);    
    ::wgpu::detail::AsNonConstReference(this->newLayout) = std::move(rhs.newLayout);    
    return *this;    
}
// SharedTextureMemoryD3DSwapchainBeginState implementation

SharedTextureMemoryD3DSwapchainBeginState::operator const WGPUSharedTextureMemoryD3DSwapchainBeginState&() const noexcept {
    return *reinterpret_cast<const WGPUSharedTextureMemoryD3DSwapchainBeginState*>(this);
}

SharedTextureMemoryD3DSwapchainBeginState::SharedTextureMemoryD3DSwapchainBeginState()
: ChainedStruct { nullptr, SType::SharedTextureMemoryD3DSwapchainBeginState } {}

struct SharedTextureMemoryD3DSwapchainBeginState::Init {
    ChainedStruct const * nextInChain = nullptr;
    Bool isSwapchain = false;
};
SharedTextureMemoryD3DSwapchainBeginState::SharedTextureMemoryD3DSwapchainBeginState(SharedTextureMemoryD3DSwapchainBeginState::Init&& init)
: ChainedStruct { init.nextInChain, SType::SharedTextureMemoryD3DSwapchainBeginState }
    ,isSwapchain(std::move(init.isSwapchain))
    {}
// SharedFenceDescriptor implementation

SharedFenceDescriptor::operator const WGPUSharedFenceDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUSharedFenceDescriptor*>(this);
}

// SharedFenceVkSemaphoreOpaqueFDDescriptor implementation

SharedFenceVkSemaphoreOpaqueFDDescriptor::operator const WGPUSharedFenceVkSemaphoreOpaqueFDDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUSharedFenceVkSemaphoreOpaqueFDDescriptor*>(this);
}

SharedFenceVkSemaphoreOpaqueFDDescriptor::SharedFenceVkSemaphoreOpaqueFDDescriptor()
: ChainedStruct { nullptr, SType::SharedFenceVkSemaphoreOpaqueFDDescriptor } {}

struct SharedFenceVkSemaphoreOpaqueFDDescriptor::Init {
    ChainedStruct const * nextInChain = nullptr;
    int handle;
};
SharedFenceVkSemaphoreOpaqueFDDescriptor::SharedFenceVkSemaphoreOpaqueFDDescriptor(SharedFenceVkSemaphoreOpaqueFDDescriptor::Init&& init)
: ChainedStruct { init.nextInChain, SType::SharedFenceVkSemaphoreOpaqueFDDescriptor }
    ,handle(std::move(init.handle))
    {}
// SharedFenceVkSemaphoreSyncFDDescriptor implementation

SharedFenceVkSemaphoreSyncFDDescriptor::operator const WGPUSharedFenceVkSemaphoreSyncFDDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUSharedFenceVkSemaphoreSyncFDDescriptor*>(this);
}

SharedFenceVkSemaphoreSyncFDDescriptor::SharedFenceVkSemaphoreSyncFDDescriptor()
: ChainedStruct { nullptr, SType::SharedFenceVkSemaphoreSyncFDDescriptor } {}

struct SharedFenceVkSemaphoreSyncFDDescriptor::Init {
    ChainedStruct const * nextInChain = nullptr;
    int handle;
};
SharedFenceVkSemaphoreSyncFDDescriptor::SharedFenceVkSemaphoreSyncFDDescriptor(SharedFenceVkSemaphoreSyncFDDescriptor::Init&& init)
: ChainedStruct { init.nextInChain, SType::SharedFenceVkSemaphoreSyncFDDescriptor }
    ,handle(std::move(init.handle))
    {}
// SharedFenceVkSemaphoreZirconHandleDescriptor implementation

SharedFenceVkSemaphoreZirconHandleDescriptor::operator const WGPUSharedFenceVkSemaphoreZirconHandleDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUSharedFenceVkSemaphoreZirconHandleDescriptor*>(this);
}

SharedFenceVkSemaphoreZirconHandleDescriptor::SharedFenceVkSemaphoreZirconHandleDescriptor()
: ChainedStruct { nullptr, SType::SharedFenceVkSemaphoreZirconHandleDescriptor } {}

struct SharedFenceVkSemaphoreZirconHandleDescriptor::Init {
    ChainedStruct const * nextInChain = nullptr;
    uint32_t handle;
};
SharedFenceVkSemaphoreZirconHandleDescriptor::SharedFenceVkSemaphoreZirconHandleDescriptor(SharedFenceVkSemaphoreZirconHandleDescriptor::Init&& init)
: ChainedStruct { init.nextInChain, SType::SharedFenceVkSemaphoreZirconHandleDescriptor }
    ,handle(std::move(init.handle))
    {}
// SharedFenceDXGISharedHandleDescriptor implementation

SharedFenceDXGISharedHandleDescriptor::operator const WGPUSharedFenceDXGISharedHandleDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUSharedFenceDXGISharedHandleDescriptor*>(this);
}

SharedFenceDXGISharedHandleDescriptor::SharedFenceDXGISharedHandleDescriptor()
: ChainedStruct { nullptr, SType::SharedFenceDXGISharedHandleDescriptor } {}

struct SharedFenceDXGISharedHandleDescriptor::Init {
    ChainedStruct const * nextInChain = nullptr;
    void * handle;
};
SharedFenceDXGISharedHandleDescriptor::SharedFenceDXGISharedHandleDescriptor(SharedFenceDXGISharedHandleDescriptor::Init&& init)
: ChainedStruct { init.nextInChain, SType::SharedFenceDXGISharedHandleDescriptor }
    ,handle(std::move(init.handle))
    {}
// SharedFenceMTLSharedEventDescriptor implementation

SharedFenceMTLSharedEventDescriptor::operator const WGPUSharedFenceMTLSharedEventDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUSharedFenceMTLSharedEventDescriptor*>(this);
}

SharedFenceMTLSharedEventDescriptor::SharedFenceMTLSharedEventDescriptor()
: ChainedStruct { nullptr, SType::SharedFenceMTLSharedEventDescriptor } {}

struct SharedFenceMTLSharedEventDescriptor::Init {
    ChainedStruct const * nextInChain = nullptr;
    void * sharedEvent;
};
SharedFenceMTLSharedEventDescriptor::SharedFenceMTLSharedEventDescriptor(SharedFenceMTLSharedEventDescriptor::Init&& init)
: ChainedStruct { init.nextInChain, SType::SharedFenceMTLSharedEventDescriptor }
    ,sharedEvent(std::move(init.sharedEvent))
    {}
// SharedFenceExportInfo implementation

SharedFenceExportInfo::operator const WGPUSharedFenceExportInfo&() const noexcept {
    return *reinterpret_cast<const WGPUSharedFenceExportInfo*>(this);
}

SharedFenceExportInfo::~SharedFenceExportInfo() {
    FreeMembers();
}
void SharedFenceExportInfo::FreeMembers() {
    // Free members here
}

SharedFenceExportInfo::SharedFenceExportInfo(SharedFenceExportInfo&& rhs) :
    nextInChain(rhs.nextInChain),    
    type(rhs.type)    
{}
SharedFenceExportInfo& SharedFenceExportInfo::operator=(SharedFenceExportInfo&& rhs) {
if (&rhs == this) {
    return *this;
}
FreeMembers();

    ::wgpu::detail::AsNonConstReference(this->nextInChain) = std::move(rhs.nextInChain);    
    ::wgpu::detail::AsNonConstReference(this->type) = std::move(rhs.type);    
    return *this;    
}
// SharedFenceVkSemaphoreOpaqueFDExportInfo implementation

SharedFenceVkSemaphoreOpaqueFDExportInfo::operator const WGPUSharedFenceVkSemaphoreOpaqueFDExportInfo&() const noexcept {
    return *reinterpret_cast<const WGPUSharedFenceVkSemaphoreOpaqueFDExportInfo*>(this);
}

SharedFenceVkSemaphoreOpaqueFDExportInfo::SharedFenceVkSemaphoreOpaqueFDExportInfo()
: ChainedStructOut { nullptr, SType::SharedFenceVkSemaphoreOpaqueFDExportInfo } {}

struct SharedFenceVkSemaphoreOpaqueFDExportInfo::Init {
    ChainedStructOut * const nextInChain = nullptr;
    int const handle = {};
};
SharedFenceVkSemaphoreOpaqueFDExportInfo::SharedFenceVkSemaphoreOpaqueFDExportInfo(SharedFenceVkSemaphoreOpaqueFDExportInfo::Init&& init)
: ChainedStructOut { init.nextInChain, SType::SharedFenceVkSemaphoreOpaqueFDExportInfo }
    ,handle(std::move(init.handle))
    {}
SharedFenceVkSemaphoreOpaqueFDExportInfo::~SharedFenceVkSemaphoreOpaqueFDExportInfo() {
    FreeMembers();
}
void SharedFenceVkSemaphoreOpaqueFDExportInfo::FreeMembers() {
    // Free members here
}

SharedFenceVkSemaphoreOpaqueFDExportInfo::SharedFenceVkSemaphoreOpaqueFDExportInfo(SharedFenceVkSemaphoreOpaqueFDExportInfo&& rhs) :
    handle(rhs.handle)    
{}
SharedFenceVkSemaphoreOpaqueFDExportInfo& SharedFenceVkSemaphoreOpaqueFDExportInfo::operator=(SharedFenceVkSemaphoreOpaqueFDExportInfo&& rhs) {
if (&rhs == this) {
    return *this;
}
FreeMembers();

    ::wgpu::detail::AsNonConstReference(this->handle) = std::move(rhs.handle);    
    return *this;    
}
// SharedFenceVkSemaphoreSyncFDExportInfo implementation

SharedFenceVkSemaphoreSyncFDExportInfo::operator const WGPUSharedFenceVkSemaphoreSyncFDExportInfo&() const noexcept {
    return *reinterpret_cast<const WGPUSharedFenceVkSemaphoreSyncFDExportInfo*>(this);
}

SharedFenceVkSemaphoreSyncFDExportInfo::SharedFenceVkSemaphoreSyncFDExportInfo()
: ChainedStructOut { nullptr, SType::SharedFenceVkSemaphoreSyncFDExportInfo } {}

struct SharedFenceVkSemaphoreSyncFDExportInfo::Init {
    ChainedStructOut * const nextInChain = nullptr;
    int const handle = {};
};
SharedFenceVkSemaphoreSyncFDExportInfo::SharedFenceVkSemaphoreSyncFDExportInfo(SharedFenceVkSemaphoreSyncFDExportInfo::Init&& init)
: ChainedStructOut { init.nextInChain, SType::SharedFenceVkSemaphoreSyncFDExportInfo }
    ,handle(std::move(init.handle))
    {}
SharedFenceVkSemaphoreSyncFDExportInfo::~SharedFenceVkSemaphoreSyncFDExportInfo() {
    FreeMembers();
}
void SharedFenceVkSemaphoreSyncFDExportInfo::FreeMembers() {
    // Free members here
}

SharedFenceVkSemaphoreSyncFDExportInfo::SharedFenceVkSemaphoreSyncFDExportInfo(SharedFenceVkSemaphoreSyncFDExportInfo&& rhs) :
    handle(rhs.handle)    
{}
SharedFenceVkSemaphoreSyncFDExportInfo& SharedFenceVkSemaphoreSyncFDExportInfo::operator=(SharedFenceVkSemaphoreSyncFDExportInfo&& rhs) {
if (&rhs == this) {
    return *this;
}
FreeMembers();

    ::wgpu::detail::AsNonConstReference(this->handle) = std::move(rhs.handle);    
    return *this;    
}
// SharedFenceVkSemaphoreZirconHandleExportInfo implementation

SharedFenceVkSemaphoreZirconHandleExportInfo::operator const WGPUSharedFenceVkSemaphoreZirconHandleExportInfo&() const noexcept {
    return *reinterpret_cast<const WGPUSharedFenceVkSemaphoreZirconHandleExportInfo*>(this);
}

SharedFenceVkSemaphoreZirconHandleExportInfo::SharedFenceVkSemaphoreZirconHandleExportInfo()
: ChainedStructOut { nullptr, SType::SharedFenceVkSemaphoreZirconHandleExportInfo } {}

struct SharedFenceVkSemaphoreZirconHandleExportInfo::Init {
    ChainedStructOut * const nextInChain = nullptr;
    uint32_t const handle = {};
};
SharedFenceVkSemaphoreZirconHandleExportInfo::SharedFenceVkSemaphoreZirconHandleExportInfo(SharedFenceVkSemaphoreZirconHandleExportInfo::Init&& init)
: ChainedStructOut { init.nextInChain, SType::SharedFenceVkSemaphoreZirconHandleExportInfo }
    ,handle(std::move(init.handle))
    {}
SharedFenceVkSemaphoreZirconHandleExportInfo::~SharedFenceVkSemaphoreZirconHandleExportInfo() {
    FreeMembers();
}
void SharedFenceVkSemaphoreZirconHandleExportInfo::FreeMembers() {
    // Free members here
}

SharedFenceVkSemaphoreZirconHandleExportInfo::SharedFenceVkSemaphoreZirconHandleExportInfo(SharedFenceVkSemaphoreZirconHandleExportInfo&& rhs) :
    handle(rhs.handle)    
{}
SharedFenceVkSemaphoreZirconHandleExportInfo& SharedFenceVkSemaphoreZirconHandleExportInfo::operator=(SharedFenceVkSemaphoreZirconHandleExportInfo&& rhs) {
if (&rhs == this) {
    return *this;
}
FreeMembers();

    ::wgpu::detail::AsNonConstReference(this->handle) = std::move(rhs.handle);    
    return *this;    
}
// SharedFenceDXGISharedHandleExportInfo implementation

SharedFenceDXGISharedHandleExportInfo::operator const WGPUSharedFenceDXGISharedHandleExportInfo&() const noexcept {
    return *reinterpret_cast<const WGPUSharedFenceDXGISharedHandleExportInfo*>(this);
}

SharedFenceDXGISharedHandleExportInfo::SharedFenceDXGISharedHandleExportInfo()
: ChainedStructOut { nullptr, SType::SharedFenceDXGISharedHandleExportInfo } {}

struct SharedFenceDXGISharedHandleExportInfo::Init {
    ChainedStructOut * const nextInChain = nullptr;
    void * const handle = {};
};
SharedFenceDXGISharedHandleExportInfo::SharedFenceDXGISharedHandleExportInfo(SharedFenceDXGISharedHandleExportInfo::Init&& init)
: ChainedStructOut { init.nextInChain, SType::SharedFenceDXGISharedHandleExportInfo }
    ,handle(std::move(init.handle))
    {}
SharedFenceDXGISharedHandleExportInfo::~SharedFenceDXGISharedHandleExportInfo() {
    FreeMembers();
}
void SharedFenceDXGISharedHandleExportInfo::FreeMembers() {
    // Free members here
}

SharedFenceDXGISharedHandleExportInfo::SharedFenceDXGISharedHandleExportInfo(SharedFenceDXGISharedHandleExportInfo&& rhs) :
    handle(rhs.handle)    
{}
SharedFenceDXGISharedHandleExportInfo& SharedFenceDXGISharedHandleExportInfo::operator=(SharedFenceDXGISharedHandleExportInfo&& rhs) {
if (&rhs == this) {
    return *this;
}
FreeMembers();

    ::wgpu::detail::AsNonConstReference(this->handle) = std::move(rhs.handle);    
    return *this;    
}
// SharedFenceMTLSharedEventExportInfo implementation

SharedFenceMTLSharedEventExportInfo::operator const WGPUSharedFenceMTLSharedEventExportInfo&() const noexcept {
    return *reinterpret_cast<const WGPUSharedFenceMTLSharedEventExportInfo*>(this);
}

SharedFenceMTLSharedEventExportInfo::SharedFenceMTLSharedEventExportInfo()
: ChainedStructOut { nullptr, SType::SharedFenceMTLSharedEventExportInfo } {}

struct SharedFenceMTLSharedEventExportInfo::Init {
    ChainedStructOut * const nextInChain = nullptr;
    void * const sharedEvent = {};
};
SharedFenceMTLSharedEventExportInfo::SharedFenceMTLSharedEventExportInfo(SharedFenceMTLSharedEventExportInfo::Init&& init)
: ChainedStructOut { init.nextInChain, SType::SharedFenceMTLSharedEventExportInfo }
    ,sharedEvent(std::move(init.sharedEvent))
    {}
SharedFenceMTLSharedEventExportInfo::~SharedFenceMTLSharedEventExportInfo() {
    FreeMembers();
}
void SharedFenceMTLSharedEventExportInfo::FreeMembers() {
    // Free members here
}

SharedFenceMTLSharedEventExportInfo::SharedFenceMTLSharedEventExportInfo(SharedFenceMTLSharedEventExportInfo&& rhs) :
    sharedEvent(rhs.sharedEvent)    
{}
SharedFenceMTLSharedEventExportInfo& SharedFenceMTLSharedEventExportInfo::operator=(SharedFenceMTLSharedEventExportInfo&& rhs) {
if (&rhs == this) {
    return *this;
}
FreeMembers();

    ::wgpu::detail::AsNonConstReference(this->sharedEvent) = std::move(rhs.sharedEvent);    
    return *this;    
}
// FormatCapabilities implementation

FormatCapabilities::operator const WGPUFormatCapabilities&() const noexcept {
    return *reinterpret_cast<const WGPUFormatCapabilities*>(this);
}

FormatCapabilities::~FormatCapabilities() {
    FreeMembers();
}
void FormatCapabilities::FreeMembers() {
    // Free members here
}

FormatCapabilities::FormatCapabilities(FormatCapabilities&& rhs) :
    nextInChain(rhs.nextInChain)    
{}
FormatCapabilities& FormatCapabilities::operator=(FormatCapabilities&& rhs) {
if (&rhs == this) {
    return *this;
}
FreeMembers();

    ::wgpu::detail::AsNonConstReference(this->nextInChain) = std::move(rhs.nextInChain);    
    return *this;    
}
// DrmFormatCapabilities implementation

DrmFormatCapabilities::operator const WGPUDrmFormatCapabilities&() const noexcept {
    return *reinterpret_cast<const WGPUDrmFormatCapabilities*>(this);
}

DrmFormatCapabilities::DrmFormatCapabilities()
: ChainedStructOut { nullptr, SType::DrmFormatCapabilities } {}

struct DrmFormatCapabilities::Init {
    ChainedStructOut * const nextInChain = nullptr;
    size_t const propertiesCount = {};
    DrmFormatProperties const * const properties = {};
};
DrmFormatCapabilities::DrmFormatCapabilities(DrmFormatCapabilities::Init&& init)
: ChainedStructOut { init.nextInChain, SType::DrmFormatCapabilities }
    ,propertiesCount(std::move(init.propertiesCount))
    ,properties(std::move(init.properties))
    {}
DrmFormatCapabilities::~DrmFormatCapabilities() {
    FreeMembers();
}
void DrmFormatCapabilities::FreeMembers() {
    // Free members here
}

DrmFormatCapabilities::DrmFormatCapabilities(DrmFormatCapabilities&& rhs) :
    propertiesCount(rhs.propertiesCount),    
    properties(rhs.properties)    
{}
DrmFormatCapabilities& DrmFormatCapabilities::operator=(DrmFormatCapabilities&& rhs) {
if (&rhs == this) {
    return *this;
}
FreeMembers();

    ::wgpu::detail::AsNonConstReference(this->propertiesCount) = std::move(rhs.propertiesCount);    
    ::wgpu::detail::AsNonConstReference(this->properties) = std::move(rhs.properties);    
    return *this;    
}
// DrmFormatProperties implementation

DrmFormatProperties::operator const WGPUDrmFormatProperties&() const noexcept {
    return *reinterpret_cast<const WGPUDrmFormatProperties*>(this);
}

// ImageCopyBuffer implementation

ImageCopyBuffer::operator const WGPUImageCopyBuffer&() const noexcept {
    return *reinterpret_cast<const WGPUImageCopyBuffer*>(this);
}

// ImageCopyTexture implementation

ImageCopyTexture::operator const WGPUImageCopyTexture&() const noexcept {
    return *reinterpret_cast<const WGPUImageCopyTexture*>(this);
}

// ImageCopyExternalTexture implementation

ImageCopyExternalTexture::operator const WGPUImageCopyExternalTexture&() const noexcept {
    return *reinterpret_cast<const WGPUImageCopyExternalTexture*>(this);
}

// Future implementation

Future::operator const WGPUFuture&() const noexcept {
    return *reinterpret_cast<const WGPUFuture*>(this);
}

// FutureWaitInfo implementation

FutureWaitInfo::operator const WGPUFutureWaitInfo&() const noexcept {
    return *reinterpret_cast<const WGPUFutureWaitInfo*>(this);
}

// InstanceFeatures implementation

InstanceFeatures::operator const WGPUInstanceFeatures&() const noexcept {
    return *reinterpret_cast<const WGPUInstanceFeatures*>(this);
}

// InstanceDescriptor implementation

InstanceDescriptor::operator const WGPUInstanceDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUInstanceDescriptor*>(this);
}

// DawnWireWGSLControl implementation

DawnWireWGSLControl::operator const WGPUDawnWireWGSLControl&() const noexcept {
    return *reinterpret_cast<const WGPUDawnWireWGSLControl*>(this);
}

DawnWireWGSLControl::DawnWireWGSLControl()
: ChainedStruct { nullptr, SType::DawnWireWGSLControl } {}

struct DawnWireWGSLControl::Init {
    ChainedStruct const * nextInChain = nullptr;
    Bool enableExperimental = false;
    Bool enableUnsafe = false;
    Bool enableTesting = false;
};
DawnWireWGSLControl::DawnWireWGSLControl(DawnWireWGSLControl::Init&& init)
: ChainedStruct { init.nextInChain, SType::DawnWireWGSLControl }
    ,enableExperimental(std::move(init.enableExperimental))
    ,enableUnsafe(std::move(init.enableUnsafe))
    ,enableTesting(std::move(init.enableTesting))
    {}
// VertexAttribute implementation

VertexAttribute::operator const WGPUVertexAttribute&() const noexcept {
    return *reinterpret_cast<const WGPUVertexAttribute*>(this);
}

// VertexBufferLayout implementation

VertexBufferLayout::operator const WGPUVertexBufferLayout&() const noexcept {
    return *reinterpret_cast<const WGPUVertexBufferLayout*>(this);
}

// Origin3D implementation

Origin3D::operator const WGPUOrigin3D&() const noexcept {
    return *reinterpret_cast<const WGPUOrigin3D*>(this);
}

// Origin2D implementation

Origin2D::operator const WGPUOrigin2D&() const noexcept {
    return *reinterpret_cast<const WGPUOrigin2D*>(this);
}

// PipelineLayoutDescriptor implementation

PipelineLayoutDescriptor::operator const WGPUPipelineLayoutDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUPipelineLayoutDescriptor*>(this);
}

// PipelineLayoutPixelLocalStorage implementation

PipelineLayoutPixelLocalStorage::operator const WGPUPipelineLayoutPixelLocalStorage&() const noexcept {
    return *reinterpret_cast<const WGPUPipelineLayoutPixelLocalStorage*>(this);
}

PipelineLayoutPixelLocalStorage::PipelineLayoutPixelLocalStorage()
: ChainedStruct { nullptr, SType::PipelineLayoutPixelLocalStorage } {}

struct PipelineLayoutPixelLocalStorage::Init {
    ChainedStruct const * nextInChain = nullptr;
    uint64_t totalPixelLocalStorageSize;
    size_t storageAttachmentCount = 0;
    PipelineLayoutStorageAttachment const * storageAttachments;
};
PipelineLayoutPixelLocalStorage::PipelineLayoutPixelLocalStorage(PipelineLayoutPixelLocalStorage::Init&& init)
: ChainedStruct { init.nextInChain, SType::PipelineLayoutPixelLocalStorage }
    ,totalPixelLocalStorageSize(std::move(init.totalPixelLocalStorageSize))
    ,storageAttachmentCount(std::move(init.storageAttachmentCount))
    ,storageAttachments(std::move(init.storageAttachments))
    {}
// PipelineLayoutStorageAttachment implementation

PipelineLayoutStorageAttachment::operator const WGPUPipelineLayoutStorageAttachment&() const noexcept {
    return *reinterpret_cast<const WGPUPipelineLayoutStorageAttachment*>(this);
}

// ProgrammableStageDescriptor implementation

ProgrammableStageDescriptor::operator const WGPUProgrammableStageDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUProgrammableStageDescriptor*>(this);
}

// QuerySetDescriptor implementation

QuerySetDescriptor::operator const WGPUQuerySetDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUQuerySetDescriptor*>(this);
}

// QueueDescriptor implementation

QueueDescriptor::operator const WGPUQueueDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUQueueDescriptor*>(this);
}

// QueueWorkDoneCallbackInfo implementation

QueueWorkDoneCallbackInfo::operator const WGPUQueueWorkDoneCallbackInfo&() const noexcept {
    return *reinterpret_cast<const WGPUQueueWorkDoneCallbackInfo*>(this);
}

// QueueWorkDoneCallbackInfo2 implementation

QueueWorkDoneCallbackInfo2::operator const WGPUQueueWorkDoneCallbackInfo2&() const noexcept {
    return *reinterpret_cast<const WGPUQueueWorkDoneCallbackInfo2*>(this);
}

// RenderBundleDescriptor implementation

RenderBundleDescriptor::operator const WGPURenderBundleDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPURenderBundleDescriptor*>(this);
}

// RenderBundleEncoderDescriptor implementation

RenderBundleEncoderDescriptor::operator const WGPURenderBundleEncoderDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPURenderBundleEncoderDescriptor*>(this);
}

// RenderPassColorAttachment implementation

RenderPassColorAttachment::operator const WGPURenderPassColorAttachment&() const noexcept {
    return *reinterpret_cast<const WGPURenderPassColorAttachment*>(this);
}

// DawnRenderPassColorAttachmentRenderToSingleSampled implementation

DawnRenderPassColorAttachmentRenderToSingleSampled::operator const WGPUDawnRenderPassColorAttachmentRenderToSingleSampled&() const noexcept {
    return *reinterpret_cast<const WGPUDawnRenderPassColorAttachmentRenderToSingleSampled*>(this);
}

DawnRenderPassColorAttachmentRenderToSingleSampled::DawnRenderPassColorAttachmentRenderToSingleSampled()
: ChainedStruct { nullptr, SType::DawnRenderPassColorAttachmentRenderToSingleSampled } {}

struct DawnRenderPassColorAttachmentRenderToSingleSampled::Init {
    ChainedStruct const * nextInChain = nullptr;
    uint32_t implicitSampleCount = 1;
};
DawnRenderPassColorAttachmentRenderToSingleSampled::DawnRenderPassColorAttachmentRenderToSingleSampled(DawnRenderPassColorAttachmentRenderToSingleSampled::Init&& init)
: ChainedStruct { init.nextInChain, SType::DawnRenderPassColorAttachmentRenderToSingleSampled }
    ,implicitSampleCount(std::move(init.implicitSampleCount))
    {}
// RenderPassDepthStencilAttachment implementation

RenderPassDepthStencilAttachment::operator const WGPURenderPassDepthStencilAttachment&() const noexcept {
    return *reinterpret_cast<const WGPURenderPassDepthStencilAttachment*>(this);
}

// RenderPassDescriptor implementation

RenderPassDescriptor::operator const WGPURenderPassDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPURenderPassDescriptor*>(this);
}

// RenderPassDescriptorMaxDrawCount implementation

RenderPassDescriptorMaxDrawCount::operator const WGPURenderPassDescriptorMaxDrawCount&() const noexcept {
    return *reinterpret_cast<const WGPURenderPassDescriptorMaxDrawCount*>(this);
}

RenderPassDescriptorMaxDrawCount::RenderPassDescriptorMaxDrawCount()
: ChainedStruct { nullptr, SType::RenderPassDescriptorMaxDrawCount } {}

struct RenderPassDescriptorMaxDrawCount::Init {
    ChainedStruct const * nextInChain = nullptr;
    uint64_t maxDrawCount = 50000000;
};
RenderPassDescriptorMaxDrawCount::RenderPassDescriptorMaxDrawCount(RenderPassDescriptorMaxDrawCount::Init&& init)
: ChainedStruct { init.nextInChain, SType::RenderPassDescriptorMaxDrawCount }
    ,maxDrawCount(std::move(init.maxDrawCount))
    {}
// RenderPassPixelLocalStorage implementation

RenderPassPixelLocalStorage::operator const WGPURenderPassPixelLocalStorage&() const noexcept {
    return *reinterpret_cast<const WGPURenderPassPixelLocalStorage*>(this);
}

RenderPassPixelLocalStorage::RenderPassPixelLocalStorage()
: ChainedStruct { nullptr, SType::RenderPassPixelLocalStorage } {}

struct RenderPassPixelLocalStorage::Init {
    ChainedStruct const * nextInChain = nullptr;
    uint64_t totalPixelLocalStorageSize;
    size_t storageAttachmentCount = 0;
    RenderPassStorageAttachment const * storageAttachments;
};
RenderPassPixelLocalStorage::RenderPassPixelLocalStorage(RenderPassPixelLocalStorage::Init&& init)
: ChainedStruct { init.nextInChain, SType::RenderPassPixelLocalStorage }
    ,totalPixelLocalStorageSize(std::move(init.totalPixelLocalStorageSize))
    ,storageAttachmentCount(std::move(init.storageAttachmentCount))
    ,storageAttachments(std::move(init.storageAttachments))
    {}
// RenderPassStorageAttachment implementation

RenderPassStorageAttachment::operator const WGPURenderPassStorageAttachment&() const noexcept {
    return *reinterpret_cast<const WGPURenderPassStorageAttachment*>(this);
}

// RenderPassTimestampWrites implementation

RenderPassTimestampWrites::operator const WGPURenderPassTimestampWrites&() const noexcept {
    return *reinterpret_cast<const WGPURenderPassTimestampWrites*>(this);
}

// RequestDeviceCallbackInfo implementation

RequestDeviceCallbackInfo::operator const WGPURequestDeviceCallbackInfo&() const noexcept {
    return *reinterpret_cast<const WGPURequestDeviceCallbackInfo*>(this);
}

// RequestDeviceCallbackInfo2 implementation

RequestDeviceCallbackInfo2::operator const WGPURequestDeviceCallbackInfo2&() const noexcept {
    return *reinterpret_cast<const WGPURequestDeviceCallbackInfo2*>(this);
}

// VertexState implementation

VertexState::operator const WGPUVertexState&() const noexcept {
    return *reinterpret_cast<const WGPUVertexState*>(this);
}

// PrimitiveState implementation

PrimitiveState::operator const WGPUPrimitiveState&() const noexcept {
    return *reinterpret_cast<const WGPUPrimitiveState*>(this);
}

// PrimitiveDepthClipControl implementation

PrimitiveDepthClipControl::operator const WGPUPrimitiveDepthClipControl&() const noexcept {
    return *reinterpret_cast<const WGPUPrimitiveDepthClipControl*>(this);
}

PrimitiveDepthClipControl::PrimitiveDepthClipControl()
: ChainedStruct { nullptr, SType::PrimitiveDepthClipControl } {}

struct PrimitiveDepthClipControl::Init {
    ChainedStruct const * nextInChain = nullptr;
    Bool unclippedDepth = false;
};
PrimitiveDepthClipControl::PrimitiveDepthClipControl(PrimitiveDepthClipControl::Init&& init)
: ChainedStruct { init.nextInChain, SType::PrimitiveDepthClipControl }
    ,unclippedDepth(std::move(init.unclippedDepth))
    {}
// DepthStencilState implementation

DepthStencilState::operator const WGPUDepthStencilState&() const noexcept {
    return *reinterpret_cast<const WGPUDepthStencilState*>(this);
}

// DepthStencilStateDepthWriteDefinedDawn implementation

DepthStencilStateDepthWriteDefinedDawn::operator const WGPUDepthStencilStateDepthWriteDefinedDawn&() const noexcept {
    return *reinterpret_cast<const WGPUDepthStencilStateDepthWriteDefinedDawn*>(this);
}

DepthStencilStateDepthWriteDefinedDawn::DepthStencilStateDepthWriteDefinedDawn()
: ChainedStruct { nullptr, SType::DepthStencilStateDepthWriteDefinedDawn } {}

struct DepthStencilStateDepthWriteDefinedDawn::Init {
    ChainedStruct const * nextInChain = nullptr;
    Bool depthWriteDefined;
};
DepthStencilStateDepthWriteDefinedDawn::DepthStencilStateDepthWriteDefinedDawn(DepthStencilStateDepthWriteDefinedDawn::Init&& init)
: ChainedStruct { init.nextInChain, SType::DepthStencilStateDepthWriteDefinedDawn }
    ,depthWriteDefined(std::move(init.depthWriteDefined))
    {}
// MultisampleState implementation

MultisampleState::operator const WGPUMultisampleState&() const noexcept {
    return *reinterpret_cast<const WGPUMultisampleState*>(this);
}

// FragmentState implementation

FragmentState::operator const WGPUFragmentState&() const noexcept {
    return *reinterpret_cast<const WGPUFragmentState*>(this);
}

// ColorTargetState implementation

ColorTargetState::operator const WGPUColorTargetState&() const noexcept {
    return *reinterpret_cast<const WGPUColorTargetState*>(this);
}

// ColorTargetStateExpandResolveTextureDawn implementation

ColorTargetStateExpandResolveTextureDawn::operator const WGPUColorTargetStateExpandResolveTextureDawn&() const noexcept {
    return *reinterpret_cast<const WGPUColorTargetStateExpandResolveTextureDawn*>(this);
}

ColorTargetStateExpandResolveTextureDawn::ColorTargetStateExpandResolveTextureDawn()
: ChainedStruct { nullptr, SType::ColorTargetStateExpandResolveTextureDawn } {}

struct ColorTargetStateExpandResolveTextureDawn::Init {
    ChainedStruct const * nextInChain = nullptr;
    Bool enabled = false;
};
ColorTargetStateExpandResolveTextureDawn::ColorTargetStateExpandResolveTextureDawn(ColorTargetStateExpandResolveTextureDawn::Init&& init)
: ChainedStruct { init.nextInChain, SType::ColorTargetStateExpandResolveTextureDawn }
    ,enabled(std::move(init.enabled))
    {}
// BlendState implementation

BlendState::operator const WGPUBlendState&() const noexcept {
    return *reinterpret_cast<const WGPUBlendState*>(this);
}

// RenderPipelineDescriptor implementation

RenderPipelineDescriptor::operator const WGPURenderPipelineDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPURenderPipelineDescriptor*>(this);
}

// SamplerDescriptor implementation

SamplerDescriptor::operator const WGPUSamplerDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUSamplerDescriptor*>(this);
}

// ShaderModuleDescriptor implementation

ShaderModuleDescriptor::operator const WGPUShaderModuleDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUShaderModuleDescriptor*>(this);
}

// ShaderModuleSPIRVDescriptor implementation

ShaderModuleSPIRVDescriptor::operator const WGPUShaderModuleSPIRVDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUShaderModuleSPIRVDescriptor*>(this);
}

ShaderModuleSPIRVDescriptor::ShaderModuleSPIRVDescriptor()
: ChainedStruct { nullptr, SType::ShaderModuleSPIRVDescriptor } {}

struct ShaderModuleSPIRVDescriptor::Init {
    ChainedStruct const * nextInChain = nullptr;
    uint32_t codeSize;
    uint32_t const * code;
};
ShaderModuleSPIRVDescriptor::ShaderModuleSPIRVDescriptor(ShaderModuleSPIRVDescriptor::Init&& init)
: ChainedStruct { init.nextInChain, SType::ShaderModuleSPIRVDescriptor }
    ,codeSize(std::move(init.codeSize))
    ,code(std::move(init.code))
    {}
// ShaderModuleWGSLDescriptor implementation

ShaderModuleWGSLDescriptor::operator const WGPUShaderModuleWGSLDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUShaderModuleWGSLDescriptor*>(this);
}

ShaderModuleWGSLDescriptor::ShaderModuleWGSLDescriptor()
: ChainedStruct { nullptr, SType::ShaderModuleWGSLDescriptor } {}

struct ShaderModuleWGSLDescriptor::Init {
    ChainedStruct const * nextInChain = nullptr;
    char const * code;
};
ShaderModuleWGSLDescriptor::ShaderModuleWGSLDescriptor(ShaderModuleWGSLDescriptor::Init&& init)
: ChainedStruct { init.nextInChain, SType::ShaderModuleWGSLDescriptor }
    ,code(std::move(init.code))
    {}
// DawnShaderModuleSPIRVOptionsDescriptor implementation

DawnShaderModuleSPIRVOptionsDescriptor::operator const WGPUDawnShaderModuleSPIRVOptionsDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUDawnShaderModuleSPIRVOptionsDescriptor*>(this);
}

DawnShaderModuleSPIRVOptionsDescriptor::DawnShaderModuleSPIRVOptionsDescriptor()
: ChainedStruct { nullptr, SType::DawnShaderModuleSPIRVOptionsDescriptor } {}

struct DawnShaderModuleSPIRVOptionsDescriptor::Init {
    ChainedStruct const * nextInChain = nullptr;
    Bool allowNonUniformDerivatives = false;
};
DawnShaderModuleSPIRVOptionsDescriptor::DawnShaderModuleSPIRVOptionsDescriptor(DawnShaderModuleSPIRVOptionsDescriptor::Init&& init)
: ChainedStruct { init.nextInChain, SType::DawnShaderModuleSPIRVOptionsDescriptor }
    ,allowNonUniformDerivatives(std::move(init.allowNonUniformDerivatives))
    {}
// ShaderModuleCompilationOptions implementation

ShaderModuleCompilationOptions::operator const WGPUShaderModuleCompilationOptions&() const noexcept {
    return *reinterpret_cast<const WGPUShaderModuleCompilationOptions*>(this);
}

ShaderModuleCompilationOptions::ShaderModuleCompilationOptions()
: ChainedStruct { nullptr, SType::ShaderModuleCompilationOptions } {}

struct ShaderModuleCompilationOptions::Init {
    ChainedStruct const * nextInChain = nullptr;
    Bool strictMath;
};
ShaderModuleCompilationOptions::ShaderModuleCompilationOptions(ShaderModuleCompilationOptions::Init&& init)
: ChainedStruct { init.nextInChain, SType::ShaderModuleCompilationOptions }
    ,strictMath(std::move(init.strictMath))
    {}
// StencilFaceState implementation

StencilFaceState::operator const WGPUStencilFaceState&() const noexcept {
    return *reinterpret_cast<const WGPUStencilFaceState*>(this);
}

// SurfaceDescriptor implementation

SurfaceDescriptor::operator const WGPUSurfaceDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUSurfaceDescriptor*>(this);
}

// SurfaceDescriptorFromAndroidNativeWindow implementation

SurfaceDescriptorFromAndroidNativeWindow::operator const WGPUSurfaceDescriptorFromAndroidNativeWindow&() const noexcept {
    return *reinterpret_cast<const WGPUSurfaceDescriptorFromAndroidNativeWindow*>(this);
}

SurfaceDescriptorFromAndroidNativeWindow::SurfaceDescriptorFromAndroidNativeWindow()
: ChainedStruct { nullptr, SType::SurfaceDescriptorFromAndroidNativeWindow } {}

struct SurfaceDescriptorFromAndroidNativeWindow::Init {
    ChainedStruct const * nextInChain = nullptr;
    void * window;
};
SurfaceDescriptorFromAndroidNativeWindow::SurfaceDescriptorFromAndroidNativeWindow(SurfaceDescriptorFromAndroidNativeWindow::Init&& init)
: ChainedStruct { init.nextInChain, SType::SurfaceDescriptorFromAndroidNativeWindow }
    ,window(std::move(init.window))
    {}
// SurfaceDescriptorFromCanvasHTMLSelector implementation

SurfaceDescriptorFromCanvasHTMLSelector::operator const WGPUSurfaceDescriptorFromCanvasHTMLSelector&() const noexcept {
    return *reinterpret_cast<const WGPUSurfaceDescriptorFromCanvasHTMLSelector*>(this);
}

SurfaceDescriptorFromCanvasHTMLSelector::SurfaceDescriptorFromCanvasHTMLSelector()
: ChainedStruct { nullptr, SType::SurfaceDescriptorFromCanvasHTMLSelector } {}

struct SurfaceDescriptorFromCanvasHTMLSelector::Init {
    ChainedStruct const * nextInChain = nullptr;
    char const * selector;
};
SurfaceDescriptorFromCanvasHTMLSelector::SurfaceDescriptorFromCanvasHTMLSelector(SurfaceDescriptorFromCanvasHTMLSelector::Init&& init)
: ChainedStruct { init.nextInChain, SType::SurfaceDescriptorFromCanvasHTMLSelector }
    ,selector(std::move(init.selector))
    {}
// SurfaceDescriptorFromMetalLayer implementation

SurfaceDescriptorFromMetalLayer::operator const WGPUSurfaceDescriptorFromMetalLayer&() const noexcept {
    return *reinterpret_cast<const WGPUSurfaceDescriptorFromMetalLayer*>(this);
}

SurfaceDescriptorFromMetalLayer::SurfaceDescriptorFromMetalLayer()
: ChainedStruct { nullptr, SType::SurfaceDescriptorFromMetalLayer } {}

struct SurfaceDescriptorFromMetalLayer::Init {
    ChainedStruct const * nextInChain = nullptr;
    void * layer;
};
SurfaceDescriptorFromMetalLayer::SurfaceDescriptorFromMetalLayer(SurfaceDescriptorFromMetalLayer::Init&& init)
: ChainedStruct { init.nextInChain, SType::SurfaceDescriptorFromMetalLayer }
    ,layer(std::move(init.layer))
    {}
// SurfaceDescriptorFromWindowsHWND implementation

SurfaceDescriptorFromWindowsHWND::operator const WGPUSurfaceDescriptorFromWindowsHWND&() const noexcept {
    return *reinterpret_cast<const WGPUSurfaceDescriptorFromWindowsHWND*>(this);
}

SurfaceDescriptorFromWindowsHWND::SurfaceDescriptorFromWindowsHWND()
: ChainedStruct { nullptr, SType::SurfaceDescriptorFromWindowsHWND } {}

struct SurfaceDescriptorFromWindowsHWND::Init {
    ChainedStruct const * nextInChain = nullptr;
    void * hinstance;
    void * hwnd;
};
SurfaceDescriptorFromWindowsHWND::SurfaceDescriptorFromWindowsHWND(SurfaceDescriptorFromWindowsHWND::Init&& init)
: ChainedStruct { init.nextInChain, SType::SurfaceDescriptorFromWindowsHWND }
    ,hinstance(std::move(init.hinstance))
    ,hwnd(std::move(init.hwnd))
    {}
// SurfaceDescriptorFromXcbWindow implementation

SurfaceDescriptorFromXcbWindow::operator const WGPUSurfaceDescriptorFromXcbWindow&() const noexcept {
    return *reinterpret_cast<const WGPUSurfaceDescriptorFromXcbWindow*>(this);
}

SurfaceDescriptorFromXcbWindow::SurfaceDescriptorFromXcbWindow()
: ChainedStruct { nullptr, SType::SurfaceDescriptorFromXcbWindow } {}

struct SurfaceDescriptorFromXcbWindow::Init {
    ChainedStruct const * nextInChain = nullptr;
    void * connection;
    uint32_t window;
};
SurfaceDescriptorFromXcbWindow::SurfaceDescriptorFromXcbWindow(SurfaceDescriptorFromXcbWindow::Init&& init)
: ChainedStruct { init.nextInChain, SType::SurfaceDescriptorFromXcbWindow }
    ,connection(std::move(init.connection))
    ,window(std::move(init.window))
    {}
// SurfaceDescriptorFromXlibWindow implementation

SurfaceDescriptorFromXlibWindow::operator const WGPUSurfaceDescriptorFromXlibWindow&() const noexcept {
    return *reinterpret_cast<const WGPUSurfaceDescriptorFromXlibWindow*>(this);
}

SurfaceDescriptorFromXlibWindow::SurfaceDescriptorFromXlibWindow()
: ChainedStruct { nullptr, SType::SurfaceDescriptorFromXlibWindow } {}

struct SurfaceDescriptorFromXlibWindow::Init {
    ChainedStruct const * nextInChain = nullptr;
    void * display;
    uint64_t window;
};
SurfaceDescriptorFromXlibWindow::SurfaceDescriptorFromXlibWindow(SurfaceDescriptorFromXlibWindow::Init&& init)
: ChainedStruct { init.nextInChain, SType::SurfaceDescriptorFromXlibWindow }
    ,display(std::move(init.display))
    ,window(std::move(init.window))
    {}
// SurfaceDescriptorFromWaylandSurface implementation

SurfaceDescriptorFromWaylandSurface::operator const WGPUSurfaceDescriptorFromWaylandSurface&() const noexcept {
    return *reinterpret_cast<const WGPUSurfaceDescriptorFromWaylandSurface*>(this);
}

SurfaceDescriptorFromWaylandSurface::SurfaceDescriptorFromWaylandSurface()
: ChainedStruct { nullptr, SType::SurfaceDescriptorFromWaylandSurface } {}

struct SurfaceDescriptorFromWaylandSurface::Init {
    ChainedStruct const * nextInChain = nullptr;
    void * display;
    void * surface;
};
SurfaceDescriptorFromWaylandSurface::SurfaceDescriptorFromWaylandSurface(SurfaceDescriptorFromWaylandSurface::Init&& init)
: ChainedStruct { init.nextInChain, SType::SurfaceDescriptorFromWaylandSurface }
    ,display(std::move(init.display))
    ,surface(std::move(init.surface))
    {}
// SurfaceDescriptorFromWindowsCoreWindow implementation

SurfaceDescriptorFromWindowsCoreWindow::operator const WGPUSurfaceDescriptorFromWindowsCoreWindow&() const noexcept {
    return *reinterpret_cast<const WGPUSurfaceDescriptorFromWindowsCoreWindow*>(this);
}

SurfaceDescriptorFromWindowsCoreWindow::SurfaceDescriptorFromWindowsCoreWindow()
: ChainedStruct { nullptr, SType::SurfaceDescriptorFromWindowsCoreWindow } {}

struct SurfaceDescriptorFromWindowsCoreWindow::Init {
    ChainedStruct const * nextInChain = nullptr;
    void * coreWindow;
};
SurfaceDescriptorFromWindowsCoreWindow::SurfaceDescriptorFromWindowsCoreWindow(SurfaceDescriptorFromWindowsCoreWindow::Init&& init)
: ChainedStruct { init.nextInChain, SType::SurfaceDescriptorFromWindowsCoreWindow }
    ,coreWindow(std::move(init.coreWindow))
    {}
// SurfaceDescriptorFromWindowsSwapChainPanel implementation

SurfaceDescriptorFromWindowsSwapChainPanel::operator const WGPUSurfaceDescriptorFromWindowsSwapChainPanel&() const noexcept {
    return *reinterpret_cast<const WGPUSurfaceDescriptorFromWindowsSwapChainPanel*>(this);
}

SurfaceDescriptorFromWindowsSwapChainPanel::SurfaceDescriptorFromWindowsSwapChainPanel()
: ChainedStruct { nullptr, SType::SurfaceDescriptorFromWindowsSwapChainPanel } {}

struct SurfaceDescriptorFromWindowsSwapChainPanel::Init {
    ChainedStruct const * nextInChain = nullptr;
    void * swapChainPanel;
};
SurfaceDescriptorFromWindowsSwapChainPanel::SurfaceDescriptorFromWindowsSwapChainPanel(SurfaceDescriptorFromWindowsSwapChainPanel::Init&& init)
: ChainedStruct { init.nextInChain, SType::SurfaceDescriptorFromWindowsSwapChainPanel }
    ,swapChainPanel(std::move(init.swapChainPanel))
    {}
// SwapChainDescriptor implementation

SwapChainDescriptor::operator const WGPUSwapChainDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUSwapChainDescriptor*>(this);
}

// SurfaceTexture implementation

SurfaceTexture::operator const WGPUSurfaceTexture&() const noexcept {
    return *reinterpret_cast<const WGPUSurfaceTexture*>(this);
}

// TextureDataLayout implementation

TextureDataLayout::operator const WGPUTextureDataLayout&() const noexcept {
    return *reinterpret_cast<const WGPUTextureDataLayout*>(this);
}

// TextureDescriptor implementation

TextureDescriptor::operator const WGPUTextureDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUTextureDescriptor*>(this);
}

// TextureBindingViewDimensionDescriptor implementation

TextureBindingViewDimensionDescriptor::operator const WGPUTextureBindingViewDimensionDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUTextureBindingViewDimensionDescriptor*>(this);
}

TextureBindingViewDimensionDescriptor::TextureBindingViewDimensionDescriptor()
: ChainedStruct { nullptr, SType::TextureBindingViewDimensionDescriptor } {}

struct TextureBindingViewDimensionDescriptor::Init {
    ChainedStruct const * nextInChain = nullptr;
    TextureViewDimension textureBindingViewDimension = TextureViewDimension::Undefined;
};
TextureBindingViewDimensionDescriptor::TextureBindingViewDimensionDescriptor(TextureBindingViewDimensionDescriptor::Init&& init)
: ChainedStruct { init.nextInChain, SType::TextureBindingViewDimensionDescriptor }
    ,textureBindingViewDimension(std::move(init.textureBindingViewDimension))
    {}
// TextureViewDescriptor implementation

TextureViewDescriptor::operator const WGPUTextureViewDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUTextureViewDescriptor*>(this);
}

// YCbCrVkDescriptor implementation

YCbCrVkDescriptor::operator const WGPUYCbCrVkDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUYCbCrVkDescriptor*>(this);
}

YCbCrVkDescriptor::YCbCrVkDescriptor()
: ChainedStruct { nullptr, SType::YCbCrVkDescriptor } {}

struct YCbCrVkDescriptor::Init {
    ChainedStruct const * nextInChain = nullptr;
    uint32_t vkFormat = 0;
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
YCbCrVkDescriptor::YCbCrVkDescriptor(YCbCrVkDescriptor::Init&& init)
: ChainedStruct { init.nextInChain, SType::YCbCrVkDescriptor }
    ,vkFormat(std::move(init.vkFormat))
    ,vkYCbCrModel(std::move(init.vkYCbCrModel))
    ,vkYCbCrRange(std::move(init.vkYCbCrRange))
    ,vkComponentSwizzleRed(std::move(init.vkComponentSwizzleRed))
    ,vkComponentSwizzleGreen(std::move(init.vkComponentSwizzleGreen))
    ,vkComponentSwizzleBlue(std::move(init.vkComponentSwizzleBlue))
    ,vkComponentSwizzleAlpha(std::move(init.vkComponentSwizzleAlpha))
    ,vkXChromaOffset(std::move(init.vkXChromaOffset))
    ,vkYChromaOffset(std::move(init.vkYChromaOffset))
    ,vkChromaFilter(std::move(init.vkChromaFilter))
    ,forceExplicitReconstruction(std::move(init.forceExplicitReconstruction))
    ,externalFormat(std::move(init.externalFormat))
    {}
// DawnTextureInternalUsageDescriptor implementation

DawnTextureInternalUsageDescriptor::operator const WGPUDawnTextureInternalUsageDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUDawnTextureInternalUsageDescriptor*>(this);
}

DawnTextureInternalUsageDescriptor::DawnTextureInternalUsageDescriptor()
: ChainedStruct { nullptr, SType::DawnTextureInternalUsageDescriptor } {}

struct DawnTextureInternalUsageDescriptor::Init {
    ChainedStruct const * nextInChain = nullptr;
    TextureUsage internalUsage = TextureUsage::None;
};
DawnTextureInternalUsageDescriptor::DawnTextureInternalUsageDescriptor(DawnTextureInternalUsageDescriptor::Init&& init)
: ChainedStruct { init.nextInChain, SType::DawnTextureInternalUsageDescriptor }
    ,internalUsage(std::move(init.internalUsage))
    {}
// DawnEncoderInternalUsageDescriptor implementation

DawnEncoderInternalUsageDescriptor::operator const WGPUDawnEncoderInternalUsageDescriptor&() const noexcept {
    return *reinterpret_cast<const WGPUDawnEncoderInternalUsageDescriptor*>(this);
}

DawnEncoderInternalUsageDescriptor::DawnEncoderInternalUsageDescriptor()
: ChainedStruct { nullptr, SType::DawnEncoderInternalUsageDescriptor } {}

struct DawnEncoderInternalUsageDescriptor::Init {
    ChainedStruct const * nextInChain = nullptr;
    Bool useInternalUsages = false;
};
DawnEncoderInternalUsageDescriptor::DawnEncoderInternalUsageDescriptor(DawnEncoderInternalUsageDescriptor::Init&& init)
: ChainedStruct { init.nextInChain, SType::DawnEncoderInternalUsageDescriptor }
    ,useInternalUsages(std::move(init.useInternalUsages))
    {}
// DawnAdapterPropertiesPowerPreference implementation

DawnAdapterPropertiesPowerPreference::operator const WGPUDawnAdapterPropertiesPowerPreference&() const noexcept {
    return *reinterpret_cast<const WGPUDawnAdapterPropertiesPowerPreference*>(this);
}

DawnAdapterPropertiesPowerPreference::DawnAdapterPropertiesPowerPreference()
: ChainedStructOut { nullptr, SType::DawnAdapterPropertiesPowerPreference } {}

struct DawnAdapterPropertiesPowerPreference::Init {
    ChainedStructOut * const nextInChain = nullptr;
    PowerPreference const powerPreference = PowerPreference::Undefined;
};
DawnAdapterPropertiesPowerPreference::DawnAdapterPropertiesPowerPreference(DawnAdapterPropertiesPowerPreference::Init&& init)
: ChainedStructOut { init.nextInChain, SType::DawnAdapterPropertiesPowerPreference }
    ,powerPreference(std::move(init.powerPreference))
    {}
DawnAdapterPropertiesPowerPreference::~DawnAdapterPropertiesPowerPreference() {
    FreeMembers();
}
void DawnAdapterPropertiesPowerPreference::FreeMembers() {
    // Free members here
}

DawnAdapterPropertiesPowerPreference::DawnAdapterPropertiesPowerPreference(DawnAdapterPropertiesPowerPreference&& rhs) :
    powerPreference(rhs.powerPreference)    
{}
DawnAdapterPropertiesPowerPreference& DawnAdapterPropertiesPowerPreference::operator=(DawnAdapterPropertiesPowerPreference&& rhs) {
if (&rhs == this) {
    return *this;
}
FreeMembers();

    ::wgpu::detail::AsNonConstReference(this->powerPreference) = std::move(rhs.powerPreference);    
    return *this;    
}
// MemoryHeapInfo implementation

MemoryHeapInfo::operator const WGPUMemoryHeapInfo&() const noexcept {
    return *reinterpret_cast<const WGPUMemoryHeapInfo*>(this);
}

// AdapterPropertiesMemoryHeaps implementation

AdapterPropertiesMemoryHeaps::operator const WGPUAdapterPropertiesMemoryHeaps&() const noexcept {
    return *reinterpret_cast<const WGPUAdapterPropertiesMemoryHeaps*>(this);
}

AdapterPropertiesMemoryHeaps::AdapterPropertiesMemoryHeaps()
: ChainedStructOut { nullptr, SType::AdapterPropertiesMemoryHeaps } {}

struct AdapterPropertiesMemoryHeaps::Init {
    ChainedStructOut * const nextInChain = nullptr;
    size_t const heapCount = {};
    MemoryHeapInfo const * const heapInfo = {};
};
AdapterPropertiesMemoryHeaps::AdapterPropertiesMemoryHeaps(AdapterPropertiesMemoryHeaps::Init&& init)
: ChainedStructOut { init.nextInChain, SType::AdapterPropertiesMemoryHeaps }
    ,heapCount(std::move(init.heapCount))
    ,heapInfo(std::move(init.heapInfo))
    {}
AdapterPropertiesMemoryHeaps::~AdapterPropertiesMemoryHeaps() {
    FreeMembers();
}
void AdapterPropertiesMemoryHeaps::FreeMembers() {
    // Free members here
}

AdapterPropertiesMemoryHeaps::AdapterPropertiesMemoryHeaps(AdapterPropertiesMemoryHeaps&& rhs) :
    heapCount(rhs.heapCount),    
    heapInfo(rhs.heapInfo)    
{}
AdapterPropertiesMemoryHeaps& AdapterPropertiesMemoryHeaps::operator=(AdapterPropertiesMemoryHeaps&& rhs) {
if (&rhs == this) {
    return *this;
}
FreeMembers();

    ::wgpu::detail::AsNonConstReference(this->heapCount) = std::move(rhs.heapCount);    
    ::wgpu::detail::AsNonConstReference(this->heapInfo) = std::move(rhs.heapInfo);    
    return *this;    
}
// AdapterPropertiesD3D implementation

AdapterPropertiesD3D::operator const WGPUAdapterPropertiesD3D&() const noexcept {
    return *reinterpret_cast<const WGPUAdapterPropertiesD3D*>(this);
}

AdapterPropertiesD3D::AdapterPropertiesD3D()
: ChainedStructOut { nullptr, SType::AdapterPropertiesD3D } {}

struct AdapterPropertiesD3D::Init {
    ChainedStructOut * const nextInChain = nullptr;
    uint32_t const shaderModel = {};
};
AdapterPropertiesD3D::AdapterPropertiesD3D(AdapterPropertiesD3D::Init&& init)
: ChainedStructOut { init.nextInChain, SType::AdapterPropertiesD3D }
    ,shaderModel(std::move(init.shaderModel))
    {}
AdapterPropertiesD3D::~AdapterPropertiesD3D() {
    FreeMembers();
}
void AdapterPropertiesD3D::FreeMembers() {
    // Free members here
}

AdapterPropertiesD3D::AdapterPropertiesD3D(AdapterPropertiesD3D&& rhs) :
    shaderModel(rhs.shaderModel)    
{}
AdapterPropertiesD3D& AdapterPropertiesD3D::operator=(AdapterPropertiesD3D&& rhs) {
if (&rhs == this) {
    return *this;
}
FreeMembers();

    ::wgpu::detail::AsNonConstReference(this->shaderModel) = std::move(rhs.shaderModel);    
    return *this;    
}
// AdapterPropertiesVk implementation

AdapterPropertiesVk::operator const WGPUAdapterPropertiesVk&() const noexcept {
    return *reinterpret_cast<const WGPUAdapterPropertiesVk*>(this);
}

AdapterPropertiesVk::AdapterPropertiesVk()
: ChainedStructOut { nullptr, SType::AdapterPropertiesVk } {}

struct AdapterPropertiesVk::Init {
    ChainedStructOut * const nextInChain = nullptr;
    uint32_t const driverVersion = {};
};
AdapterPropertiesVk::AdapterPropertiesVk(AdapterPropertiesVk::Init&& init)
: ChainedStructOut { init.nextInChain, SType::AdapterPropertiesVk }
    ,driverVersion(std::move(init.driverVersion))
    {}
AdapterPropertiesVk::~AdapterPropertiesVk() {
    FreeMembers();
}
void AdapterPropertiesVk::FreeMembers() {
    // Free members here
}

AdapterPropertiesVk::AdapterPropertiesVk(AdapterPropertiesVk&& rhs) :
    driverVersion(rhs.driverVersion)    
{}
AdapterPropertiesVk& AdapterPropertiesVk::operator=(AdapterPropertiesVk&& rhs) {
if (&rhs == this) {
    return *this;
}
FreeMembers();

    ::wgpu::detail::AsNonConstReference(this->driverVersion) = std::move(rhs.driverVersion);    
    return *this;    
}
// DawnBufferDescriptorErrorInfoFromWireClient implementation

DawnBufferDescriptorErrorInfoFromWireClient::operator const WGPUDawnBufferDescriptorErrorInfoFromWireClient&() const noexcept {
    return *reinterpret_cast<const WGPUDawnBufferDescriptorErrorInfoFromWireClient*>(this);
}

DawnBufferDescriptorErrorInfoFromWireClient::DawnBufferDescriptorErrorInfoFromWireClient()
: ChainedStruct { nullptr, SType::DawnBufferDescriptorErrorInfoFromWireClient } {}

struct DawnBufferDescriptorErrorInfoFromWireClient::Init {
    ChainedStruct const * nextInChain = nullptr;
    Bool outOfMemory = false;
};
DawnBufferDescriptorErrorInfoFromWireClient::DawnBufferDescriptorErrorInfoFromWireClient(DawnBufferDescriptorErrorInfoFromWireClient::Init&& init)
: ChainedStruct { init.nextInChain, SType::DawnBufferDescriptorErrorInfoFromWireClient }
    ,outOfMemory(std::move(init.outOfMemory))
    {}

// Adapter implementation

Instance Adapter::GetInstance () const {
    auto result = wgpuAdapterGetInstance(Get());    
    return Instance::Acquire(result);    
}
Status Adapter::GetLimits (SupportedLimits * limits) const {
    auto result = wgpuAdapterGetLimits(Get(), reinterpret_cast<WGPUSupportedLimits * >(limits));    
    return static_cast<Status>(result);    
}
Status Adapter::GetInfo (AdapterInfo * info) const {
    auto result = wgpuAdapterGetInfo(Get(), reinterpret_cast<WGPUAdapterInfo * >(info));    
    return static_cast<Status>(result);    
}
Status Adapter::GetProperties (AdapterProperties * properties) const {
    auto result = wgpuAdapterGetProperties(Get(), reinterpret_cast<WGPUAdapterProperties * >(properties));    
    return static_cast<Status>(result);    
}
bool Adapter::HasFeature (FeatureName feature) const {
    auto result = wgpuAdapterHasFeature(Get(), *reinterpret_cast<WGPUFeatureName const*>(&feature));    
    return result;    
}
size_t Adapter::EnumerateFeatures (FeatureName * features) const {
    auto result = wgpuAdapterEnumerateFeatures(Get(), reinterpret_cast<WGPUFeatureName * >(features));    
    return result;    
}
void Adapter::RequestDevice (DeviceDescriptor const* descriptor, RequestDeviceCallback callback, void * userdata) const {
    wgpuAdapterRequestDevice(Get(), reinterpret_cast<WGPUDeviceDescriptor const* >(descriptor), *reinterpret_cast<WGPURequestDeviceCallback const*>(&callback), userdata);    
}
Device Adapter::CreateDevice (DeviceDescriptor const* descriptor) const {
    auto result = wgpuAdapterCreateDevice(Get(), reinterpret_cast<WGPUDeviceDescriptor const* >(descriptor));    
    return Device::Acquire(result);    
}
Status Adapter::GetFormatCapabilities (TextureFormat format, FormatCapabilities * capabilities) const {
    auto result = wgpuAdapterGetFormatCapabilities(Get(), *reinterpret_cast<WGPUTextureFormat const*>(&format), reinterpret_cast<WGPUFormatCapabilities * >(capabilities));    
    return static_cast<Status>(result);    
}

void Adapter::WGPUAddRef(WGPUAdapter handle) {
    if (handle != nullptr) {
        wgpuAdapterAddRef(handle);
    }
}
void Adapter::WGPURelease(WGPUAdapter handle) {
    if (handle != nullptr) {
        wgpuAdapterRelease(handle);
    }
}

// BindGroup implementation

void BindGroup::SetLabel (char const* label) const {
    wgpuBindGroupSetLabel(Get(), label);    
}
void BindGroup::SetLabel2 (NullableStringView label) const {
    wgpuBindGroupSetLabel2(Get(), *reinterpret_cast<WGPUStringView const*>(&label));    
}

void BindGroup::WGPUAddRef(WGPUBindGroup handle) {
    if (handle != nullptr) {
        wgpuBindGroupAddRef(handle);
    }
}
void BindGroup::WGPURelease(WGPUBindGroup handle) {
    if (handle != nullptr) {
        wgpuBindGroupRelease(handle);
    }
}

// BindGroupLayout implementation

void BindGroupLayout::SetLabel (char const* label) const {
    wgpuBindGroupLayoutSetLabel(Get(), label);    
}
void BindGroupLayout::SetLabel2 (NullableStringView label) const {
    wgpuBindGroupLayoutSetLabel2(Get(), *reinterpret_cast<WGPUStringView const*>(&label));    
}

void BindGroupLayout::WGPUAddRef(WGPUBindGroupLayout handle) {
    if (handle != nullptr) {
        wgpuBindGroupLayoutAddRef(handle);
    }
}
void BindGroupLayout::WGPURelease(WGPUBindGroupLayout handle) {
    if (handle != nullptr) {
        wgpuBindGroupLayoutRelease(handle);
    }
}

// Buffer implementation

void Buffer::MapAsync (MapMode mode, size_t offset, size_t size, BufferMapCallback callback, void * userdata) const {
    wgpuBufferMapAsync(Get(), *reinterpret_cast<WGPUMapMode const*>(&mode), offset, size, *reinterpret_cast<WGPUBufferMapCallback const*>(&callback), userdata);    
}
void * Buffer::GetMappedRange (size_t offset, size_t size) const {
    auto result = wgpuBufferGetMappedRange(Get(), offset, size);    
    return result;    
}
void const * Buffer::GetConstMappedRange (size_t offset, size_t size) const {
    auto result = wgpuBufferGetConstMappedRange(Get(), offset, size);    
    return result;    
}
void Buffer::SetLabel (char const* label) const {
    wgpuBufferSetLabel(Get(), label);    
}
void Buffer::SetLabel2 (NullableStringView label) const {
    wgpuBufferSetLabel2(Get(), *reinterpret_cast<WGPUStringView const*>(&label));    
}
BufferUsage Buffer::GetUsage () const {
    auto result = wgpuBufferGetUsage(Get());    
    return static_cast<BufferUsage>(result);    
}
uint64_t Buffer::GetSize () const {
    auto result = wgpuBufferGetSize(Get());    
    return result;    
}
BufferMapState Buffer::GetMapState () const {
    auto result = wgpuBufferGetMapState(Get());    
    return static_cast<BufferMapState>(result);    
}
void Buffer::Unmap () const {
    wgpuBufferUnmap(Get());    
}
void Buffer::Destroy () const {
    wgpuBufferDestroy(Get());    
}

void Buffer::WGPUAddRef(WGPUBuffer handle) {
    if (handle != nullptr) {
        wgpuBufferAddRef(handle);
    }
}
void Buffer::WGPURelease(WGPUBuffer handle) {
    if (handle != nullptr) {
        wgpuBufferRelease(handle);
    }
}

// CommandBuffer implementation

void CommandBuffer::SetLabel (char const* label) const {
    wgpuCommandBufferSetLabel(Get(), label);    
}
void CommandBuffer::SetLabel2 (NullableStringView label) const {
    wgpuCommandBufferSetLabel2(Get(), *reinterpret_cast<WGPUStringView const*>(&label));    
}

void CommandBuffer::WGPUAddRef(WGPUCommandBuffer handle) {
    if (handle != nullptr) {
        wgpuCommandBufferAddRef(handle);
    }
}
void CommandBuffer::WGPURelease(WGPUCommandBuffer handle) {
    if (handle != nullptr) {
        wgpuCommandBufferRelease(handle);
    }
}

// CommandEncoder implementation

CommandBuffer CommandEncoder::Finish (CommandBufferDescriptor const* descriptor) const {
    auto result = wgpuCommandEncoderFinish(Get(), reinterpret_cast<WGPUCommandBufferDescriptor const* >(descriptor));    
    return CommandBuffer::Acquire(result);    
}
ComputePassEncoder CommandEncoder::BeginComputePass (ComputePassDescriptor const* descriptor) const {
    auto result = wgpuCommandEncoderBeginComputePass(Get(), reinterpret_cast<WGPUComputePassDescriptor const* >(descriptor));    
    return ComputePassEncoder::Acquire(result);    
}
RenderPassEncoder CommandEncoder::BeginRenderPass (RenderPassDescriptor const* descriptor) const {
    auto result = wgpuCommandEncoderBeginRenderPass(Get(), reinterpret_cast<WGPURenderPassDescriptor const* >(descriptor));    
    return RenderPassEncoder::Acquire(result);    
}
void CommandEncoder::CopyBufferToBuffer (Buffer source, uint64_t sourceOffset, Buffer destination, uint64_t destinationOffset, uint64_t size) const {
    wgpuCommandEncoderCopyBufferToBuffer(Get(), *reinterpret_cast<WGPUBuffer const*>(&source), sourceOffset, *reinterpret_cast<WGPUBuffer const*>(&destination), destinationOffset, size);    
}
void CommandEncoder::CopyBufferToTexture (ImageCopyBuffer const* source, ImageCopyTexture const* destination, Extent3D const* copySize) const {
    wgpuCommandEncoderCopyBufferToTexture(Get(), reinterpret_cast<WGPUImageCopyBuffer const* >(source), reinterpret_cast<WGPUImageCopyTexture const* >(destination), reinterpret_cast<WGPUExtent3D const* >(copySize));    
}
void CommandEncoder::CopyTextureToBuffer (ImageCopyTexture const* source, ImageCopyBuffer const* destination, Extent3D const* copySize) const {
    wgpuCommandEncoderCopyTextureToBuffer(Get(), reinterpret_cast<WGPUImageCopyTexture const* >(source), reinterpret_cast<WGPUImageCopyBuffer const* >(destination), reinterpret_cast<WGPUExtent3D const* >(copySize));    
}
void CommandEncoder::CopyTextureToTexture (ImageCopyTexture const* source, ImageCopyTexture const* destination, Extent3D const* copySize) const {
    wgpuCommandEncoderCopyTextureToTexture(Get(), reinterpret_cast<WGPUImageCopyTexture const* >(source), reinterpret_cast<WGPUImageCopyTexture const* >(destination), reinterpret_cast<WGPUExtent3D const* >(copySize));    
}
void CommandEncoder::ClearBuffer (Buffer buffer, uint64_t offset, uint64_t size) const {
    wgpuCommandEncoderClearBuffer(Get(), *reinterpret_cast<WGPUBuffer const*>(&buffer), offset, size);    
}
void CommandEncoder::InjectValidationError (char const* message) const {
    wgpuCommandEncoderInjectValidationError(Get(), message);    
}
void CommandEncoder::InjectValidationError2 (StringView message) const {
    wgpuCommandEncoderInjectValidationError2(Get(), *reinterpret_cast<WGPUStringView const*>(&message));    
}
void CommandEncoder::InsertDebugMarker (char const* markerLabel) const {
    wgpuCommandEncoderInsertDebugMarker(Get(), markerLabel);    
}
void CommandEncoder::InsertDebugMarker2 (StringView markerLabel) const {
    wgpuCommandEncoderInsertDebugMarker2(Get(), *reinterpret_cast<WGPUStringView const*>(&markerLabel));    
}
void CommandEncoder::PopDebugGroup () const {
    wgpuCommandEncoderPopDebugGroup(Get());    
}
void CommandEncoder::PushDebugGroup (char const* groupLabel) const {
    wgpuCommandEncoderPushDebugGroup(Get(), groupLabel);    
}
void CommandEncoder::PushDebugGroup2 (StringView groupLabel) const {
    wgpuCommandEncoderPushDebugGroup2(Get(), *reinterpret_cast<WGPUStringView const*>(&groupLabel));    
}
void CommandEncoder::ResolveQuerySet (QuerySet querySet, uint32_t firstQuery, uint32_t queryCount, Buffer destination, uint64_t destinationOffset) const {
    wgpuCommandEncoderResolveQuerySet(Get(), *reinterpret_cast<WGPUQuerySet const*>(&querySet), firstQuery, queryCount, *reinterpret_cast<WGPUBuffer const*>(&destination), destinationOffset);    
}
void CommandEncoder::WriteBuffer (Buffer buffer, uint64_t bufferOffset, uint8_t const* data, uint64_t size) const {
    wgpuCommandEncoderWriteBuffer(Get(), *reinterpret_cast<WGPUBuffer const*>(&buffer), bufferOffset, data, size);    
}
void CommandEncoder::WriteTimestamp (QuerySet querySet, uint32_t queryIndex) const {
    wgpuCommandEncoderWriteTimestamp(Get(), *reinterpret_cast<WGPUQuerySet const*>(&querySet), queryIndex);    
}
void CommandEncoder::SetLabel (char const* label) const {
    wgpuCommandEncoderSetLabel(Get(), label);    
}
void CommandEncoder::SetLabel2 (NullableStringView label) const {
    wgpuCommandEncoderSetLabel2(Get(), *reinterpret_cast<WGPUStringView const*>(&label));    
}

void CommandEncoder::WGPUAddRef(WGPUCommandEncoder handle) {
    if (handle != nullptr) {
        wgpuCommandEncoderAddRef(handle);
    }
}
void CommandEncoder::WGPURelease(WGPUCommandEncoder handle) {
    if (handle != nullptr) {
        wgpuCommandEncoderRelease(handle);
    }
}

// ComputePassEncoder implementation

void ComputePassEncoder::InsertDebugMarker (char const* markerLabel) const {
    wgpuComputePassEncoderInsertDebugMarker(Get(), markerLabel);    
}
void ComputePassEncoder::InsertDebugMarker2 (StringView markerLabel) const {
    wgpuComputePassEncoderInsertDebugMarker2(Get(), *reinterpret_cast<WGPUStringView const*>(&markerLabel));    
}
void ComputePassEncoder::PopDebugGroup () const {
    wgpuComputePassEncoderPopDebugGroup(Get());    
}
void ComputePassEncoder::PushDebugGroup (char const* groupLabel) const {
    wgpuComputePassEncoderPushDebugGroup(Get(), groupLabel);    
}
void ComputePassEncoder::PushDebugGroup2 (StringView groupLabel) const {
    wgpuComputePassEncoderPushDebugGroup2(Get(), *reinterpret_cast<WGPUStringView const*>(&groupLabel));    
}
void ComputePassEncoder::SetPipeline (ComputePipeline pipeline) const {
    wgpuComputePassEncoderSetPipeline(Get(), *reinterpret_cast<WGPUComputePipeline const*>(&pipeline));    
}
void ComputePassEncoder::SetBindGroup (uint32_t groupIndex, BindGroup group, size_t dynamicOffsetCount, uint32_t const* dynamicOffsets) const {
    wgpuComputePassEncoderSetBindGroup(Get(), groupIndex, *reinterpret_cast<WGPUBindGroup const*>(&group), dynamicOffsetCount, dynamicOffsets);    
}
void ComputePassEncoder::WriteTimestamp (QuerySet querySet, uint32_t queryIndex) const {
    wgpuComputePassEncoderWriteTimestamp(Get(), *reinterpret_cast<WGPUQuerySet const*>(&querySet), queryIndex);    
}
void ComputePassEncoder::DispatchWorkgroups (uint32_t workgroupCountX, uint32_t workgroupCountY, uint32_t workgroupCountZ) const {
    wgpuComputePassEncoderDispatchWorkgroups(Get(), workgroupCountX, workgroupCountY, workgroupCountZ);    
}
void ComputePassEncoder::DispatchWorkgroupsIndirect (Buffer indirectBuffer, uint64_t indirectOffset) const {
    wgpuComputePassEncoderDispatchWorkgroupsIndirect(Get(), *reinterpret_cast<WGPUBuffer const*>(&indirectBuffer), indirectOffset);    
}
void ComputePassEncoder::End () const {
    wgpuComputePassEncoderEnd(Get());    
}
void ComputePassEncoder::SetLabel (char const* label) const {
    wgpuComputePassEncoderSetLabel(Get(), label);    
}
void ComputePassEncoder::SetLabel2 (NullableStringView label) const {
    wgpuComputePassEncoderSetLabel2(Get(), *reinterpret_cast<WGPUStringView const*>(&label));    
}

void ComputePassEncoder::WGPUAddRef(WGPUComputePassEncoder handle) {
    if (handle != nullptr) {
        wgpuComputePassEncoderAddRef(handle);
    }
}
void ComputePassEncoder::WGPURelease(WGPUComputePassEncoder handle) {
    if (handle != nullptr) {
        wgpuComputePassEncoderRelease(handle);
    }
}

// ComputePipeline implementation

BindGroupLayout ComputePipeline::GetBindGroupLayout (uint32_t groupIndex) const {
    auto result = wgpuComputePipelineGetBindGroupLayout(Get(), groupIndex);    
    return BindGroupLayout::Acquire(result);    
}
void ComputePipeline::SetLabel (char const* label) const {
    wgpuComputePipelineSetLabel(Get(), label);    
}
void ComputePipeline::SetLabel2 (NullableStringView label) const {
    wgpuComputePipelineSetLabel2(Get(), *reinterpret_cast<WGPUStringView const*>(&label));    
}

void ComputePipeline::WGPUAddRef(WGPUComputePipeline handle) {
    if (handle != nullptr) {
        wgpuComputePipelineAddRef(handle);
    }
}
void ComputePipeline::WGPURelease(WGPUComputePipeline handle) {
    if (handle != nullptr) {
        wgpuComputePipelineRelease(handle);
    }
}

// Device implementation

BindGroup Device::CreateBindGroup (BindGroupDescriptor const* descriptor) const {
    auto result = wgpuDeviceCreateBindGroup(Get(), reinterpret_cast<WGPUBindGroupDescriptor const* >(descriptor));    
    return BindGroup::Acquire(result);    
}
BindGroupLayout Device::CreateBindGroupLayout (BindGroupLayoutDescriptor const* descriptor) const {
    auto result = wgpuDeviceCreateBindGroupLayout(Get(), reinterpret_cast<WGPUBindGroupLayoutDescriptor const* >(descriptor));    
    return BindGroupLayout::Acquire(result);    
}
Buffer Device::CreateBuffer (BufferDescriptor const* descriptor) const {
    auto result = wgpuDeviceCreateBuffer(Get(), reinterpret_cast<WGPUBufferDescriptor const* >(descriptor));    
    return Buffer::Acquire(result);    
}
Buffer Device::CreateErrorBuffer (BufferDescriptor const* descriptor) const {
    auto result = wgpuDeviceCreateErrorBuffer(Get(), reinterpret_cast<WGPUBufferDescriptor const* >(descriptor));    
    return Buffer::Acquire(result);    
}
CommandEncoder Device::CreateCommandEncoder (CommandEncoderDescriptor const* descriptor) const {
    auto result = wgpuDeviceCreateCommandEncoder(Get(), reinterpret_cast<WGPUCommandEncoderDescriptor const* >(descriptor));    
    return CommandEncoder::Acquire(result);    
}
ComputePipeline Device::CreateComputePipeline (ComputePipelineDescriptor const* descriptor) const {
    auto result = wgpuDeviceCreateComputePipeline(Get(), reinterpret_cast<WGPUComputePipelineDescriptor const* >(descriptor));    
    return ComputePipeline::Acquire(result);    
}
void Device::CreateComputePipelineAsync (ComputePipelineDescriptor const* descriptor, CreateComputePipelineAsyncCallback callback, void * userdata) const {
    wgpuDeviceCreateComputePipelineAsync(Get(), reinterpret_cast<WGPUComputePipelineDescriptor const* >(descriptor), *reinterpret_cast<WGPUCreateComputePipelineAsyncCallback const*>(&callback), userdata);    
}
ExternalTexture Device::CreateExternalTexture (ExternalTextureDescriptor const* externalTextureDescriptor) const {
    auto result = wgpuDeviceCreateExternalTexture(Get(), reinterpret_cast<WGPUExternalTextureDescriptor const* >(externalTextureDescriptor));    
    return ExternalTexture::Acquire(result);    
}
ExternalTexture Device::CreateErrorExternalTexture () const {
    auto result = wgpuDeviceCreateErrorExternalTexture(Get());    
    return ExternalTexture::Acquire(result);    
}
PipelineLayout Device::CreatePipelineLayout (PipelineLayoutDescriptor const* descriptor) const {
    auto result = wgpuDeviceCreatePipelineLayout(Get(), reinterpret_cast<WGPUPipelineLayoutDescriptor const* >(descriptor));    
    return PipelineLayout::Acquire(result);    
}
QuerySet Device::CreateQuerySet (QuerySetDescriptor const* descriptor) const {
    auto result = wgpuDeviceCreateQuerySet(Get(), reinterpret_cast<WGPUQuerySetDescriptor const* >(descriptor));    
    return QuerySet::Acquire(result);    
}
void Device::CreateRenderPipelineAsync (RenderPipelineDescriptor const* descriptor, CreateRenderPipelineAsyncCallback callback, void * userdata) const {
    wgpuDeviceCreateRenderPipelineAsync(Get(), reinterpret_cast<WGPURenderPipelineDescriptor const* >(descriptor), *reinterpret_cast<WGPUCreateRenderPipelineAsyncCallback const*>(&callback), userdata);    
}
RenderBundleEncoder Device::CreateRenderBundleEncoder (RenderBundleEncoderDescriptor const* descriptor) const {
    auto result = wgpuDeviceCreateRenderBundleEncoder(Get(), reinterpret_cast<WGPURenderBundleEncoderDescriptor const* >(descriptor));    
    return RenderBundleEncoder::Acquire(result);    
}
RenderPipeline Device::CreateRenderPipeline (RenderPipelineDescriptor const* descriptor) const {
    auto result = wgpuDeviceCreateRenderPipeline(Get(), reinterpret_cast<WGPURenderPipelineDescriptor const* >(descriptor));    
    return RenderPipeline::Acquire(result);    
}
Sampler Device::CreateSampler (SamplerDescriptor const* descriptor) const {
    auto result = wgpuDeviceCreateSampler(Get(), reinterpret_cast<WGPUSamplerDescriptor const* >(descriptor));    
    return Sampler::Acquire(result);    
}
ShaderModule Device::CreateShaderModule (ShaderModuleDescriptor const* descriptor) const {
    auto result = wgpuDeviceCreateShaderModule(Get(), reinterpret_cast<WGPUShaderModuleDescriptor const* >(descriptor));    
    return ShaderModule::Acquire(result);    
}
ShaderModule Device::CreateErrorShaderModule (ShaderModuleDescriptor const* descriptor, char const* errorMessage) const {
    auto result = wgpuDeviceCreateErrorShaderModule(Get(), reinterpret_cast<WGPUShaderModuleDescriptor const* >(descriptor), errorMessage);    
    return ShaderModule::Acquire(result);    
}
ShaderModule Device::CreateErrorShaderModule2 (ShaderModuleDescriptor const* descriptor, StringView errorMessage) const {
    auto result = wgpuDeviceCreateErrorShaderModule2(Get(), reinterpret_cast<WGPUShaderModuleDescriptor const* >(descriptor), *reinterpret_cast<WGPUStringView const*>(&errorMessage));    
    return ShaderModule::Acquire(result);    
}
SwapChain Device::CreateSwapChain (Surface surface, SwapChainDescriptor const* descriptor) const {
    auto result = wgpuDeviceCreateSwapChain(Get(), *reinterpret_cast<WGPUSurface const*>(&surface), reinterpret_cast<WGPUSwapChainDescriptor const* >(descriptor));    
    return SwapChain::Acquire(result);    
}
Texture Device::CreateTexture (TextureDescriptor const* descriptor) const {
    auto result = wgpuDeviceCreateTexture(Get(), reinterpret_cast<WGPUTextureDescriptor const* >(descriptor));    
    return Texture::Acquire(result);    
}
SharedBufferMemory Device::ImportSharedBufferMemory (SharedBufferMemoryDescriptor const* descriptor) const {
    auto result = wgpuDeviceImportSharedBufferMemory(Get(), reinterpret_cast<WGPUSharedBufferMemoryDescriptor const* >(descriptor));    
    return SharedBufferMemory::Acquire(result);    
}
SharedTextureMemory Device::ImportSharedTextureMemory (SharedTextureMemoryDescriptor const* descriptor) const {
    auto result = wgpuDeviceImportSharedTextureMemory(Get(), reinterpret_cast<WGPUSharedTextureMemoryDescriptor const* >(descriptor));    
    return SharedTextureMemory::Acquire(result);    
}
SharedFence Device::ImportSharedFence (SharedFenceDescriptor const* descriptor) const {
    auto result = wgpuDeviceImportSharedFence(Get(), reinterpret_cast<WGPUSharedFenceDescriptor const* >(descriptor));    
    return SharedFence::Acquire(result);    
}
Texture Device::CreateErrorTexture (TextureDescriptor const* descriptor) const {
    auto result = wgpuDeviceCreateErrorTexture(Get(), reinterpret_cast<WGPUTextureDescriptor const* >(descriptor));    
    return Texture::Acquire(result);    
}
void Device::Destroy () const {
    wgpuDeviceDestroy(Get());    
}
Status Device::GetAHardwareBufferProperties (void * handle, AHardwareBufferProperties * properties) const {
    auto result = wgpuDeviceGetAHardwareBufferProperties(Get(), handle, reinterpret_cast<WGPUAHardwareBufferProperties * >(properties));    
    return static_cast<Status>(result);    
}
Status Device::GetLimits (SupportedLimits * limits) const {
    auto result = wgpuDeviceGetLimits(Get(), reinterpret_cast<WGPUSupportedLimits * >(limits));    
    return static_cast<Status>(result);    
}
bool Device::HasFeature (FeatureName feature) const {
    auto result = wgpuDeviceHasFeature(Get(), *reinterpret_cast<WGPUFeatureName const*>(&feature));    
    return result;    
}
size_t Device::EnumerateFeatures (FeatureName * features) const {
    auto result = wgpuDeviceEnumerateFeatures(Get(), reinterpret_cast<WGPUFeatureName * >(features));    
    return result;    
}
Adapter Device::GetAdapter () const {
    auto result = wgpuDeviceGetAdapter(Get());    
    return Adapter::Acquire(result);    
}
Queue Device::GetQueue () const {
    auto result = wgpuDeviceGetQueue(Get());    
    return Queue::Acquire(result);    
}
void Device::InjectError (ErrorType type, char const* message) const {
    wgpuDeviceInjectError(Get(), *reinterpret_cast<WGPUErrorType const*>(&type), message);    
}
void Device::InjectError2 (ErrorType type, StringView message) const {
    wgpuDeviceInjectError2(Get(), *reinterpret_cast<WGPUErrorType const*>(&type), *reinterpret_cast<WGPUStringView const*>(&message));    
}
void Device::ForceLoss (DeviceLostReason type, char const* message) const {
    wgpuDeviceForceLoss(Get(), *reinterpret_cast<WGPUDeviceLostReason const*>(&type), message);    
}
void Device::ForceLoss2 (DeviceLostReason type, StringView message) const {
    wgpuDeviceForceLoss2(Get(), *reinterpret_cast<WGPUDeviceLostReason const*>(&type), *reinterpret_cast<WGPUStringView const*>(&message));    
}
void Device::Tick () const {
    wgpuDeviceTick(Get());    
}
void Device::SetUncapturedErrorCallback (ErrorCallback callback, void * userdata) const {
    wgpuDeviceSetUncapturedErrorCallback(Get(), *reinterpret_cast<WGPUErrorCallback const*>(&callback), userdata);    
}
void Device::SetLoggingCallback (LoggingCallback callback, void * userdata) const {
    wgpuDeviceSetLoggingCallback(Get(), *reinterpret_cast<WGPULoggingCallback const*>(&callback), userdata);    
}
void Device::SetDeviceLostCallback (DeviceLostCallback callback, void * userdata) const {
    wgpuDeviceSetDeviceLostCallback(Get(), *reinterpret_cast<WGPUDeviceLostCallback const*>(&callback), userdata);    
}
void Device::PushErrorScope (ErrorFilter filter) const {
    wgpuDevicePushErrorScope(Get(), *reinterpret_cast<WGPUErrorFilter const*>(&filter));    
}
void Device::PopErrorScope (ErrorCallback oldCallback, void * userdata) const {
    wgpuDevicePopErrorScope(Get(), *reinterpret_cast<WGPUErrorCallback const*>(&oldCallback), userdata);    
}
void Device::SetLabel (char const* label) const {
    wgpuDeviceSetLabel(Get(), label);    
}
void Device::SetLabel2 (NullableStringView label) const {
    wgpuDeviceSetLabel2(Get(), *reinterpret_cast<WGPUStringView const*>(&label));    
}
void Device::ValidateTextureDescriptor (TextureDescriptor const* descriptor) const {
    wgpuDeviceValidateTextureDescriptor(Get(), reinterpret_cast<WGPUTextureDescriptor const* >(descriptor));    
}
TextureUsage Device::GetSupportedSurfaceUsage (Surface surface) const {
    auto result = wgpuDeviceGetSupportedSurfaceUsage(Get(), *reinterpret_cast<WGPUSurface const*>(&surface));    
    return static_cast<TextureUsage>(result);    
}

void Device::WGPUAddRef(WGPUDevice handle) {
    if (handle != nullptr) {
        wgpuDeviceAddRef(handle);
    }
}
void Device::WGPURelease(WGPUDevice handle) {
    if (handle != nullptr) {
        wgpuDeviceRelease(handle);
    }
}

// ExternalTexture implementation

void ExternalTexture::SetLabel (char const* label) const {
    wgpuExternalTextureSetLabel(Get(), label);    
}
void ExternalTexture::SetLabel2 (NullableStringView label) const {
    wgpuExternalTextureSetLabel2(Get(), *reinterpret_cast<WGPUStringView const*>(&label));    
}
void ExternalTexture::Destroy () const {
    wgpuExternalTextureDestroy(Get());    
}
void ExternalTexture::Expire () const {
    wgpuExternalTextureExpire(Get());    
}
void ExternalTexture::Refresh () const {
    wgpuExternalTextureRefresh(Get());    
}

void ExternalTexture::WGPUAddRef(WGPUExternalTexture handle) {
    if (handle != nullptr) {
        wgpuExternalTextureAddRef(handle);
    }
}
void ExternalTexture::WGPURelease(WGPUExternalTexture handle) {
    if (handle != nullptr) {
        wgpuExternalTextureRelease(handle);
    }
}

// SharedBufferMemory implementation

void SharedBufferMemory::SetLabel (char const* label) const {
    wgpuSharedBufferMemorySetLabel(Get(), label);    
}
void SharedBufferMemory::SetLabel2 (NullableStringView label) const {
    wgpuSharedBufferMemorySetLabel2(Get(), *reinterpret_cast<WGPUStringView const*>(&label));    
}
Status SharedBufferMemory::GetProperties (SharedBufferMemoryProperties * properties) const {
    auto result = wgpuSharedBufferMemoryGetProperties(Get(), reinterpret_cast<WGPUSharedBufferMemoryProperties * >(properties));    
    return static_cast<Status>(result);    
}
Buffer SharedBufferMemory::CreateBuffer (BufferDescriptor const* descriptor) const {
    auto result = wgpuSharedBufferMemoryCreateBuffer(Get(), reinterpret_cast<WGPUBufferDescriptor const* >(descriptor));    
    return Buffer::Acquire(result);    
}
Status SharedBufferMemory::BeginAccess (Buffer buffer, SharedBufferMemoryBeginAccessDescriptor const* descriptor) const {
    auto result = wgpuSharedBufferMemoryBeginAccess(Get(), *reinterpret_cast<WGPUBuffer const*>(&buffer), reinterpret_cast<WGPUSharedBufferMemoryBeginAccessDescriptor const* >(descriptor));    
    return static_cast<Status>(result);    
}
Status SharedBufferMemory::EndAccess (Buffer buffer, SharedBufferMemoryEndAccessState * descriptor) const {
    auto result = wgpuSharedBufferMemoryEndAccess(Get(), *reinterpret_cast<WGPUBuffer const*>(&buffer), reinterpret_cast<WGPUSharedBufferMemoryEndAccessState * >(descriptor));    
    return static_cast<Status>(result);    
}
bool SharedBufferMemory::IsDeviceLost () const {
    auto result = wgpuSharedBufferMemoryIsDeviceLost(Get());    
    return result;    
}

void SharedBufferMemory::WGPUAddRef(WGPUSharedBufferMemory handle) {
    if (handle != nullptr) {
        wgpuSharedBufferMemoryAddRef(handle);
    }
}
void SharedBufferMemory::WGPURelease(WGPUSharedBufferMemory handle) {
    if (handle != nullptr) {
        wgpuSharedBufferMemoryRelease(handle);
    }
}

// SharedTextureMemory implementation

void SharedTextureMemory::SetLabel (char const* label) const {
    wgpuSharedTextureMemorySetLabel(Get(), label);    
}
void SharedTextureMemory::SetLabel2 (NullableStringView label) const {
    wgpuSharedTextureMemorySetLabel2(Get(), *reinterpret_cast<WGPUStringView const*>(&label));    
}
Status SharedTextureMemory::GetProperties (SharedTextureMemoryProperties * properties) const {
    auto result = wgpuSharedTextureMemoryGetProperties(Get(), reinterpret_cast<WGPUSharedTextureMemoryProperties * >(properties));    
    return static_cast<Status>(result);    
}
Texture SharedTextureMemory::CreateTexture (TextureDescriptor const* descriptor) const {
    auto result = wgpuSharedTextureMemoryCreateTexture(Get(), reinterpret_cast<WGPUTextureDescriptor const* >(descriptor));    
    return Texture::Acquire(result);    
}
Status SharedTextureMemory::BeginAccess (Texture texture, SharedTextureMemoryBeginAccessDescriptor const* descriptor) const {
    auto result = wgpuSharedTextureMemoryBeginAccess(Get(), *reinterpret_cast<WGPUTexture const*>(&texture), reinterpret_cast<WGPUSharedTextureMemoryBeginAccessDescriptor const* >(descriptor));    
    return static_cast<Status>(result);    
}
Status SharedTextureMemory::EndAccess (Texture texture, SharedTextureMemoryEndAccessState * descriptor) const {
    auto result = wgpuSharedTextureMemoryEndAccess(Get(), *reinterpret_cast<WGPUTexture const*>(&texture), reinterpret_cast<WGPUSharedTextureMemoryEndAccessState * >(descriptor));    
    return static_cast<Status>(result);    
}
bool SharedTextureMemory::IsDeviceLost () const {
    auto result = wgpuSharedTextureMemoryIsDeviceLost(Get());    
    return result;    
}

void SharedTextureMemory::WGPUAddRef(WGPUSharedTextureMemory handle) {
    if (handle != nullptr) {
        wgpuSharedTextureMemoryAddRef(handle);
    }
}
void SharedTextureMemory::WGPURelease(WGPUSharedTextureMemory handle) {
    if (handle != nullptr) {
        wgpuSharedTextureMemoryRelease(handle);
    }
}

// SharedFence implementation

void SharedFence::ExportInfo (SharedFenceExportInfo * info) const {
    wgpuSharedFenceExportInfo(Get(), reinterpret_cast<WGPUSharedFenceExportInfo * >(info));    
}

void SharedFence::WGPUAddRef(WGPUSharedFence handle) {
    if (handle != nullptr) {
        wgpuSharedFenceAddRef(handle);
    }
}
void SharedFence::WGPURelease(WGPUSharedFence handle) {
    if (handle != nullptr) {
        wgpuSharedFenceRelease(handle);
    }
}

// Instance implementation

Surface Instance::CreateSurface (SurfaceDescriptor const* descriptor) const {
    auto result = wgpuInstanceCreateSurface(Get(), reinterpret_cast<WGPUSurfaceDescriptor const* >(descriptor));    
    return Surface::Acquire(result);    
}
void Instance::ProcessEvents () const {
    wgpuInstanceProcessEvents(Get());    
}
WaitStatus Instance::WaitAny (size_t futureCount, FutureWaitInfo * futures, uint64_t timeoutNS) const {
    auto result = wgpuInstanceWaitAny(Get(), futureCount, reinterpret_cast<WGPUFutureWaitInfo * >(futures), timeoutNS);    
    return static_cast<WaitStatus>(result);    
}
void Instance::RequestAdapter (RequestAdapterOptions const* options, RequestAdapterCallback callback, void * userdata) const {
    wgpuInstanceRequestAdapter(Get(), reinterpret_cast<WGPURequestAdapterOptions const* >(options), *reinterpret_cast<WGPURequestAdapterCallback const*>(&callback), userdata);    
}
bool Instance::HasWGSLLanguageFeature (WGSLFeatureName feature) const {
    auto result = wgpuInstanceHasWGSLLanguageFeature(Get(), *reinterpret_cast<WGPUWGSLFeatureName const*>(&feature));    
    return result;    
}
size_t Instance::EnumerateWGSLLanguageFeatures (WGSLFeatureName * features) const {
    auto result = wgpuInstanceEnumerateWGSLLanguageFeatures(Get(), reinterpret_cast<WGPUWGSLFeatureName * >(features));    
    return result;    
}

void Instance::WGPUAddRef(WGPUInstance handle) {
    if (handle != nullptr) {
        wgpuInstanceAddRef(handle);
    }
}
void Instance::WGPURelease(WGPUInstance handle) {
    if (handle != nullptr) {
        wgpuInstanceRelease(handle);
    }
}

// PipelineLayout implementation

void PipelineLayout::SetLabel (char const* label) const {
    wgpuPipelineLayoutSetLabel(Get(), label);    
}
void PipelineLayout::SetLabel2 (NullableStringView label) const {
    wgpuPipelineLayoutSetLabel2(Get(), *reinterpret_cast<WGPUStringView const*>(&label));    
}

void PipelineLayout::WGPUAddRef(WGPUPipelineLayout handle) {
    if (handle != nullptr) {
        wgpuPipelineLayoutAddRef(handle);
    }
}
void PipelineLayout::WGPURelease(WGPUPipelineLayout handle) {
    if (handle != nullptr) {
        wgpuPipelineLayoutRelease(handle);
    }
}

// QuerySet implementation

void QuerySet::SetLabel (char const* label) const {
    wgpuQuerySetSetLabel(Get(), label);    
}
void QuerySet::SetLabel2 (NullableStringView label) const {
    wgpuQuerySetSetLabel2(Get(), *reinterpret_cast<WGPUStringView const*>(&label));    
}
QueryType QuerySet::GetType () const {
    auto result = wgpuQuerySetGetType(Get());    
    return static_cast<QueryType>(result);    
}
uint32_t QuerySet::GetCount () const {
    auto result = wgpuQuerySetGetCount(Get());    
    return result;    
}
void QuerySet::Destroy () const {
    wgpuQuerySetDestroy(Get());    
}

void QuerySet::WGPUAddRef(WGPUQuerySet handle) {
    if (handle != nullptr) {
        wgpuQuerySetAddRef(handle);
    }
}
void QuerySet::WGPURelease(WGPUQuerySet handle) {
    if (handle != nullptr) {
        wgpuQuerySetRelease(handle);
    }
}

// Queue implementation

void Queue::Submit (size_t commandCount, CommandBuffer const* commands) const {
    wgpuQueueSubmit(Get(), commandCount, reinterpret_cast<WGPUCommandBuffer const* >(commands));    
}
void Queue::WriteBuffer (Buffer buffer, uint64_t bufferOffset, void const* data, size_t size) const {
    wgpuQueueWriteBuffer(Get(), *reinterpret_cast<WGPUBuffer const*>(&buffer), bufferOffset, data, size);    
}
void Queue::WriteTexture (ImageCopyTexture const* destination, void const* data, size_t dataSize, TextureDataLayout const* dataLayout, Extent3D const* writeSize) const {
    wgpuQueueWriteTexture(Get(), reinterpret_cast<WGPUImageCopyTexture const* >(destination), data, dataSize, reinterpret_cast<WGPUTextureDataLayout const* >(dataLayout), reinterpret_cast<WGPUExtent3D const* >(writeSize));    
}
void Queue::CopyTextureForBrowser (ImageCopyTexture const* source, ImageCopyTexture const* destination, Extent3D const* copySize, CopyTextureForBrowserOptions const* options) const {
    wgpuQueueCopyTextureForBrowser(Get(), reinterpret_cast<WGPUImageCopyTexture const* >(source), reinterpret_cast<WGPUImageCopyTexture const* >(destination), reinterpret_cast<WGPUExtent3D const* >(copySize), reinterpret_cast<WGPUCopyTextureForBrowserOptions const* >(options));    
}
void Queue::CopyExternalTextureForBrowser (ImageCopyExternalTexture const* source, ImageCopyTexture const* destination, Extent3D const* copySize, CopyTextureForBrowserOptions const* options) const {
    wgpuQueueCopyExternalTextureForBrowser(Get(), reinterpret_cast<WGPUImageCopyExternalTexture const* >(source), reinterpret_cast<WGPUImageCopyTexture const* >(destination), reinterpret_cast<WGPUExtent3D const* >(copySize), reinterpret_cast<WGPUCopyTextureForBrowserOptions const* >(options));    
}
void Queue::SetLabel (char const* label) const {
    wgpuQueueSetLabel(Get(), label);    
}
void Queue::SetLabel2 (NullableStringView label) const {
    wgpuQueueSetLabel2(Get(), *reinterpret_cast<WGPUStringView const*>(&label));    
}

void Queue::WGPUAddRef(WGPUQueue handle) {
    if (handle != nullptr) {
        wgpuQueueAddRef(handle);
    }
}
void Queue::WGPURelease(WGPUQueue handle) {
    if (handle != nullptr) {
        wgpuQueueRelease(handle);
    }
}

// RenderBundle implementation

void RenderBundle::SetLabel (char const* label) const {
    wgpuRenderBundleSetLabel(Get(), label);    
}
void RenderBundle::SetLabel2 (NullableStringView label) const {
    wgpuRenderBundleSetLabel2(Get(), *reinterpret_cast<WGPUStringView const*>(&label));    
}

void RenderBundle::WGPUAddRef(WGPURenderBundle handle) {
    if (handle != nullptr) {
        wgpuRenderBundleAddRef(handle);
    }
}
void RenderBundle::WGPURelease(WGPURenderBundle handle) {
    if (handle != nullptr) {
        wgpuRenderBundleRelease(handle);
    }
}

// RenderBundleEncoder implementation

void RenderBundleEncoder::SetPipeline (RenderPipeline pipeline) const {
    wgpuRenderBundleEncoderSetPipeline(Get(), *reinterpret_cast<WGPURenderPipeline const*>(&pipeline));    
}
void RenderBundleEncoder::SetBindGroup (uint32_t groupIndex, BindGroup group, size_t dynamicOffsetCount, uint32_t const* dynamicOffsets) const {
    wgpuRenderBundleEncoderSetBindGroup(Get(), groupIndex, *reinterpret_cast<WGPUBindGroup const*>(&group), dynamicOffsetCount, dynamicOffsets);    
}
void RenderBundleEncoder::Draw (uint32_t vertexCount, uint32_t instanceCount, uint32_t firstVertex, uint32_t firstInstance) const {
    wgpuRenderBundleEncoderDraw(Get(), vertexCount, instanceCount, firstVertex, firstInstance);    
}
void RenderBundleEncoder::DrawIndexed (uint32_t indexCount, uint32_t instanceCount, uint32_t firstIndex, int32_t baseVertex, uint32_t firstInstance) const {
    wgpuRenderBundleEncoderDrawIndexed(Get(), indexCount, instanceCount, firstIndex, baseVertex, firstInstance);    
}
void RenderBundleEncoder::DrawIndirect (Buffer indirectBuffer, uint64_t indirectOffset) const {
    wgpuRenderBundleEncoderDrawIndirect(Get(), *reinterpret_cast<WGPUBuffer const*>(&indirectBuffer), indirectOffset);    
}
void RenderBundleEncoder::DrawIndexedIndirect (Buffer indirectBuffer, uint64_t indirectOffset) const {
    wgpuRenderBundleEncoderDrawIndexedIndirect(Get(), *reinterpret_cast<WGPUBuffer const*>(&indirectBuffer), indirectOffset);    
}
void RenderBundleEncoder::InsertDebugMarker (char const* markerLabel) const {
    wgpuRenderBundleEncoderInsertDebugMarker(Get(), markerLabel);    
}
void RenderBundleEncoder::InsertDebugMarker2 (StringView markerLabel) const {
    wgpuRenderBundleEncoderInsertDebugMarker2(Get(), *reinterpret_cast<WGPUStringView const*>(&markerLabel));    
}
void RenderBundleEncoder::PopDebugGroup () const {
    wgpuRenderBundleEncoderPopDebugGroup(Get());    
}
void RenderBundleEncoder::PushDebugGroup (char const* groupLabel) const {
    wgpuRenderBundleEncoderPushDebugGroup(Get(), groupLabel);    
}
void RenderBundleEncoder::PushDebugGroup2 (StringView groupLabel) const {
    wgpuRenderBundleEncoderPushDebugGroup2(Get(), *reinterpret_cast<WGPUStringView const*>(&groupLabel));    
}
void RenderBundleEncoder::SetVertexBuffer (uint32_t slot, Buffer buffer, uint64_t offset, uint64_t size) const {
    wgpuRenderBundleEncoderSetVertexBuffer(Get(), slot, *reinterpret_cast<WGPUBuffer const*>(&buffer), offset, size);    
}
void RenderBundleEncoder::SetIndexBuffer (Buffer buffer, IndexFormat format, uint64_t offset, uint64_t size) const {
    wgpuRenderBundleEncoderSetIndexBuffer(Get(), *reinterpret_cast<WGPUBuffer const*>(&buffer), *reinterpret_cast<WGPUIndexFormat const*>(&format), offset, size);    
}
RenderBundle RenderBundleEncoder::Finish (RenderBundleDescriptor const* descriptor) const {
    auto result = wgpuRenderBundleEncoderFinish(Get(), reinterpret_cast<WGPURenderBundleDescriptor const* >(descriptor));    
    return RenderBundle::Acquire(result);    
}
void RenderBundleEncoder::SetLabel (char const* label) const {
    wgpuRenderBundleEncoderSetLabel(Get(), label);    
}
void RenderBundleEncoder::SetLabel2 (NullableStringView label) const {
    wgpuRenderBundleEncoderSetLabel2(Get(), *reinterpret_cast<WGPUStringView const*>(&label));    
}

void RenderBundleEncoder::WGPUAddRef(WGPURenderBundleEncoder handle) {
    if (handle != nullptr) {
        wgpuRenderBundleEncoderAddRef(handle);
    }
}
void RenderBundleEncoder::WGPURelease(WGPURenderBundleEncoder handle) {
    if (handle != nullptr) {
        wgpuRenderBundleEncoderRelease(handle);
    }
}

// RenderPassEncoder implementation

void RenderPassEncoder::SetPipeline (RenderPipeline pipeline) const {
    wgpuRenderPassEncoderSetPipeline(Get(), *reinterpret_cast<WGPURenderPipeline const*>(&pipeline));    
}
void RenderPassEncoder::SetBindGroup (uint32_t groupIndex, BindGroup group, size_t dynamicOffsetCount, uint32_t const* dynamicOffsets) const {
    wgpuRenderPassEncoderSetBindGroup(Get(), groupIndex, *reinterpret_cast<WGPUBindGroup const*>(&group), dynamicOffsetCount, dynamicOffsets);    
}
void RenderPassEncoder::Draw (uint32_t vertexCount, uint32_t instanceCount, uint32_t firstVertex, uint32_t firstInstance) const {
    wgpuRenderPassEncoderDraw(Get(), vertexCount, instanceCount, firstVertex, firstInstance);    
}
void RenderPassEncoder::DrawIndexed (uint32_t indexCount, uint32_t instanceCount, uint32_t firstIndex, int32_t baseVertex, uint32_t firstInstance) const {
    wgpuRenderPassEncoderDrawIndexed(Get(), indexCount, instanceCount, firstIndex, baseVertex, firstInstance);    
}
void RenderPassEncoder::DrawIndirect (Buffer indirectBuffer, uint64_t indirectOffset) const {
    wgpuRenderPassEncoderDrawIndirect(Get(), *reinterpret_cast<WGPUBuffer const*>(&indirectBuffer), indirectOffset);    
}
void RenderPassEncoder::DrawIndexedIndirect (Buffer indirectBuffer, uint64_t indirectOffset) const {
    wgpuRenderPassEncoderDrawIndexedIndirect(Get(), *reinterpret_cast<WGPUBuffer const*>(&indirectBuffer), indirectOffset);    
}
void RenderPassEncoder::ExecuteBundles (size_t bundleCount, RenderBundle const* bundles) const {
    wgpuRenderPassEncoderExecuteBundles(Get(), bundleCount, reinterpret_cast<WGPURenderBundle const* >(bundles));    
}
void RenderPassEncoder::InsertDebugMarker (char const* markerLabel) const {
    wgpuRenderPassEncoderInsertDebugMarker(Get(), markerLabel);    
}
void RenderPassEncoder::InsertDebugMarker2 (StringView markerLabel) const {
    wgpuRenderPassEncoderInsertDebugMarker2(Get(), *reinterpret_cast<WGPUStringView const*>(&markerLabel));    
}
void RenderPassEncoder::PopDebugGroup () const {
    wgpuRenderPassEncoderPopDebugGroup(Get());    
}
void RenderPassEncoder::PushDebugGroup (char const* groupLabel) const {
    wgpuRenderPassEncoderPushDebugGroup(Get(), groupLabel);    
}
void RenderPassEncoder::PushDebugGroup2 (StringView groupLabel) const {
    wgpuRenderPassEncoderPushDebugGroup2(Get(), *reinterpret_cast<WGPUStringView const*>(&groupLabel));    
}
void RenderPassEncoder::SetStencilReference (uint32_t reference) const {
    wgpuRenderPassEncoderSetStencilReference(Get(), reference);    
}
void RenderPassEncoder::SetBlendConstant (Color const* color) const {
    wgpuRenderPassEncoderSetBlendConstant(Get(), reinterpret_cast<WGPUColor const* >(color));    
}
void RenderPassEncoder::SetViewport (float x, float y, float width, float height, float minDepth, float maxDepth) const {
    wgpuRenderPassEncoderSetViewport(Get(), x, y, width, height, minDepth, maxDepth);    
}
void RenderPassEncoder::SetScissorRect (uint32_t x, uint32_t y, uint32_t width, uint32_t height) const {
    wgpuRenderPassEncoderSetScissorRect(Get(), x, y, width, height);    
}
void RenderPassEncoder::SetVertexBuffer (uint32_t slot, Buffer buffer, uint64_t offset, uint64_t size) const {
    wgpuRenderPassEncoderSetVertexBuffer(Get(), slot, *reinterpret_cast<WGPUBuffer const*>(&buffer), offset, size);    
}
void RenderPassEncoder::SetIndexBuffer (Buffer buffer, IndexFormat format, uint64_t offset, uint64_t size) const {
    wgpuRenderPassEncoderSetIndexBuffer(Get(), *reinterpret_cast<WGPUBuffer const*>(&buffer), *reinterpret_cast<WGPUIndexFormat const*>(&format), offset, size);    
}
void RenderPassEncoder::BeginOcclusionQuery (uint32_t queryIndex) const {
    wgpuRenderPassEncoderBeginOcclusionQuery(Get(), queryIndex);    
}
void RenderPassEncoder::EndOcclusionQuery () const {
    wgpuRenderPassEncoderEndOcclusionQuery(Get());    
}
void RenderPassEncoder::WriteTimestamp (QuerySet querySet, uint32_t queryIndex) const {
    wgpuRenderPassEncoderWriteTimestamp(Get(), *reinterpret_cast<WGPUQuerySet const*>(&querySet), queryIndex);    
}
void RenderPassEncoder::PixelLocalStorageBarrier () const {
    wgpuRenderPassEncoderPixelLocalStorageBarrier(Get());    
}
void RenderPassEncoder::End () const {
    wgpuRenderPassEncoderEnd(Get());    
}
void RenderPassEncoder::SetLabel (char const* label) const {
    wgpuRenderPassEncoderSetLabel(Get(), label);    
}
void RenderPassEncoder::SetLabel2 (NullableStringView label) const {
    wgpuRenderPassEncoderSetLabel2(Get(), *reinterpret_cast<WGPUStringView const*>(&label));    
}

void RenderPassEncoder::WGPUAddRef(WGPURenderPassEncoder handle) {
    if (handle != nullptr) {
        wgpuRenderPassEncoderAddRef(handle);
    }
}
void RenderPassEncoder::WGPURelease(WGPURenderPassEncoder handle) {
    if (handle != nullptr) {
        wgpuRenderPassEncoderRelease(handle);
    }
}

// RenderPipeline implementation

BindGroupLayout RenderPipeline::GetBindGroupLayout (uint32_t groupIndex) const {
    auto result = wgpuRenderPipelineGetBindGroupLayout(Get(), groupIndex);    
    return BindGroupLayout::Acquire(result);    
}
void RenderPipeline::SetLabel (char const* label) const {
    wgpuRenderPipelineSetLabel(Get(), label);    
}
void RenderPipeline::SetLabel2 (NullableStringView label) const {
    wgpuRenderPipelineSetLabel2(Get(), *reinterpret_cast<WGPUStringView const*>(&label));    
}

void RenderPipeline::WGPUAddRef(WGPURenderPipeline handle) {
    if (handle != nullptr) {
        wgpuRenderPipelineAddRef(handle);
    }
}
void RenderPipeline::WGPURelease(WGPURenderPipeline handle) {
    if (handle != nullptr) {
        wgpuRenderPipelineRelease(handle);
    }
}

// Sampler implementation

void Sampler::SetLabel (char const* label) const {
    wgpuSamplerSetLabel(Get(), label);    
}
void Sampler::SetLabel2 (NullableStringView label) const {
    wgpuSamplerSetLabel2(Get(), *reinterpret_cast<WGPUStringView const*>(&label));    
}

void Sampler::WGPUAddRef(WGPUSampler handle) {
    if (handle != nullptr) {
        wgpuSamplerAddRef(handle);
    }
}
void Sampler::WGPURelease(WGPUSampler handle) {
    if (handle != nullptr) {
        wgpuSamplerRelease(handle);
    }
}

// ShaderModule implementation

void ShaderModule::GetCompilationInfo (CompilationInfoCallback callback, void * userdata) const {
    wgpuShaderModuleGetCompilationInfo(Get(), *reinterpret_cast<WGPUCompilationInfoCallback const*>(&callback), userdata);    
}
void ShaderModule::SetLabel (char const* label) const {
    wgpuShaderModuleSetLabel(Get(), label);    
}
void ShaderModule::SetLabel2 (NullableStringView label) const {
    wgpuShaderModuleSetLabel2(Get(), *reinterpret_cast<WGPUStringView const*>(&label));    
}

void ShaderModule::WGPUAddRef(WGPUShaderModule handle) {
    if (handle != nullptr) {
        wgpuShaderModuleAddRef(handle);
    }
}
void ShaderModule::WGPURelease(WGPUShaderModule handle) {
    if (handle != nullptr) {
        wgpuShaderModuleRelease(handle);
    }
}

// Surface implementation

void Surface::Configure (SurfaceConfiguration const* config) const {
    wgpuSurfaceConfigure(Get(), reinterpret_cast<WGPUSurfaceConfiguration const* >(config));    
}
Status Surface::GetCapabilities (Adapter adapter, SurfaceCapabilities * capabilities) const {
    auto result = wgpuSurfaceGetCapabilities(Get(), *reinterpret_cast<WGPUAdapter const*>(&adapter), reinterpret_cast<WGPUSurfaceCapabilities * >(capabilities));    
    return static_cast<Status>(result);    
}
void Surface::GetCurrentTexture (SurfaceTexture * surfaceTexture) const {
    wgpuSurfaceGetCurrentTexture(Get(), reinterpret_cast<WGPUSurfaceTexture * >(surfaceTexture));    
}
TextureFormat Surface::GetPreferredFormat (Adapter adapter) const {
    auto result = wgpuSurfaceGetPreferredFormat(Get(), *reinterpret_cast<WGPUAdapter const*>(&adapter));    
    return static_cast<TextureFormat>(result);    
}
void Surface::Present () const {
    wgpuSurfacePresent(Get());    
}
void Surface::Unconfigure () const {
    wgpuSurfaceUnconfigure(Get());    
}
void Surface::SetLabel (char const* label) const {
    wgpuSurfaceSetLabel(Get(), label);    
}
void Surface::SetLabel2 (NullableStringView label) const {
    wgpuSurfaceSetLabel2(Get(), *reinterpret_cast<WGPUStringView const*>(&label));    
}

void Surface::WGPUAddRef(WGPUSurface handle) {
    if (handle != nullptr) {
        wgpuSurfaceAddRef(handle);
    }
}
void Surface::WGPURelease(WGPUSurface handle) {
    if (handle != nullptr) {
        wgpuSurfaceRelease(handle);
    }
}

// SwapChain implementation

TextureView SwapChain::GetCurrentTextureView () const {
    auto result = wgpuSwapChainGetCurrentTextureView(Get());    
    return TextureView::Acquire(result);    
}
Texture SwapChain::GetCurrentTexture () const {
    auto result = wgpuSwapChainGetCurrentTexture(Get());    
    return Texture::Acquire(result);    
}
void SwapChain::Present () const {
    wgpuSwapChainPresent(Get());    
}

void SwapChain::WGPUAddRef(WGPUSwapChain handle) {
    if (handle != nullptr) {
        wgpuSwapChainAddRef(handle);
    }
}
void SwapChain::WGPURelease(WGPUSwapChain handle) {
    if (handle != nullptr) {
        wgpuSwapChainRelease(handle);
    }
}

// Texture implementation

TextureView Texture::CreateView (TextureViewDescriptor const* descriptor) const {
    auto result = wgpuTextureCreateView(Get(), reinterpret_cast<WGPUTextureViewDescriptor const* >(descriptor));    
    return TextureView::Acquire(result);    
}
TextureView Texture::CreateErrorView (TextureViewDescriptor const* descriptor) const {
    auto result = wgpuTextureCreateErrorView(Get(), reinterpret_cast<WGPUTextureViewDescriptor const* >(descriptor));    
    return TextureView::Acquire(result);    
}
void Texture::SetLabel (char const* label) const {
    wgpuTextureSetLabel(Get(), label);    
}
void Texture::SetLabel2 (NullableStringView label) const {
    wgpuTextureSetLabel2(Get(), *reinterpret_cast<WGPUStringView const*>(&label));    
}
uint32_t Texture::GetWidth () const {
    auto result = wgpuTextureGetWidth(Get());    
    return result;    
}
uint32_t Texture::GetHeight () const {
    auto result = wgpuTextureGetHeight(Get());    
    return result;    
}
uint32_t Texture::GetDepthOrArrayLayers () const {
    auto result = wgpuTextureGetDepthOrArrayLayers(Get());    
    return result;    
}
uint32_t Texture::GetMipLevelCount () const {
    auto result = wgpuTextureGetMipLevelCount(Get());    
    return result;    
}
uint32_t Texture::GetSampleCount () const {
    auto result = wgpuTextureGetSampleCount(Get());    
    return result;    
}
TextureDimension Texture::GetDimension () const {
    auto result = wgpuTextureGetDimension(Get());    
    return static_cast<TextureDimension>(result);    
}
TextureFormat Texture::GetFormat () const {
    auto result = wgpuTextureGetFormat(Get());    
    return static_cast<TextureFormat>(result);    
}
TextureUsage Texture::GetUsage () const {
    auto result = wgpuTextureGetUsage(Get());    
    return static_cast<TextureUsage>(result);    
}
void Texture::Destroy () const {
    wgpuTextureDestroy(Get());    
}

void Texture::WGPUAddRef(WGPUTexture handle) {
    if (handle != nullptr) {
        wgpuTextureAddRef(handle);
    }
}
void Texture::WGPURelease(WGPUTexture handle) {
    if (handle != nullptr) {
        wgpuTextureRelease(handle);
    }
}

// TextureView implementation

void TextureView::SetLabel (char const* label) const {
    wgpuTextureViewSetLabel(Get(), label);    
}
void TextureView::SetLabel2 (NullableStringView label) const {
    wgpuTextureViewSetLabel2(Get(), *reinterpret_cast<WGPUStringView const*>(&label));    
}

void TextureView::WGPUAddRef(WGPUTextureView handle) {
    if (handle != nullptr) {
        wgpuTextureViewAddRef(handle);
    }
}
void TextureView::WGPURelease(WGPUTextureView handle) {
    if (handle != nullptr) {
        wgpuTextureViewRelease(handle);
    }
}
Instance CreateInstance (InstanceDescriptor const* descriptor) {
    auto result = wgpuCreateInstance(reinterpret_cast<WGPUInstanceDescriptor const* >(descriptor));    
    return Instance::Acquire(result);    
}
Status GetInstanceFeatures (InstanceFeatures * features) {
    auto result = wgpuGetInstanceFeatures(reinterpret_cast<WGPUInstanceFeatures * >(features));    
    return static_cast<Status>(result);    
}


    StringView::operator std::string_view() const {
        const bool isNull = this->data == nullptr;
        const bool useStrlen = this->length == SIZE_MAX;
        //DAWN_ASSERT(!(isNull && useStrlen));
        return std::string_view(this->data, isNull      ? 0
                                            : useStrlen ? std::strlen(this->data)
                                                        : this->length);
    }

    NullableStringView::operator std::optional<std::string_view>() const {
        const bool isNull = this->data == nullptr;
        const bool useStrlen = this->length == SIZE_MAX;
        if (isNull && useStrlen) {
            return std::nullopt;
        }
        return std::string_view(this->data, isNull      ? 0
                                            : useStrlen ? std::strlen(this->data)
                                                        : this->length);
    }

} //namespace wgpu