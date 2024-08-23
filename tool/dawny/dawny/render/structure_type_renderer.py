from .renderer import Renderer
from ..node import StructureType, RecordMember

class StructureTypeRenderer(Renderer[StructureType]):
    def exclude_member(self, member: RecordMember) -> bool:
        '''
        if self.node.chained:
            if member.name.get() == "next in chain":
                return True
        '''
        return super().exclude_node(member)