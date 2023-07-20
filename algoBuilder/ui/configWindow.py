from .qtUiFiles import ui_configLoader

from ..data.datalocator import SETTINGS_FILE

from PySide2 import QtWidgets, QtCore
import configparser
import os


class configWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Load UI file
        self._ui = ui_configLoader.Ui_ConfigLoader()
        self._ui.setupUi(self)

        # Load defaults
        config = configparser.ConfigParser()
        config.read(SETTINGS_FILE)
        if "Configs" in config:
            self._ui.blockFileLine.setText(
                os.path.abspath(config.get("Configs", "Block", fallback=""))
            )
            self._ui.handlerFileLine.setText(
                os.path.abspath(config.get("Configs", "Handler", fallback=""))
            )
            self.defaultDir = config.get("Configs", "Handler", fallback=None)

        # Set up signals and slots
        self._ui.blockLoadButton.clicked.connect(self.showFileDialog)
        self._ui.handlerLoadButton.clicked.connect(self.showFileDialog)
        self._ui.otherLoadButton.clicked.connect(self.showFileDialog)

    @QtCore.Slot()
    def showFileDialog(self):
        button = self.sender()
        objName = button.objectName()
        fileName = ""
        if objName == "blockLoadButton":
            fileName = self._ui.blockFileLine.text()
        elif objName == "handlerLoadButton":
            fileName = self._ui.handlerFileLine.text()
        elif objName == "otherLoadButton":
            fileName = self._ui.otherFileLine.text()

        if not fileName:
            fileName = os.path.abspath(os.sep)

        newFileTuple = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open Config File", fileName, "Yaml (*.yml)"
        )

        if newFileTuple[0]:
            if objName == "blockLoadButton":
                self._ui.blockFileLine.setText(newFileTuple[0])
            elif objName == "handlerLoadButton":
                self._ui.handlerFileLine.setText(newFileTuple[0])
            elif objName == "otherLoadButton":
                self._ui.otherFileLine.setText(newFileTuple[0])
