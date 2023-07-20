from abc import ABC, abstractmethod
import typing

from PySide2 import QtWidgets, QtCore


class FuncSelectorPageBaseMeta(type(ABC), type(QtWidgets.QWidget)):
    pass


class FuncSelectorPageBase(QtWidgets.QWidget, ABC, metaclass=FuncSelectorPageBaseMeta):
    funcSelected = QtCore.Signal(dict)

    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(parent, f)

    @abstractmethod
    def updateData(self) -> None:
        pass
