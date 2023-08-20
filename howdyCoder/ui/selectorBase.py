from .util import abstractQt

import typing

from PySide6 import QtWidgets, QtCore


class SelectorBase(
    QtWidgets.QWidget, metaclass=abstractQt.getAbstactQtResolver(QtWidgets.QWidget)
):
    itemSelected = QtCore.Signal(object)

    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(parent, f)

    def __new__(self, *args, **kwargs):
        abstractQt.handleAbstractMethods(self)
        return super().__new__(self, *args, **kwargs)
