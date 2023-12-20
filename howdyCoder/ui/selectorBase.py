from .tutorialOverlay import AbstractTutorialClass
from .util import abstractQt

import typing
from dataclasses import dataclass

from PySide6 import QtWidgets, QtCore


@dataclass
class HelperData:
    index: QtCore.QModelIndex = None


class SelectorBase(
    AbstractTutorialClass,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstactQtResolver(QtWidgets.QWidget, AbstractTutorialClass),
):
    itemSelected = QtCore.Signal(object)

    def __init__(
        self,
        resource_prefix: str,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(resource_prefix, parent, f)

    def __new__(self, *args, **kwargs):
        abstractQt.handleAbstractMethods(self)
        return super().__new__(self, *args, **kwargs)

    def setDefaultPrompt(self, new_prompt: str) -> None:
        """Can be overriden in child selector to set default prompt"""
        pass

    def setData(self, data: typing.Any) -> None:
        """Can be overriden in child selector to pass in data at show time"""
        pass

    def reset(self) -> None:
        """Can be overriden in child selector reset"""
        pass
