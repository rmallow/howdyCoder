from ..core.configConstants import InputType
from ..core.commonGlobals import InputData

import typing

from PySide6 import QtWidgets, QtCore


class InputBox(QtWidgets.QWidget):
    INPUT_TYPE_TO_WIDGET = {
        InputType.SHORT_TEXT: QtWidgets.QLineEdit,
        InputType.LONG_TEXT: QtWidgets.QPlainTextEdit,
        InputType.NUMBER: QtWidgets.QDoubleSpinBox,
    }

    INPUT_TYPE_TO_GETTER = {
        InputType.SHORT_TEXT: QtWidgets.QLineEdit.text,
        InputType.LONG_TEXT: QtWidgets.QLineEdit.text,
        InputType.NUMBER: QtWidgets.QDoubleSpinBox.value,
    }

    INPUT_TYPE_TO_RESET = {
        InputType.SHORT_TEXT: QtWidgets.QLineEdit.clear,
        InputType.LONG_TEXT: QtWidgets.QPlainTextEdit.clear,
        InputType.NUMBER: lambda obj: obj.setValue(0.0),
    }

    inputEntered = QtCore.Signal(InputData)

    def __init__(
        self,
        data_source_name: str,
        input_type: InputType,
        parent: QtWidgets.QWidget | None = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(parent, f)
        self._data_source_name = data_source_name
        self._input_type = input_type
        assert self._input_type in self.INPUT_TYPE_TO_WIDGET
        layout = QtWidgets.QVBoxLayout()
        button_box = QtWidgets.QHBoxLayout()
        button_box_widget = QtWidgets.QWidget(self)
        label = QtWidgets.QLabel(f"Data Source - {self._data_source_name}", self)
        self._input_widget = self.INPUT_TYPE_TO_WIDGET[self._input_type](self)
        enter_button = QtWidgets.QPushButton("Enter", self)
        reset_button = QtWidgets.QPushButton("Reset", self)
        enter_button.released.connect(self.enterPressed)
        reset_button.released.connect(self.resetPressed)
        button_box.addWidget(enter_button)
        button_box.addWidget(reset_button)
        button_box_widget.setLayout(button_box)
        layout.addWidget(label)
        layout.addWidget(self._input_widget)
        layout.addWidget(button_box_widget)
        self.setLayout(layout)

    @QtCore.Slot()
    def enterPressed(self):
        val = self.INPUT_TYPE_TO_GETTER[self._input_type](self._input_widget)
        self.inputEntered.emit(
            InputData(code="", data_source_name=self._data_source_name, val=val)
        )

    @QtCore.Slot()
    def resetPressed(self):
        self.INPUT_TYPE_TO_RESET[self._input_type](self._input_widget)
