from ...core.commonGlobals import (
    ActionTypeEnum,
    DataSourcesTypeEnum,
    ENUM_DISPLAY,
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
        type_dict: typing.Dict[str, str],
        resource_prefix: str,
        sub_type_dict: typing.Dict[str, typing.Dict[str, str]] = None,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, resource_prefix, parent=parent)

        # accessing ui from base page
        self._ui = ui_createDataSourceType.Ui_CreateDataSourceType()
        self._ui.setupUi(self)

        for k, v in type_dict.items():
            item = QtWidgets.QListWidgetItem(k)
            item.setData(QtCore.Qt.ItemDataRole.UserRole, v)
            self._ui.type_view.addItem(item)

        self._sub_type_dict = sub_type_dict if sub_type_dict is not None else {}

        self.back_enabled = False
        self._ui.type_view.currentRowChanged.connect(self.typeSelected)
        self._ui.sub_type_view.currentRowChanged.connect(self.subTypeSelected)
        self._ui.type_view.setCurrentRow(-1)
        self._ui.sub_type_view.setCurrentRow(-1)
        self._ui.sub_type_wrapper.hide()

    @QtCore.Slot()
    def subTypeSelected(self, row: int) -> None:
        if row >= 0 and row < self._ui.sub_type_view.count():
            self._ui.sub_type_description.setText(
                self._ui.sub_type_view.item(row).data(QtCore.Qt.ItemDataRole.UserRole)
            )
        else:
            self._ui.sub_type_description.setText(NO_SELECTION_TEXT)

    @QtCore.Slot()
    def typeSelected(self, row: int) -> None:
        self._ui.sub_type_wrapper.hide()
        self._ui.sub_type_description.setText(NO_SELECTION_TEXT)
        if row >= 0 and row < self._ui.type_view.count():
            self._ui.type_description.setText(
                self._ui.type_view.item(row).data(QtCore.Qt.ItemDataRole.UserRole)
            )
            text = self._ui.type_view.item(row).text()
            if text in self._sub_type_dict:
                self._ui.sub_type_view.selectionModel().clearSelection()
                self._ui.sub_type_view.clear()
                for k, v in self._sub_type_dict[text].items():
                    item = QtWidgets.QListWidgetItem(k)
                    item.setData(QtCore.Qt.ItemDataRole.UserRole, v)
                    self._ui.sub_type_view.addItem(item)
                self._ui.sub_type_wrapper.show()

        else:
            self._ui.type_description.setText(NO_SELECTION_TEXT)

    def validate(self) -> typing.Dict[QtWidgets.QWidget | str, ItemValidity]:
        return {
            self._ui.type_view: ItemValidity.getEnum(
                self._ui.type_view.currentRow() != -1
            ),
            self._ui.sub_type_view: ItemValidity.getEnum(
                self._ui.type_view.currentRow() == -1
                or self._ui.type_view.currentItem().text() not in self._sub_type_dict
                or self._ui.sub_type_view.currentRow() != -1
            ),
            self._ui.name_edit: ItemValidity.getEnum(
                self.validateText(self._ui.name_edit.text())
            ),
        }

    def save(self) -> None:
        """Set the name as a new dict with the type"""
        new_type = self._ui.type_view.currentItem().text()
        new_sub_type = None
        if new_type in self._sub_type_dict:
            new_sub_type = self._ui.sub_type_view.currentItem().text()
        if new_type != self.getConfig().type_ or (
            new_sub_type is not None and new_sub_type != self.getConfig().sub_type
        ):
            self.getConfig().clear()
        self.getConfig().name = self._ui.name_edit.text().strip()
        self.getConfig().type_ = new_type
        if new_sub_type is not None:
            self.getConfig().sub_type = new_sub_type

    def reset(self) -> None:
        self._ui.type_view.selectionModel().clearSelection()
        self._ui.sub_type_wrapper.hide()
        self._ui.sub_type_view.selectionModel().clearSelection()
        self._ui.sub_type_view.clear()
        self._ui.name_edit.setText("")

    def loadPage(self) -> None:
        items = self._ui.type_view.findItems(
            self.getConfig().type_, QtCore.Qt.MatchFlag.MatchExactly
        )
        if items:
            self._ui.type_view.setCurrentItem(items[0])
            if self._ui.type_view.currentItem().text() in self._sub_type_dict:
                items = self._ui.sub_type_view.findItems(
                    self.getConfig().sub_type, QtCore.Qt.MatchFlag.MatchExactly
                )
                if items:
                    self._ui.sub_type_view.setCurrentItem(items[0])
        self._ui.name_edit.setText(self.getConfig().name)
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
        #    Only necessary if the function would normally be used in a multithreaded environment.
        #    """,
        DataSourcesTypeEnum.INPUT.display: """
    Take user input data as the source of the data. \n
    When this option is used, after the program is created, a window can be opened that has the selected input option for inputting user data. \n
    Useful for if you need to tell the program dynamically your own data.
    """,
    }
    PAGE_KEY = PageKeys.DATA_SOURCE_TYPE

    TUTORIAL_RESOURCE_PREFIX = "CreateTypeDataSource"

    def __init__(
        self,
        current_config: ItemSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(
            current_config,
            self.TYPE_DESCRIPTION,
            self.TUTORIAL_RESOURCE_PREFIX,
            parent=parent,
        )

    @QtCore.Slot()
    def typeSelected(self, row: int) -> None:
        super().typeSelected(row)
        current_type = self._ui.type_view.item(row).text()
        if current_type == getattr(DataSourcesTypeEnum.INPUT, ENUM_DISPLAY, ""):
            self.setSkipPages.emit([PageKeys.PARAMETERS, PageKeys.SETTINGS])
        else:
            self.setSkipPages.emit([])


class CreateActionTypePage(CreateTypePage):
    PAGE_KEY = PageKeys.ACTION_TYPE

    TUTORIAL_RESOURCE_PREFIX = "CreateTypeAction"

    TYPE_DESCRIPTION = {
        ActionTypeEnum.TRIGGER.value: """Executes an output function based on the given conditions. \n
            Does not create new data and triggers will not expect functions called to return data.""",
        ActionTypeEnum.EVENT.value: """Takes the input data and generated new data based on the function.\n
            This function can either be loaded in from a library, generated by an AI or added in by hand.""",
        ActionTypeEnum.TEXT_MERGER.value: """Combines textual data from the dataset in a text editor.\n
            This is useful for sending the the text externally, such as to an AI or as an email.""",
        ActionTypeEnum.CALCULATOR.value: """Perform calculations using numbers from the data set.\n
            A standard calculator will be provided.""",
    }

    def __init__(
        self,
        current_config: ItemSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(
            current_config,
            self.TYPE_DESCRIPTION,
            self.TUTORIAL_RESOURCE_PREFIX,
            parent=parent,
        )

    @QtCore.Slot()
    def typeSelected(self, row: int) -> None:
        super().typeSelected(row)
        current_type = self._ui.type_view.item(row).text()
        if current_type == ActionTypeEnum.TRIGGER.value:
            self.setSkipPages.emit([PageKeys.SETTINGS])
        else:
            self.setSkipPages.emit([])
