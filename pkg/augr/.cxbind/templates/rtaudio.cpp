#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

#include <RtAudio.h>
#include <iostream>

#include <cxbind/cxbind.h>
#include <crunge/augr/conversions.h>

namespace py = pybind11;

using namespace rt::audio;

void init_rtaudio_py_auto(py::module &_augr, Registry &registry) {
{{body}}
}