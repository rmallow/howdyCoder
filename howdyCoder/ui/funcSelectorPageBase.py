from .tutorialOverlay import AbstractTutorialClass
from .util import abstractQt

from abc import abstractmethod
import typing

from PySide6 import QtWidgets, QtCore


class FuncSelectorPageBase(
    AbstractTutorialClass,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstactQtResolver(QtWidgets.QWidget, AbstractTutorialClass),
):
    # we are actually emitting a dict, but PySide6 has an error with dict Signals, so change to object
    funcSelected = QtCore.Signal(object)

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

    @abstractmethod
    def updateData(self) -> None:
        pass

    def getTutorialClasses(self) -> typing.List:
        return [self]

    def setDefaultPrompt(self, prompt_name: str):
        """Can be overriden in child page to set default prompt"""
        pass

    def setData(self, data: typing.Any) -> None:
        """Can be overriden in child page to pass in data at show time"""
        pass

    def reset(self) -> None:
        """Can be overriden in child page reset"""
        pass
