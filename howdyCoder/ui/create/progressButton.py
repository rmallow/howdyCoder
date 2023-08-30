from ..uiConstants import (
    PROGRESS_BAR_COMPLETED_COLOR_STR,
    PROGRESS_BAR_UNCOMPLETED_COLOR_STR,
    PROGRESS_BAR_FAILED_COLOR_STR,
    PROGRESS_BAR_CURRENT_COLOR_STR,
)
from ..qtUiFiles import ui_progressButton

from ..util import qtResourceManager

import typing

from PySide6 import QtWidgets, QtCore, QtGui


class ProgressButton(QtWidgets.QWidget):
    def __init__(
        self,
        labelText: str,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(parent, f)
        # Load UI file
        self._ui = ui_progressButton.Ui_ProgressButton()
        self._ui.setupUi(self)

        self._ui.label.setText(labelText)
        # there are three completed states, None - gray, False - Red, True - Green
        self._completed = None
        self._current = False
        self.setCompleted(self._completed)

    def setCompleted(self, completed: bool) -> None:
        self._completed = completed or self._completed
        color = None
        if self._current:
            color = PROGRESS_BAR_CURRENT_COLOR_STR
            self._ui.button.setIcon(QtGui.QIcon())
        elif self._completed is None:
            color = PROGRESS_BAR_UNCOMPLETED_COLOR_STR
            self._ui.button.setIcon(QtGui.QIcon())
        elif self._completed:
            color = PROGRESS_BAR_COMPLETED_COLOR_STR
            self._ui.button.setIcon(
                qtResourceManager.getResourceByName("icons", "checkmark.png")
            )
        else:
            color = PROGRESS_BAR_FAILED_COLOR_STR
            self._ui.button.setIcon(
                qtResourceManager.getResourceByName("icons", "x.png")
            )
        self._ui.button.setStyleSheet(
            self._ui.button.styleSheet() + f"background-color:{color};"
        )

    def setCurrent(self, current: bool):
        self._current = current

    def getButtonRect(self) -> QtCore.QRect:
        return self._ui.button.rect()

    def getButtonMiddleLeftPoint(self) -> QtCore.QPoint:
        rect = self._ui.button.rect()
        point: QtCore.QPoint = rect.topLeft()
        point.setY(point.y() + rect.height() / 2)
        return point

    def getButtonMiddleRightPoint(self) -> QtCore.QPoint:
        rect = self._ui.button.rect()
        point: QtCore.QPoint = rect.topRight()
        point.setY(point.y() + rect.height() / 2)
        return point

    def mapButtonPointToParent(
        self, parent: QtWidgets.QWidget, point: QtCore.QPoint
    ) -> QtCore.QPoint:
        return self._ui.button.mapTo(parent, point)
