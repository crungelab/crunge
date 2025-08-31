#include <limits>
#include <filesystem>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#define BUILDING_DLL

#include <cxbind/cxbind.h>

#include <crunge/tmx/crunge-tmx.h>
#include <crunge/tmx/conversions.h>

#include <tmxlite/Map.hpp>
#include <tmxlite/Layer.hpp>

namespace py = pybind11;

void init_tmx_layer_py(py::module &_tmx, Registry &registry)
{
    PYEXTEND_BEGIN(tmx::Layer, Layer)
    _Layer.def_property_readonly("name", [](tmx::Layer& l){
        return l.getName();
    });
    PYEXTEND_END
}
