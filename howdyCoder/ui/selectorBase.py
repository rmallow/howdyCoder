from .tutorialOverlay import AbstractTutorialClass
from .util import abstractQt

import typing

from PySide6 import QtWidgets, QtCore


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
