from .selectorBase import SelectorBase, HelperData
import typing
from PySide6 import QtWidgets

from dataclasses import dataclass


@dataclass
class PathWithHelperData(HelperData):
    path: str = ""


class PathSelector(SelectorBase):
    """
    Wrapper on a selector for selecting a path
    """

    TUTORIAL_RESOURCE_PREFIX = "None"

    def __init__(self, parent=None):
        super().__init__(self.TUTORIAL_RESOURCE_PREFIX, parent)

        self.parentIndex = None

    def show(self):
        """Called when this widget should be shown but instead we're going to show a file selection"""
        path = QtWidgets.QFileDialog.getOpenFileName()[0]
        if path:
            self.itemSelected.emit(PathWithHelperData(self.parentIndex, path))

    def showNormal(self):
        pass

    def getTutorialClasses(self) -> typing.List:
        return []
