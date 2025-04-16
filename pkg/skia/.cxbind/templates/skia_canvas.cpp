#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

#include <tiny_gltf.h>
#include <iostream>

#include <cxbind/cxbind.h>
#include <crunge/skia/conversions.h>

namespace py = pybind11;

using namespace tinygltf;

void init_generated(py::module &_gltf, Registry &registry) {
{{body}}
}