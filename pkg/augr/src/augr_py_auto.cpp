#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

#include <RtAudio.h>
#include <iostream>

#include <cxbind/cxbind.h>
#include <crunge/augr/conversions.h>

#include "augr.h"

namespace py = pybind11;

using namespace rt::audio;

void init_augr_py_auto(py::module &_augr, Registry &registry) {
    py::enum_<AudioFormat>(_augr, "AudioFormat", py::arithmetic())
        .value("SINT8", AudioFormat::SINT8)
        .value("SINT16", AudioFormat::SINT16)
        .value("SINT24", AudioFormat::SINT24)
        .value("SINT32", AudioFormat::SINT32)
        .value("FLOAT32", AudioFormat::FLOAT32)
        .value("FLOAT64", AudioFormat::FLOAT64)
        .export_values()
    ;
    py::enum_<AudioStreamFlags>(_augr, "AudioStreamFlags", py::arithmetic())
        .value("NONINTERLEAVED", AudioStreamFlags::NONINTERLEAVED)
        .value("MINIMIZE_LATENCY", AudioStreamFlags::MINIMIZE_LATENCY)
        .value("HOG_DEVICE", AudioStreamFlags::HOG_DEVICE)
        .value("SCHEDULE_REALTIME", AudioStreamFlags::SCHEDULE_REALTIME)
        .value("ALSA_USE_DEFAULT", AudioStreamFlags::ALSA_USE_DEFAULT)
        .value("JACK_DONT_CONNECT", AudioStreamFlags::JACK_DONT_CONNECT)
        .export_values()
    ;
    py::enum_<AudioStreamStatus>(_augr, "AudioStreamStatus", py::arithmetic())
        .value("INPUT_OVERFLOW", AudioStreamStatus::INPUT_OVERFLOW)
        .value("OUTPUT_UNDERFLOW", AudioStreamStatus::OUTPUT_UNDERFLOW)
        .export_values()
    ;
    py::class_<AudioStream> _AudioStream(_augr, "AudioStream");
    registry.on(_augr, "AudioStream", _AudioStream);
        _AudioStream
        .def(py::init<>())
        .def("open", &AudioStream::open
            )
        .def("close", &AudioStream::close
            )
        .def("start", &AudioStream::start
            )
        .def("stop", &AudioStream::stop
            )
        .def("process", &AudioStream::process
            , py::arg("output_buffer")
            , py::arg("input_buffer")
            , py::arg("n_buffer_frames")
            , py::arg("stream_time")
            , py::arg("status")
            )
        .def_readwrite("audio", &AudioStream::audio)
        .def_readwrite("output_parameters", &AudioStream::outputParameters)
        .def_readwrite("input_parameters", &AudioStream::inputParameters)
        .def_readwrite("format", &AudioStream::format)
        .def_readwrite("sample_rate", &AudioStream::sampleRate)
        .def_readwrite("buffer_frames", &AudioStream::bufferFrames)
        .def_readwrite("callback", &AudioStream::callback)
        .def_readwrite("options", &AudioStream::options)
        .def(py::init([](const py::kwargs& kwargs)
        {
            AudioStream obj{};
            if (kwargs.contains("audio"))
            {
                auto value = kwargs["audio"].cast<rt::audio::RtAudio>();
                obj.audio = value;
            }
            if (kwargs.contains("output_parameters"))
            {
                auto value = kwargs["output_parameters"].cast<rt::audio::RtAudio::StreamParameters *>();
                obj.outputParameters = value;
            }
            if (kwargs.contains("input_parameters"))
            {
                auto value = kwargs["input_parameters"].cast<rt::audio::RtAudio::StreamParameters *>();
                obj.inputParameters = value;
            }
            if (kwargs.contains("format"))
            {
                auto value = kwargs["format"].cast<AudioFormat>();
                obj.format = value;
            }
            if (kwargs.contains("sample_rate"))
            {
                auto value = kwargs["sample_rate"].cast<unsigned int>();
                obj.sampleRate = value;
            }
            if (kwargs.contains("buffer_frames"))
            {
                auto value = kwargs["buffer_frames"].cast<unsigned int>();
                obj.bufferFrames = value;
            }
            if (kwargs.contains("callback"))
            {
                auto value = kwargs["callback"].cast<pybind11::function>();
                obj.callback = value;
            }
            if (kwargs.contains("options"))
            {
                auto value = kwargs["options"].cast<rt::audio::RtAudio::StreamOptions *>();
                obj.options = value;
            }
            return obj;
        }))
        .def("__repr__", [](const AudioStream &self) {
            std::stringstream ss;
            ss << "AudioStream(";
            ss << "audio=" << py::repr(py::cast(self.audio)).cast<std::string>();
            ss << ", ";
            ss << "outputParameters=" << py::repr(py::cast(self.outputParameters)).cast<std::string>();
            ss << ", ";
            ss << "inputParameters=" << py::repr(py::cast(self.inputParameters)).cast<std::string>();
            ss << ", ";
            ss << "format=" << py::repr(py::cast(self.format)).cast<std::string>();
            ss << ", ";
            ss << "sampleRate=" << py::repr(py::cast(self.sampleRate)).cast<std::string>();
            ss << ", ";
            ss << "bufferFrames=" << py::repr(py::cast(self.bufferFrames)).cast<std::string>();
            ss << ", ";
            ss << "callback=" << py::repr(self.callback).cast<std::string>();
            ss << ", ";
            ss << "options=" << py::repr(py::cast(self.options)).cast<std::string>();
            ss << ")";
            return ss.str();
        })
    ;


}