from .qtUiFiles import ui_configWindow

from PySide6 import QtWidgets, QtCore


class ConfigWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Load UI file
        self._ui = ui_configWindow.Ui_ConfigWindow()
        self._ui.setupUi(self)

        self.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        # Set up signals and slots
        self._ui.loadButton.clicked.connect(self.showFileDialog)

    @QtCore.Slot()
    def showFileDialog(self):
        self._ui.config_edit.setText(
            QtWidgets.QFileDialog.getOpenFileName(
                self, "Open Config File", filter="Yaml (*.yml)"
            )[0]
        )

    def getFile(self):
        return self._ui.config_edit.text()
