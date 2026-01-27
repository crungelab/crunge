from typing import TYPE_CHECKING, Generic

from ....renderer.phase.bucket_phase import BucketPhase, T_PhaseItem

if TYPE_CHECKING:
    from ..scene_renderer_3d import SceneRenderer3D


class BucketPhase3D(Generic[T_PhaseItem], BucketPhase["SceneRenderer3D", T_PhaseItem]):
    pass
