from . import datalocator
from .libraryBase import Library, loadLibraryPy, loadLibraryAfl

import typing
import pathlib
import os
import copy
from functools import cache


INTERNAL = "internal"

"""Used to store the loaded library values between func selectors"""
_libraries: typing.List[Library] = []


def loadLibrary(file_path: str, name: str = "", group: str = "") -> Library:
    if "/" in file_path:
        file_path = os.path.join(os.path.sep, *file_path.split("/"))
    lib = None
    if file_path.lower().endswith(".py"):
        lib = loadLibraryPy(file_path)
    elif file_path.lower().endswith(".afl"):
        lib = loadLibraryAfl(file_path)
    if lib:
        if not lib.name:
            lib.name = name if name else pathlib.Path(file_path).stem
        if not lib.group:
            lib.group = group
        _libraries.append(lib)
    return lib


def getLibraries() -> typing.List[Library]:
    """Return a copy of the libraries so they can't be modified"""
    return [copy.deepcopy(lib) for lib in _libraries if lib.group != INTERNAL]


@cache
def getInternalLibrary() -> Library:
    return next(copy.deepcopy(lib) for lib in _libraries if lib.group == INTERNAL)


"""If the library singleton is being loaded for the first time run some initalization code"""
# we'll make sure we're not parsing any default keys
for section_key, section_config in datalocator.getConfig(datalocator.LIBRARIES).items():
    if section_key != "locations":
        for key, value in section_config.items():
            loadLibrary(value, key, section_key)
