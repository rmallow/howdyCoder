from ..core.commonGlobals import InputType
from ..core.dataStructs import InputData

from .inputGetter import InputGetterBase, MousePosGetter, AudioGetter

import typing

from PySide6 import QtWidgets, QtCore


class InputBox(QtWidgets.QWidget):
    INPUT_TYPE_TO_WIDGET = {
        InputType.SHORT_TEXT: QtWidgets.QLineEdit,
        InputType.LONG_TEXT: QtWidgets.QPlainTextEdit,
        InputType.NUMBER: QtWidgets.QDoubleSpinBox,
        InputType.MOUSE_POS: MousePosGetter,
        InputType.SPEECH_TO_TEXT: AudioGetter,
    }

    INPUT_TYPE_TO_GETTER = {
        InputType.SHORT_TEXT: QtWidgets.QLineEdit.text,
        InputType.LONG_TEXT: QtWidgets.QPlainTextEdit.toPlainText,
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
        self._input_widget: InputGetterBase | QtWidgets.QWidget = (
            self.INPUT_TYPE_TO_WIDGET[self._input_type](self)
        )
        hide_enter = hide_reset = False
        if isinstance(self._input_widget, InputGetterBase):
            hide_enter = self._input_widget.HIDE_ENTER
            hide_reset = self._input_widget.HIDE_RESET
            self._input_widget.inputEntered.connect(self.inputEnteredWrapper)
        """Manual UI setup"""
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(
            QtWidgets.QLabel(f"Data Source - {self._data_source_name}", self)
        )
        layout.addWidget(self._input_widget)
        if not (hide_enter and hide_reset):
            button_box_widget = QtWidgets.QWidget(self)
            button_box = QtWidgets.QHBoxLayout()
        if not hide_enter:
            enter_button = QtWidgets.QPushButton("Enter", self)
            enter_button.released.connect(self.enterPressed)
            button_box.addWidget(enter_button)
        if not hide_reset:
            reset_button = QtWidgets.QPushButton("Reset", self)
            reset_button.released.connect(self.resetPressed)
            button_box.addWidget(reset_button)
        if not (hide_enter and hide_reset):
            button_box_widget.setLayout(button_box)
            layout.addWidget(button_box_widget)
        self.setLayout(layout)

    @QtCore.Slot()
    def enterPressed(self):
        val = None
        if self._input_type in self.INPUT_TYPE_TO_GETTER:
            val = self.INPUT_TYPE_TO_GETTER[self._input_type](self._input_widget)
        else:
            val = self._input_widget.value()
        if val is not None:
            self.inputEntered.emit(
                InputData(code="", data_source_name=self._data_source_name, val=val)
            )

    @QtCore.Slot()
    def resetPressed(self):
        if self._input_type in self.INPUT_TYPE_TO_RESET:
            self.INPUT_TYPE_TO_RESET[self._input_type](self._input_widget)
        else:
            self._input_widget.clear()

    @QtCore.Slot()
    def inputEnteredWrapper(self, input_data: InputData):
        input_data.data_source_name = self._data_source_name
        self.inputEntered.emit(input_data)
