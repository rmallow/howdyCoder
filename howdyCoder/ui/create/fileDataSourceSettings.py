from ..qtUiFiles import ui_fileDataSourceSettings

import typing

from PySide6 import QtWidgets, QtGui, QtCore


class FileDataSourceSettings(QtWidgets.QWidget):
    headerSettingsChanged = QtCore.Signal()
    sheetSettingsChanged = QtCore.Signal()

    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        f: QtCore.Qt.WindowType = QtCore.Qt.WindowType(),
    ) -> None:
        super().__init__(parent, f)

        self._ui = ui_fileDataSourceSettings.Ui_FileDataSourceSettings()
        self._ui.setupUi(self)
        self._ui.header_switch.released.connect(self.headerSettingsChanged)
        self._ui.orientation_switch.released.connect(self.headerSettingsChanged)
        self._ui.sheet_combo_box.currentIndexChanged.connect(self.sheetSettingsChanged)

    def reset(self):
        self.setCustomHeader(False)
        self.setDataInRows(False)
        self.setExampleHeaderText("")
        self.showSheetSettings(False)

    def showSheetSettings(self, show: bool) -> None:
        if show:
            self._ui.sheet_select_box.show()
        else:
            self._ui.sheet_select_box.hide()

    def getCustomHeaderSet(self) -> bool:
        return self._ui.header_switch.isChecked()

    def getDataInRows(self) -> bool:
        return self._ui.orientation_switch.isChecked()

    def setCustomHeader(self, is_set: bool) -> None:
        self._ui.header_switch.setChecked(is_set)

    ROW = "row"
    COLUMN = "column"

    def setDataInRows(self, is_set: bool) -> None:
        self._ui.orientation_switch.setChecked(is_set)
        self._ui.first_header_label.setText(
            f"First {self.COLUMN if self.getDataInRows() else self.ROW} is header"
        )

    def setExampleHeaderText(self, text: str) -> None:
        self._ui.example_header_label.setText(text)

    def setSheetSelected(self, sheet_name: str) -> None:
        index = self._ui.sheet_combo_box.findText(sheet_name)
        self._ui.sheet_combo_box.setCurrentIndex(index)

    def setSheetsAvailable(self, sheets: typing.List[str]):
        self._ui.sheet_combo_box.clear()
        self._ui.sheet_combo_box.addItems(sheets)

    def getSheetSelected(self) -> str:
        return self._ui.sheet_combo_box.currentText()
