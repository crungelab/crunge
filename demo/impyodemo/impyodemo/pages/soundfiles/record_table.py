import os

from pyo import *

from .. import Page


class RecordTable(Page):
    """
    06-record-table.py - Recording live sound in RAM.

    By recording a stream of sound in RAM, one can quickly re-use the
    samples in the current process. A combination NewTable - TableRec
    is all what one need to record any stream in a table.

    The NewTable object has a `feedback` argument, allowing overdub.

    The TableRec object starts a new recording (records until the table
    is full) every time its method `play()` is called.

    """
    def create_server(self):
        # Audio inputs must be available.
        #self.server = Server(audio='jack', duplex=1).boot()
        self.server = Server(duplex=1).boot()

    def do_reset(self):
        # Creates a two seconds stereo empty table. The "feedback" argument
        # is the amount of old data to mix with a new recording (overdub).
        self.t = t = NewTable(length=2, chnls=2, feedback=0.5)

        # Retrieves the stereo input
        inp = Input([0, 1])

        # Table recorder. Call rec.play() to start a recording, it stops
        # when the table is full. Call it multiple times to overdub.
        self.rec = TableRec(inp, table=t, fadetime=0.05)

        # Reads the content of the table in loop.
        self.osc = Osc(table=t, freq=t.getRate(), mul=0.5)

    def do_start(self):
        self.rec.play()
        self.osc.out()

        # Path of the recorded sound file.
        path = os.path.join(os.path.expanduser("~"), "Desktop", "synth.wav")

        def saveToDisk():
            print("save to disk")
            savefileFromTable(table=self.t, path=path, fileformat=0, sampletype=3)

        # After two seconds, the table content is saved to a file on disk.
        sv = CallAfter(saveToDisk, time=2).play()
