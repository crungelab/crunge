import time
import sys

from loguru import logger
import glfw
import glm

from crunge import wgpu
from crunge import skia

from ..common import Demo

shader_code = """
@vertex
fn vs_main(@builtin(vertex_index) idx: u32) -> @builtin(position) vec4<f32> {
    var pos = array<vec2<f32>, 3>(
        vec2<f32>(0.0, 0.5), vec2<f32>(-0.5, -0.5), vec2<f32>(0.5, -0.5));
    return vec4<f32>(pos[idx], 0.0, 1.0);
}
@fragment
fn fs_main() -> @location(0) vec4<f32> {
    return vec4<f32>(0.0, 0.502, 1.0, 1.0); // 0x80/0xff ~= 0.502
}
"""


class RectangleDemo(Demo):
    depth_stencil_view: wgpu.TextureView = None

    def __init__(self):
        super().__init__()
        self.skia_context = skia.create_context(self.context.instance, self.context.device)

    def resize(self, size: glm.ivec2):
        super().resize(size)
        self.create_depth_stencil_view()

    def create_device_objects(self):
        self.create_depth_stencil_view()
        self.create_pipeline()

    def create_depth_stencil_view(self):
        descriptor = wgpu.TextureDescriptor(
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
            size=wgpu.Extent3D(self.size.x, self.size.y, 1),
            format=wgpu.TextureFormat.DEPTH32_FLOAT,
        )
        self.depth_stencil_view = self.device.create_texture(descriptor).create_view()

    def create_pipeline(self):
        logger.debug("Creating pipeline")

        logger.debug("Creating shader module")
        shader_module = self.create_shader_module(shader_code)

        logger.debug("Creating colorTargetState")

        colorTargetStates = [
            wgpu.ColorTargetState(format=wgpu.TextureFormat.BGRA8_UNORM)
        ]

        logger.debug("Creating fragmentState")
        fragmentState = wgpu.FragmentState(
            module=shader_module,
            entry_point="fs_main",
            target_count=1,
            targets=colorTargetStates,
        )

        logger.debug("Creating depthStencilState")
        depthStencilState = wgpu.DepthStencilState(
            format=wgpu.TextureFormat.DEPTH32_FLOAT,
            depth_write_enabled=False,
        )

        logger.debug("Creating primitive")
        primitive = wgpu.PrimitiveState(topology=wgpu.PrimitiveTopology.TRIANGLE_LIST)

        logger.debug("Creating vertex_state")
        vertex_state = wgpu.VertexState(
            module=shader_module,
            entry_point="vs_main",
        )

        logger.debug("Creating render pipeline descriptor")
        descriptor = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            vertex=vertex_state,
            primitive=primitive,
            depth_stencil=depthStencilState,
            fragment=fragmentState,
        )
        logger.debug(descriptor)

        logger.debug("Creating render pipeline")
        self.pipeline = self.device.create_render_pipeline(descriptor)
        logger.debug(self.pipeline)

    def render(self, view: wgpu.TextureView, depthStencilView: wgpu.TextureView):
        color_attachments = [
            wgpu.RenderPassColorAttachment(
                view=view,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_color=wgpu.Color(0, 0, 0, 1),
            )
        ]

        depth_stencil_attachment = wgpu.RenderPassDepthStencilAttachment(
            view=depthStencilView,
            depth_load_op=wgpu.LoadOp.CLEAR,
            depth_store_op=wgpu.StoreOp.STORE,
            depth_clear_value=0,
        )

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachment_count=1,
            color_attachments=color_attachments,
            depth_stencil_attachment=depth_stencil_attachment,
        )

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
        pass_enc.set_pipeline(self.pipeline)
        pass_enc.draw(3)
        pass_enc.end()
        commands = encoder.finish()

        self.queue.submit(1, commands)

        # Skia rendering
        recorder = self.skia_context.make_recorder(skia.RecorderOptions())
        surface_texture = wgpu.SurfaceTexture()
        self.surface.get_current_texture(surface_texture)
        backend_texture = surface_texture.texture
        skia_surface = skia.create_surface(backend_texture, recorder)

        if skia_surface:
            skia_canvas = skia_surface.get_canvas()
            #skia_canvas.clear(skia.Color(0, 0, 0, 1))

            paint = skia.Paint()
            #paint.set_color(skia.Color(1, 1, 1, 1))
            paint.set_color(0xFFFFFFFF)
            skia_canvas.draw_rect(skia.Rect(10, 10, 210, 110), paint)
            #skia_canvas.draw_rect(skia.Rect([10, 10, 210, 110]), paint)

            recording = recorder.snap()

            if recording:
                insert_info = skia.InsertRecordingInfo()
                insert_info.f_recording = recording
                self.skia_context.insert_recording(insert_info)
                self.skia_context.submit(skia.SyncToCpu.K_NO)

        '''
        auto backbuffer = getBackbufferSurface();
        if (backbuffer) {
            auto canvas = backbuffer->getCanvas();
            SkPaint paint;
            paint.setColor(SK_ColorWHITE);
            //canvas->drawColor(SK_ColorBLACK);
            canvas->drawRect(SkRect::MakeXYWH(10, 10, 200, 100), paint);

            std::unique_ptr<skgpu::graphite::Recording> recording = fGraphiteRecorder->snap();

            if (recording) {
                skgpu::graphite::InsertRecordingInfo info;
                info.fRecording = recording.get();
                fGraphiteContext->insertRecording(info);
                fGraphiteContext->submit(skgpu::graphite::SyncToCpu::kNo);
            }
        }
        '''
def main():
    RectangleDemo().run()


if __name__ == "__main__":
    main()
