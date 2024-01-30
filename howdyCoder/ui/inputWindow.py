from .inputBox import InputBox

from .util.qtUtil import StayOnTopInFocus

import typing

from PySide6 import QtWidgets, QtCore, QtGui


class InputWindow(StayOnTopInFocus, QtWidgets.QDialog):
    def __init__(
        self,
        inputs: typing.List[InputBox],
        code: str,
        parent: QtWidgets.QWidget | None = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(parent, f)
        self.raise_()
        top_layout = QtWidgets.QVBoxLayout(self)
        self._change_direction_button = QtWidgets.QPushButton("Change Direction", self)
        self._change_direction_button.released.connect(self.changeWindowDirection)
        sub_widget = QtWidgets.QWidget(self)

        self._input_layout = QtWidgets.QBoxLayout(
            QtWidgets.QBoxLayout.Direction.LeftToRight, sub_widget
        )
        for w in inputs:
            self._input_layout.addWidget(w)
        sub_widget.setLayout(self._input_layout)
        top_layout.addWidget(QtWidgets.QLabel(f"Input for {code}"))
        top_layout.addWidget(self._change_direction_button)
        top_layout.addWidget(sub_widget)

    @QtCore.Slot()
    def changeWindowDirection(self):
        new_direction_int = self._input_layout.direction().value + 1
        if new_direction_int > QtWidgets.QBoxLayout.Direction.BottomToTop.value:
            new_direction_int = 0
        self._input_layout.setDirection(
            QtWidgets.QBoxLayout.Direction(new_direction_int)
        )
