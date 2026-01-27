from typing import TYPE_CHECKING, Generic
from ....renderer.phase.bucket_phase import BucketPhase, T_PhaseItem

if TYPE_CHECKING:
    from .. import SceneRenderer2D


class BucketPhase2D(Generic[T_PhaseItem], BucketPhase["SceneRenderer2D", T_PhaseItem]):
    pass
