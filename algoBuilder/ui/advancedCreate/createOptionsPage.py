from .createBasePage import CreateBasePage

from .qtUiFiles import ui_createOptionsPage

from ..core.configConstants import NAME, EXPORT, CSV

import typing

from PySide2 import QtWidgets


class CreateOptionsPage(CreateBasePage):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = None):
        super().__init__(parent=parent)

        self._ui = ui_createOptionsPage.Ui_CreateOptionsPage()
        self._ui.setupUi(self)

    def validate(self) -> bool:
        """Check if the name is entered and valid"""
        valid = False
        text = self._ui.nameEdit.text()
        if text and text.strip():
            text = text.strip()
            if not text[0].isnumeric():
                valid = True
        return valid

    def getConfig(self) -> typing.Dict[str, typing.Any]:
        """Return the configuration for that page"""
        returnDict = {NAME: self._ui.nameEdit.text()}
        if self._ui.csvCheckBox.isChecked():
            returnDict[EXPORT] = CSV
        return returnDict
