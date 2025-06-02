import contextlib

from crunge import skia
from crunge.engine import Renderer
from crunge import demo


class Page(demo.Page):
    def __init__(self, name: str, title: str):
        super().__init__(name, title)
        '''
        self.skia_context = skia.create_context(self.gfx.instance, self.gfx.device)
        recorder_options = skia.create_standard_recorder_options()
        self.recorder = self.skia_context.make_recorder(recorder_options)
        '''

    '''
    @contextlib.contextmanager
    def canvas_target(self, renderer: Renderer) :
        target = renderer.viewport.color_texture
        skia_surface = skia.create_surface(target, self.recorder)
        canvas = skia_surface.get_canvas()
        yield canvas
        recording = self.recorder.snap()
        if recording:
            insert_info = skia.InsertRecordingInfo()
            insert_info.f_recording = recording
            self.skia_context.insert_recording(insert_info)
            self.skia_context.submit(skia.SyncToCpu.K_NO)
    '''