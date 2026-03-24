#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

#include <RtAudio.h>
#include <iostream>

#include <cxbind/cxbind.h>
#include <crunge/rtaudio/conversions.h>

namespace py = pybind11;

using namespace rt::audio;

void init_rtaudio_py_auto(py::module &_rtaudio, Registry &registry) {
    py::enum_<rt::audio::RtAudioErrorType>(_rtaudio, "AudioErrorType", py::arithmetic())
        .value("RTAUDIO_NO_ERROR", rt::audio::RtAudioErrorType::RTAUDIO_NO_ERROR)
        .value("RTAUDIO_WARNING", rt::audio::RtAudioErrorType::RTAUDIO_WARNING)
        .value("RTAUDIO_UNKNOWN_ERROR", rt::audio::RtAudioErrorType::RTAUDIO_UNKNOWN_ERROR)
        .value("RTAUDIO_NO_DEVICES_FOUND", rt::audio::RtAudioErrorType::RTAUDIO_NO_DEVICES_FOUND)
        .value("RTAUDIO_INVALID_DEVICE", rt::audio::RtAudioErrorType::RTAUDIO_INVALID_DEVICE)
        .value("RTAUDIO_DEVICE_DISCONNECT", rt::audio::RtAudioErrorType::RTAUDIO_DEVICE_DISCONNECT)
        .value("RTAUDIO_MEMORY_ERROR", rt::audio::RtAudioErrorType::RTAUDIO_MEMORY_ERROR)
        .value("RTAUDIO_INVALID_PARAMETER", rt::audio::RtAudioErrorType::RTAUDIO_INVALID_PARAMETER)
        .value("RTAUDIO_INVALID_USE", rt::audio::RtAudioErrorType::RTAUDIO_INVALID_USE)
        .value("RTAUDIO_DRIVER_ERROR", rt::audio::RtAudioErrorType::RTAUDIO_DRIVER_ERROR)
        .value("RTAUDIO_SYSTEM_ERROR", rt::audio::RtAudioErrorType::RTAUDIO_SYSTEM_ERROR)
        .value("RTAUDIO_THREAD_ERROR", rt::audio::RtAudioErrorType::RTAUDIO_THREAD_ERROR)
        .export_values()
    ;
    py::class_<rt::audio::RtAudio> _RtAudio(_rtaudio, "RtAudio");
    registry.on(_rtaudio, "RtAudio", _RtAudio);
        py::enum_<rt::audio::RtAudio::Api>(_RtAudio, "Api", py::arithmetic())
            .value("UNSPECIFIED", rt::audio::RtAudio::Api::UNSPECIFIED)
            .value("MACOSX_CORE", rt::audio::RtAudio::Api::MACOSX_CORE)
            .value("LINUX_ALSA", rt::audio::RtAudio::Api::LINUX_ALSA)
            .value("UNIX_JACK", rt::audio::RtAudio::Api::UNIX_JACK)
            .value("LINUX_PULSE", rt::audio::RtAudio::Api::LINUX_PULSE)
            .value("LINUX_OSS", rt::audio::RtAudio::Api::LINUX_OSS)
            .value("WINDOWS_ASIO", rt::audio::RtAudio::Api::WINDOWS_ASIO)
            .value("WINDOWS_WASAPI", rt::audio::RtAudio::Api::WINDOWS_WASAPI)
            .value("WINDOWS_DS", rt::audio::RtAudio::Api::WINDOWS_DS)
            .value("RTAUDIO_DUMMY", rt::audio::RtAudio::Api::RTAUDIO_DUMMY)
            .value("NUM_APIS", rt::audio::RtAudio::Api::NUM_APIS)
            .export_values()
        ;
        py::class_<rt::audio::RtAudio::DeviceInfo> _RtAudioDeviceInfo(_rtaudio, "RtAudioDeviceInfo");
        registry.on(_rtaudio, "RtAudioDeviceInfo", _RtAudioDeviceInfo);
            _RtAudioDeviceInfo
            .def_readwrite("id", &rt::audio::RtAudio::DeviceInfo::ID)
            .def_readwrite("name", &rt::audio::RtAudio::DeviceInfo::name)
            .def_readwrite("output_channels", &rt::audio::RtAudio::DeviceInfo::outputChannels)
            .def_readwrite("input_channels", &rt::audio::RtAudio::DeviceInfo::inputChannels)
            .def_readwrite("duplex_channels", &rt::audio::RtAudio::DeviceInfo::duplexChannels)
            .def_readwrite("is_default_output", &rt::audio::RtAudio::DeviceInfo::isDefaultOutput)
            .def_readwrite("is_default_input", &rt::audio::RtAudio::DeviceInfo::isDefaultInput)
            .def_readwrite("sample_rates", &rt::audio::RtAudio::DeviceInfo::sampleRates)
            .def_readwrite("current_sample_rate", &rt::audio::RtAudio::DeviceInfo::currentSampleRate)
            .def_readwrite("preferred_sample_rate", &rt::audio::RtAudio::DeviceInfo::preferredSampleRate)
            .def_readwrite("native_formats", &rt::audio::RtAudio::DeviceInfo::nativeFormats)
            .def("__repr__", [](const rt::audio::RtAudio::DeviceInfo &self) {
                std::stringstream ss;
                ss << "RtAudioDeviceInfo(";
                ss << "ID=" << py::repr(py::cast(self.ID)).cast<std::string>();
                ss << ", ";
                ss << "name=" << py::repr(py::cast(self.name)).cast<std::string>();
                ss << ", ";
                ss << "outputChannels=" << py::repr(py::cast(self.outputChannels)).cast<std::string>();
                ss << ", ";
                ss << "inputChannels=" << py::repr(py::cast(self.inputChannels)).cast<std::string>();
                ss << ", ";
                ss << "duplexChannels=" << py::repr(py::cast(self.duplexChannels)).cast<std::string>();
                ss << ", ";
                ss << "isDefaultOutput=" << py::repr(py::cast(self.isDefaultOutput)).cast<std::string>();
                ss << ", ";
                ss << "isDefaultInput=" << py::repr(py::cast(self.isDefaultInput)).cast<std::string>();
                ss << ", ";
                ss << "sampleRates=" << py::repr(py::cast(self.sampleRates)).cast<std::string>();
                ss << ", ";
                ss << "currentSampleRate=" << py::repr(py::cast(self.currentSampleRate)).cast<std::string>();
                ss << ", ";
                ss << "preferredSampleRate=" << py::repr(py::cast(self.preferredSampleRate)).cast<std::string>();
                ss << ", ";
                ss << "nativeFormats=" << py::repr(py::cast(self.nativeFormats)).cast<std::string>();
                ss << ")";
                return ss.str();
            })
        ;

        py::class_<rt::audio::RtAudio::StreamParameters> _RtAudioStreamParameters(_rtaudio, "RtAudioStreamParameters");
        registry.on(_rtaudio, "RtAudioStreamParameters", _RtAudioStreamParameters);
            _RtAudioStreamParameters
            .def_readwrite("device_id", &rt::audio::RtAudio::StreamParameters::deviceId)
            .def_readwrite("n_channels", &rt::audio::RtAudio::StreamParameters::nChannels)
            .def_readwrite("first_channel", &rt::audio::RtAudio::StreamParameters::firstChannel)
            .def(py::init([](const py::kwargs& kwargs)
            {
                rt::audio::RtAudio::StreamParameters obj{};
                if (kwargs.contains("device_id"))
                {
                    auto value = kwargs["device_id"].cast<unsigned int>();
                    obj.deviceId = value;
                }
                if (kwargs.contains("n_channels"))
                {
                    auto value = kwargs["n_channels"].cast<unsigned int>();
                    obj.nChannels = value;
                }
                if (kwargs.contains("first_channel"))
                {
                    auto value = kwargs["first_channel"].cast<unsigned int>();
                    obj.firstChannel = value;
                }
                return obj;
            }))
            .def("__repr__", [](const rt::audio::RtAudio::StreamParameters &self) {
                std::stringstream ss;
                ss << "RtAudioStreamParameters(";
                ss << "deviceId=" << py::repr(py::cast(self.deviceId)).cast<std::string>();
                ss << ", ";
                ss << "nChannels=" << py::repr(py::cast(self.nChannels)).cast<std::string>();
                ss << ", ";
                ss << "firstChannel=" << py::repr(py::cast(self.firstChannel)).cast<std::string>();
                ss << ")";
                return ss.str();
            })
        ;

        py::class_<rt::audio::RtAudio::StreamOptions> _RtAudioStreamOptions(_rtaudio, "RtAudioStreamOptions");
        registry.on(_rtaudio, "RtAudioStreamOptions", _RtAudioStreamOptions);
            _RtAudioStreamOptions
            .def_readwrite("flags", &rt::audio::RtAudio::StreamOptions::flags)
            .def_readwrite("number_of_buffers", &rt::audio::RtAudio::StreamOptions::numberOfBuffers)
            .def_readwrite("stream_name", &rt::audio::RtAudio::StreamOptions::streamName)
            .def_readwrite("priority", &rt::audio::RtAudio::StreamOptions::priority)
            .def(py::init([](const py::kwargs& kwargs)
            {
                rt::audio::RtAudio::StreamOptions obj{};
                if (kwargs.contains("flags"))
                {
                    auto value = kwargs["flags"].cast<unsigned int>();
                    obj.flags = value;
                }
                if (kwargs.contains("number_of_buffers"))
                {
                    auto value = kwargs["number_of_buffers"].cast<unsigned int>();
                    obj.numberOfBuffers = value;
                }
                if (kwargs.contains("stream_name"))
                {
                    auto value = kwargs["stream_name"].cast<std::basic_string<char>>();
                    obj.streamName = value;
                }
                if (kwargs.contains("priority"))
                {
                    auto value = kwargs["priority"].cast<int>();
                    obj.priority = value;
                }
                return obj;
            }))
            .def("__repr__", [](const rt::audio::RtAudio::StreamOptions &self) {
                std::stringstream ss;
                ss << "RtAudioStreamOptions(";
                ss << "flags=" << py::repr(py::cast(self.flags)).cast<std::string>();
                ss << ", ";
                ss << "numberOfBuffers=" << py::repr(py::cast(self.numberOfBuffers)).cast<std::string>();
                ss << ", ";
                ss << "streamName=" << py::repr(py::cast(self.streamName)).cast<std::string>();
                ss << ", ";
                ss << "priority=" << py::repr(py::cast(self.priority)).cast<std::string>();
                ss << ")";
                return ss.str();
            })
        ;

        _RtAudio
        .def_static("get_version", &rt::audio::RtAudio::getVersion
            )
        .def_static("get_compiled_api", [](std::vector<rt::audio::RtAudio::Api> & apis)
            {
                rt::audio::RtAudio::getCompiledApi(apis);
                return std::make_tuple(apis);
            }
            , py::arg("apis")
            )
        .def_static("get_api_name", &rt::audio::RtAudio::getApiName
            , py::arg("api")
            )
        .def_static("get_api_display_name", &rt::audio::RtAudio::getApiDisplayName
            , py::arg("api")
            )
        .def_static("get_compiled_api_by_name", &rt::audio::RtAudio::getCompiledApiByName
            , py::arg("name")
            )
        .def_static("get_compiled_api_by_display_name", &rt::audio::RtAudio::getCompiledApiByDisplayName
            , py::arg("name")
            )
        .def(py::init<rt::audio::RtAudio::Api, rt::audio::RtAudioErrorCallback &&>()
        , py::arg("api") = rt::audio::RtAudio::Api::UNSPECIFIED
        , py::arg("error_callback") = nullptr
        )
        .def("get_current_api", py::overload_cast<>(&rt::audio::RtAudio::getCurrentApi)
            )
        .def("get_device_count", py::overload_cast<>(&rt::audio::RtAudio::getDeviceCount)
            )
        .def("get_device_ids", py::overload_cast<>(&rt::audio::RtAudio::getDeviceIds)
            )
        .def("get_device_names", py::overload_cast<>(&rt::audio::RtAudio::getDeviceNames)
            )
        .def("get_device_info", py::overload_cast<unsigned int>(&rt::audio::RtAudio::getDeviceInfo)
            , py::arg("device_id")
            )
        .def("get_default_output_device", py::overload_cast<>(&rt::audio::RtAudio::getDefaultOutputDevice)
            )
        .def("get_default_input_device", py::overload_cast<>(&rt::audio::RtAudio::getDefaultInputDevice)
            )
        .def("open_stream", [](rt::audio::RtAudio& self, rt::audio::RtAudio::StreamParameters * outputParameters, rt::audio::RtAudio::StreamParameters * inputParameters, rt::audio::RtAudioFormat format, unsigned int sampleRate, unsigned int * bufferFrames, rt::audio::RtAudioCallback callback, void * userData, rt::audio::RtAudio::StreamOptions * options)
            {
                auto _ret = self.openStream(outputParameters, inputParameters, format, sampleRate, bufferFrames, callback, userData, options);
                return std::make_tuple(_ret, bufferFrames);
            }
            , py::arg("output_parameters")
            , py::arg("input_parameters")
            , py::arg("format")
            , py::arg("sample_rate")
            , py::arg("buffer_frames")
            , py::arg("callback")
            , py::arg("user_data") = nullptr
            , py::arg("options") = nullptr
            )
        .def("close_stream", py::overload_cast<>(&rt::audio::RtAudio::closeStream)
            )
        .def("start_stream", py::overload_cast<>(&rt::audio::RtAudio::startStream)
            )
        .def("stop_stream", py::overload_cast<>(&rt::audio::RtAudio::stopStream)
            )
        .def("abort_stream", py::overload_cast<>(&rt::audio::RtAudio::abortStream)
            )
        .def("get_error_text", py::overload_cast<>(&rt::audio::RtAudio::getErrorText)
            )
        .def("is_stream_open", py::overload_cast<>(&rt::audio::RtAudio::isStreamOpen, py::const_)
            )
        .def("is_stream_running", py::overload_cast<>(&rt::audio::RtAudio::isStreamRunning, py::const_)
            )
        .def("get_stream_time", py::overload_cast<>(&rt::audio::RtAudio::getStreamTime)
            )
        .def("set_stream_time", py::overload_cast<double>(&rt::audio::RtAudio::setStreamTime)
            , py::arg("time")
            )
        .def("get_stream_latency", py::overload_cast<>(&rt::audio::RtAudio::getStreamLatency)
            )
        .def("get_stream_sample_rate", py::overload_cast<>(&rt::audio::RtAudio::getStreamSampleRate)
            )
        .def("set_error_callback", py::overload_cast<rt::audio::RtAudioErrorCallback>(&rt::audio::RtAudio::setErrorCallback)
            , py::arg("error_callback")
            )
        .def("show_warnings", py::overload_cast<bool>(&rt::audio::RtAudio::showWarnings)
            , py::arg("value") = true
            )
    ;

    py::class_<rt::audio::CallbackInfo> _CallbackInfo(_rtaudio, "CallbackInfo");
    registry.on(_rtaudio, "CallbackInfo", _CallbackInfo);
        _CallbackInfo
        .def_readwrite("object", &rt::audio::CallbackInfo::object)
        .def_readwrite("thread", &rt::audio::CallbackInfo::thread)
        .def_readwrite("callback", &rt::audio::CallbackInfo::callback)
        .def_readwrite("user_data", &rt::audio::CallbackInfo::userData)
        .def_readwrite("api_info", &rt::audio::CallbackInfo::apiInfo)
        .def_readwrite("is_running", &rt::audio::CallbackInfo::isRunning)
        .def_readwrite("do_realtime", &rt::audio::CallbackInfo::doRealtime)
        .def_readwrite("priority", &rt::audio::CallbackInfo::priority)
        .def_readwrite("device_disconnected", &rt::audio::CallbackInfo::deviceDisconnected)
    ;

    py::class_<rt::audio::S24> _S24(_rtaudio, "S24");
    registry.on(_rtaudio, "S24", _S24);
        _S24
        .def(py::init<>())
        .def(py::init<const double &>()
        , py::arg("d")
        )
        .def(py::init<const float &>()
        , py::arg("f")
        )
        .def(py::init<const short &>()
        , py::arg("s")
        )
        .def(py::init<const char &>()
        , py::arg("c")
        )
        .def("as_int", &rt::audio::S24::asInt
            )
    ;


}