from .startWizardBasePage import StartWizardBasePage
from .qtUiFiles import ui_startWizardTablePage
from .util import qtUtil, qtResourceManager

import typing

from PySide6 import QtWidgets, QtGui, QtCore


class BaseTablePage(StartWizardBasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ui = ui_startWizardTablePage.Ui_StartWizardTablePage()
        self._ui.setupUi(self)

        self._ui.table.setHorizontalHeader(
            qtUtil.WordWrapHeader(QtCore.Qt.Orientation.Horizontal, self._ui.table)
        )
        self._ui.table.verticalHeader().hide()

        self._no_values = True
        self._missing_values = False

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        for x in range(self._ui.table.model().columnCount()):
            self._ui.table.setColumnWidth(
                x, self._ui.table.width() // self._ui.table.model().columnCount()
            )
        return super().resizeEvent(event)

    def reset(self):
        self._no_values = True
        self._missing_values = False
        self._table_model.removeRows(0, self._ui.table.model().rowCount())

    def startPage(self):
        if self._no_values:
            self.pageFinished.emit()
        elif self._missing_values:
            self.setOk.emit(False)
