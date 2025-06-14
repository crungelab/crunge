import importlib.resources
import json

from loguru import logger

from crunge import wgpu
from crunge import gltf


from crunge.engine.d3.material_3d import Material3D
from crunge.engine.resource.texture import Texture
from crunge.engine.resource.texture.cube_texture import CubeTexture

from crunge.engine.loader.texture.texture_2d_loader import Texture2DLoader
from crunge.engine.loader.texture.cube_texture_loader import CubeTextureLoader
from crunge.engine.loader.image_loader import HdrImageLoader

from . import GltfBuilder
from .builder_context import BuilderContext
from .texture_builder import TextureBuilder


class MaterialBuilder(GltfBuilder):
    def __init__(self, context: BuilderContext, material_index: int) -> None:
        super().__init__(context)
        self.material_index = material_index
        self.tf_material: gltf.Material = None
        self.material = Material3D()
        self.use_environment_map = False

    def build(self) -> None:
        if self.material_index in self.context.material_cache:
            return self.context.material_cache[self.material_index]

        self.tf_material = tf_material = self.tf_model.materials[self.material_index]
        logger.debug(tf_material)

        self.material.name = tf_material.name

        # Alpha Mode
        alpha_mode = tf_material.alpha_mode
        logger.debug(f"Alpha Mode: {alpha_mode}")
        self.material.alpha_mode = alpha_mode

        # Alpha Cutoff
        alpha_cutoff = tf_material.alpha_cutoff
        logger.debug(f"Alpha Cutoff: {alpha_cutoff}")
        self.material.alpha_cutoff = alpha_cutoff

        # Double Sided
        double_sided = tf_material.double_sided
        logger.debug(f"Double Sided: {double_sided}")
        self.material.double_sided = double_sided

        # PBR Metallic Roughness
        pbr = tf_material.pbr_metallic_roughness
        logger.debug(pbr)

        # Base Color Factor
        base_color_factor = pbr.base_color_factor
        logger.debug(f"Base Color Factor: {base_color_factor}")
        self.material.base_color_factor = base_color_factor

        # Base Color Texture
        if pbr.base_color_texture.index >= 0:
            self.build_texture("baseColor", pbr.base_color_texture.index)

        # Metallic Factor
        metallic_factor = pbr.metallic_factor
        logger.debug(f"metallic_factor: {metallic_factor}")
        self.material.metallic_factor = metallic_factor

        # Roughness Factor
        roughness_factor = pbr.roughness_factor
        logger.debug(f"roughness_factor: {roughness_factor}")
        self.material.roughness_factor = roughness_factor

        # Metallic Roughness Texture
        if pbr.metallic_roughness_texture.index >= 0:
            self.build_texture("metallicRoughness", pbr.metallic_roughness_texture.index)
            self.use_environment_map = True

        # Normal Texture
        if tf_material.normal_texture.index >= 0:
            self.build_texture("normal", tf_material.normal_texture.index)

        # Occlusion Texture
        if tf_material.occlusion_texture.index >= 0:
            self.material.occlusion_strength = tf_material.occlusion_texture.strength
            self.build_texture("occlusion", tf_material.occlusion_texture.index)

        # Emissive Factor
        emissive_factor = tf_material.emissive_factor
        logger.debug(f"emissive_factor: {emissive_factor}")
        self.material.emissive_factor = emissive_factor

        # Emissive Texture
        if tf_material.emissive_texture.index >= 0:
            self.build_texture("emissive", tf_material.emissive_texture.index)

        # Environment Map
        if self.use_environment_map:
            self.build_environment_map()

        self.build_transmission()

        self.build_bind_group_layout()
        self.build_bind_group()

        self.context.material_cache[self.material_index] = self.material
        return self.material

    def build_texture(self, name: str, texture_index: int) -> None:
        texture = TextureBuilder(self.context, name, texture_index).build()
        self.material.add_texture(texture)

    '''
    def build_texture(self, name: str, texture_info: gltf.TextureInfo) -> None:
        texture = TextureBuilder(self.context, name, texture_info).build()
        self.material.add_texture(texture)
    '''

    def build_environment_map(self) -> None:
        # texture = self.build_environment_texture()
        texture = self.build_cube_environment_texture()
        self.material.add_texture(texture)

    def build_environment_texture(self) -> Texture:
        path = importlib.resources.path(
            "crunge.engine.resources.textures", "environment.hdr"
        )
        texture = Texture2DLoader(image_loader=HdrImageLoader()).load(
            path, name="environment"
        )
        texture.view = texture.texture.create_view()
        texture.sampler = self.gfx.device.create_sampler()
        return texture

    def build_cube_environment_texture(self) -> Texture:
        root = importlib.resources.path("crunge.engine.resources.textures.cubemaps", "")
        name = "gcanyon_cube"
        ext = "png"
        paths = [
            root / f"{name}_px.{ext}",
            root / f"{name}_nx.{ext}",
            root / f"{name}_py.{ext}",
            root / f"{name}_ny.{ext}",
            root / f"{name}_pz.{ext}",
            root / f"{name}_nz.{ext}",
        ]
        texture = CubeTextureLoader().load(paths, name="environment")
        texture_view_desc = wgpu.TextureViewDescriptor(
            dimension=wgpu.TextureViewDimension.CUBE,
        )
        texture.view = texture.texture.create_view(texture_view_desc)
        texture.sampler = self.gfx.device.create_sampler()
        return texture

    def build_snapshot_texture(self) -> Texture:
        texture = Texture()
        
    def build_transmission(self) -> None:
        extension = self.tf_material.extensions.get("KHR_materials_transmission")
        if extension is None:
            return
        logger.debug(f"Transmission Extension: {extension}")
        transmission_factor = extension.get("transmissionFactor").get_number_as_double()
        logger.debug(f"Transmission Factor: {transmission_factor}")
        self.material.transmission_factor = transmission_factor

        transmissionTexture = extension.get("transmissionTexture", None)
        if transmissionTexture is None:
            return
        '''
        transmissionTexture = extension.get("transmissionTexture")
        logger.debug(type(transmissionTexture.type()))

        if transmissionTexture.type() == gltf.Type.NULL_TYPE:
            return
        '''

        logger.debug(f"Transmission Texture: {transmissionTexture}, type: {transmissionTexture.type()}")

        texture_value = transmissionTexture.get("index")
        texture_index = texture_value.get_number_as_int()
        logger.debug(f"Transmission Texture Index: {texture_index}")

        if texture_index >= 0:  # Texture is present
            self.build_texture("transmission", texture_index)

    def build_bind_group_layout(self) -> wgpu.BindGroupLayout:
        material_bgl_entries = []

        for i, texture in enumerate(self.material.textures):
            view_dimension = wgpu.TextureViewDimension.E2D
            if isinstance(texture, CubeTexture):
                view_dimension = wgpu.TextureViewDimension.CUBE

            # Sampler
            material_bgl_entries.append(
                wgpu.BindGroupLayoutEntry(
                    binding=i * 2,
                    visibility=wgpu.ShaderStage.FRAGMENT,
                    sampler=wgpu.SamplerBindingLayout(
                        type=wgpu.SamplerBindingType.FILTERING
                    ),
                )
            )

            # Texture
            material_bgl_entries.append(
                wgpu.BindGroupLayoutEntry(
                    binding=i * 2 + 1,
                    visibility=wgpu.ShaderStage.FRAGMENT,
                    texture=wgpu.TextureBindingLayout(
                        sample_type=wgpu.TextureSampleType.FLOAT,
                        view_dimension=view_dimension,
                    ),
                )
            )

        material_bgl_desc = wgpu.BindGroupLayoutDescriptor(entries=material_bgl_entries)
        material_bgl = self.device.create_bind_group_layout(material_bgl_desc)
        self.material.bind_group_layout = material_bgl

    def build_bind_group(self) -> wgpu.BindGroup:
        material_bg_entries = []
        for i, texture in enumerate(self.material.textures):
            material_bg_entries.append(
                wgpu.BindGroupEntry(binding=i * 2, sampler=texture.sampler)
            )
            material_bg_entries.append(
                wgpu.BindGroupEntry(binding=i * 2 + 1, texture_view=texture.view)
            )

        material_bg_desc = wgpu.BindGroupDescriptor(
            label="Material Bind Group",
            layout=self.material.bind_group_layout,
            entries=material_bg_entries,
        )

        self.material.bind_group = self.device.create_bind_group(material_bg_desc)
