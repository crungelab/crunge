#include <limits>
#include <filesystem>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <dawn/webgpu_cpp.h>
#include "dawn/native/DawnNative.h"
#include <dawn/dawn_proc.h>

#include <crunge/core/bindtools.h>
#include <crunge/wgpu/crunge-wgpu.h>

namespace py = pybind11;

using namespace wgpu;

/*void RequestAdapter() {
    Instance CreateInstance(InstanceDescriptor const * descriptor = nullptr);
    Instance instance = CreateInstance();
}*/

/*static dawn::native::Adapter RequestAdapter(WGPUBackendType type1st, WGPUBackendType type2nd = WGPUBackendType_Null) {
	static dawn::native::Instance instance;
	instance.DiscoverDefaultAdapters();
	wgpu::AdapterProperties properties;
	std::vector<dawn::native::Adapter> adapters = instance.GetAdapters();
	for (auto it = adapters.begin(); it != adapters.end(); ++it) {
		it->GetProperties(&properties);
		if (static_cast<WGPUBackendType>(properties.backendType) == type1st) {
			return *it;
		}
	}
	if (type2nd) {
		for (auto it = adapters.begin(); it != adapters.end(); ++it) {
			it->GetProperties(&properties);
			if (static_cast<WGPUBackendType>(properties.backendType) == type2nd) {
				return *it;
			}
		}
	}
	return dawn::native::Adapter();
}*/

/*static dawn::native::Adapter NativeRequestAdapter(WGPUBackendType type1st, WGPUBackendType type2nd = WGPUBackendType_Null) {
	static dawn::native::Instance instance;
	instance.DiscoverDefaultAdapters();
	wgpu::AdapterProperties properties;
	std::vector<dawn::native::Adapter> adapters = instance.GetAdapters();
	for (auto it = adapters.begin(); it != adapters.end(); ++it) {
		it->GetProperties(&properties);
		if (static_cast<WGPUBackendType>(properties.backendType) == type1st) {
			return *it;
		}
	}
	if (type2nd) {
		for (auto it = adapters.begin(); it != adapters.end(); ++it) {
			it->GetProperties(&properties);
			if (static_cast<WGPUBackendType>(properties.backendType) == type2nd) {
				return *it;
			}
		}
	}
	return dawn::native::Adapter();
}

static Adapter RequestAdapter(BackendType type1st, BackendType type2nd = BackendType::Null) {
    auto adapter = NativeRequestAdapter((WGPUBackendType)type1st, (WGPUBackendType)type2nd);
    return reinterpret_cast<Adapter>(adapter);
}*/

void CreateProcTable() {
    DawnProcTable procs(dawn::native::GetProcs());
    dawnProcSetProcs(&procs);
}

void init_main(py::module &_wgpu, Registry &registry) {
    /*_wgpu.def("request_adapter", &RequestAdapter
        , py::arg("descriptor") = nullptr
        , py::return_value_policy::automatic_reference);*/
    /*_wgpu.def("request_adapter", &RequestAdapter
    , py::arg("first")
    , py::arg("second")
    , py::return_value_policy::automatic_reference);*/

    _wgpu.def("create_proc_table", &CreateProcTable);

    PYEXTEND_BEGIN(wgpu::Instance, Instance)
    Instance.def("request_adapter", [](const wgpu::Instance& self)
    {
        RequestAdapterOptions options;
        //RequestAdapterCallback cb;
        //typedef void (*WGPURequestAdapterCallback)(WGPURequestAdapterStatus status, WGPUAdapter adapter, char const * message, void * userdata);
        static Adapter adapter;
        auto cb = [](WGPURequestAdapterStatus status, WGPUAdapter _adapter, char const* message, void* userdata) {
            adapter = static_cast<Adapter>(_adapter);
        };
        int userdata = 0;
        self.RequestAdapter(&options, cb, &userdata);
		return adapter;
    });
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::AdapterProperties, AdapterProperties)
        AdapterProperties.def(py::init<>());
    PYEXTEND_END

    PYEXTEND_BEGIN(wgpu::ShaderModuleDescriptor, ShaderModuleDescriptor)
        ShaderModuleDescriptor.def(py::init<>());
    PYEXTEND_END

}

//void RequestAdapter(RequestAdapterOptions const * options, RequestAdapterCallback callback, void * userdata) const;