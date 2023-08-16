from .util import abstractQt

from abc import abstractmethod
import typing

from PySide6 import QtWidgets, QtCore


class FuncSelectorPageBase(
    QtWidgets.QWidget, metaclass=abstractQt.getAbstactQtResolver(QtWidgets.QWidget)
):
    # we are actually emitting a dict, but PySide6 has an error with dict Signals, so change to object
    funcSelected = QtCore.Signal(object)

    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(parent, f)

    def __new__(self, *args, **kwargs):
        abstractQt.handleAbstractMethods(self)
        return super().__new__(self, *args, **kwargs)

    @abstractmethod
    def updateData(self) -> None:
        pass
