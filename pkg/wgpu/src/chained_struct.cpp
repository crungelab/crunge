#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>
#include <limits>

#include <dawn/webgpu_cpp.h>
//#include <wgpu.h>

#include <cxbind/cxbind.h>
#include <crunge/wgpu/conversions.h>

namespace py = pybind11;

using namespace wgpu;

void init_chained_struct(py::module &_wgpu, Registry &registry) {
    PYCLASS_BEGIN(_wgpu, wgpu::ChainedStruct, ChainedStruct)
        ChainedStruct.def_readwrite("next_in_chain", &wgpu::ChainedStruct::nextInChain);
        ChainedStruct.def_readwrite("s_type", &wgpu::ChainedStruct::sType);
    PYCLASS_END(_wgpu, wgpu::ChainedStruct, ChainedStruct)

    PYCLASS_BEGIN(_wgpu, wgpu::ChainedStructOut, ChainedStructOut)
        ChainedStructOut.def_readwrite("next_in_chain", &wgpu::ChainedStructOut::nextInChain);
        ChainedStructOut.def_readwrite("s_type", &wgpu::ChainedStructOut::sType);
    PYCLASS_END(_wgpu, wgpu::ChainedStructOut, ChainedStructOut)


}