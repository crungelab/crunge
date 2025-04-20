#include <iostream>
#include <pybind11/iostream.h>

#include "callbacks.h"

namespace py = pybind11;

namespace crunge {
namespace wgpu {

void ErrorCallback(WGPUErrorType type, const char *msg, void *userdata)
{
    py::scoped_ostream_redirect stream(
    std::cerr,                                // std::ostream&
    py::module_::import("sys").attr("stderr") // Python output
    );

    switch (type)
    {
    case WGPUErrorType_OutOfMemory:
        std::cerr << "[Error] Out Of Memory: " << msg << std::endl;
        abort();
    case WGPUErrorType_Validation:
        std::cerr << "[Error Validation: " << msg << std::endl;
        abort();
        //break;
    case WGPUErrorType_NoError:
    case WGPUErrorType_Unknown:
    //case WGPUErrorType_DeviceLost:
    case WGPUErrorType_Force32:
    case WGPUErrorType_Internal:
        std::cerr << msg << std::endl;
        break;
    }
}

/*
typedef enum WGPUDeviceLostReason {
    WGPUDeviceLostReason_Unknown = 0x00000001,
    WGPUDeviceLostReason_Destroyed = 0x00000002,
    WGPUDeviceLostReason_InstanceDropped = 0x00000003,
    WGPUDeviceLostReason_FailedCreation = 0x00000004,
    WGPUDeviceLostReason_Force32 = 0x7FFFFFFF
} WGPUDeviceLostReason WGPU_ENUM_ATTRIBUTE;
*/

void DeviceLostCallback(WGPUDeviceLostReason reason, char const *msg, void *userdata)
{
    /*
    py::scoped_ostream_redirect stream(
    std::cerr,                                // std::ostream&
    py::module_::import("sys").attr("stderr") // Python output
    );
    */

    std::cerr << "[Device Lost]: ";
    switch (reason)
    {
    /*case WGPUDeviceLostReason::WGPUDeviceLostReason_Undefined:
        std::cerr << "Undefined: " << msg << std::endl;
        break;*/
    case WGPUDeviceLostReason::WGPUDeviceLostReason_Destroyed:
        std::cerr << "Destroyed: " << msg << std::endl;
        break;
    case WGPUDeviceLostReason::WGPUDeviceLostReason_Force32:
        std::cerr << "Force32: " << msg << std::endl;
        break;
    }
}

void LoggingCallback(WGPULoggingType type, WGPUStringView message)
{
    std::string msg = message.data ? std::string(message.data, message.length) : "No message";
{
    py::scoped_ostream_redirect stream(
    std::cerr,                                // std::ostream&
    py::module_::import("sys").attr("stderr") // Python output
    );

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
}}

}}  // namespace crunge::wgpu