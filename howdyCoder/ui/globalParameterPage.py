from .qtUiFiles import ui_globalParameterPage
from .tutorialOverlay import AbstractTutorialClass
from .mainWindowPageBase import MainWindowPageBase


from .util import abstractQt

import typing

from PySide6 import QtWidgets, QtCore, QtGui


class GlobalParameterPage(
    AbstractTutorialClass,
    MainWindowPageBase,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstactQtResolver(QtWidgets.QWidget, AbstractTutorialClass),
):
    TUTORIAL_RESOURCE_PREFIX = "None"

    def __new__(self, *args, **kwargs):
        abstractQt.handleAbstractMethods(self)
        return super().__new__(self, *args, **kwargs)

    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        f: QtCore.Qt.WindowType = QtCore.Qt.WindowType(),
    ) -> None:
        super().__init__(self.TUTORIAL_RESOURCE_PREFIX, parent, f)

        self._ui = ui_globalParameterPage.Ui_GlobalParameterPage()
        self._ui.setupUi(self)

    def getTutorialClasses(self) -> typing.List:
        return []

    def leaveMainPage(self):
        self._ui.globalParameterPageWidget.saveParameters()

    def loadMainPage(self):
        self._ui.globalParameterPageWidget.loadParameters()
