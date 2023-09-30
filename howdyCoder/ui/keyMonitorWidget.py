from ..core import keySingleton
from .uiConstants import GUI_REFRESH_INTERVAL

from ..commonUtil import helpers

import typing

from PySide6 import QtWidgets, QtCore


class KeyMonitorWidget(QtWidgets.QWidget):
    allKeysValid = QtCore.Signal(bool)

    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        f: QtCore.Qt.WindowType = QtCore.Qt.WindowType(),
    ) -> None:
        super().__init__(parent, f)
        self._keys_to_watch = []
        self.all_valid = False  # this can be viewed from outside
        self.label = QtWidgets.QLabel(self)
        self.label.setStyleSheet("color:red")
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.timer = QtCore.QTimer()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.onTimer)
        self.timer.start(GUI_REFRESH_INTERVAL)

    def watchKey(self, key: str):
        self._keys_to_watch.append(key)

    def clearKeys(self):
        self._keys_to_watch.clear()

    def onTimer(self):
        invalid = []
        for k in self._keys_to_watch:
            if k not in keySingleton.key_status or not keySingleton.key_status[k].valid:
                invalid.append(k)
        if invalid:
            if self.all_valid:
                self.show()
                self.allKeysValid.emit(False)
            self.label.setText(
                helpers.listToFormattedString(
                    "Keys either not set or not valid, set these keys in the Key Window at the top bar: ",
                    invalid,
                )
            )
        else:
            if not self.all_valid:
                self.hide()
                self.allKeysValid.emit(True)
        self.all_valid = len(invalid) == 0
