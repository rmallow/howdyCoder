from abc import ABC
import typing

from PySide2 import QtWidgets, QtCore


class selectorBaseMeta(type(ABC), type(QtWidgets.QWidget)):
    pass


class SelectorBase(QtWidgets.QWidget, ABC, metaclass=selectorBaseMeta):
    itemSelected = QtCore.Signal(object)

    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(parent, f)
