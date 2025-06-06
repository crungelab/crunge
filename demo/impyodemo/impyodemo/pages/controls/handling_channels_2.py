from pyo import *

from .. import Page


class HandlingChannels2(Page):
    """
    09-handling-channels-2.py - The `out` method and the physical outputs.

    In a multichannel environment, we can carefully choose which stream
    goes to which output channel. To achieve this, we use the `chnl` and
    `inc` arguments of the out method.

    chnl : Physical output assigned to the first audio stream of the object.
    inc : Output channel increment value.

    """
    def create_server(self):
        # Creates a Server with 8 channels
        #self.server = Server(audio='jack', nchnls=8).boot()
        self.server = Server(nchnls=8).boot()

    def do_reset(self):
        # Generates a sine wave
        a = Sine(freq=500, mul=0.3)

        # Mixes it up to four streams
        self.b = a.mix(4)

    def do_start(self):
        # Outputs to channels 0, 2, 4 and 6
        self.b.out(chnl=0, inc=2)
