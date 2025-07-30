from typing import TYPE_CHECKING, TypeVar

from crunge import wgpu

from ..resource import Resource

if TYPE_CHECKING:
    from .model_group import ModelGroup

T_Model = TypeVar("T_Membership", bound="Model")

class ModelMembership:
    def __init__(self, member: "Model", group: "ModelGroup", index: int) -> None:
        self.member: "Model" = member
        self.group: "ModelGroup" = group
        self.index = index


class Model(Resource):
    def __init__(self) -> None:
        super().__init__()
