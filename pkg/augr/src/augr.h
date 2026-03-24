#pragma once

#include <RtAudio.h>
#include <pybind11/pybind11.h>

using namespace rt::audio;

namespace py = pybind11;

enum class AudioFormat : unsigned int {
    SINT8   = RTAUDIO_SINT8,
    SINT16  = RTAUDIO_SINT16,
    SINT24  = RTAUDIO_SINT24,
    SINT32  = RTAUDIO_SINT32,
    FLOAT32 = RTAUDIO_FLOAT32,
    FLOAT64 = RTAUDIO_FLOAT64
};

enum class AudioStreamFlags : unsigned int {
    NONINTERLEAVED = RTAUDIO_NONINTERLEAVED,
    MINIMIZE_LATENCY = RTAUDIO_MINIMIZE_LATENCY,
    HOG_DEVICE = RTAUDIO_HOG_DEVICE,
    SCHEDULE_REALTIME = RTAUDIO_SCHEDULE_REALTIME,
    ALSA_USE_DEFAULT = RTAUDIO_ALSA_USE_DEFAULT,
    JACK_DONT_CONNECT = RTAUDIO_JACK_DONT_CONNECT
};

enum class AudioStreamStatus : unsigned int {
    INPUT_OVERFLOW = RTAUDIO_INPUT_OVERFLOW,
    OUTPUT_UNDERFLOW = RTAUDIO_OUTPUT_UNDERFLOW
};

class AudioStream {
public:
    /*
    AudioStream(
        RtAudio &dac,
        RtAudio::StreamParameters outputParameters =
            RtAudio::StreamParameters(),
        RtAudio::StreamParameters inputParameters = RtAudio::StreamParameters(),
        RtAudioFormat format = RTAUDIO_SINT16, unsigned int sampleRate = 44100,
        unsigned int bufferFrames = 256, py::function callback = py::none(),
        RtAudio::StreamOptions options = RtAudio::StreamOptions())
        : dac(dac), outputParameters(outputParameters),
          inputParameters(inputParameters), format(format),
          sampleRate(sampleRate), bufferFrames(bufferFrames),
          callback(callback), options(options) {};
    */

    AudioStream();
    ~AudioStream();

    RtAudioErrorType open();
    void close();
    RtAudioErrorType start();
    RtAudioErrorType stop();

    int process(void *outputBuffer, void *inputBuffer,
                unsigned int nBufferFrames, double streamTime,
                RtAudioStreamStatus status);

    // Data members
    RtAudio dac;
    RtAudio::StreamParameters *outputParameters = nullptr;
    RtAudio::StreamParameters *inputParameters = nullptr;
    //RtAudioFormat format = RTAUDIO_SINT16;
    AudioFormat format = AudioFormat::SINT16;
    unsigned int sampleRate = 44100;
    unsigned int bufferFrames = 256;
    // RtAudioCallback callback;
    py::function callback; // Python callback function
    // void *userData;
    RtAudio::StreamOptions *options = nullptr;

private:
    static int _callback(void *outputBuffer, void *inputBuffer,
                         unsigned int nBufferFrames, double streamTime,
                         RtAudioStreamStatus status, void *userData);
};