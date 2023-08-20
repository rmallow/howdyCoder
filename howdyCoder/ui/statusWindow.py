from .qtUiFiles import ui_statusWindow
from .statusModel import statusModel

from PySide6 import QtWidgets, QtCore


class statusWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Load UI file
        self._ui = ui_statusWindow.Ui_StatusWindow()
        self._ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)

        self.statusModel = statusModel()
        self._ui.processView.setModel(self.statusModel)
