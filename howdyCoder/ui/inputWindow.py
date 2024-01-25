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
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel(f"Input for {code}")
        layout.addWidget(label)
        for w in inputs:
            layout.addWidget(w)
        self.setLayout(layout)
