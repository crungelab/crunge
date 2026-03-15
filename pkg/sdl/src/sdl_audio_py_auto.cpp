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
        , py::return_value_policy::automatic_reference)
    .def("get_audio_driver", &SDL_GetAudioDriver
        , py::arg("index")
        , py::return_value_policy::automatic_reference)
    .def("get_current_audio_driver", &SDL_GetCurrentAudioDriver
        , py::return_value_policy::automatic_reference)
    .def("get_audio_playback_devices", [](int * count)
        {
            SDL_GetAudioPlaybackDevices(count);
            return std::make_tuple(count);
        }
        , py::arg("count")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_recording_devices", [](int * count)
        {
            SDL_GetAudioRecordingDevices(count);
            return std::make_tuple(count);
        }
        , py::arg("count")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_device_name", &SDL_GetAudioDeviceName
        , py::arg("devid")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_device_format", [](SDL_AudioDeviceID devid, SDL_AudioSpec * spec, int * sample_frames)
        {
            SDL_GetAudioDeviceFormat(devid, spec, sample_frames);
            return std::make_tuple(sample_frames);
        }
        , py::arg("devid")
        , py::arg("spec")
        , py::arg("sample_frames")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_device_channel_map", [](SDL_AudioDeviceID devid, int * count)
        {
            SDL_GetAudioDeviceChannelMap(devid, count);
            return std::make_tuple(count);
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
    .def("bind_audio_streams", &SDL_BindAudioStreams
        , py::arg("devid")
        , py::arg("streams")
        , py::arg("num_streams")
        , py::return_value_policy::automatic_reference)
    .def("bind_audio_stream", [](SDL_AudioDeviceID devid, const py::capsule& stream)
        {
            return SDL_BindAudioStream(devid, stream.get());
        }
        , py::arg("devid")
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("unbind_audio_streams", &SDL_UnbindAudioStreams
        , py::arg("streams")
        , py::arg("num_streams")
        , py::return_value_policy::automatic_reference)
    .def("unbind_audio_stream", [](const py::capsule& stream)
        {
            return SDL_UnbindAudioStream(stream.get());
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_stream_device", [](const py::capsule& stream)
        {
            return SDL_GetAudioStreamDevice(stream.get());
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("create_audio_stream", [](const SDL_AudioSpec * src_spec, const SDL_AudioSpec * dst_spec)
        {
            return py::capsule(SDL_CreateAudioStream(src_spec, dst_spec));
        }
        , py::arg("src_spec")
        , py::arg("dst_spec")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_stream_properties", [](const py::capsule& stream)
        {
            return SDL_GetAudioStreamProperties(stream.get());
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_stream_format", [](const py::capsule& stream, SDL_AudioSpec * src_spec, SDL_AudioSpec * dst_spec)
        {
            return SDL_GetAudioStreamFormat(stream.get(), src_spec, dst_spec);
        }
        , py::arg("stream")
        , py::arg("src_spec")
        , py::arg("dst_spec")
        , py::return_value_policy::automatic_reference)
    .def("set_audio_stream_format", [](const py::capsule& stream, const SDL_AudioSpec * src_spec, const SDL_AudioSpec * dst_spec)
        {
            return SDL_SetAudioStreamFormat(stream.get(), src_spec, dst_spec);
        }
        , py::arg("stream")
        , py::arg("src_spec")
        , py::arg("dst_spec")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_stream_frequency_ratio", [](const py::capsule& stream)
        {
            return SDL_GetAudioStreamFrequencyRatio(stream.get());
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("set_audio_stream_frequency_ratio", [](const py::capsule& stream, float ratio)
        {
            return SDL_SetAudioStreamFrequencyRatio(stream.get(), ratio);
        }
        , py::arg("stream")
        , py::arg("ratio")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_stream_gain", [](const py::capsule& stream)
        {
            return SDL_GetAudioStreamGain(stream.get());
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("set_audio_stream_gain", [](const py::capsule& stream, float gain)
        {
            return SDL_SetAudioStreamGain(stream.get(), gain);
        }
        , py::arg("stream")
        , py::arg("gain")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_stream_input_channel_map", [](const py::capsule& stream, int * count)
        {
            SDL_GetAudioStreamInputChannelMap(stream.get(), count);
            return std::make_tuple(count);
        }
        , py::arg("stream")
        , py::arg("count")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_stream_output_channel_map", [](const py::capsule& stream, int * count)
        {
            SDL_GetAudioStreamOutputChannelMap(stream.get(), count);
            return std::make_tuple(count);
        }
        , py::arg("stream")
        , py::arg("count")
        , py::return_value_policy::automatic_reference)
    .def("set_audio_stream_input_channel_map", [](const py::capsule& stream, const int * chmap, int count)
        {
            return SDL_SetAudioStreamInputChannelMap(stream.get(), chmap, count);
        }
        , py::arg("stream")
        , py::arg("chmap")
        , py::arg("count")
        , py::return_value_policy::automatic_reference)
    .def("set_audio_stream_output_channel_map", [](const py::capsule& stream, const int * chmap, int count)
        {
            return SDL_SetAudioStreamOutputChannelMap(stream.get(), chmap, count);
        }
        , py::arg("stream")
        , py::arg("chmap")
        , py::arg("count")
        , py::return_value_policy::automatic_reference)
    .def("put_audio_stream_data", [](const py::capsule& stream, const void * buf, int len)
        {
            return SDL_PutAudioStreamData(stream.get(), buf, len);
        }
        , py::arg("stream")
        , py::arg("buf")
        , py::arg("len")
        , py::return_value_policy::automatic_reference)
    .def("put_audio_stream_planar_data", [](const py::capsule& stream, const void *const * channel_buffers, int num_channels, int num_samples)
        {
            return SDL_PutAudioStreamPlanarData(stream.get(), channel_buffers, num_channels, num_samples);
        }
        , py::arg("stream")
        , py::arg("channel_buffers")
        , py::arg("num_channels")
        , py::arg("num_samples")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_stream_data", [](const py::capsule& stream, void * buf, int len)
        {
            return SDL_GetAudioStreamData(stream.get(), buf, len);
        }
        , py::arg("stream")
        , py::arg("buf")
        , py::arg("len")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_stream_available", [](const py::capsule& stream)
        {
            return SDL_GetAudioStreamAvailable(stream.get());
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("get_audio_stream_queued", [](const py::capsule& stream)
        {
            return SDL_GetAudioStreamQueued(stream.get());
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("flush_audio_stream", [](const py::capsule& stream)
        {
            return SDL_FlushAudioStream(stream.get());
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("clear_audio_stream", [](const py::capsule& stream)
        {
            return SDL_ClearAudioStream(stream.get());
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("pause_audio_stream_device", [](const py::capsule& stream)
        {
            return SDL_PauseAudioStreamDevice(stream.get());
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("resume_audio_stream_device", [](const py::capsule& stream)
        {
            return SDL_ResumeAudioStreamDevice(stream.get());
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("audio_stream_device_paused", [](const py::capsule& stream)
        {
            return SDL_AudioStreamDevicePaused(stream.get());
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("lock_audio_stream", [](const py::capsule& stream)
        {
            return SDL_LockAudioStream(stream.get());
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("unlock_audio_stream", [](const py::capsule& stream)
        {
            return SDL_UnlockAudioStream(stream.get());
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("destroy_audio_stream", [](const py::capsule& stream)
        {
            return SDL_DestroyAudioStream(stream.get());
        }
        , py::arg("stream")
        , py::return_value_policy::automatic_reference)
    .def("open_audio_device_stream", [](SDL_AudioDeviceID devid, const SDL_AudioSpec * spec, SDL_AudioStreamCallback callback, void * userdata)
        {
            return py::capsule(SDL_OpenAudioDeviceStream(devid, spec, callback, userdata));
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
    .def("load_wav_io", [](SDL_IOStream * src, _Bool closeio, SDL_AudioSpec * spec, Uint8 ** audio_buf, Uint32 * audio_len)
        {
            SDL_LoadWAV_IO(src, closeio, spec, audio_buf, audio_len);
            return std::make_tuple(audio_len);
        }
        , py::arg("src")
        , py::arg("closeio")
        , py::arg("spec")
        , py::arg("audio_buf")
        , py::arg("audio_len")
        , py::return_value_policy::automatic_reference)
    .def("load_wav", [](const char * path, SDL_AudioSpec * spec, Uint8 ** audio_buf, Uint32 * audio_len)
        {
            SDL_LoadWAV(path, spec, audio_buf, audio_len);
            return std::make_tuple(audio_len);
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
    .def("convert_audio_samples", [](const SDL_AudioSpec * src_spec, const Uint8 * src_data, int src_len, const SDL_AudioSpec * dst_spec, Uint8 ** dst_data, int * dst_len)
        {
            SDL_ConvertAudioSamples(src_spec, src_data, src_len, dst_spec, dst_data, dst_len);
            return std::make_tuple(dst_len);
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