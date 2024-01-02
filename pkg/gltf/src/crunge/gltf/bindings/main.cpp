#include <limits>
#include <filesystem>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#define BUILDING_DLL

#include <tiny_gltf.h>

#include <crunge/core/bindtools.h>

#include <crunge/gltf/crunge-gltf.h>
#include <crunge/gltf/conversions.h>

namespace py = pybind11;

void init_main(py::module &_gltf, Registry &registry) {
}

