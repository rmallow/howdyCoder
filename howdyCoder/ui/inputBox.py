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
        name: str,
        input_type: InputType,
        hide_enter: bool = False,
        hide_reset: bool = False,
        hide_label: bool = False,
        widget_constructor: typing.Callable | None = None,
        getter: typing.Callable | None = None,
        resetter: typing.Callable | None = None,
        parent: QtWidgets.QWidget | None = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(parent, f)
        self._name = name
        self._input_type = input_type
        self._widget_constructor = (
            widget_constructor
            if widget_constructor is not None
            else self.INPUT_TYPE_TO_WIDGET[self._input_type]
        )
        self._getter = (
            getter
            if getter is not None
            else self.INPUT_TYPE_TO_GETTER.get(self._input_type, InputGetterBase.value)
        )
        self._resetter = (
            resetter
            if resetter is not None
            else self.INPUT_TYPE_TO_RESET.get(self._input_type, InputGetterBase.clear)
        )
        self._input_widget: InputGetterBase | QtWidgets.QWidget = (
            self._widget_constructor(self)
        )
        if isinstance(self._input_widget, InputGetterBase):
            hide_enter = self._input_widget.HIDE_ENTER
            hide_reset = self._input_widget.HIDE_RESET
            self._input_widget.inputEntered.connect(self.inputEnteredWrapper)
        """Manual UI setup"""
        layout = QtWidgets.QVBoxLayout()
        if not hide_label:
            layout.addWidget(QtWidgets.QLabel(f"Data Source - {self._name}", self))
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

    def getInput(self) -> typing.Any | None:
        return self._getter(self._input_widget)

    @QtCore.Slot()
    def enterPressed(self):
        val = self.getInput()
        if val is not None:
            self.inputEntered.emit(
                InputData(code="", data_source_name=self._name, val=val)
            )

    @QtCore.Slot()
    def resetPressed(self):
        self._resetter(self._input_widget)

    @QtCore.Slot()
    def inputEnteredWrapper(self, input_data: InputData):
        input_data.data_source_name = self._name
        self.inputEntered.emit(input_data)
