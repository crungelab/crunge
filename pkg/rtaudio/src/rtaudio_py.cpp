#include <limits>
#include <filesystem>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#define BUILDING_DLL

#include <RtAudio.h>

#include <cxbind/cxbind.h>

#include <crunge/rtaudio/crunge-rtaudio.h>
#include <crunge/rtaudio/conversions.h>

namespace py = pybind11;

enum class PyRtAudioFormat : unsigned int {
    SINT8   = RTAUDIO_SINT8,
    SINT16  = RTAUDIO_SINT16,
    SINT24  = RTAUDIO_SINT24,
    SINT32  = RTAUDIO_SINT32,
    FLOAT32 = RTAUDIO_FLOAT32,
    FLOAT64 = RTAUDIO_FLOAT64
};

/*
typedef unsigned int RtAudioStreamFlags;
static const RtAudioStreamFlags RTAUDIO_NONINTERLEAVED = 0x1;    // Use non-interleaved buffers (default = interleaved).
static const RtAudioStreamFlags RTAUDIO_MINIMIZE_LATENCY = 0x2;  // Attempt to set stream parameters for lowest possible latency.
static const RtAudioStreamFlags RTAUDIO_HOG_DEVICE = 0x4;        // Attempt grab device and prevent use by others.
static const RtAudioStreamFlags RTAUDIO_SCHEDULE_REALTIME = 0x8; // Try to select realtime scheduling for callback thread.
static const RtAudioStreamFlags RTAUDIO_ALSA_USE_DEFAULT = 0x10; // Use the "default" PCM device (ALSA only).
static const RtAudioStreamFlags RTAUDIO_JACK_DONT_CONNECT = 0x20; // Do not automatically connect ports (JACK only).
*/

enum class PyRtAudioStreamFlags : unsigned int {
    NONINTERLEAVED = RTAUDIO_NONINTERLEAVED,
    MINIMIZE_LATENCY = RTAUDIO_MINIMIZE_LATENCY,
    HOG_DEVICE = RTAUDIO_HOG_DEVICE,
    SCHEDULE_REALTIME = RTAUDIO_SCHEDULE_REALTIME,
    ALSA_USE_DEFAULT = RTAUDIO_ALSA_USE_DEFAULT,
    JACK_DONT_CONNECT = RTAUDIO_JACK_DONT_CONNECT
};

/*
typedef unsigned int RtAudioStreamStatus;
static const RtAudioStreamStatus RTAUDIO_INPUT_OVERFLOW = 0x1;    // Input data was discarded because of an overflow condition at the driver.
static const RtAudioStreamStatus RTAUDIO_OUTPUT_UNDERFLOW = 0x2;  // The output buffer ran low, likely causing a gap in the output sound.
*/

enum class PyRtAudioStreamStatus : unsigned int {
    INPUT_OVERFLOW = RTAUDIO_INPUT_OVERFLOW,
    OUTPUT_UNDERFLOW = RTAUDIO_OUTPUT_UNDERFLOW
};

void init_rtaudio_py(py::module &_rtaudio, Registry &registry) {

    py::enum_<PyRtAudioFormat>(_rtaudio, "RtAudioFormat")
        .value("SINT8",   PyRtAudioFormat::SINT8)
        .value("SINT16",  PyRtAudioFormat::SINT16)
        .value("SINT24",  PyRtAudioFormat::SINT24)
        .value("SINT32",  PyRtAudioFormat::SINT32)
        .value("FLOAT32", PyRtAudioFormat::FLOAT32)
        .value("FLOAT64", PyRtAudioFormat::FLOAT64)
        .export_values();

    py::enum_<PyRtAudioStreamFlags>(_rtaudio, "RtAudioStreamFlags", py::arithmetic())
        .value("NONINTERLEAVED", PyRtAudioStreamFlags::NONINTERLEAVED)
        .value("MINIMIZE_LATENCY", PyRtAudioStreamFlags::MINIMIZE_LATENCY)
        .value("HOG_DEVICE", PyRtAudioStreamFlags::HOG_DEVICE)
        .value("SCHEDULE_REALTIME", PyRtAudioStreamFlags::SCHEDULE_REALTIME)
        .value("ALSA_USE_DEFAULT", PyRtAudioStreamFlags::ALSA_USE_DEFAULT)
        .value("JACK_DONT_CONNECT", PyRtAudioStreamFlags::JACK_DONT_CONNECT)
        .export_values();

    py::enum_<PyRtAudioStreamStatus>(_rtaudio, "RtAudioStreamStatus", py::arithmetic())
        .value("INPUT_OVERFLOW", PyRtAudioStreamStatus::INPUT_OVERFLOW)
        .value("OUTPUT_UNDERFLOW", PyRtAudioStreamStatus::OUTPUT_UNDERFLOW)
        .export_values();
}