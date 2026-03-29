#include <stdbool.h>
#include <limits>
#include <iostream>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <SDL3/SDL.h>
#include <SDL3/SDL_audio.h>
#include <SDL3/SDL_iostream.h>

#include <SDL3_mixer/SDL_mixer.h>

#include <cxbind/cxbind.h>

#include <crunge/sdl/crunge-sdl.h>
#include <crunge/sdl/conversions.h>

namespace py = pybind11;

void init_sdl_mixer_py_auto(py::module &_sdl, Registry &registry) {
    _sdl
    .def("version", &MIX_Version
        )
    .def("init", &MIX_Init
        )
    .def("quit", &MIX_Quit
        )
    .def("get_num_audio_decoders", &MIX_GetNumAudioDecoders
        )
    .def("get_audio_decoder", &MIX_GetAudioDecoder
        , py::arg("index")
        )
    .def("create_mixer_device", [](SDL_AudioDeviceID devid, const SDL_AudioSpec * spec)
        {
            return py::capsule(MIX_CreateMixerDevice(devid, spec), "MIX_Mixer");
        }
        , py::arg("devid")
        , py::arg("spec")
        )
    .def("create_mixer", [](const SDL_AudioSpec * spec)
        {
            return py::capsule(MIX_CreateMixer(spec), "MIX_Mixer");
        }
        , py::arg("spec")
        )
    .def("destroy_mixer", [](py::capsule mixer)
        {
            return MIX_DestroyMixer(static_cast<MIX_Mixer *>(mixer.get_pointer()));
        }
        , py::arg("mixer")
        )
    .def("get_mixer_properties", [](py::capsule mixer)
        {
            return MIX_GetMixerProperties(static_cast<MIX_Mixer *>(mixer.get_pointer()));
        }
        , py::arg("mixer")
        )
    .def("get_mixer_format", [](py::capsule mixer, SDL_AudioSpec * spec)
        {
            return MIX_GetMixerFormat(static_cast<MIX_Mixer *>(mixer.get_pointer()), spec);
        }
        , py::arg("mixer")
        , py::arg("spec")
        )
    .def("lock_mixer", [](py::capsule mixer)
        {
            return MIX_LockMixer(static_cast<MIX_Mixer *>(mixer.get_pointer()));
        }
        , py::arg("mixer")
        )
    .def("unlock_mixer", [](py::capsule mixer)
        {
            return MIX_UnlockMixer(static_cast<MIX_Mixer *>(mixer.get_pointer()));
        }
        , py::arg("mixer")
        )
    .def("load_audio_io", [](py::capsule mixer, py::capsule io, bool predecode, bool closeio)
        {
            return py::capsule(MIX_LoadAudio_IO(static_cast<MIX_Mixer *>(mixer.get_pointer()), static_cast<SDL_IOStream *>(io.get_pointer()), predecode, closeio), "MIX_Audio");
        }
        , py::arg("mixer")
        , py::arg("io")
        , py::arg("predecode")
        , py::arg("closeio")
        )
    .def("load_audio", [](py::capsule mixer, const char * path, bool predecode)
        {
            return py::capsule(MIX_LoadAudio(static_cast<MIX_Mixer *>(mixer.get_pointer()), path, predecode), "MIX_Audio");
        }
        , py::arg("mixer")
        , py::arg("path")
        , py::arg("predecode")
        )
    .def("load_audio_no_copy", [](py::capsule mixer, const void * data, size_t datalen, bool free_when_done)
        {
            return py::capsule(MIX_LoadAudioNoCopy(static_cast<MIX_Mixer *>(mixer.get_pointer()), data, datalen, free_when_done), "MIX_Audio");
        }
        , py::arg("mixer")
        , py::arg("data")
        , py::arg("datalen")
        , py::arg("free_when_done")
        )
    .def("load_audio_with_properties", [](SDL_PropertiesID props)
        {
            return py::capsule(MIX_LoadAudioWithProperties(props), "MIX_Audio");
        }
        , py::arg("props")
        )
    .def("load_raw_audio_io", [](py::capsule mixer, py::capsule io, const SDL_AudioSpec * spec, bool closeio)
        {
            return py::capsule(MIX_LoadRawAudio_IO(static_cast<MIX_Mixer *>(mixer.get_pointer()), static_cast<SDL_IOStream *>(io.get_pointer()), spec, closeio), "MIX_Audio");
        }
        , py::arg("mixer")
        , py::arg("io")
        , py::arg("spec")
        , py::arg("closeio")
        )
    .def("load_raw_audio", [](py::capsule mixer, const void * data, size_t datalen, const SDL_AudioSpec * spec)
        {
            return py::capsule(MIX_LoadRawAudio(static_cast<MIX_Mixer *>(mixer.get_pointer()), data, datalen, spec), "MIX_Audio");
        }
        , py::arg("mixer")
        , py::arg("data")
        , py::arg("datalen")
        , py::arg("spec")
        )
    .def("load_raw_audio_no_copy", [](py::capsule mixer, const void * data, size_t datalen, const SDL_AudioSpec * spec, bool free_when_done)
        {
            return py::capsule(MIX_LoadRawAudioNoCopy(static_cast<MIX_Mixer *>(mixer.get_pointer()), data, datalen, spec, free_when_done), "MIX_Audio");
        }
        , py::arg("mixer")
        , py::arg("data")
        , py::arg("datalen")
        , py::arg("spec")
        , py::arg("free_when_done")
        )
    .def("create_sine_wave_audio", [](py::capsule mixer, int hz, float amplitude, Sint64 ms)
        {
            return py::capsule(MIX_CreateSineWaveAudio(static_cast<MIX_Mixer *>(mixer.get_pointer()), hz, amplitude, ms), "MIX_Audio");
        }
        , py::arg("mixer")
        , py::arg("hz")
        , py::arg("amplitude")
        , py::arg("ms")
        )
    .def("get_audio_properties", [](py::capsule audio)
        {
            return MIX_GetAudioProperties(static_cast<MIX_Audio *>(audio.get_pointer()));
        }
        , py::arg("audio")
        )
    .def("get_audio_duration", [](py::capsule audio)
        {
            return MIX_GetAudioDuration(static_cast<MIX_Audio *>(audio.get_pointer()));
        }
        , py::arg("audio")
        )
    .def("get_audio_format", [](py::capsule audio, SDL_AudioSpec * spec)
        {
            return MIX_GetAudioFormat(static_cast<MIX_Audio *>(audio.get_pointer()), spec);
        }
        , py::arg("audio")
        , py::arg("spec")
        )
    .def("destroy_audio", [](py::capsule audio)
        {
            return MIX_DestroyAudio(static_cast<MIX_Audio *>(audio.get_pointer()));
        }
        , py::arg("audio")
        )
    .def("create_track", [](py::capsule mixer)
        {
            return py::capsule(MIX_CreateTrack(static_cast<MIX_Mixer *>(mixer.get_pointer())), "MIX_Track");
        }
        , py::arg("mixer")
        )
    .def("destroy_track", [](py::capsule track)
        {
            return MIX_DestroyTrack(static_cast<MIX_Track *>(track.get_pointer()));
        }
        , py::arg("track")
        )
    .def("get_track_properties", [](py::capsule track)
        {
            return MIX_GetTrackProperties(static_cast<MIX_Track *>(track.get_pointer()));
        }
        , py::arg("track")
        )
    .def("get_track_mixer", [](py::capsule track)
        {
            return py::capsule(MIX_GetTrackMixer(static_cast<MIX_Track *>(track.get_pointer())), "MIX_Mixer");
        }
        , py::arg("track")
        )
    .def("set_track_audio", [](py::capsule track, py::capsule audio)
        {
            return MIX_SetTrackAudio(static_cast<MIX_Track *>(track.get_pointer()), static_cast<MIX_Audio *>(audio.get_pointer()));
        }
        , py::arg("track")
        , py::arg("audio")
        )
    .def("set_track_audio_stream", [](py::capsule track, py::capsule stream)
        {
            return MIX_SetTrackAudioStream(static_cast<MIX_Track *>(track.get_pointer()), static_cast<SDL_AudioStream *>(stream.get_pointer()));
        }
        , py::arg("track")
        , py::arg("stream")
        )
    .def("set_track_io_stream", [](py::capsule track, py::capsule io, bool closeio)
        {
            return MIX_SetTrackIOStream(static_cast<MIX_Track *>(track.get_pointer()), static_cast<SDL_IOStream *>(io.get_pointer()), closeio);
        }
        , py::arg("track")
        , py::arg("io")
        , py::arg("closeio")
        )
    .def("set_track_raw_io_stream", [](py::capsule track, py::capsule io, const SDL_AudioSpec * spec, bool closeio)
        {
            return MIX_SetTrackRawIOStream(static_cast<MIX_Track *>(track.get_pointer()), static_cast<SDL_IOStream *>(io.get_pointer()), spec, closeio);
        }
        , py::arg("track")
        , py::arg("io")
        , py::arg("spec")
        , py::arg("closeio")
        )
    .def("tag_track", [](py::capsule track, const char * tag)
        {
            return MIX_TagTrack(static_cast<MIX_Track *>(track.get_pointer()), tag);
        }
        , py::arg("track")
        , py::arg("tag")
        )
    .def("untag_track", [](py::capsule track, const char * tag)
        {
            return MIX_UntagTrack(static_cast<MIX_Track *>(track.get_pointer()), tag);
        }
        , py::arg("track")
        , py::arg("tag")
        )
    .def("get_tagged_tracks", [](py::capsule mixer, const char * tag, int * count)
        {
            auto _ret = py::capsule(MIX_GetTaggedTracks(static_cast<MIX_Mixer *>(mixer.get_pointer()), tag, count), "MIX_Track");
            return std::make_tuple(_ret, count);
        }
        , py::arg("mixer")
        , py::arg("tag")
        , py::arg("count")
        )
    .def("set_track_playback_position", [](py::capsule track, Sint64 frames)
        {
            return MIX_SetTrackPlaybackPosition(static_cast<MIX_Track *>(track.get_pointer()), frames);
        }
        , py::arg("track")
        , py::arg("frames")
        )
    .def("get_track_playback_position", [](py::capsule track)
        {
            return MIX_GetTrackPlaybackPosition(static_cast<MIX_Track *>(track.get_pointer()));
        }
        , py::arg("track")
        )
    .def("get_track_fade_frames", [](py::capsule track)
        {
            return MIX_GetTrackFadeFrames(static_cast<MIX_Track *>(track.get_pointer()));
        }
        , py::arg("track")
        )
    .def("get_track_loops", [](py::capsule track)
        {
            return MIX_GetTrackLoops(static_cast<MIX_Track *>(track.get_pointer()));
        }
        , py::arg("track")
        )
    .def("set_track_loops", [](py::capsule track, int num_loops)
        {
            return MIX_SetTrackLoops(static_cast<MIX_Track *>(track.get_pointer()), num_loops);
        }
        , py::arg("track")
        , py::arg("num_loops")
        )
    .def("get_track_audio", [](py::capsule track)
        {
            return py::capsule(MIX_GetTrackAudio(static_cast<MIX_Track *>(track.get_pointer())), "MIX_Audio");
        }
        , py::arg("track")
        )
    .def("get_track_audio_stream", [](py::capsule track)
        {
            return py::capsule(MIX_GetTrackAudioStream(static_cast<MIX_Track *>(track.get_pointer())), "SDL_AudioStream");
        }
        , py::arg("track")
        )
    .def("get_track_remaining", [](py::capsule track)
        {
            return MIX_GetTrackRemaining(static_cast<MIX_Track *>(track.get_pointer()));
        }
        , py::arg("track")
        )
    .def("track_ms_to_frames", [](py::capsule track, Sint64 ms)
        {
            return MIX_TrackMSToFrames(static_cast<MIX_Track *>(track.get_pointer()), ms);
        }
        , py::arg("track")
        , py::arg("ms")
        )
    .def("track_frames_to_ms", [](py::capsule track, Sint64 frames)
        {
            return MIX_TrackFramesToMS(static_cast<MIX_Track *>(track.get_pointer()), frames);
        }
        , py::arg("track")
        , py::arg("frames")
        )
    .def("audio_ms_to_frames", [](py::capsule audio, Sint64 ms)
        {
            return MIX_AudioMSToFrames(static_cast<MIX_Audio *>(audio.get_pointer()), ms);
        }
        , py::arg("audio")
        , py::arg("ms")
        )
    .def("audio_frames_to_ms", [](py::capsule audio, Sint64 frames)
        {
            return MIX_AudioFramesToMS(static_cast<MIX_Audio *>(audio.get_pointer()), frames);
        }
        , py::arg("audio")
        , py::arg("frames")
        )
    .def("ms_to_frames", &MIX_MSToFrames
        , py::arg("sample_rate")
        , py::arg("ms")
        )
    .def("frames_to_ms", &MIX_FramesToMS
        , py::arg("sample_rate")
        , py::arg("frames")
        )
    .def("play_track", [](py::capsule track, SDL_PropertiesID options)
        {
            return MIX_PlayTrack(static_cast<MIX_Track *>(track.get_pointer()), options);
        }
        , py::arg("track")
        , py::arg("options")
        )
    .def("play_tag", [](py::capsule mixer, const char * tag, SDL_PropertiesID options)
        {
            return MIX_PlayTag(static_cast<MIX_Mixer *>(mixer.get_pointer()), tag, options);
        }
        , py::arg("mixer")
        , py::arg("tag")
        , py::arg("options")
        )
    .def("play_audio", [](py::capsule mixer, py::capsule audio)
        {
            return MIX_PlayAudio(static_cast<MIX_Mixer *>(mixer.get_pointer()), static_cast<MIX_Audio *>(audio.get_pointer()));
        }
        , py::arg("mixer")
        , py::arg("audio")
        )
    .def("stop_track", [](py::capsule track, Sint64 fade_out_frames)
        {
            return MIX_StopTrack(static_cast<MIX_Track *>(track.get_pointer()), fade_out_frames);
        }
        , py::arg("track")
        , py::arg("fade_out_frames")
        )
    .def("stop_all_tracks", [](py::capsule mixer, Sint64 fade_out_ms)
        {
            return MIX_StopAllTracks(static_cast<MIX_Mixer *>(mixer.get_pointer()), fade_out_ms);
        }
        , py::arg("mixer")
        , py::arg("fade_out_ms")
        )
    .def("stop_tag", [](py::capsule mixer, const char * tag, Sint64 fade_out_ms)
        {
            return MIX_StopTag(static_cast<MIX_Mixer *>(mixer.get_pointer()), tag, fade_out_ms);
        }
        , py::arg("mixer")
        , py::arg("tag")
        , py::arg("fade_out_ms")
        )
    .def("pause_track", [](py::capsule track)
        {
            return MIX_PauseTrack(static_cast<MIX_Track *>(track.get_pointer()));
        }
        , py::arg("track")
        )
    .def("pause_all_tracks", [](py::capsule mixer)
        {
            return MIX_PauseAllTracks(static_cast<MIX_Mixer *>(mixer.get_pointer()));
        }
        , py::arg("mixer")
        )
    .def("pause_tag", [](py::capsule mixer, const char * tag)
        {
            return MIX_PauseTag(static_cast<MIX_Mixer *>(mixer.get_pointer()), tag);
        }
        , py::arg("mixer")
        , py::arg("tag")
        )
    .def("resume_track", [](py::capsule track)
        {
            return MIX_ResumeTrack(static_cast<MIX_Track *>(track.get_pointer()));
        }
        , py::arg("track")
        )
    .def("resume_all_tracks", [](py::capsule mixer)
        {
            return MIX_ResumeAllTracks(static_cast<MIX_Mixer *>(mixer.get_pointer()));
        }
        , py::arg("mixer")
        )
    .def("resume_tag", [](py::capsule mixer, const char * tag)
        {
            return MIX_ResumeTag(static_cast<MIX_Mixer *>(mixer.get_pointer()), tag);
        }
        , py::arg("mixer")
        , py::arg("tag")
        )
    .def("track_playing", [](py::capsule track)
        {
            return MIX_TrackPlaying(static_cast<MIX_Track *>(track.get_pointer()));
        }
        , py::arg("track")
        )
    .def("track_paused", [](py::capsule track)
        {
            return MIX_TrackPaused(static_cast<MIX_Track *>(track.get_pointer()));
        }
        , py::arg("track")
        )
    .def("set_mixer_gain", [](py::capsule mixer, float gain)
        {
            return MIX_SetMixerGain(static_cast<MIX_Mixer *>(mixer.get_pointer()), gain);
        }
        , py::arg("mixer")
        , py::arg("gain")
        )
    .def("get_mixer_gain", [](py::capsule mixer)
        {
            return MIX_GetMixerGain(static_cast<MIX_Mixer *>(mixer.get_pointer()));
        }
        , py::arg("mixer")
        )
    .def("set_track_gain", [](py::capsule track, float gain)
        {
            return MIX_SetTrackGain(static_cast<MIX_Track *>(track.get_pointer()), gain);
        }
        , py::arg("track")
        , py::arg("gain")
        )
    .def("get_track_gain", [](py::capsule track)
        {
            return MIX_GetTrackGain(static_cast<MIX_Track *>(track.get_pointer()));
        }
        , py::arg("track")
        )
    .def("set_tag_gain", [](py::capsule mixer, const char * tag, float gain)
        {
            return MIX_SetTagGain(static_cast<MIX_Mixer *>(mixer.get_pointer()), tag, gain);
        }
        , py::arg("mixer")
        , py::arg("tag")
        , py::arg("gain")
        )
    .def("set_mixer_frequency_ratio", [](py::capsule mixer, float ratio)
        {
            return MIX_SetMixerFrequencyRatio(static_cast<MIX_Mixer *>(mixer.get_pointer()), ratio);
        }
        , py::arg("mixer")
        , py::arg("ratio")
        )
    .def("get_mixer_frequency_ratio", [](py::capsule mixer)
        {
            return MIX_GetMixerFrequencyRatio(static_cast<MIX_Mixer *>(mixer.get_pointer()));
        }
        , py::arg("mixer")
        )
    .def("set_track_frequency_ratio", [](py::capsule track, float ratio)
        {
            return MIX_SetTrackFrequencyRatio(static_cast<MIX_Track *>(track.get_pointer()), ratio);
        }
        , py::arg("track")
        , py::arg("ratio")
        )
    .def("get_track_frequency_ratio", [](py::capsule track)
        {
            return MIX_GetTrackFrequencyRatio(static_cast<MIX_Track *>(track.get_pointer()));
        }
        , py::arg("track")
        )
    .def("set_track_output_channel_map", [](py::capsule track, const int * chmap, int count)
        {
            return MIX_SetTrackOutputChannelMap(static_cast<MIX_Track *>(track.get_pointer()), chmap, count);
        }
        , py::arg("track")
        , py::arg("chmap")
        , py::arg("count")
        )
    ;

    py::class_<MIX_StereoGains> _StereoGains(_sdl, "StereoGains");
    registry.on(_sdl, "StereoGains", _StereoGains);
        _StereoGains
        .def_readwrite("left", &MIX_StereoGains::left)
        .def_readwrite("right", &MIX_StereoGains::right)
    ;

    _sdl
    .def("set_track_stereo", [](py::capsule track, const MIX_StereoGains * gains)
        {
            return MIX_SetTrackStereo(static_cast<MIX_Track *>(track.get_pointer()), gains);
        }
        , py::arg("track")
        , py::arg("gains")
        )
    ;

    py::class_<MIX_Point3D> _Point3D(_sdl, "Point3D");
    registry.on(_sdl, "Point3D", _Point3D);
        _Point3D
        .def_readwrite("x", &MIX_Point3D::x)
        .def_readwrite("y", &MIX_Point3D::y)
        .def_readwrite("z", &MIX_Point3D::z)
    ;

    _sdl
    .def("set_track3_d_position", [](py::capsule track, const MIX_Point3D * position)
        {
            return MIX_SetTrack3DPosition(static_cast<MIX_Track *>(track.get_pointer()), position);
        }
        , py::arg("track")
        , py::arg("position")
        )
    .def("get_track3_d_position", [](py::capsule track, MIX_Point3D * position)
        {
            return MIX_GetTrack3DPosition(static_cast<MIX_Track *>(track.get_pointer()), position);
        }
        , py::arg("track")
        , py::arg("position")
        )
    .def("create_group", [](py::capsule mixer)
        {
            return py::capsule(MIX_CreateGroup(static_cast<MIX_Mixer *>(mixer.get_pointer())), "MIX_Group");
        }
        , py::arg("mixer")
        )
    .def("destroy_group", [](py::capsule group)
        {
            return MIX_DestroyGroup(static_cast<MIX_Group *>(group.get_pointer()));
        }
        , py::arg("group")
        )
    .def("get_group_properties", [](py::capsule group)
        {
            return MIX_GetGroupProperties(static_cast<MIX_Group *>(group.get_pointer()));
        }
        , py::arg("group")
        )
    .def("get_group_mixer", [](py::capsule group)
        {
            return py::capsule(MIX_GetGroupMixer(static_cast<MIX_Group *>(group.get_pointer())), "MIX_Mixer");
        }
        , py::arg("group")
        )
    .def("set_track_group", [](py::capsule track, py::capsule group)
        {
            return MIX_SetTrackGroup(static_cast<MIX_Track *>(track.get_pointer()), static_cast<MIX_Group *>(group.get_pointer()));
        }
        , py::arg("track")
        , py::arg("group")
        )
    .def("set_track_stopped_callback", [](py::capsule track, void (*cb)(void *, struct MIX_Track *), void * userdata)
        {
            return MIX_SetTrackStoppedCallback(static_cast<MIX_Track *>(track.get_pointer()), cb, userdata);
        }
        , py::arg("track")
        , py::arg("cb")
        , py::arg("userdata")
        )
    .def("set_track_raw_callback", [](py::capsule track, void (*cb)(void *, struct MIX_Track *, const struct SDL_AudioSpec *, float *, int), void * userdata)
        {
            return MIX_SetTrackRawCallback(static_cast<MIX_Track *>(track.get_pointer()), cb, userdata);
        }
        , py::arg("track")
        , py::arg("cb")
        , py::arg("userdata")
        )
    .def("set_track_cooked_callback", [](py::capsule track, void (*cb)(void *, struct MIX_Track *, const struct SDL_AudioSpec *, float *, int), void * userdata)
        {
            return MIX_SetTrackCookedCallback(static_cast<MIX_Track *>(track.get_pointer()), cb, userdata);
        }
        , py::arg("track")
        , py::arg("cb")
        , py::arg("userdata")
        )
    .def("set_group_post_mix_callback", [](py::capsule group, void (*cb)(void *, struct MIX_Group *, const struct SDL_AudioSpec *, float *, int), void * userdata)
        {
            return MIX_SetGroupPostMixCallback(static_cast<MIX_Group *>(group.get_pointer()), cb, userdata);
        }
        , py::arg("group")
        , py::arg("cb")
        , py::arg("userdata")
        )
    .def("set_post_mix_callback", [](py::capsule mixer, void (*cb)(void *, struct MIX_Mixer *, const struct SDL_AudioSpec *, float *, int), void * userdata)
        {
            return MIX_SetPostMixCallback(static_cast<MIX_Mixer *>(mixer.get_pointer()), cb, userdata);
        }
        , py::arg("mixer")
        , py::arg("cb")
        , py::arg("userdata")
        )
    .def("generate", [](py::capsule mixer, void * buffer, int buflen)
        {
            return MIX_Generate(static_cast<MIX_Mixer *>(mixer.get_pointer()), buffer, buflen);
        }
        , py::arg("mixer")
        , py::arg("buffer")
        , py::arg("buflen")
        )
    .def("create_audio_decoder", [](const char * path, SDL_PropertiesID props)
        {
            return py::capsule(MIX_CreateAudioDecoder(path, props), "MIX_AudioDecoder");
        }
        , py::arg("path")
        , py::arg("props")
        )
    .def("create_audio_decoder_io", [](py::capsule io, bool closeio, SDL_PropertiesID props)
        {
            return py::capsule(MIX_CreateAudioDecoder_IO(static_cast<SDL_IOStream *>(io.get_pointer()), closeio, props), "MIX_AudioDecoder");
        }
        , py::arg("io")
        , py::arg("closeio")
        , py::arg("props")
        )
    .def("destroy_audio_decoder", [](py::capsule audiodecoder)
        {
            return MIX_DestroyAudioDecoder(static_cast<MIX_AudioDecoder *>(audiodecoder.get_pointer()));
        }
        , py::arg("audiodecoder")
        )
    .def("get_audio_decoder_properties", [](py::capsule audiodecoder)
        {
            return MIX_GetAudioDecoderProperties(static_cast<MIX_AudioDecoder *>(audiodecoder.get_pointer()));
        }
        , py::arg("audiodecoder")
        )
    .def("get_audio_decoder_format", [](py::capsule audiodecoder, SDL_AudioSpec * spec)
        {
            return MIX_GetAudioDecoderFormat(static_cast<MIX_AudioDecoder *>(audiodecoder.get_pointer()), spec);
        }
        , py::arg("audiodecoder")
        , py::arg("spec")
        )
    .def("decode_audio", [](py::capsule audiodecoder, void * buffer, int buflen, const SDL_AudioSpec * spec)
        {
            return MIX_DecodeAudio(static_cast<MIX_AudioDecoder *>(audiodecoder.get_pointer()), buffer, buflen, spec);
        }
        , py::arg("audiodecoder")
        , py::arg("buffer")
        , py::arg("buflen")
        , py::arg("spec")
        )
    ;


}