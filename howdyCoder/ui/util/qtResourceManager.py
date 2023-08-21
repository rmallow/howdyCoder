from ..qtUiFiles import res_rc

from functools import cache

from PySide6 import QtCore, QtGui

_registered_prefixes = set()


def getPrefStr(prefix):
    return f":/{prefix}"


@cache
def getFilesInPrefix(prefix: str):
    return QtCore.QDir(getPrefStr(prefix)).entryList()


@cache
def getResourceByIndex(prefix: str, index: int) -> QtGui.QPixmap:
    resources = QtCore.QDir(getPrefStr(prefix)).entryList()
    if index < len(resources):
        return QtGui.QPixmap(f"{getPrefStr(prefix)}/{resources[index]}")
    assert False, "invalid res index"
    return QtGui.QPixmap()


@cache
def getResourceByName(prefix: str, name: str) -> QtGui.QPixmap:
    resources = QtCore.QDir(getPrefStr(prefix))
    if resources.exists(name):
        return QtGui.QPixmap(f"{getPrefStr(prefix)}/{name}")
    assert False, "invalid res name"
    return QtGui.QPixmap()


def registerPrefix(prefix: str):
    if prefix in _registered_prefixes:
        pass  # TODO: uncomment below
        # assert False, f"prefix: {prefix} already registered"
    _registered_prefixes.add(prefix)


"""Singleton Module"""
first_import = True
if first_import == True:
    first_import = False
