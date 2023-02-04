#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

/*
 * On Windows x86/x64 Dawn should have been built with the D3D12 and Vulkan
 * support; macOS/iOS it should be Metal only; Linux (and others) should be
 * Vulkan only. None of the platforms are built with OpenGL support.
 * 
 * TODO: are we doing GL?
 */
#if __has_include("d3d12.h") || (_MSC_VER >= 1900)
#define DAWN_ENABLE_BACKEND_D3D12
#endif
#if __has_include("vulkan/vulkan.h") && (defined(__i386__) || defined(__x86_64__) || defined(_M_IX86) || defined(_M_X64))
#define DAWN_ENABLE_BACKEND_VULKAN
#endif

//****************************************************************************/

#include <dawn/native/DawnNative.h>
#include <dawn/dawn_proc.h>
#include <dawn/webgpu_cpp.h>
#include <dawn/native/NullBackend.h>
#ifdef DAWN_ENABLE_BACKEND_D3D12
#include <dawn/native/D3D12Backend.h>
#endif
#ifdef DAWN_ENABLE_BACKEND_VULKAN
#include <dawn/native/VulkanBackend.h>
#include <vulkan/vulkan_win32.h>
#endif

//#pragma comment(lib, "dawn_native.dll.lib")
//#pragma comment(lib, "dawn_proc.dll.lib")
#ifdef DAWN_ENABLE_BACKEND_VULKAN
#pragma comment(lib, "vulkan-1.lib")
#endif

#include <crunge/core/bindtools.h>

namespace py = pybind11;

void init_generated(py::module &_wgpu, Registry &registry) {
{{body}}
}