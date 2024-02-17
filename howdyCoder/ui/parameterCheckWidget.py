from .startWizardBasePage import StartWizardBasePage
from .qtUiFiles import ui_parameterCheckWidget
from .util import qtUtil, qtResourceManager

from ..core.dataStructs import Parameter
from ..core import parameterSingleton

import typing

from PySide6 import QtWidgets, QtGui, QtCore


class ParameterCheckWidget(StartWizardBasePage):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._ui = ui_parameterCheckWidget.Ui_ParameterCheckWidget()
        self._ui.setupUi(self)
        self._no_global_or_keys = True
        self._missing_values = False
        self._table_model = QtGui.QStandardItemModel(self._ui.parameter_table)
        self._ui.parameter_table.setHorizontalHeader(
            qtUtil.WordWrapHeader(
                QtCore.Qt.Orientation.Horizontal, self._ui.parameter_table
            )
        )
        self._table_model.setHorizontalHeaderLabels(
            ["Item Name", "Parameter Name", "Global/Key Name", "Global/Key Value"]
        )
        self._ui.parameter_table.verticalHeader().hide()
        self._ui.parameter_table.setModel(self._table_model)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        for x in range(self._table_model.columnCount()):
            self._ui.parameter_table.setColumnWidth(
                x, self._ui.parameter_table.width() // self._table_model.columnCount()
            )
        return super().resizeEvent(event)

    def reset(self):
        self._no_global_or_keys = True
        self._missing_values = False
        self._table_model.removeRows(0, self._table_model.rowCount())

    def startPage(self):
        if self._no_global_or_keys:
            self.pageFinished.emit()
        elif self._missing_values:
            self.setOk.emit(False)

    def updateValues(
        self, global_to_param_names: typing.Dict[str, typing.List[Parameter]]
    ):
        self.reset()
        self._no_global_or_keys = not bool(global_to_param_names)
        for item, param_list in global_to_param_names.items():
            for param in param_list:
                item_name = QtGui.QStandardItem(item)
                param_name = QtGui.QStandardItem(param.name)
                global_name = QtGui.QStandardItem(param.value)
                global_value = parameterSingleton.getParameter(param.value)
                global_value_item = None
                if global_value is not None:
                    global_value_item = QtGui.QStandardItem(
                        QtGui.QIcon(
                            qtResourceManager.getResourceByName(
                                qtResourceManager.ICONS_PREFIX,
                                qtResourceManager.GREEN_CHECKMARK,
                            )
                        ),
                        global_value,
                    )
                else:
                    self._missing_values = True
                    global_value_item = QtGui.QStandardItem(
                        QtGui.QIcon(
                            self.style().standardPixmap(
                                self.style().StandardPixmap.SP_MessageBoxCritical
                            )
                        ),
                        "MISSING",
                    )
                self._table_model.appendRow(
                    [item_name, param_name, global_name, global_value_item]
                )
