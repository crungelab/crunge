from typing import TYPE_CHECKING, TypeVar

from crunge import wgpu

from ..resource import Resource

if TYPE_CHECKING:
    from .model_group import ModelGroup

T_Model = TypeVar("T_Membership", bound="Model")

class ModelMembership:
    def __init__(self, group: "ModelGroup", member: "Model", index: int) -> None:
        self.group: "ModelGroup" = group
        self.member: "Model" = member
        self.index = index


class Model(Resource):
    def __init__(self) -> None:
        super().__init__()
