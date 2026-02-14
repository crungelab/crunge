#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

//#include <iostream>

#include <cxbind/cxbind.h>

#include <crunge/tmx/crunge-tmx.h>
#include <crunge/tmx/conversions.h>

#include <tmxlite/Map.hpp>
#include <tmxlite/LayerGroup.hpp>

namespace py = pybind11;

void init_tmx_layer_group_py(py::module &_tmx, Registry &registry) {
    PYEXTEND_BEGIN(tmx::LayerGroup, LayerGroup)
        _LayerGroup
        .def("get_layers", [](const tmx::LayerGroup& self) {
            py::list result;
            for (const auto& layer : self.getLayers()) {
                result.append(layer.get());
            }
            return result;
        }, py::return_value_policy::reference)
    ;

    PYEXTEND_END
}