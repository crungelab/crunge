#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

#include <SDL3/SDL.h>
#include <SDL3/SDL_audio.h>
#include <SDL3/SDL_iostream.h>
#include <iostream>

#include <cxbind/cxbind.h>

#include <crunge/sdl/crunge-sdl.h>
#include <crunge/sdl/conversions.h>

namespace py = pybind11;

void init_sdl_audio_py_auto(py::module &_sdl, Registry &registry) {
    py::enum_<SDL_AudioFormat>(_sdl, "AudioFormat", py::arithmetic())
        .value("AUDIO_UNKNOWN", SDL_AudioFormat::SDL_AUDIO_UNKNOWN)
        .value("AUDIO_U8", SDL_AudioFormat::SDL_AUDIO_U8)
        .value("AUDIO_S8", SDL_AudioFormat::SDL_AUDIO_S8)
        .value("AUDIO_S16_LE", SDL_AudioFormat::SDL_AUDIO_S16LE)
        .value("AUDIO_S16_BE", SDL_AudioFormat::SDL_AUDIO_S16BE)
        .value("AUDIO_S32_LE", SDL_AudioFormat::SDL_AUDIO_S32LE)
        .value("AUDIO_S32_BE", SDL_AudioFormat::SDL_AUDIO_S32BE)
        .value("AUDIO_F32_LE", SDL_AudioFormat::SDL_AUDIO_F32LE)
        .value("AUDIO_F32_BE", SDL_AudioFormat::SDL_AUDIO_F32BE)
        .value("AUDIO_S16", SDL_AudioFormat::SDL_AUDIO_S16)
        .value("AUDIO_S32", SDL_AudioFormat::SDL_AUDIO_S32)
        .value("AUDIO_F32", SDL_AudioFormat::SDL_AUDIO_F32)
        .export_values()
    ;
    py::class_<SDL_AudioSpec> _AudioSpec(_sdl, "AudioSpec");
    registry.on(_sdl, "AudioSpec", _AudioSpec);
        _AudioSpec
        .def_readwrite("format", &SDL_AudioSpec::format)
        .def_readwrite("channels", &SDL_AudioSpec::channels)
        .def_readwrite("freq", &SDL_AudioSpec::freq)
    ;

    _sdl
    .def("get_num_audio_drivers", &SDL_GetNumAudioDrivers
        , py::return_value_policy::automatic_reference)
    .def("get_audio_driver", &SDL_GetAudioDriver
        , py::arg("index")
        , py::return_value_policy::automatic_reference)
    .def("get_current_audio_driver", &SDL_GetCurrentAudioDriver
        , py::return_value_policy::automatic_reference)
    .def("get_audio_playback_devices", [](int * count)
        {
            auto ret = SDL_GetAudioPlaybackDevices(count);
            return std::make_tuple(ret, count);
        }
        , py::arg("count")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_recording_devices", [](int * count)
        {
            auto ret = SDL_GetAudioRecordingDevices(count);
            return std::make_tuple(ret, count);
        }
        , py::arg("count")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_device_name", &SDL_GetAudioDeviceName
        , py::arg("devid")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_device_format", [](unsigned int devid, SDL_AudioSpec * spec, int * sample_frames)
        {
            auto ret = SDL_GetAudioDeviceFormat(devid, spec, sample_frames);
            return std::make_tuple(ret, sample_frames);
        }
        , py::arg("devid")
        , py::arg("spec")
        , py::arg("sample_frames")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_device_channel_map", [](unsigned int devid, int * count)
        {
            auto ret = SDL_GetAudioDeviceChannelMap(devid, count);
            return std::make_tuple(ret, count);
        }
        , py::arg("devid")
        , py::arg("count")
        , py::return_value_policy::automatic_reference)
    .def("open_audio_device", &SDL_OpenAudioDevice
        , py::arg("devid")
        , py::arg("spec")
        , py::return_value_policy::automatic_reference)
    .def("is_audio_device_physical", &SDL_IsAudioDevicePhysical
        , py::arg("devid")
        , py::return_value_policy::automatic_reference)
    .def("is_audio_device_playback", &SDL_IsAudioDevicePlayback
        , py::arg("devid")
        , py::return_value_policy::automatic_reference)
    .def("pause_audio_device", &SDL_PauseAudioDevice
        , py::arg("devid")
        , py::return_value_policy::automatic_reference)
    .def("resume_audio_device", &SDL_ResumeAudioDevice
        , py::arg("devid")
        , py::return_value_policy::automatic_reference)
    .def("audio_device_paused", &SDL_AudioDevicePaused
        , py::arg("devid")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_device_gain", &SDL_GetAudioDeviceGain
        , py::arg("devid")
        , py::return_value_policy::automatic_reference)
    .def("set_audio_device_gain", &SDL_SetAudioDeviceGain
        , py::arg("devid")
        , py::arg("gain")
        , py::return_value_policy::automatic_reference)
    .def("close_audio_device", &SDL_CloseAudioDevice
        , py::arg("devid")
        , py::return_value_policy::automatic_reference)
    .def("bind_audio_streams", [](unsigned int devid, const py::capsule& streams, int num_streams)
        {
            auto ret = SDL_BindAudioStreams(devid, streams, num_streams);
            return ret;
        }
        , py::arg("devid")
        , py::arg("streams")
        , py::arg("num_streams")
        , py::return_value_policy::automatic_reference)
    .def("bind_audio_stream", [](unsigned int devid, const py::capsule& stream)
        {
            auto ret = SDL_BindAudioStream(devid, stream);
            return ret;
        }
        , py::arg("devid")
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("unbind_audio_streams", [](const py::capsule& streams, int num_streams)
        {
            SDL_UnbindAudioStreams(streams, num_streams);
            return ;
        }
        , py::arg("streams")
        , py::arg("num_streams")
        , py::return_value_policy::automatic_reference)
    .def("unbind_audio_stream", [](const py::capsule& stream)
        {
            SDL_UnbindAudioStream(stream);
            return ;
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_stream_device", [](const py::capsule& stream)
        {
            auto ret = SDL_GetAudioStreamDevice(stream);
            return ret;
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("create_audio_stream", [](const SDL_AudioSpec * src_spec, const SDL_AudioSpec * dst_spec)
        {
            auto ret = py::capsule(SDL_CreateAudioStream(src_spec, dst_spec), "SDL_AudioStream");
            return ret;
        }
        , py::arg("src_spec")
        , py::arg("dst_spec")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_stream_properties", [](const py::capsule& stream)
        {
            auto ret = SDL_GetAudioStreamProperties(stream);
            return ret;
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_stream_format", [](const py::capsule& stream, SDL_AudioSpec * src_spec, SDL_AudioSpec * dst_spec)
        {
            auto ret = SDL_GetAudioStreamFormat(stream, src_spec, dst_spec);
            return ret;
        }
        , py::arg("stream")
        , py::arg("src_spec")
        , py::arg("dst_spec")
        , py::return_value_policy::automatic_reference)
    .def("set_audio_stream_format", [](const py::capsule& stream, const SDL_AudioSpec * src_spec, const SDL_AudioSpec * dst_spec)
        {
            auto ret = SDL_SetAudioStreamFormat(stream, src_spec, dst_spec);
            return ret;
        }
        , py::arg("stream")
        , py::arg("src_spec")
        , py::arg("dst_spec")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_stream_frequency_ratio", [](const py::capsule& stream)
        {
            auto ret = SDL_GetAudioStreamFrequencyRatio(stream);
            return ret;
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("set_audio_stream_frequency_ratio", [](const py::capsule& stream, float ratio)
        {
            auto ret = SDL_SetAudioStreamFrequencyRatio(stream, ratio);
            return ret;
        }
        , py::arg("stream")
        , py::arg("ratio")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_stream_gain", [](const py::capsule& stream)
        {
            auto ret = SDL_GetAudioStreamGain(stream);
            return ret;
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("set_audio_stream_gain", [](const py::capsule& stream, float gain)
        {
            auto ret = SDL_SetAudioStreamGain(stream, gain);
            return ret;
        }
        , py::arg("stream")
        , py::arg("gain")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_stream_input_channel_map", [](const py::capsule& stream, int * count)
        {
            auto ret = SDL_GetAudioStreamInputChannelMap(stream, count);
            return std::make_tuple(ret, count);
        }
        , py::arg("stream")
        , py::arg("count")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_stream_output_channel_map", [](const py::capsule& stream, int * count)
        {
            auto ret = SDL_GetAudioStreamOutputChannelMap(stream, count);
            return std::make_tuple(ret, count);
        }
        , py::arg("stream")
        , py::arg("count")
        , py::return_value_policy::automatic_reference)
    .def("set_audio_stream_input_channel_map", [](const py::capsule& stream, const int * chmap, int count)
        {
            auto ret = SDL_SetAudioStreamInputChannelMap(stream, chmap, count);
            return ret;
        }
        , py::arg("stream")
        , py::arg("chmap")
        , py::arg("count")
        , py::return_value_policy::automatic_reference)
    .def("set_audio_stream_output_channel_map", [](const py::capsule& stream, const int * chmap, int count)
        {
            auto ret = SDL_SetAudioStreamOutputChannelMap(stream, chmap, count);
            return ret;
        }
        , py::arg("stream")
        , py::arg("chmap")
        , py::arg("count")
        , py::return_value_policy::automatic_reference)
    .def("put_audio_stream_data", [](const py::capsule& stream, const void * buf, int len)
        {
            auto ret = SDL_PutAudioStreamData(stream, buf, len);
            return ret;
        }
        , py::arg("stream")
        , py::arg("buf")
        , py::arg("len")
        , py::return_value_policy::automatic_reference)
    .def("put_audio_stream_planar_data", [](const py::capsule& stream, const void *const * channel_buffers, int num_channels, int num_samples)
        {
            auto ret = SDL_PutAudioStreamPlanarData(stream, channel_buffers, num_channels, num_samples);
            return ret;
        }
        , py::arg("stream")
        , py::arg("channel_buffers")
        , py::arg("num_channels")
        , py::arg("num_samples")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_stream_data", [](const py::capsule& stream, void * buf, int len)
        {
            auto ret = SDL_GetAudioStreamData(stream, buf, len);
            return ret;
        }
        , py::arg("stream")
        , py::arg("buf")
        , py::arg("len")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_stream_available", [](const py::capsule& stream)
        {
            auto ret = SDL_GetAudioStreamAvailable(stream);
            return ret;
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_stream_queued", [](const py::capsule& stream)
        {
            auto ret = SDL_GetAudioStreamQueued(stream);
            return ret;
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("flush_audio_stream", [](const py::capsule& stream)
        {
            auto ret = SDL_FlushAudioStream(stream);
            return ret;
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("clear_audio_stream", [](const py::capsule& stream)
        {
            auto ret = SDL_ClearAudioStream(stream);
            return ret;
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("pause_audio_stream_device", [](const py::capsule& stream)
        {
            auto ret = SDL_PauseAudioStreamDevice(stream);
            return ret;
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("resume_audio_stream_device", [](const py::capsule& stream)
        {
            auto ret = SDL_ResumeAudioStreamDevice(stream);
            return ret;
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("audio_stream_device_paused", [](const py::capsule& stream)
        {
            auto ret = SDL_AudioStreamDevicePaused(stream);
            return ret;
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("lock_audio_stream", [](const py::capsule& stream)
        {
            auto ret = SDL_LockAudioStream(stream);
            return ret;
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("unlock_audio_stream", [](const py::capsule& stream)
        {
            auto ret = SDL_UnlockAudioStream(stream);
            return ret;
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("destroy_audio_stream", [](const py::capsule& stream)
        {
            SDL_DestroyAudioStream(stream);
            return ;
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("open_audio_device_stream", [](unsigned int devid, const SDL_AudioSpec * spec, void (*)(void *, SDL_AudioStream *, int, int) callback, void * userdata)
        {
            auto ret = py::capsule(SDL_OpenAudioDeviceStream(devid, spec, callback, userdata), "SDL_AudioStream");
            return ret;
        }
        , py::arg("devid")
        , py::arg("spec")
        , py::arg("callback")
        , py::arg("userdata")
        , py::return_value_policy::automatic_reference)
    .def("set_audio_postmix_callback", &SDL_SetAudioPostmixCallback
        , py::arg("devid")
        , py::arg("callback")
        , py::arg("userdata")
        , py::return_value_policy::automatic_reference)
    .def("load_wav_io", [](SDL_IOStream * src, bool closeio, SDL_AudioSpec * spec, unsigned char ** audio_buf, unsigned int * audio_len)
        {
            auto ret = SDL_LoadWAV_IO(src, closeio, spec, audio_buf, audio_len);
            return std::make_tuple(ret, audio_len);
        }
        , py::arg("src")
        , py::arg("closeio")
        , py::arg("spec")
        , py::arg("audio_buf")
        , py::arg("audio_len")
        , py::return_value_policy::automatic_reference)
    .def("load_wav", [](const char * path, SDL_AudioSpec * spec, unsigned char ** audio_buf, unsigned int * audio_len)
        {
            auto ret = SDL_LoadWAV(path, spec, audio_buf, audio_len);
            return std::make_tuple(ret, audio_len);
        }
        , py::arg("path")
        , py::arg("spec")
        , py::arg("audio_buf")
        , py::arg("audio_len")
        , py::return_value_policy::automatic_reference)
    .def("mix_audio", &SDL_MixAudio
        , py::arg("dst")
        , py::arg("src")
        , py::arg("format")
        , py::arg("len")
        , py::arg("volume")
        , py::return_value_policy::automatic_reference)
    .def("convert_audio_samples", [](const SDL_AudioSpec * src_spec, const unsigned char * src_data, int src_len, const SDL_AudioSpec * dst_spec, unsigned char ** dst_data, int * dst_len)
        {
            auto ret = SDL_ConvertAudioSamples(src_spec, src_data, src_len, dst_spec, dst_data, dst_len);
            return std::make_tuple(ret, dst_len);
        }
        , py::arg("src_spec")
        , py::arg("src_data")
        , py::arg("src_len")
        , py::arg("dst_spec")
        , py::arg("dst_data")
        , py::arg("dst_len")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_format_name", &SDL_GetAudioFormatName
        , py::arg("format")
        , py::return_value_policy::automatic_reference)
    .def("get_silence_value_for_format", &SDL_GetSilenceValueForFormat
        , py::arg("format")
        , py::return_value_policy::automatic_reference)
    ;


}