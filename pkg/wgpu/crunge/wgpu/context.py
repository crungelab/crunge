from loguru import logger

from crunge.core import klass

from .utils import create_instance, request_adapter, create_device

#_current_context = None

@klass.singleton
class Context:
    def __init__(self):
        global _current_context
        #_current_context = self

        self.instance = create_instance()
        self.adapter = request_adapter(self.instance)
        self.device = create_device(self.adapter)
        self.queue = self.device.queue

    '''
    def __del__(self):
        #super().__del__()
        #self.device.destroy()
        logger.debug("Context destroyed")
    '''