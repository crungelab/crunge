#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/conversions.h>

#include "include/gpu/graphite/Context.h"

#include "include/core/SkColorSpace.h"
#include "include/core/SkPathTypes.h"
#include "include/core/SkTraceMemoryDump.h"
#include "include/effects/SkRuntimeEffect.h"
#include "include/gpu/graphite/BackendTexture.h"
#include "include/gpu/graphite/PrecompileContext.h"
#include "include/gpu/graphite/Recorder.h"
#include "include/gpu/graphite/Recording.h"
#include "include/gpu/graphite/Surface.h"
#include "include/gpu/graphite/TextureInfo.h"
#include "include/private/base/SkOnce.h"
#include "src/base/SkRectMemcpy.h"
#include "src/core/SkAutoPixmapStorage.h"
#include "src/core/SkColorFilterPriv.h"
#include "src/core/SkConvertPixels.h"
#include "src/core/SkTraceEvent.h"
#include "src/core/SkYUVMath.h"
#include "src/gpu/RefCntedCallback.h"
#include "src/gpu/graphite/AtlasProvider.h"
#include "src/gpu/graphite/BufferManager.h"
#include "src/gpu/graphite/Caps.h"
#include "src/gpu/graphite/ClientMappedBufferManager.h"
#include "src/gpu/graphite/CommandBuffer.h"
#include "src/gpu/graphite/ContextPriv.h"
#include "src/gpu/graphite/DrawAtlas.h"
#include "src/gpu/graphite/GlobalCache.h"
#include "src/gpu/graphite/GraphicsPipeline.h"
#include "src/gpu/graphite/GraphicsPipelineDesc.h"
#include "src/gpu/graphite/Image_Base_Graphite.h"
#include "src/gpu/graphite/Image_Graphite.h"
#include "src/gpu/graphite/KeyContext.h"
#include "src/gpu/graphite/Log.h"
#include "src/gpu/graphite/QueueManager.h"
#include "src/gpu/graphite/RecorderPriv.h"
#include "src/gpu/graphite/RecordingPriv.h"
#include "src/gpu/graphite/Renderer.h"
#include "src/gpu/graphite/RendererProvider.h"
#include "src/gpu/graphite/ResourceProvider.h"
#include "src/gpu/graphite/RuntimeEffectDictionary.h"
#include "src/gpu/graphite/ShaderCodeDictionary.h"
#include "src/gpu/graphite/SharedContext.h"
#include "src/gpu/graphite/Surface_Graphite.h"
#include "src/gpu/graphite/TextureProxyView.h"
#include "src/gpu/graphite/TextureUtils.h"
#include "src/gpu/graphite/task/CopyTask.h"
#include "src/gpu/graphite/task/SynchronizeToCpuTask.h"
#include "src/gpu/graphite/task/UploadTask.h"
#include "src/image/SkSurface_Base.h"
#include "src/sksl/SkSLGraphiteModules.h"

#include <include/gpu/graphite/dawn/DawnBackendContext.h>
#include <tools/window/GraphiteDisplayParams.h>
#include <include/gpu/graphite/BackendTexture.h>
#include <include/gpu/graphite/dawn/DawnGraphiteTypes.h>

#include <crunge/wgpu/pywgpu.h>

namespace py = pybind11;

using namespace skgpu::graphite;

SkSurface* CreateSurface(pywgpu::Texture& _texture, skgpu::graphite::Recorder* recorder) {
    auto backendTex = skgpu::graphite::BackendTextures::MakeDawn(_texture.Get());
    //SkASSERT(recorder);
    auto surface = SkSurfaces::WrapBackendTexture(recorder,
                                                backendTex,
                                                 kBGRA_8888_SkColorType,
                                                 nullptr,
                                                 nullptr);
    //SkASSERT(surface);
    return surface.release();
}

void init_skia_surface_py(py::module &_skia, Registry &registry) {
    _skia.def("create_surface", &CreateSurface);
}
