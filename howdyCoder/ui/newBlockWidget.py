from .tutorialOverlay import AbstractTutorialClass

from .util import abstractQt

from .qtUiFiles import ui_newBlockWidget

import typing

from PySide6 import QtWidgets, QtCore


class NewBlockWidget(
    AbstractTutorialClass,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstractQtResolver(
        QtWidgets.QWidget, AbstractTutorialClass
    ),
):
    TUTORIAL_RESOURCE_PREFIX = "NewBlockWidget"

    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(self.TUTORIAL_RESOURCE_PREFIX, parent=parent, f=f)
        # accessed by main window
        self.ui = ui_newBlockWidget.Ui_NewBlockWidget()
        self.ui.setupUi(self)

    def getTutorialClasses(self) -> typing.List:
        return [self]
