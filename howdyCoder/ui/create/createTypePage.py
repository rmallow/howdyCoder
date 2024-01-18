from ...core.commonGlobals import (
    ACTION_LIST,
    DATA_SOURCES,
    ActionTypeEnum,
    DataSourcesTypeEnum,
)
from ...core.dataStructs import ItemSettings
from ..uiConstants import PageKeys
from .createBasePage import CreateBasePage, ItemValidity

from ..qtUiFiles import ui_createDataSourceType

import typing

from PySide6 import QtWidgets, QtGui, QtCore

NO_SELECTION_TEXT = "Select a type to the left to view its description"


class CreateTypePage(CreateBasePage):
    def __init__(
        self,
        current_config: ItemSettings,
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

        for k, v in type_dict.items():
            item = QtWidgets.QListWidgetItem(k)
            item.setData(QtCore.Qt.ItemDataRole.UserRole, v)
            self._ui.typeView.addItem(item)

        self.back_enabled = False
        self._ui.typeView.currentRowChanged.connect(self.typeSelected)
        self._ui.typeView.setCurrentRow(-1)

    def typeSelected(self, row: int):
        if row >= 0 and row < self._ui.typeView.count():
            self._ui.typeDescription.setText(
                self._ui.typeView.item(row).data(QtCore.Qt.ItemDataRole.UserRole)
            )
        else:
            self._ui.typeDescription.setText(NO_SELECTION_TEXT)

    def validate(self) -> typing.Dict[QtWidgets.QWidget | str, ItemValidity]:
        return {
            self._ui.typeView: ItemValidity.getEnum(
                self._ui.typeView.currentRow() != -1
            ),
            self._ui.nameEdit: ItemValidity.getEnum(
                self.validateText(self._ui.nameEdit.text())
            ),
        }

    def save(self) -> None:
        """Set the name as a new dict with the type"""
        new_type = self._ui.typeView.currentItem().text()
        if new_type != self.getConfig().type_:
            self.getConfig().clear()
        self.getConfig().name = self._ui.nameEdit.text().strip()
        self.getConfig().type_ = new_type

    def reset(self) -> None:
        self._ui.typeView.selectionModel().clearSelection()
        self._ui.nameEdit.setText("")

    def loadPage(self) -> None:
        items = self._ui.typeView.findItems(
            self.getConfig().type_, QtCore.Qt.MatchFlag.MatchExactly
        )
        if items:
            self._ui.typeView.setCurrentRow(self._ui.typeView.row(items[0]))
        self._ui.nameEdit.setText(self.getConfig().name)
        return super().loadPage()

    def getTutorialClasses(self) -> typing.List:
        return [self]


class CreateDataSourceTypePage(CreateTypePage):
    TYPE_DESCRIPTION = {
        DataSourcesTypeEnum.FUNC.display: """
    Use a given function call as the source of the data. \n
    On the next page you can choose what function to use.
    """,
        #        DataSourcesTypeEnum.THREADED.display: """
        #    A more advanced version of Func data source. \n
        #    Only necessary if the funciton would normally be used in a multithreaded environment.
        #    """,
        DataSourcesTypeEnum.INPUT.display: """
    Take user input data as the source of the data. \n
    When this option is used, after the program is created, a window can be opened that has the selected input option for inputting user data. \n
    Useful for if you need to tell the program dynamically your own data.
    """,
    }
    PAGE_KEY = PageKeys.DATA_SOURCE_TYPE
    EXIT = PageKeys.ADD_DATA_SOURCE

    TUTORIAL_RESOURCE_PREFIX = "CreateTypeDataSource"

    def __init__(
        self,
        current_config: ItemSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(
            current_config,
            "Data Source Type",
            self.TYPE_DESCRIPTION,
            self.TUTORIAL_RESOURCE_PREFIX,
            parent=parent,
        )


class CreateActionTypePage(CreateTypePage):
    PAGE_KEY = PageKeys.ACTION_TYPE
    EXIT = PageKeys.ADD_ACTION

    TUTORIAL_RESOURCE_PREFIX = "CreateTypeAction"

    TYPE_DESCRIPTION = {
        ActionTypeEnum.TRIGGER.display: """
    Executes an output function based on the given conditions. \n
    Does not create new data and triggers will not expect functions called to return data.
    """,
        ActionTypeEnum.EVENT.display: """
    Takes input data and creates new data based on the given function. \n
    For events, the name of the event will be the name of the output data. \n
    The functions called by events will be expected to return data.
    """,
    }

    def __init__(
        self,
        current_config: ItemSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(
            current_config,
            "Action Type",
            self.TYPE_DESCRIPTION,
            self.TUTORIAL_RESOURCE_PREFIX,
            parent=parent,
        )
