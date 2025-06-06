#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>
#include <limits>

//#include <dawn/webgpu_cpp.h>
//#include <wgpu.h>

#include <cxbind/cxbind.h>
#include <crunge/wgpu/pywgpu.h>
#include <crunge/wgpu/conversions.h>

namespace py = pybind11;

using namespace pywgpu;

void init_chained_struct(py::module &_wgpu, Registry &registry) {
    PYCLASS_BEGIN(_wgpu, pywgpu::ChainedStruct, ChainedStruct)
        ChainedStruct.def_readwrite("next_in_chain", &pywgpu::ChainedStruct::nextInChain);
        ChainedStruct.def_readwrite("s_type", &pywgpu::ChainedStruct::sType);
    PYCLASS_END(_wgpu, pywgpu::ChainedStruct, ChainedStruct)

    PYCLASS_BEGIN(_wgpu, pywgpu::ChainedStructOut, ChainedStructOut)
        ChainedStructOut.def_readwrite("next_in_chain", &pywgpu::ChainedStructOut::nextInChain);
        ChainedStructOut.def_readwrite("s_type", &pywgpu::ChainedStructOut::sType);
    PYCLASS_END(_wgpu, pywgpu::ChainedStructOut, ChainedStructOut)


}