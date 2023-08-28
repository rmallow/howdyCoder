from .createBasePage import CreateBasePage

from ..qtUiFiles import ui_createDataSourceType

import typing

from PySide6 import QtWidgets, QtGui, QtCore

from ...core.configConstants import (
    TYPE,
)

from ...core.commonGlobals import AlgoSettings

NO_SELECTION_TEXT = "Select a type to the left to view its description"


class CreateTypeBasePage(CreateBasePage):
    def __init__(
        self,
        current_config: AlgoSettings,
        type_label: str,
        type_dict: typing.Dict[str, str],
        resource_prefix: str,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, resource_prefix, parent=parent)

        # accessing ui from base page
        self._ui = ui_createDataSourceType.Ui_CreateDataSourceType()
        self._ui.setupUi(self)
        self._ui.typeLabel.setText(type_label)

        self._type_model = QtGui.QStandardItemModel()

        for k, v in type_dict.items():
            item = QtGui.QStandardItem(k)
            item.setData(v)
            self._type_model.appendRow(item)
        self._ui.typeView.setModel(self._type_model)

        self.next_enabled = False
        self.back_enabled = False
        self._ui.typeView.selectionModel().selectionChanged.connect(self.typeSelected)
        self._ui.nameEdit.textChanged.connect(self.enableCheck)

    def typeSelected(self, selection: QtCore.QItemSelection, _):
        if selection.indexes() and selection.indexes()[0].isValid():
            self._ui.typeDescription.setText(
                self._type_model.itemFromIndex(selection.indexes()[0]).data()
            )
        else:
            self._ui.typeDescription.setText(NO_SELECTION_TEXT)
        self.enableCheck()

    def validate(self) -> bool:
        return (
            len(self._ui.typeView.selectionModel().selectedIndexes()) > 0
            and self._ui.typeView.selectionModel().selectedIndexes()[0].isValid()
            and self.validateText(self._ui.nameEdit.text())
            and self._ui.nameEdit.text().strip() not in self.getConfigGroup()
        )

    def save(self) -> None:
        """Set the name as a new dict with the type"""
        self.getTempConfig().clear()
        self.getTempConfig().name = self._ui.nameEdit.text().strip()
        self.getTempConfig().type_ = (
            self._ui.typeView.selectionModel().selectedIndexes()[0].data()
        )

    def reset(self) -> None:
        self._ui.typeView.selectionModel().clearSelection()
        self._ui.nameEdit.setText("")

    def loadPage(self) -> None:
        return super().loadPage()

    def getTutorialClasses(self) -> typing.List:
        return [self]
