__version__ = '0.1.0'

import crunge

crunge.add_plugin(__file__)

from ._wgpu import *
from ._wgpu import create_proc_table

create_proc_table()