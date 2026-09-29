https://chromium.googlesource.com/chromium/src/+/main/docs/security/research/graphics/webgpu_technical_report.md

# Ref - Dawn's smart pointer template class

src/dawn/common/Ref.h
src/dawn/common/RefBase.h

## These are the main classes that are ref counted

src/dawn/native/BindGroup.h
  58,23: class BindGroupBase : public ApiObjectBase

src/dawn/native/BindGroupLayout.h
  41,35: class BindGroupLayoutBase final : public ApiObjectBase

src/dawn/native/BindGroupLayoutInternal.h
  66,37: class BindGroupLayoutInternalBase : public ApiObjectBase,

src/dawn/native/Buffer.h
  69,20: class BufferBase : public ApiObjectBase

src/dawn/native/CommandBuffer.h
  48,27: class CommandBufferBase : public ApiObjectBase

src/dawn/native/CommandEncoder.h
  51,30: class CommandEncoder final : public ApiObjectBase

src/dawn/native/ExternalTexture.h
  57,29: class ExternalTextureBase : public ApiObjectBase

src/dawn/native/Pipeline.h
  68,22: class PipelineBase : public ApiObjectBase, public CachedObject

src/dawn/native/PipelineLayout.h
  69,28: class PipelineLayoutBase : public ApiObjectBase,

src/dawn/native/ProgrammableEncoder.h
  46,29: class ProgrammableEncoder : public ApiObjectBase

src/dawn/native/QuerySet.h
  43,22: class QuerySetBase : public ApiObjectBase

src/dawn/native/Queue.h
  64,19: class QueueBase : public ApiObjectBase, public ExecutionQueueBase

src/dawn/native/RenderBundle.h
  50,32: class RenderBundleBase final : public ApiObjectBase

src/dawn/native/Sampler.h
  45,21: class SamplerBase : public ApiObjectBase,

src/dawn/native/ShaderModule.h
  291,26: class ShaderModuleBase : public ApiObjectBase,

src/dawn/native/SharedFence.h
  39,25: class SharedFenceBase : public ApiObjectBase

src/dawn/native/SharedTextureMemory.h
  50,33: class SharedTextureMemoryBase : public ApiObjectBase,

src/dawn/native/SwapChain.h
  44,23: class SwapChainBase : public ApiObjectBase

src/dawn/native/Texture.h
  79,21: class TextureBase : public ApiObjectBase
  207,25: class TextureViewBase : public ApiObjectBase