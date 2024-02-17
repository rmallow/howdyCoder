from .util import qtResourceManager, qtUtil, toggleSwitch
from ..commonUtil import keyringUtil
from ..core.keySingleton import KeySetData
from ..core import keySingleton, datalocator, parameterSingleton
from ..core.commonGlobals import EditorType

import typing

from PySide6 import QtWidgets, QtCore, QtGui
from .qtUiFiles.ui_keySetWidget import Ui_KeySetWidget

SET_API_KEY = "Key was validated and set."
INVALID_API_KEY = "Key was invalid and was not set."

KEY_RETRIEVED = "Key was retrieved"


class KeySetWindow(qtUtil.StayOnTopInFocus, QtWidgets.QDialog):
    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        f: QtCore.Qt.WindowType = QtCore.Qt.WindowType(),
    ) -> None:
        super().__init__(parent, f)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(KeySetWidget(self))
        self.setLayout(layout)


class KeySetWidget(QtWidgets.QWidget):
    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        f: QtCore.Qt.WindowType = QtCore.Qt.WindowType(),
    ) -> None:
        super().__init__(parent, f)
        self._ui = Ui_KeySetWidget()
        self._ui.setupUi(self)

        assert keySingleton.key_set_data_mapping

        self._key_set_data: KeySetData = None

        for k, v in keySingleton.key_set_data_mapping.items():
            self._ui.key_choice_combo.addItem(k, v)

        self._ui.arrow_label.setPixmap(
            self.style().standardPixmap(QtWidgets.QStyle.StandardPixmap.SP_ArrowRight)
        )

        self._ui.set_button.released.connect(self.setKey)
        self._ui.user_manual_button.released.connect(
            lambda: QtGui.QDesktopServices.openUrl(
                QtCore.QUrl("https://howdycoder.io/docs/apikeys.html")
            )
        )
        self._ui.key_choice_combo.currentIndexChanged.connect(self.keyComboChanged)
        self._ui.key_choice_combo.setCurrentIndex(0)
        self.keyComboChanged(0)
        if self._ui.key_choice_combo.count() < 2:
            self._ui.key_choice_combo.setEnabled(False)

        """
        layout = QtWidgets.QHBoxLayout(self._ui.toggle_switch_box)
        self._toggle_switch = toggleSwitch.Switch(
            self._ui.toggle_switch_box, thumb_radius=12, track_radius=12
        )
        layout.addWidget(self._toggle_switch)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._ui.toggle_switch_box.setLayout(layout)
        self._toggle_switch.released.connect(self.toggleSwitchReleased)
        self.toggleSwitchReleased()
        

    @QtCore.Slot()
    def toggleSwitchReleased(self):
        self._ui.key_select_combo.setCurrentIndex(-1)
        self._ui.api_key_edit.clear()
        self._ui.api_key_edit.setEnabled(not self._toggle_switch.isChecked())
        self._ui.key_select_combo.setEnabled(self._toggle_switch.isChecked())

        """

    @QtCore.Slot()
    def keyComboChanged(self, _: int):
        self.changeKeySetter(self._ui.key_choice_combo.currentData())

    def getCurrentKeyToBeSet(self):
        pass

    @QtCore.Slot()
    def setKey(self) -> bool:
        assert self._key_set_data is not None
        if qtUtil.showKeyWarning() and self._key_set_data.validation_function(
            self._ui.api_key_edit.text()
        ):
            self.setStatus(True, SET_API_KEY)
            self._key_set_data.set_function(self._ui.api_key_edit.text())
            keySingleton.key_status[self._ui.key_choice_combo.currentText()].valid = (
                True
            )
            keySingleton.key_status[self._ui.key_choice_combo.currentText()].current = (
                self._ui.api_key_edit.text()
            )
            datalocator.modifyValue(
                datalocator.SETTINGS,
                keySingleton.KEYS,
                self._ui.key_choice_combo.currentText(),
                str(True),
            )
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

    def setStatus(self, valid: bool, label: str) -> None:
        self._ui.status_icon_label.setPixmap(
            qtResourceManager.getResourceByName(
                qtResourceManager.ICONS_PREFIX,
                (
                    qtResourceManager.GREEN_CHECKMARK
                    if valid
                    else qtResourceManager.RED_X
                ),
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
