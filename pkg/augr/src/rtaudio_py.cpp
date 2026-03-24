#include <limits>
#include <filesystem>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#define BUILDING_DLL

#include <cxbind/cxbind.h>

#include <crunge/augr/crunge-augr.h>
#include <crunge/augr/conversions.h>

#include <RtAudio.h>


namespace py = pybind11;


void init_rtaudio_py(py::module &_rtaudio, Registry &registry) {

}