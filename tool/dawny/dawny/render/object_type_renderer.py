from .renderer import Renderer
from ..node import ObjectType, Method

class ObjectTypeRenderer(Renderer[ObjectType]):
    def exclude_method(self, method: Method):
        '''
        if method.returns and method.returns == "future":
            return True
        '''
        return super().exclude_node(method)
