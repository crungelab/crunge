import time
from pathlib import Path

from loguru import logger

from crunge import sdl
from crunge.sdl import mixer as mxr

success = sdl.init(sdl.InitFlags.INIT_AUDIO)
logger.debug(f"SDL_Init: {success}")

ASSETS_DIR = Path(__file__).parent.parent / "assets"

wav_path = ASSETS_DIR / "mixkit-cinematic-laser-gun-thunder-1287.wav"


logger.debug("Initializing mixer")
mxr.init()
mixer = mxr.create_mixer_device(sdl.AUDIO_DEVICE_DEFAULT_PLAYBACK, None)

logger.debug("Loading audio")
#audio = MIX_LoadAudio(mixer, path, false);
audio = mxr.load_audio(mixer, str(wav_path), False)

if audio is None:
    logger.error("Failed to load audio")

#track = MIX_CreateTrack(mixer);
track = mxr.create_track(mixer);

if track is None:
    logger.error("Failed to create track")

#MIX_SetTrackAudio(track, audio);
mxr.set_track_audio(track, audio)

#MIX_PlayTrack(track, 0);  /* no extra options this time, so a zero for the second argument. */
mxr.play_track(track, 0)

logger.debug("Sleeping so audio can play...")
time.sleep(5)
