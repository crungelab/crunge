from pyo import *

from .. import Page


class FuzzDisto(Page):
    """
    03-fuzz-disto.py - Hand-written asymmetrical tranfert function.

    This example implements a fuzz distortion. Bandpass filtered signal is
    eavily boosted, then feeded to an asymmetrical transfert function, and
    finally lowpass filtered to smooth out the sound. Balance between the
    dry and the distorted sound is applied before sending the signal to the 
    outputs.

    Builtin objects to distort an audio signal:

        Disto, Clip, Mirror, Wrap

    Degrade object applies some kind of distortion to a signal by changing
    its sampling rate and bit depth. 

    """

    def create_server(self):
        #self.server = Server(audio='jack', duplex=0).boot()
        self.server = Server(duplex=0).boot()

    def do_reset(self):
        gui = self.gui
        # The audio source (try with your own sounds).
        SOURCE = str(self.resource_path / "snds" / "flute.aif")

        # Distortion parameters
        BP_CENTER_FREQ = 400  # Bandpass filter center frequency.
        BP_Q = 3  # Bandpass Q (center_freq / Q = bandwidth).
        BOOST = 25  # Pre-boost (linear gain).
        LP_CUTOFF_FREQ = 3000  # Lowpass filter cutoff frequency.
        BALANCE = 0.7  # Balance dry - wet.

        src = SfPlayer(SOURCE, loop=True).mix(2)

        # The transfert function is build in two phases.

        # 1. Transfert function for signal lower than 0.
        table = ExpTable([(0, -0.25), (4096, 0), (8192, 0)], exp=30)

        # 2. Transfert function for signal higher than 0.
        # First, create an exponential function from 1 (at the beginning of the table)
        # to 0 (in the middle of the table).
        high_table = ExpTable([(0, 1), (2000, 1), (4096, 0), (4598, 0), (8192, 0)], exp=5, inverse=False)
        # Then, reverse the table’s data in time, to put the shape in the second
        # part of the table.
        high_table.reverse()

        # Finally, add the second table to the first, point by point.
        table.add(high_table)

        # Show the transfert function.
        gui.view(table, title="Transfert function")

        # Bandpass filter and boost gain applied on input signal.
        bp = ButBP(src, freq=BP_CENTER_FREQ, q=BP_Q)
        boost = Sig(bp, mul=BOOST)

        # Apply the transfert function.
        sig = Lookup(table, boost)

        # Lowpass filter on the distorted signal.
        lp = ButLP(sig, freq=LP_CUTOFF_FREQ, mul=0.7)

        # Balance between dry and wet signals.
        mixed = Interp(src, lp, interp=BALANCE)

        # Send the signal to the outputs.
        self.out = (mixed * 0.3)

        # Show the resulting waveform.
        self.gui.scope(mixed)


    def do_start(self):
        self.out.out()
