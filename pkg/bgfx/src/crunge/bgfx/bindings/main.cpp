#include <limits>
#include <filesystem>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include <crunge/core/bindtools.h>

#include <bgfx/bgfx.h>

using namespace bgfx;

namespace py = pybind11;

void init_main(py::module &_bgfx, Registry &registry) {
    PYCLASS_BEGIN(_bgfx, bgfx::Memory, Memory)
    //Memory.def(py::init<>());
    Memory.def_readwrite("data", &bgfx::Memory::data);
    Memory.def_readwrite("size", &bgfx::Memory::size);
    PYCLASS_END(_bgfx, bgfx::Memory, Memory)
}

