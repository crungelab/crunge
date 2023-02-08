import ctypes
from array import ArrayType
from typing import Any

import numpy

from loguru import logger


null_ptr = ctypes.POINTER(ctypes.c_long)()

def as_capsule(obj: Any) -> ctypes.py_object:
    ctypes.pythonapi.PyCapsule_New.restype = ctypes.py_object
    ctypes.pythonapi.PyCapsule_New.argtypes = [
        ctypes.c_void_p,
        ctypes.c_char_p,
        ctypes.c_void_p,
    ]

    if type(obj) == ArrayType:
        obj = obj.buffer_info()[0]
    if isinstance(obj, numpy.ndarray):
        obj = obj.ctypes.data_as(ctypes.POINTER(ctypes.c_void_p))
    if type(obj) != ctypes.c_void_p:
        obj = ctypes.cast(obj, ctypes.c_void_p)

    capsule = ctypes.pythonapi.PyCapsule_New(obj, None, None)

    return capsule

def from_capsule(capsule):
    ctypes.pythonapi.PyCapsule_GetPointer.restype = ctypes.c_void_p
    ctypes.pythonapi.PyCapsule_GetPointer.argtypes = [ctypes.py_object, ctypes.c_char_p]
    return ctypes.pythonapi.PyCapsule_GetPointer(capsule, None)
