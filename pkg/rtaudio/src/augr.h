#pragma once

#include <RtAudio.h>
#include <pybind11/pybind11.h>

using namespace rt::audio;

namespace py = pybind11;

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
    RtAudioFormat format = RTAUDIO_SINT16;
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