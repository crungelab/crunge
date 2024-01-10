#include <iostream>

#include "callbacks.h"

namespace crunge {
namespace wgpu {

void ErrorCallback(WGPUErrorType type, const char *msg, void *userdata)
{
    switch (type)
    {
    case WGPUErrorType_OutOfMemory:
        std::cerr << "[Error] Out Of Memory: " << msg << std::endl;
        abort();
    case WGPUErrorType_Validation:
        std::cerr << "[Error Validation: " << msg << std::endl;
        abort();
        // break;
    case WGPUErrorType_NoError:
    case WGPUErrorType_Unknown:
    case WGPUErrorType_DeviceLost:
    case WGPUErrorType_Force32:
    case WGPUErrorType_Internal:
        std::cerr << msg << std::endl;
        break;
    }
}

void DeviceLostCallback(WGPUDeviceLostReason reason, char const *msg, void *userdata)
{
    std::cerr << "[Device Lost]: ";
    switch (reason)
    {
    case WGPUDeviceLostReason_Undefined:
        std::cerr << "Undefined: " << msg << std::endl;
        break;
    case WGPUDeviceLostReason_Destroyed:
        std::cerr << "Destroyed: " << msg << std::endl;
        break;
    case WGPUDeviceLostReason_Force32:
        std::cerr << "Force32: " << msg << std::endl;
        break;
    }
}

void LoggingCallback(WGPULoggingType type, const char *msg, void *)
{
    switch (type)
    {
    case WGPULoggingType_Verbose:
        std::cerr << "Log [Verbose]: ";
        break;
    case WGPULoggingType_Info:
        std::cerr << "Log [Info]: ";
        break;
    case WGPULoggingType_Warning:
        std::cerr << "Log [Warning]: ";
        break;
    case WGPULoggingType_Error:
        std::cerr << "Log [Error]: ";
        break;
    case WGPULoggingType_Force32:
        std::cerr << "Log [Force32]: ";
        break;
    }
    std::cerr << msg << std::endl;
}

}}  // namespace crunge::wgpu