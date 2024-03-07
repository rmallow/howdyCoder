from .baseTablePage import BaseTablePage
from .qtUiFiles import ui_startWizardTablePage
from .util import qtUtil, qtResourceManager

from ..core.dataStructs import Parameter
from ..core import parameterSingleton
from ..core.commonGlobals import EditorType

import typing

from PySide6 import QtWidgets, QtGui, QtCore


class ParameterCheckWidget(BaseTablePage):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._table_model = QtGui.QStandardItemModel(self._ui.table)
        self._table_model.setHorizontalHeaderLabels(
            ["Item Name", "Parameter Name", "Global/Key Name", "Global/Key Value"]
        )
        self._ui.table.setModel(self._table_model)

    def updateValues(
        self, global_to_param_names: typing.Dict[str, typing.List[Parameter]]
    ):
        self.reset()
        self._no_values = not bool(global_to_param_names)
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
                        (
                            global_value.value
                            if global_value.type_ != EditorType.FUNC.display
                            else f"function: {global_value.value.name}"
                        ),
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
        self.checkPage(self._no_values, self._missing_values)
