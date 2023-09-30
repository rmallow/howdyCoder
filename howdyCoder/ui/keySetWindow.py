from .qtUiFiles import ui_keySetWindow

from ..core import keySingleton, datalocator

from PySide6 import QtWidgets, QtCore


class KeySetWindow(QtWidgets.QDialog):
    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        f: QtCore.Qt.WindowType = QtCore.Qt.WindowType(),
    ) -> None:
        super().__init__(parent, f)
        self._ui = ui_keySetWindow.Ui_KeySetWindow()
        self._ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint, True)

        assert keySingleton.key_set_data_mapping
        for k, v in keySingleton.key_set_data_mapping.items():
            self._ui.key_choice_combo.addItem(k, v)

        self._ui.key_choice_combo.currentIndexChanged.connect(self.keyComboChanged)
        self._ui.key_choice_combo.setCurrentIndex(0)
        self.keyComboChanged(0)

        self._ui.key_set_widget.alwaysRetrieve.connect(self.alwaysRetrieve)
        self._ui.key_set_widget.keySet.connect(self.keySet)

    @QtCore.Slot()
    def keyComboChanged(self, _: int):
        self._ui.key_set_widget.changeKeySetter(self._ui.key_choice_combo.currentData())

    @QtCore.Slot()
    def alwaysRetrieve(self):
        datalocator.modifyValue(
            datalocator.SETTINGS,
            keySingleton.KEYS,
            self._ui.key_choice_combo.currentText(),
            str(True),
        )

    @QtCore.Slot()
    def keySet(self, key: str):
        keySingleton.key_status[self._ui.key_choice_combo.currentText()].valid = True
        keySingleton.key_status[self._ui.key_choice_combo.currentText()].current = key
