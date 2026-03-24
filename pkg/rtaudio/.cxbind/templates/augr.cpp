#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

#include <RtAudio.h>
#include <iostream>

#include <cxbind/cxbind.h>
#include <crunge/rtaudio/conversions.h>

#include "augr.h"

namespace py = pybind11;

using namespace rt::audio;

void init_augr_py_auto(py::module &_rtaudio, Registry &registry) {
{{body}}
}