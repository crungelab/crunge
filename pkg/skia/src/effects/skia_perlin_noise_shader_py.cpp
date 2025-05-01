#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/effects/SkPerlinNoiseShader.h>
#include <include/core/SkMatrix.h>

namespace py = pybind11;

class PyPerlinNoiseShader {};

void init_skia_perlin_noise_shader_py(py::module &_skia, Registry &registry) {
    py::class_<PyPerlinNoiseShader> PerlinNoiseShader(_skia, "PerlinNoiseShader");
    registry.on(_skia, "PerlinNoiseShader", PerlinNoiseShader);

    PerlinNoiseShader
    .def_static("make_fractal_noise", &SkShaders::MakeFractalNoise,
        py::arg("base_frequency_x"), py::arg("base_frequency_y"),
        py::arg("num_octaves"), py::arg("seed"), py::arg("tile_size") = nullptr/*,
        py::return_value_policy::take_ownership*/
    )
    .def_static("make_turbulence", &SkShaders::MakeTurbulence,
        py::arg("base_frequency_x"), py::arg("base_frequency_y"),
        py::arg("num_octaves"), py::arg("seed"), py::arg("tile_size") = nullptr/*,
        py::return_value_policy::take_ownership*/
    )
    ;
}
