from .baseTablePage import BaseTablePage
from .qtUiFiles import ui_startWizardTablePage
from .util import qtUtil, qtResourceManager

from ..core.dataStructs import Parameter
from ..core import parameterSingleton
from ..core.commonGlobals import EditorType

import typing

from PySide6 import QtWidgets, QtGui, QtCore


class FileCheckWidget(BaseTablePage):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._table_model = QtGui.QStandardItemModel(self._ui.table)
        self._table_model.setHorizontalHeaderLabels(
            ["Item Name", "File Loaded As", "File Path", "File Exists"]
        )
        self._ui.table.setModel(self._table_model)

    def updateValues(
        self, file_exists: typing.Dict[str, typing.List[typing.Tuple[str, str, bool]]]
    ):
        self.reset()
        self._no_values = not bool(file_exists)
        for item, file_list in file_exists.items():
            for file_tuple in file_list:
                item_name = QtGui.QStandardItem(item)
                file_name = QtGui.QStandardItem(file_tuple[0])
                file_path = QtGui.QStandardItem(file_tuple[1])
                file_exists_item = None
                if file_tuple[2]:
                    file_exists_item = QtGui.QStandardItem(
                        QtGui.QIcon(
                            qtResourceManager.getResourceByName(
                                qtResourceManager.ICONS_PREFIX,
                                qtResourceManager.GREEN_CHECKMARK,
                            )
                        ),
                        "",
                    )
                else:
                    self._missing_values = True
                    file_exists_item = QtGui.QStandardItem(
                        QtGui.QIcon(
                            self.style().standardPixmap(
                                self.style().StandardPixmap.SP_MessageBoxCritical
                            )
                        ),
                        "",
                    )
                self._table_model.appendRow(
                    [item_name, file_name, file_path, file_exists_item]
                )
