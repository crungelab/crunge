from pyo import *

from crunge import imgui

from . import Page


class Basic(Page):
    def do_reset(self):
        # FM implements the basic Chowning algorithm
        fm1 = FM(carrier=250, ratio=[1.5, 1.49], index=10, mul=0.3)
        #fm1.ctrl()

        # CrossFM implements a frequency modulation synthesis where the
        # output of both oscillators modulates the frequency of the other one.
        fm2 = CrossFM(carrier=250, ratio=[1.5, 1.49], ind1=10, ind2=2, mul=0.3)
        #fm2.ctrl()

        # Interpolates between input objects to produce a single output
        self.sel = Selector([fm1, fm2])
        #sel.ctrl(title="Input interpolator (0=FM, 1=CrossFM)")
        #time.sleep(3)

    def draw(self):
        imgui.begin(self.title)

        if imgui.button('Play'):
            self.sel.out()
        
        if imgui.button('Stop'):
            self.reset()

        imgui.end()

def install(app):
    app.add_page(Basic, "basic")