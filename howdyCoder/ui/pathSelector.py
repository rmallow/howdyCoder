from .selectorBase import SelectorBase
from .util import helperData

from ..core.commonGlobals import PathType

import typing

from PySide6 import QtWidgets


class PathSelector(SelectorBase):
    """
    Wrapper on a selector for selecting a path
    """

    TUTORIAL_RESOURCE_PREFIX = "None"

    def __init__(self, path_type: PathType, parent=None):
        super().__init__(self.TUTORIAL_RESOURCE_PREFIX, parent)

        self.parentIndex = None
        self._path_type = path_type

    def show(self):
        """Called when this widget should be shown but instead we're going to show a file selection"""
        path = ""
        if self._path_type == PathType.FOLDER:
            path = QtWidgets.QFileDialog.getExistingDirectory()
        elif self._path_type == PathType.FILE:
            path = QtWidgets.QFileDialog.getOpenFileName(
                options=QtWidgets.QFileDialog.Option.DontConfirmOverwrite
            )[0]
        if path:
            self.itemSelected.emit(
                helperData.PathWithHelperData(self.parentIndex, path)
            )

    def showNormal(self):
        pass

    def getTutorialClasses(self) -> typing.List:
        return []
