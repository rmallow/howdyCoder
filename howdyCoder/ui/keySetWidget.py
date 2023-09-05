from .util import qtResourceManager
from ..commonUtil import keyringUtil

import typing

from PySide6 import QtWidgets, QtCore
from .qtUiFiles.ui_keySetWidget import Ui_KeySetWidget

SET_API_KEY = "API key was validated and set."
INVALID_API_KEY = "API key was not valid and was not set."


class KeySetWidget(QtWidgets.QWidget):
    def __init__(
        self,
        key_name: str = "",
        key_validation_function: typing.Callable = None,
        output_function: typing.Callable = None,
        parent: QtWidgets.QWidget | None = None,
        f: QtCore.Qt.WindowType = QtCore.Qt.WindowType(),
    ) -> None:
        super().__init__(parent, f)
        self._ui = Ui_KeySetWidget()
        self._ui.setupUi(self)

        self.key_name: str = key_name
        self._key_validation_function: typing.Callable = key_validation_function
        self.output_function: typing.Callable = output_function

        self._ui.api_key_button.released.connect(self.keySet)

    @QtCore.Slot()
    def keySet(self) -> None:
        assert self.key_name and self._key_validation_function
        if self._key_validation_function(self._ui.api_key_edit.text()):
            self.setStatus(True)
            keyringUtil.setKey(self.key_name, self._ui.api_key_edit.text())
            self.output_function(True)

        else:
            self.setStatus(False)

    def setStatus(self, valid: bool) -> None:
        self._ui.status_icon_label.setPixmap(
            qtResourceManager.getResourceByName(
                "icons", ("checkmark_green.png" if valid else "x_red.png")
            ).scaled(
                self._ui.status_icon_label.width(), self._ui.status_icon_label.height()
            )
        )
        self._ui.status_text_label.setText(SET_API_KEY if valid else INVALID_API_KEY)
