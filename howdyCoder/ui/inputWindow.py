from .inputBox import InputBox

import typing

from PySide6 import QtWidgets, QtCore


class InputWindow(QtWidgets.QDialog):
    def __init__(
        self,
        inputs: typing.List[InputBox],
        code: str,
        parent: QtWidgets.QWidget | None = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel(f"Input for {code}")
        layout.addWidget(label)
        for w in inputs:
            layout.add(w)
        self.setLayout(layout)
