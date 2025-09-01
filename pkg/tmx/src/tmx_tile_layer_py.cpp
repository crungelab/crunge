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
#include <tmxlite/TileLayer.hpp>

namespace py = pybind11;

void init_tmx_tile_layer_py(py::module &_tmx, Registry &registry)
{
    PYEXTEND_BEGIN(tmx::TileLayer, TileLayer)
    _TileLayer.def_property_readonly("properties", [](tmx::TileLayer& l){
        return l.getProperties();
    });

    _TileLayer.def_property_readonly("tiles", [](tmx::TileLayer& l){
        return l.getTiles();
    });
    PYEXTEND_END
}
