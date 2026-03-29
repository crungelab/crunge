#include <stdbool.h>
#include <limits>
#include <iostream>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <SDL3/SDL.h>
#include <SDL3/SDL_audio.h>
#include <SDL3/SDL_iostream.h>

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
        )
    .def("get_audio_driver", &SDL_GetAudioDriver
        , py::arg("index")
        )
    .def("get_current_audio_driver", &SDL_GetCurrentAudioDriver
        )
    .def("get_audio_playback_devices", [](int * count)
        {
            auto _ret = SDL_GetAudioPlaybackDevices(count);
            return std::make_tuple(_ret, count);
        }
        , py::arg("count")
        )
    .def("get_audio_recording_devices", [](int * count)
        {
            auto _ret = SDL_GetAudioRecordingDevices(count);
            return std::make_tuple(_ret, count);
        }
        , py::arg("count")
        )
    .def("get_audio_device_name", &SDL_GetAudioDeviceName
        , py::arg("devid")
        )
    .def("get_audio_device_format", [](SDL_AudioDeviceID devid, SDL_AudioSpec * spec, int * sample_frames)
        {
            auto _ret = SDL_GetAudioDeviceFormat(devid, spec, sample_frames);
            return std::make_tuple(_ret, sample_frames);
        }
        , py::arg("devid")
        , py::arg("spec")
        , py::arg("sample_frames")
        )
    .def("get_audio_device_channel_map", [](SDL_AudioDeviceID devid, int * count)
        {
            auto _ret = SDL_GetAudioDeviceChannelMap(devid, count);
            return std::make_tuple(_ret, count);
        }
        , py::arg("devid")
        , py::arg("count")
        )
    .def("open_audio_device", &SDL_OpenAudioDevice
        , py::arg("devid")
        , py::arg("spec")
        )
    .def("is_audio_device_physical", &SDL_IsAudioDevicePhysical
        , py::arg("devid")
        )
    .def("is_audio_device_playback", &SDL_IsAudioDevicePlayback
        , py::arg("devid")
        )
    .def("pause_audio_device", &SDL_PauseAudioDevice
        , py::arg("devid")
        )
    .def("resume_audio_device", &SDL_ResumeAudioDevice
        , py::arg("devid")
        )
    .def("audio_device_paused", &SDL_AudioDevicePaused
        , py::arg("devid")
        )
    .def("get_audio_device_gain", &SDL_GetAudioDeviceGain
        , py::arg("devid")
        )
    .def("set_audio_device_gain", &SDL_SetAudioDeviceGain
        , py::arg("devid")
        , py::arg("gain")
        )
    .def("close_audio_device", &SDL_CloseAudioDevice
        , py::arg("devid")
        )
    .def("bind_audio_stream", [](SDL_AudioDeviceID devid, py::capsule stream)
        {
            return SDL_BindAudioStream(devid, static_cast<SDL_AudioStream *>(stream.get_pointer()));
        }
        , py::arg("devid")
        , py::arg("stream")
        )
    .def("unbind_audio_stream", [](py::capsule stream)
        {
            return SDL_UnbindAudioStream(static_cast<SDL_AudioStream *>(stream.get_pointer()));
        }
        , py::arg("stream")
        )
    .def("get_audio_stream_device", [](py::capsule stream)
        {
            return SDL_GetAudioStreamDevice(static_cast<SDL_AudioStream *>(stream.get_pointer()));
        }
        , py::arg("stream")
        )
    .def("create_audio_stream", [](const SDL_AudioSpec * src_spec, const SDL_AudioSpec * dst_spec)
        {
            return py::capsule(SDL_CreateAudioStream(src_spec, dst_spec), "SDL_AudioStream");
        }
        , py::arg("src_spec")
        , py::arg("dst_spec")
        )
    .def("get_audio_stream_properties", [](py::capsule stream)
        {
            return SDL_GetAudioStreamProperties(static_cast<SDL_AudioStream *>(stream.get_pointer()));
        }
        , py::arg("stream")
        )
    .def("get_audio_stream_format", [](py::capsule stream, SDL_AudioSpec * src_spec, SDL_AudioSpec * dst_spec)
        {
            return SDL_GetAudioStreamFormat(static_cast<SDL_AudioStream *>(stream.get_pointer()), src_spec, dst_spec);
        }
        , py::arg("stream")
        , py::arg("src_spec")
        , py::arg("dst_spec")
        )
    .def("set_audio_stream_format", [](py::capsule stream, const SDL_AudioSpec * src_spec, const SDL_AudioSpec * dst_spec)
        {
            return SDL_SetAudioStreamFormat(static_cast<SDL_AudioStream *>(stream.get_pointer()), src_spec, dst_spec);
        }
        , py::arg("stream")
        , py::arg("src_spec")
        , py::arg("dst_spec")
        )
    .def("get_audio_stream_frequency_ratio", [](py::capsule stream)
        {
            return SDL_GetAudioStreamFrequencyRatio(static_cast<SDL_AudioStream *>(stream.get_pointer()));
        }
        , py::arg("stream")
        )
    .def("set_audio_stream_frequency_ratio", [](py::capsule stream, float ratio)
        {
            return SDL_SetAudioStreamFrequencyRatio(static_cast<SDL_AudioStream *>(stream.get_pointer()), ratio);
        }
        , py::arg("stream")
        , py::arg("ratio")
        )
    .def("get_audio_stream_gain", [](py::capsule stream)
        {
            return SDL_GetAudioStreamGain(static_cast<SDL_AudioStream *>(stream.get_pointer()));
        }
        , py::arg("stream")
        )
    .def("set_audio_stream_gain", [](py::capsule stream, float gain)
        {
            return SDL_SetAudioStreamGain(static_cast<SDL_AudioStream *>(stream.get_pointer()), gain);
        }
        , py::arg("stream")
        , py::arg("gain")
        )
    .def("get_audio_stream_input_channel_map", [](py::capsule stream, int * count)
        {
            auto _ret = SDL_GetAudioStreamInputChannelMap(static_cast<SDL_AudioStream *>(stream.get_pointer()), count);
            return std::make_tuple(_ret, count);
        }
        , py::arg("stream")
        , py::arg("count")
        )
    .def("get_audio_stream_output_channel_map", [](py::capsule stream, int * count)
        {
            auto _ret = SDL_GetAudioStreamOutputChannelMap(static_cast<SDL_AudioStream *>(stream.get_pointer()), count);
            return std::make_tuple(_ret, count);
        }
        , py::arg("stream")
        , py::arg("count")
        )
    .def("set_audio_stream_input_channel_map", [](py::capsule stream, const int * chmap, int count)
        {
            return SDL_SetAudioStreamInputChannelMap(static_cast<SDL_AudioStream *>(stream.get_pointer()), chmap, count);
        }
        , py::arg("stream")
        , py::arg("chmap")
        , py::arg("count")
        )
    .def("set_audio_stream_output_channel_map", [](py::capsule stream, const int * chmap, int count)
        {
            return SDL_SetAudioStreamOutputChannelMap(static_cast<SDL_AudioStream *>(stream.get_pointer()), chmap, count);
        }
        , py::arg("stream")
        , py::arg("chmap")
        , py::arg("count")
        )
    .def("put_audio_stream_data", [](py::capsule stream, const void * buf, int len)
        {
            return SDL_PutAudioStreamData(static_cast<SDL_AudioStream *>(stream.get_pointer()), buf, len);
        }
        , py::arg("stream")
        , py::arg("buf")
        , py::arg("len")
        )
    .def("get_audio_stream_data", [](py::capsule stream, void * buf, int len)
        {
            return SDL_GetAudioStreamData(static_cast<SDL_AudioStream *>(stream.get_pointer()), buf, len);
        }
        , py::arg("stream")
        , py::arg("buf")
        , py::arg("len")
        )
    .def("get_audio_stream_available", [](py::capsule stream)
        {
            return SDL_GetAudioStreamAvailable(static_cast<SDL_AudioStream *>(stream.get_pointer()));
        }
        , py::arg("stream")
        )
    .def("get_audio_stream_queued", [](py::capsule stream)
        {
            return SDL_GetAudioStreamQueued(static_cast<SDL_AudioStream *>(stream.get_pointer()));
        }
        , py::arg("stream")
        )
    .def("flush_audio_stream", [](py::capsule stream)
        {
            return SDL_FlushAudioStream(static_cast<SDL_AudioStream *>(stream.get_pointer()));
        }
        , py::arg("stream")
        )
    .def("clear_audio_stream", [](py::capsule stream)
        {
            return SDL_ClearAudioStream(static_cast<SDL_AudioStream *>(stream.get_pointer()));
        }
        , py::arg("stream")
        )
    .def("pause_audio_stream_device", [](py::capsule stream)
        {
            return SDL_PauseAudioStreamDevice(static_cast<SDL_AudioStream *>(stream.get_pointer()));
        }
        , py::arg("stream")
        )
    .def("resume_audio_stream_device", [](py::capsule stream)
        {
            return SDL_ResumeAudioStreamDevice(static_cast<SDL_AudioStream *>(stream.get_pointer()));
        }
        , py::arg("stream")
        )
    .def("audio_stream_device_paused", [](py::capsule stream)
        {
            return SDL_AudioStreamDevicePaused(static_cast<SDL_AudioStream *>(stream.get_pointer()));
        }
        , py::arg("stream")
        )
    .def("lock_audio_stream", [](py::capsule stream)
        {
            return SDL_LockAudioStream(static_cast<SDL_AudioStream *>(stream.get_pointer()));
        }
        , py::arg("stream")
        )
    .def("unlock_audio_stream", [](py::capsule stream)
        {
            return SDL_UnlockAudioStream(static_cast<SDL_AudioStream *>(stream.get_pointer()));
        }
        , py::arg("stream")
        )
    .def("destroy_audio_stream", [](py::capsule stream)
        {
            return SDL_DestroyAudioStream(static_cast<SDL_AudioStream *>(stream.get_pointer()));
        }
        , py::arg("stream")
        )
    .def("open_audio_device_stream", [](SDL_AudioDeviceID devid, const SDL_AudioSpec * spec, void (*callback)(void *, struct SDL_AudioStream *, int, int), void * userdata)
        {
            return py::capsule(SDL_OpenAudioDeviceStream(devid, spec, callback, userdata), "SDL_AudioStream");
        }
        , py::arg("devid")
        , py::arg("spec")
        , py::arg("callback")
        , py::arg("userdata")
        )
    .def("set_audio_postmix_callback", &SDL_SetAudioPostmixCallback
        , py::arg("devid")
        , py::arg("callback")
        , py::arg("userdata")
        )
    .def("mix_audio", &SDL_MixAudio
        , py::arg("dst")
        , py::arg("src")
        , py::arg("format")
        , py::arg("len")
        , py::arg("volume")
        )
    .def("get_audio_format_name", &SDL_GetAudioFormatName
        , py::arg("format")
        )
    .def("get_silence_value_for_format", &SDL_GetSilenceValueForFormat
        , py::arg("format")
        )
    ;


}