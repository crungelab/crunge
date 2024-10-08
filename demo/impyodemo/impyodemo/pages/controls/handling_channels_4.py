from pyo import *

from .. import Page


class HandlingChannels4(Page):
    """
    11-handling-channels-4.py - Explicit control of the physical outputs.

    If `chnl` is a list, successive values in the list will be assigned
    to successive streams.

    """

    def create_server(self):
        # Creates a Server with 8 channels
        #self.server = Server(audio='jack', nchnls=8).boot()
        self.server = Server(nchnls=8).boot()

    def do_reset(self):
        amps = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4]

        # Generates 8 sine waves with
        # increasing amplitudes
        self.a = Sine(freq=500, mul=amps)


    def do_start(self):
        # Sets the output channels ordering
        self.a.out(chnl=[3, 4, 2, 5, 1, 6, 0, 7])

