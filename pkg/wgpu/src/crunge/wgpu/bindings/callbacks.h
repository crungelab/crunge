#pragma once

#include <dawn/webgpu_cpp.h>

namespace crunge {
namespace wgpu {

void ErrorCallback(WGPUErrorType type, const char* msg, void*);
void DeviceLostCallback(WGPUDeviceLostReason reason, char const* msg, void*);
void LoggingCallback(WGPULoggingType type, const char* msg, void*);

}}  // namespace crunge::wgpu
