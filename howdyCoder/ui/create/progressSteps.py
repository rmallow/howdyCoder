from ..uiConstants import (
    PROGRESS_BAR_HEIGHT,
    PROGRESS_BAR_COMPLETED_COLOR,
    PROGRESS_BAR_UNCOMPLETED_COLOR,
)
from .progressButton import ProgressButton

import typing

from PySide6 import QtWidgets, QtCore, QtGui


class ProgressSteps(QtWidgets.QWidget):
    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(parent, f)
        self._steps: typing.List[str] = []
        self._cur_step_index: int = 0
        self._completed_steps = []
        self._buttons: typing.List[ProgressButton] = []

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        stillCompleted = True
        for i in range(0, len(self._buttons) - 1):
            button1 = self._buttons[i]
            button2 = self._buttons[i + 1]

            # the left point of the rect is the right of the first button
            leftPoint = button1.mapButtonPointToParent(
                self, button1.getButtonMiddleRightPoint()
            )
            rightPoint = button2.mapButtonPointToParent(
                self, button2.getButtonMiddleLeftPoint()
            )
            leftPoint.setY(leftPoint.y() - PROGRESS_BAR_HEIGHT / 2)
            rightPoint.setY(rightPoint.y() + PROGRESS_BAR_HEIGHT / 2)
            rect = QtCore.QRect(leftPoint, rightPoint)
            color = PROGRESS_BAR_UNCOMPLETED_COLOR
            if stillCompleted and self._completed_steps[i]:
                color = PROGRESS_BAR_COMPLETED_COLOR
            else:
                stillCompleted = False
            painter.fillRect(rect, color)

        return super().paintEvent(event)

    def setSteps(self, steps: typing.List[str]) -> None:
        """Based on the passed in values set up the display"""
        self._steps = steps
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        for step in self._steps:
            button = ProgressButton(step, parent=self)
            self._buttons.append(button)
            layout.addWidget(button)
        self.setLayout(layout)
        self.reset()

    def next(self):
        """Increment current step"""
        if self._cur_step_index + 1 < len(self._steps):
            self._cur_step_index += 1
        self.updateDisplay()

    def back(self):
        """Decrement current step"""
        if self._cur_step_index > 0:
            self._cur_step_index -= 1
        self.updateDisplay()

    def reset(self) -> None:
        """Change current step back to 0"""
        self._cur_step_index = 0
        self._completed_steps = [None] * len(self._steps)
        self.updateDisplay()

    def goTo(self, index: int) -> None:
        """Change current step to given step"""
        if index < len(self._steps) and index >= 0:
            self._cur_step_index = index
        self.updateDisplay()

    def setCompletedStep(self, index: int, value: bool) -> None:
        """set the completed step in the list"""
        if index < len(self._completed_steps):
            self._completed_steps[index] = value or self._completed_steps[index]

    def updateDisplay(self):
        for x in range(len(self._buttons)):
            self._buttons[x].setCurrent(x == self._cur_step_index)
            self._buttons[x].setCompleted(self._completed_steps[x])
        self.update()
