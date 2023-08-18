from .tutorialOverlay import AbstractTutorialClass

from .util import abstractQt

from .qtUiFiles import ui_newBlockWidget

import typing

from PySide6 import QtWidgets, QtCore


class NewBlockWidget(
    AbstractTutorialClass,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstactQtResolver(QtWidgets.QWidget, AbstractTutorialClass),
):
    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__("test", parent, f)
        # accessed by main window
        self.ui = ui_newBlockWidget.Ui_NewBlockWidget()
        self.ui.setupUi(self)

    def getTutorialClasses(self) -> typing.List:
        return [self]
