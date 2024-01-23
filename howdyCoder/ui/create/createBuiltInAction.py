from typing import Optional
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QWidget
from .createBasePage import ItemValidity, CreateBasePage

from ..tutorialOverlay import AbstractTutorialClass
from ..util import abstractQt
from ..uiConstants import SceneMode
from ..qtUiFiles import ui_createBuiltInAction

from ...core.dataStructs import ActionSettings, InputSettings
from ...core import librarySingleton

from ...libraries.textMerger import VARIABLE_TEXT_LIST_ARG_NAME

import typing
from collections import Counter

from PySide6 import QtWidgets, QtCore, QtGui

SELECTED_NAME_COLUMN = 0
SELECTED_REQUIRES_NEW_COLUMN = 1


class WordWrapHeader(QtWidgets.QHeaderView):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setDefaultAlignment(
            QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.TextFlag.TextWordWrap
        )

    def sectionSizeFromContents(self, logicalIndex: int) -> QSize:
        text = self.model().headerData(
            logicalIndex, self.orientation(), QtCore.Qt.ItemDataRole.DisplayRole
        )
        fM = self.fontMetrics()
        rect = fM.boundingRect(
            QtCore.QRect(0, 0, self.sectionSize(logicalIndex), 5000),
            self.defaultAlignment(),
            text,
        )
        buffer = QtCore.QSize(2, 25)
        together = rect.size() + buffer
        return together


class CreateBuiltInAction(
    AbstractTutorialClass,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstactQtResolver(QtWidgets.QWidget, AbstractTutorialClass),
):
    def __init__(self, *args, **kwargs):
        super().__init__("None", *args, **kwargs)
        self._ui = ui_createBuiltInAction.Ui_CreateBuiltInAction()
        self._ui.setupUi(self)
        self.parent_page: CreateBasePage = None

        self._selected_counter = Counter()
        self._selected_input_table_model = QtGui.QStandardItemModel()
        self._ui.selected_table_view.setHorizontalHeader(
            WordWrapHeader(
                QtCore.Qt.Orientation.Horizontal, self._ui.selected_table_view
            )
        )

        self._selected_input_table_model.setHorizontalHeaderLabels(
            ["Source", "Requires New"]
        )
        self._ui.selected_table_view.setModel(self._selected_input_table_model)

        self._ui.drag_edit.insertedBlock.connect(self.insertedBlock)
        self._ui.drag_edit.removedBlocks.connect(self.removedBlock)

    def resizeEvent(self, event: QResizeEvent) -> None:
        size = (
            self._ui.selected_table_view.horizontalHeader()
            .fontMetrics()
            .boundingRect(
                QtCore.QRect(0, 0, 2000, 5000),
                self._ui.selected_table_view.horizontalHeader().defaultAlignment(),
                "Requires New",
            )
        ).size() + QtCore.QSize(40, 25)
        self._ui.selected_table_view.horizontalHeader().setMinimumSectionSize(
            size.width()
        )
        self._ui.selected_table_view.setColumnWidth(
            0,
            self._ui.selected_table_view.width()
            - self._ui.selected_table_view.horizontalHeader().minimumSectionSize(),
        )
        self._ui.selected_table_view.setColumnWidth(
            1,
            self._ui.selected_table_view.horizontalHeader().minimumSectionSize(),
        )

        return super().resizeEvent(event)

    def loadPage(self) -> None:
        curr_settings: ActionSettings = self.parent_page.getConfig()
        self._ui.graphics_view.setScene(self.parent_page.scene)
        self.parent_page.scene.setMode(SceneMode.ACTION, self.parent_page.editing_name)
        if (
            curr_settings.calc_function
            and VARIABLE_TEXT_LIST_ARG_NAME
            in curr_settings.calc_function.internal_parameters
        ):
            self._ui.drag_edit.setTextFromList(
                curr_settings.calc_function.internal_parameters[
                    VARIABLE_TEXT_LIST_ARG_NAME
                ],
                self.parent_page.scene.current_items,
            )

    def validate(self) -> typing.Dict[QtWidgets.QWidget | str, ItemValidity]:
        return {
            self._ui.drag_edit: ItemValidity.getEnum(self._ui.drag_edit.toPlainText()),
            self._ui.data_set_box: ItemValidity.getEnum(
                self._selected_input_table_model.rowCount() > 0
            ),
        }

    def reset(self) -> None:
        self._selected_input_table_model.removeRows(
            0, self._selected_input_table_model.rowCount()
        )
        self._selected_counter = Counter()
        self._ui.drag_edit.clear()

    def save(self) -> None:
        curr_settings: ActionSettings = self.parent_page.getConfig()
        curr_settings.calc_function = librarySingleton.getInternalLibrary().functions[0]
        curr_settings.calc_function.internal_parameters[
            VARIABLE_TEXT_LIST_ARG_NAME
        ] = self._ui.drag_edit.getVariableText()
        for row in range(self._selected_input_table_model.rowCount()):
            input_settings = InputSettings()
            input_settings.name = self._selected_input_table_model.item(
                row, SELECTED_NAME_COLUMN
            ).text()
            input_settings.requires_new = (
                self._selected_input_table_model.item(
                    row, SELECTED_REQUIRES_NEW_COLUMN
                ).checkState()
                == QtCore.Qt.CheckState.Checked
            )
            curr_settings.input_[input_settings.name] = input_settings
        self._ui.graphics_view.setScene(QtWidgets.QGraphicsScene())

    def getTutorialClasses(self) -> typing.List:
        return [self]

    def addToSelectedTable(self, text: str, requires_new: bool = False):
        source = QtGui.QStandardItem(text)
        requires_new_item = QtGui.QStandardItem()
        requires_new_item.setCheckable(True)
        requires_new_item.setCheckState(
            QtCore.Qt.CheckState.Checked
            if requires_new
            else QtCore.Qt.CheckState.Unchecked
        )
        self._selected_input_table_model.appendRow([source, requires_new_item])

    def removeFromSelectedTable(self, text: str):
        items = self._selected_input_table_model.findItems(text)
        for item in items:
            self._selected_input_table_model.removeRow(item.row())

    @QtCore.Slot()
    def insertedBlock(self, text: str) -> None:
        if self._selected_counter[text] == 0:
            self.addToSelectedTable(text)
        self._selected_counter[text] += 1

    @QtCore.Slot()
    def removedBlock(self, text: str) -> None:
        if self._selected_counter[text] == 1:
            self.removeFromSelectedTable(text)
        self._selected_counter[text] -= 1
