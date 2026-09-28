"""SDL_mixer: load a sound and play it through a mixer device.

Silent by default: SDL's "dummy" audio driver takes the output, so neither
collecting nor running these tests makes a sound, while still exercising the
real device path. To hear the sound:

    CRUNGE_AUDIBLE=1 pytest tests/test_mixer.py -s

Nothing runs at import time. Test discovery (VS Code runs it in the background)
imports this module; everything with an effect lives in fixtures and tests.
"""

from __future__ import annotations

import os
import time
from pathlib import Path

import pytest

from crunge import sdl
from crunge.sdl import mixer as mxr

ASSETS_DIR = Path(__file__).parent.parent / "assets"
LASER_WAV = ASSETS_DIR / "mixkit-cinematic-laser-gun-thunder-1287.wav"

AUDIBLE = os.environ.get("CRUNGE_AUDIBLE") == "1"
PLAYBACK_TIMEOUT = 10.0  # seconds; the clip is shorter than this


@pytest.fixture(scope="module")
def mixer():
    """A mixer on the default playback device, silent unless CRUNGE_AUDIBLE=1."""
    with pytest.MonkeyPatch.context() as mp:
        if not AUDIBLE:
            # Must be set before SDL opens its audio subsystem.
            mp.setenv("SDL_AUDIO_DRIVER", "dummy")
        assert mxr.init(), sdl.get_error()
        device = mxr.create_mixer_device(sdl.AUDIO_DEVICE_DEFAULT_PLAYBACK, None)
        assert device is not None, sdl.get_error()
        yield device
        mxr.destroy_mixer(device)
        mxr.quit()


@pytest.fixture
def laser(mixer):
    audio = mxr.load_audio(mixer, str(LASER_WAV), False)
    assert audio is not None, sdl.get_error()
    yield audio
    mxr.destroy_audio(audio)


@pytest.fixture
def track(mixer):
    track = mxr.create_track(mixer)
    assert track is not None, sdl.get_error()
    yield track
    mxr.destroy_track(track)


def test_asset_exists():
    assert LASER_WAV.is_file(), LASER_WAV


def test_load_audio(laser):
    assert laser is not None


def test_load_missing_file_fails(mixer):
    assert mxr.load_audio(mixer, str(ASSETS_DIR / "no-such-file.wav"), False) is None


def test_play_track(track, laser):
    assert mxr.set_track_audio(track, laser), sdl.get_error()
    assert mxr.play_track(track, 0), sdl.get_error()
    assert mxr.track_playing(track)

    if not AUDIBLE:
        mxr.stop_track(track, 0)  # playback started; no need to sit through it
        return

    deadline = time.monotonic() + PLAYBACK_TIMEOUT
    while mxr.track_playing(track):
        assert time.monotonic() < deadline, "track still playing after the timeout"
        time.sleep(0.05)