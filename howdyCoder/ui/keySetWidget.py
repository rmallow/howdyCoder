from .util import qtResourceManager
from ..commonUtil import keyringUtil
from ..core.keySingleton import KeySetData

import typing

from PySide6 import QtWidgets, QtCore, QtGui
from .qtUiFiles.ui_keySetWidget import Ui_KeySetWidget

SET_API_KEY = "Key was validated and set."
INVALID_API_KEY = "Key was invalid and was not set."

KEY_RETRIEVED = "Key was retrieved"


class KeySetWidget(QtWidgets.QWidget):
    keySet = QtCore.Signal(str)
    alwaysRetrieve = QtCore.Signal()

    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        f: QtCore.Qt.WindowType = QtCore.Qt.WindowType(),
    ) -> None:
        super().__init__(parent, f)
        self._ui = Ui_KeySetWidget()
        self._ui.setupUi(self)

        self._key_set_data: KeySetData = None

        self._ui.set_button.released.connect(self.setKey)
        self._ui.store_button.released.connect(self.storeKey)
        self._ui.retrieve_button.released.connect(self.retrieveKey)
        self._ui.always_retrieve_button.released.connect(self.alwaysRetrieveKey)
        self._ui.user_manual_button.released.connect(
            lambda: QtGui.QDesktopServices.openUrl(
                QtCore.QUrl("https://howdycoder.io/docs/apikeys.html")
            )
        )

    @QtCore.Slot()
    def setKey(self) -> bool:
        assert self._key_set_data is not None
        if self._key_set_data.validation_function(self._ui.api_key_edit.text()):
            self.setStatus(True, SET_API_KEY)
            self._key_set_data.set_function(self._ui.api_key_edit.text())
            self.keySet.emit(self._ui.api_key_edit.text())
            return True
        else:
            self.setStatus(False, INVALID_API_KEY)
            return False

    @QtCore.Slot()
    def storeKey(self) -> None:
        if self.setKey():
            keyringUtil.storeKey(
                self._key_set_data.key_name, self._ui.api_key_edit.text()
            )

    @QtCore.Slot()
    def retrieveKey(self) -> bool:
        assert self._key_set_data is not None
        key = keyringUtil.getKey(self._key_set_data.key_name)
        if self._key_set_data.validation_function(key):
            self.setStatus(True, f"{KEY_RETRIEVED} and {SET_API_KEY}")
            self._key_set_data.set_function(key)
            self.keySet.emit(key)
            return True
        else:
            self.setStatus(False, f"{KEY_RETRIEVED} but {INVALID_API_KEY}")
            return False

    @QtCore.Slot()
    def alwaysRetrieveKey(self) -> None:
        if self.retrieveKey():
            self.alwaysRetrieve.emit()

    def setStatus(self, valid: bool, label: str) -> None:
        self._ui.status_icon_label.setPixmap(
            qtResourceManager.getResourceByName(
                "icons", ("checkmark_green.png" if valid else "x_red.png")
            ).scaled(
                self._ui.status_icon_label.width(), self._ui.status_icon_label.height()
            )
        )
        self._ui.status_text_label.setText(label)

    def changeKeySetter(self, key_set_data: KeySetData):
        self._ui.status_icon_label.clear()
        self._ui.status_text_label.clear()
        self._ui.api_key_edit.clear()
        self._key_set_data = key_set_data
