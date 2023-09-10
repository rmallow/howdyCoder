from .qtUiFiles.ui_mousePosGetter import Ui_MousePosGetter
from .util import abstractQt
from .uiConstants import GUI_REFRESH_INTERVAL
from .tutorialOverlay import AbstractTutorialClass

from ..core.dataStructs import InputData

from abc import abstractmethod
import typing
import time

from PySide6 import QtWidgets, QtCore, QtGui

import pyautogui


class InputGetterBase(
    AbstractTutorialClass,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstactQtResolver(QtWidgets.QWidget, AbstractTutorialClass),
):
    HIDE_ENTER = False
    HIDE_RESET = False

    inputEntered = QtCore.Signal(InputData)

    def __new__(self, *args, **kwargs):
        abstractQt.handleAbstractMethods(self)
        return super().__new__(self, *args, **kwargs)

    @abstractmethod
    def value(self):
        pass

    @abstractmethod
    def clear(self):
        pass


class MousePosGetter(InputGetterBase):
    TUTORIAL_RESOURCE_PREFIX = "test"

    HIDE_ENTER = True
    HIDE_RESET = True

    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(self.TUTORIAL_RESOURCE_PREFIX, parent, f)
        self._ui = Ui_MousePosGetter()
        self._ui.setupUi(self)

        self.timer = QtCore.QTimer()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updatePos)
        self.timer.start(GUI_REFRESH_INTERVAL)

        self._last_check_time = time.time()
        self.x = self.y = None

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if (
            self._ui.active_check.isChecked()
            and event.key() == QtGui.Qt.Key.Key_Space
            and time.time() - self._last_check_time >= 1
            and self.x is not None
            and self.y is not None
        ):
            self._last_check_time = time.time()
            self.inputEntered.emit(InputData(val=(self.x, self.y)))
        return super().keyPressEvent(event)

    def getTutorialClasses(self) -> typing.List:
        return [self]

    def value(self):
        pass

    def clear(self):
        pass

    def updatePos(self):
        if self._ui.active_check.isChecked():
            self.setFocusPolicy(QtGui.Qt.FocusPolicy.StrongFocus)
            self.x, self.y = pyautogui.position()
            self._ui.pos_label.setText(f"x:{self.x}, y:{self.y}")
        else:
            self.x = self.y = None
            self._ui.pos_label.setText("Not Active")
