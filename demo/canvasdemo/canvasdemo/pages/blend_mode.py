from loguru import logger

from crunge import skia
from crunge.engine import Renderer, App
from crunge.demo import PageChannel

from ..page import Page

modes = [
    skia.BlendMode.K_CLEAR,
    skia.BlendMode.K_SRC,
    skia.BlendMode.K_DST,
    skia.BlendMode.K_SRC_OVER,
    skia.BlendMode.K_DST_OVER,
    skia.BlendMode.K_SRC_IN,
    skia.BlendMode.K_DST_IN,
    skia.BlendMode.K_SRC_OUT,
    skia.BlendMode.K_DST_OUT,
    skia.BlendMode.K_SRC_A_TOP,
    skia.BlendMode.K_DST_A_TOP,
    skia.BlendMode.K_XOR,
    skia.BlendMode.K_PLUS,
    skia.BlendMode.K_MODULATE,
    skia.BlendMode.K_SCREEN,
    skia.BlendMode.K_OVERLAY,
    skia.BlendMode.K_DARKEN,
    skia.BlendMode.K_LIGHTEN,
    skia.BlendMode.K_COLOR_DODGE,
    skia.BlendMode.K_COLOR_BURN,
    skia.BlendMode.K_HARD_LIGHT,
    skia.BlendMode.K_SOFT_LIGHT,
    skia.BlendMode.K_DIFFERENCE,
    skia.BlendMode.K_EXCLUSION,
    skia.BlendMode.K_MULTIPLY,
    skia.BlendMode.K_HUE,
    skia.BlendMode.K_SATURATION,
    skia.BlendMode.K_COLOR,
    skia.BlendMode.K_LUMINOSITY,
]

def draw_utf8_string(canvas, text, x, y, font, paint):
    blob = skia.TextBlob.make_from_string(text, font)
    canvas.draw_text_blob(blob, x, y, paint)
    #canvas.draw_text_blob(skia.TextBlob(text, font), x, y, paint)

class BlendModePage(Page):
    def draw(self, renderer: Renderer):
        #with self.canvas_target(renderer) as canvas:
        with renderer.canvas_target() as canvas:
            rect = skia.Rect(0.0, 0.0, 64.0, 64.0)
            #font = skia.Font(None, 24)
            font = skia.Font()
            font.set_size(24)
            #stroke = skia.Paint(Style=skia.Paint.Style.K_STROKE_STYLE)
            stroke = skia.Paint()
            stroke.set_style(skia.Paint.Style.K_STROKE_STYLE)
            '''
            src = skia.Paint(
                Shader=skia.GradientShader.make_linear(
                    [skia.Point(0.0, 0.0), skia.Point(64.0, 0.0)],
                    [skia.colors.MAGENTA & 0x00FFFFFF, skia.colors.MAGENTA]
                )
            )
            '''
            src = skia.Paint()
            src.set_shader(
                skia.GradientShader.make_linear(
                    [skia.Point(0.0, 0.0), skia.Point(64.0, 0.0)],
                    [skia.colors.MAGENTA & 0x00FFFFFF, skia.colors.MAGENTA]
                )
            )
            '''
            dst = skia.Paint(
                Shader=skia.GradientShader.make_linear(
                    [skia.Point(0.0, 0.0), skia.Point(0.0, 64.0)],
                    [skia.colors.CYAN & 0x00FFFFFF, skia.colors.CYAN])
            )
            '''
            dst = skia.Paint()
            dst.set_shader(
                skia.GradientShader.make_linear(
                    [skia.Point(0.0, 0.0), skia.Point(0.0, 64.0)],
                    [skia.colors.CYAN & 0x00FFFFFF, skia.colors.CYAN])
            )
            canvas.clear(skia.colors.WHITE)
            N = len(modes)
            K = (N - 1) // 3 + 1
            assert K * 64 >= 640, "Not tall enough"
            for i in range(N):
                with skia.AutoCanvasRestore(canvas, True):
                    canvas.translate(192.0 * (i // K), 64.0 * (i % K))
                    desc = skia.blend_mode_name(modes[i])
                    draw_utf8_string(canvas, desc, 68.0, 30.0, font, skia.Paint())
                    canvas.clip_rect(skia.Rect(0.0, 0.0, 64.0, 64.0))
                    canvas.draw_color(skia.colors.LTGRAY)
                    save_layer_rec = skia.CanvasSaveLayerRec()
                    canvas.save_layer(save_layer_rec)
                    canvas.clear(skia.colors.TRANSPARENT)
                    canvas.draw_paint(dst)
                    src.set_blend_mode(modes[i])
                    canvas.draw_paint(src)
                    canvas.draw_rect(rect, stroke)

        super().draw(renderer)

def install(app: App):
    app.add_channel(PageChannel(BlendModePage, "blend_mode", "Blend Mode"))
