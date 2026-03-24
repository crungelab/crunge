#include <pybind11/numpy.h>

#include "augr.h"

/*
AudioStream::AudioStream() {
    // Initialize data members with default values
    outputParameters.deviceId = 0;
    outputParameters.nChannels = 2;
    outputParameters.firstChannel = 0;

    inputParameters.deviceId = 0;
    inputParameters.nChannels = 2;
    inputParameters.firstChannel = 0;

    format = RTAUDIO_SINT16;
    sampleRate = 44100;
    bufferFrames = 256;

    options.flags = 0; // No special options by default
}
*/
AudioStream::AudioStream() {}
AudioStream::~AudioStream() {
    // Ensure the stream is closed when the object is destroyed
    if (dac.isStreamOpen()) {
        dac.closeStream();
    }
}

RtAudioErrorType AudioStream::open() {
    // Open the audio stream with the specified parameters
    return dac.openStream(outputParameters, inputParameters, static_cast<RtAudioFormat>(format), sampleRate,
                          &bufferFrames, &AudioStream::_callback, this,
                          options);
}

void AudioStream::close() { dac.closeStream(); }

RtAudioErrorType AudioStream::start() { return dac.startStream(); }

RtAudioErrorType AudioStream::stop() { return dac.stopStream(); }

int AudioStream::_callback(void *outputBuffer, void *inputBuffer,
                           unsigned int nBufferFrames, double streamTime,
                           RtAudioStreamStatus status, void *userData) {
    // Cast userData back to AudioStream instance
    AudioStream *stream = static_cast<AudioStream *>(userData);
    return stream->process(outputBuffer, inputBuffer, nBufferFrames, streamTime,
                           status);
}

int AudioStream::process(void *outputBuffer, void *inputBuffer,
                         unsigned int nBufferFrames, double streamTime,
                         RtAudioStreamStatus status) {
    if (!callback)
        return 0;

    py::gil_scoped_acquire gil;

    // Map RtAudioFormat to numpy dtype string
    const char *dtype;
    size_t elementSize;
    switch (format) {
    case AudioFormat::SINT8:
        dtype = "int8";
        elementSize = 1;
        break;
    case AudioFormat::SINT16:
        dtype = "int16";
        elementSize = 2;
        break;
    case AudioFormat::SINT24: // fall through, no numpy sint24
    case AudioFormat::SINT32:
        dtype = "int32";
        elementSize = 4;
        break;
    case AudioFormat::FLOAT32:
        dtype = "float32";
        elementSize = 4;
        break;
    case AudioFormat::FLOAT64:
        dtype = "float64";
        elementSize = 8;
        break;
    default:
        dtype = "float32";
        elementSize = 4;
        break;
    }

    auto make_array = [&](void *buf, unsigned int nChannels) -> py::object {
        if (!buf)
            return py::none();
        py::capsule base(
            buf, [](void *) {}); // no-op deleter, RtAudio owns the buffer
        return py::array(
            py::dtype(dtype),
            {(py::ssize_t)nBufferFrames, (py::ssize_t)nChannels},
            {(py::ssize_t)(nChannels * elementSize), (py::ssize_t)elementSize},
            buf, base);
    };

    /*
    auto make_array = [&](void *buf) -> py::object {
        if (!buf)
            return py::none();
        return py::array(
            py::dtype(dtype),
            {(py::ssize_t)nBufferFrames, (py::ssize_t)nChannels},
            {(py::ssize_t)(nChannels * elementSize), (py::ssize_t)elementSize},
            buf,
            py::cast(0) // <-- base object, prevents copy
        );
    };
    */

    unsigned int outChannels = outputParameters ? outputParameters->nChannels : 0;
    unsigned int inChannels = inputParameters ? inputParameters->nChannels : 0;

    py::object out = make_array(outputBuffer, outChannels);
    py::object in  = make_array(inputBuffer, inChannels);

    return callback(out, in, nBufferFrames, streamTime, status).cast<int>();
}
