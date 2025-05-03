#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
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

namespace py = pybind11;

using namespace skgpu::graphite;

void init_skia_context_py_auto(py::module &_skia, Registry &registry) {
    py::class_<skgpu::graphite::Context> Context(_skia, "Context");
    registry.on(_skia, "Context", Context);
        Context
        .def("backend", &skgpu::graphite::Context::backend
            , py::return_value_policy::automatic_reference)
        .def("make_recorder", &skgpu::graphite::Context::makeRecorder
            , py::arg("") = skgpu::graphite::RecorderOptions{}
            , py::return_value_policy::automatic_reference)
        .def("make_precompile_context", &skgpu::graphite::Context::makePrecompileContext
            , py::return_value_policy::automatic_reference)
        .def("insert_recording", &skgpu::graphite::Context::insertRecording
            , py::arg("")
            , py::return_value_policy::automatic_reference)
        .def("submit", &skgpu::graphite::Context::submit
            , py::arg("") = SyncToCpu::kNo
            , py::return_value_policy::automatic_reference)
        .def("has_unfinished_gpu_work", &skgpu::graphite::Context::hasUnfinishedGpuWork
            , py::return_value_policy::automatic_reference)
        .def("async_rescale_and_read_pixels", py::overload_cast<const SkImage *, const SkImageInfo &, const SkIRect &, SkImage::RescaleGamma, SkImage::RescaleMode, void (void *, std::unique_ptr<const SkImage::AsyncReadResult>), void *>(&skgpu::graphite::Context::asyncRescaleAndReadPixels)
            , py::arg("src")
            , py::arg("dst_image_info")
            , py::arg("src_rect")
            , py::arg("rescale_gamma")
            , py::arg("rescale_mode")
            , py::arg("callback")
            , py::arg("context")
            , py::return_value_policy::automatic_reference)
        .def("async_rescale_and_read_pixels", py::overload_cast<const SkSurface *, const SkImageInfo &, const SkIRect &, SkImage::RescaleGamma, SkImage::RescaleMode, void (void *, std::unique_ptr<const SkImage::AsyncReadResult>), void *>(&skgpu::graphite::Context::asyncRescaleAndReadPixels)
            , py::arg("src")
            , py::arg("dst_image_info")
            , py::arg("src_rect")
            , py::arg("rescale_gamma")
            , py::arg("rescale_mode")
            , py::arg("callback")
            , py::arg("context")
            , py::return_value_policy::automatic_reference)
        .def("async_rescale_and_read_pixels_yuv420", py::overload_cast<const SkImage *, SkYUVColorSpace, sk_sp<SkColorSpace>, const SkIRect &, const SkISize &, SkImage::RescaleGamma, SkImage::RescaleMode, void (void *, std::unique_ptr<const SkImage::AsyncReadResult>), void *>(&skgpu::graphite::Context::asyncRescaleAndReadPixelsYUV420)
            , py::arg("src")
            , py::arg("yuv_color_space")
            , py::arg("dst_color_space")
            , py::arg("src_rect")
            , py::arg("dst_size")
            , py::arg("rescale_gamma")
            , py::arg("rescale_mode")
            , py::arg("callback")
            , py::arg("context")
            , py::return_value_policy::automatic_reference)
        .def("async_rescale_and_read_pixels_yuv420", py::overload_cast<const SkSurface *, SkYUVColorSpace, sk_sp<SkColorSpace>, const SkIRect &, const SkISize &, SkImage::RescaleGamma, SkImage::RescaleMode, void (void *, std::unique_ptr<const SkImage::AsyncReadResult>), void *>(&skgpu::graphite::Context::asyncRescaleAndReadPixelsYUV420)
            , py::arg("src")
            , py::arg("yuv_color_space")
            , py::arg("dst_color_space")
            , py::arg("src_rect")
            , py::arg("dst_size")
            , py::arg("rescale_gamma")
            , py::arg("rescale_mode")
            , py::arg("callback")
            , py::arg("context")
            , py::return_value_policy::automatic_reference)
        .def("async_rescale_and_read_pixels_yuva420", py::overload_cast<const SkImage *, SkYUVColorSpace, sk_sp<SkColorSpace>, const SkIRect &, const SkISize &, SkImage::RescaleGamma, SkImage::RescaleMode, void (void *, std::unique_ptr<const SkImage::AsyncReadResult>), void *>(&skgpu::graphite::Context::asyncRescaleAndReadPixelsYUVA420)
            , py::arg("src")
            , py::arg("yuv_color_space")
            , py::arg("dst_color_space")
            , py::arg("src_rect")
            , py::arg("dst_size")
            , py::arg("rescale_gamma")
            , py::arg("rescale_mode")
            , py::arg("callback")
            , py::arg("context")
            , py::return_value_policy::automatic_reference)
        .def("async_rescale_and_read_pixels_yuva420", py::overload_cast<const SkSurface *, SkYUVColorSpace, sk_sp<SkColorSpace>, const SkIRect &, const SkISize &, SkImage::RescaleGamma, SkImage::RescaleMode, void (void *, std::unique_ptr<const SkImage::AsyncReadResult>), void *>(&skgpu::graphite::Context::asyncRescaleAndReadPixelsYUVA420)
            , py::arg("src")
            , py::arg("yuv_color_space")
            , py::arg("dst_color_space")
            , py::arg("src_rect")
            , py::arg("dst_size")
            , py::arg("rescale_gamma")
            , py::arg("rescale_mode")
            , py::arg("callback")
            , py::arg("context")
            , py::return_value_policy::automatic_reference)
        .def("check_async_work_completion", &skgpu::graphite::Context::checkAsyncWorkCompletion
            , py::return_value_policy::automatic_reference)
        .def("delete_backend_texture", &skgpu::graphite::Context::deleteBackendTexture
            , py::arg("")
            , py::return_value_policy::automatic_reference)
        .def("free_gpu_resources", &skgpu::graphite::Context::freeGpuResources
            , py::return_value_policy::automatic_reference)
        .def("perform_deferred_cleanup", &skgpu::graphite::Context::performDeferredCleanup
            , py::arg("ms_not_used")
            , py::return_value_policy::automatic_reference)
        .def("current_budgeted_bytes", &skgpu::graphite::Context::currentBudgetedBytes
            , py::return_value_policy::automatic_reference)
        .def("current_purgeable_bytes", &skgpu::graphite::Context::currentPurgeableBytes
            , py::return_value_policy::automatic_reference)
        .def("max_budgeted_bytes", &skgpu::graphite::Context::maxBudgetedBytes
            , py::return_value_policy::automatic_reference)
        .def("set_max_budgeted_bytes", &skgpu::graphite::Context::setMaxBudgetedBytes
            , py::arg("bytes")
            , py::return_value_policy::automatic_reference)
        .def("dump_memory_statistics", &skgpu::graphite::Context::dumpMemoryStatistics
            , py::arg("trace_memory_dump")
            , py::return_value_policy::automatic_reference)
        .def("is_device_lost", &skgpu::graphite::Context::isDeviceLost
            , py::return_value_policy::automatic_reference)
        .def("max_texture_size", &skgpu::graphite::Context::maxTextureSize
            , py::return_value_policy::automatic_reference)
        .def("supports_protected_content", &skgpu::graphite::Context::supportsProtectedContent
            , py::return_value_policy::automatic_reference)
        .def("supported_gpu_stats", &skgpu::graphite::Context::supportedGpuStats
            , py::return_value_policy::automatic_reference)
        .def("priv", py::overload_cast<>(&skgpu::graphite::Context::priv)
            , py::return_value_policy::automatic_reference)
        .def("priv", py::overload_cast<>(&skgpu::graphite::Context::priv, py::const_)
            , py::return_value_policy::automatic_reference)
        ;

        py::class_<skgpu::graphite::Context::ContextID> ContextContextID(_skia, "ContextContextID");
        registry.on(_skia, "ContextContextID", ContextContextID);
            ContextContextID
            .def_static("next", &skgpu::graphite::Context::ContextID::Next
                , py::return_value_policy::automatic_reference)
            .def(py::init<>())
            .def("make_invalid", &skgpu::graphite::Context::ContextID::makeInvalid
                , py::return_value_policy::automatic_reference)
            .def("is_valid", &skgpu::graphite::Context::ContextID::isValid
                , py::return_value_policy::automatic_reference)
        ;

        Context
        .def("context_id", &skgpu::graphite::Context::contextID
            , py::return_value_policy::automatic_reference)
    ;


}