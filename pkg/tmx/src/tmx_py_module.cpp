#include <pybind11/pybind11.h>

#include <cxbind/cxbind.h>

namespace py = pybind11;

void init_tmx_layer_py_auto(py::module &, Registry& registry);
void init_tmx_tile_layer_py_auto(py::module &, Registry& registry);
void init_tmx_object_group_py_auto(py::module &, Registry& registry);

void init_tmx_map_py(py::module &, Registry& registry);
void init_tmx_map_py_auto(py::module &, Registry& registry);

PYBIND11_MODULE(_tmx, m) {
    Registry r;
    init_tmx_layer_py_auto(m, r);
    init_tmx_tile_layer_py_auto(m, r);
    init_tmx_object_group_py_auto(m, r);

    init_tmx_map_py(m, r);
    init_tmx_map_py_auto(m, r);
}