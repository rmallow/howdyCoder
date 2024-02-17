from ..qtUiFiles import res_rc

from functools import cache

from PySide6 import QtCore, QtGui


def getPrefStr(prefix):
    return f":/{prefix}"


@cache
def getFilesInPrefix(prefix: str, folder=None):
    path = getPrefStr(prefix) + ("" if folder is None else f"/{folder}")
    resources = sorted(QtCore.QDir(path).entryList())
    return resources


@cache
def getResourceByIndex(prefix: str, index: int, folder=None) -> QtGui.QPixmap:
    path = f"{getPrefStr(prefix)}/{'' if folder is None else folder}"
    resources = sorted(QtCore.QDir(path).entryList())
    if index < len(resources):
        return QtGui.QPixmap(f"{path}/{resources[index]}")
    assert False, "invalid res index"
    return QtGui.QPixmap()


GREEN_CHECKMARK = "checkmark_green.png"
RED_X = "x_red.png"
ICONS_PREFIX = "icons"


@cache
def getResourceByName(prefix: str, name: str, folder=None) -> QtGui.QPixmap:
    path = f"{getPrefStr(prefix)}/{'' if folder is None else folder}"
    resources = sorted(QtCore.QDir(path).entryList())
    if name in resources:
        return QtGui.QPixmap(f"{path}/{name}")
    assert False, "invalid res name"
    return QtGui.QPixmap()
