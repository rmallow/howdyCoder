from .createBasePage import ItemValidity, CreateBasePage

from ..tutorialOverlay import AbstractTutorialClass
from ..util import abstractQt
from ..uiConstants import SceneMode
from ..qtUiFiles import ui_createBuiltInAction

from ...core.dataStructs import ActionSettings, InputSettings
from ...core import librarySingleton

from ...libraries.textMerger import VARIABLE_TEXT_LIST_ARG_NAME, isVarText

import typing
from collections import Counter

from PySide6 import QtWidgets, QtCore, QtGui

SELECTED_NAME_COLUMN = 0
SELECTED_REQUIRES_NEW_COLUMN = 1


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
        self._selected_input_table_model.setHorizontalHeaderLabels(
            ["Source", "Requires New"]
        )
        self._ui.selected_table_view.setModel(self._selected_input_table_model)

        self._ui.drag_edit.insertedBlock.connect(self.insertedBlock)
        self._ui.drag_edit.removedBlocks.connect(self.removedBlock)

    def loadPage(self) -> None:
        curr_settings: ActionSettings = self.parent_page.getConfig()
        self._ui.graphics_view.setScene(self.parent_page.scene)
        self.parent_page.scene.setMode(SceneMode.ACTION, curr_settings.name)
        if (
            curr_settings.calc_function
            and VARIABLE_TEXT_LIST_ARG_NAME
            in curr_settings.calc_function.internal_parameters
        ):
            for text in curr_settings.calc_function.internal_parameters[
                VARIABLE_TEXT_LIST_ARG_NAME
            ]:
                if (
                    isVarText(text)
                    and text[1:-1] in self.parent_page.scene.current_items
                    and self.parent_page.scene.current_items[text[1:-1]].isVisible()
                ):
                    self._ui.drag_edit.insertTextBlock(text[1:-1])
                else:
                    cursor = self._ui.drag_edit.textCursor()
                    cursor.movePosition(
                        QtGui.QTextCursor.MoveOperation.End,
                        QtGui.QTextCursor.MoveMode.MoveAnchor,
                    )
                    cursor.insertText(text)

    def validate(self) -> typing.Dict[QtWidgets.QWidget | str, ItemValidity]:
        return {
            self._ui.drag_edit: ItemValidity.getEnum(self._ui.drag_edit.toPlainText()),
            self._ui.data_set_box: ItemValidity.getEnum(
                self._selected_input_table_model.rowCount() > 0
            ),
        }

    def reset(self) -> None:
        self._selected_input_table_model.clear()
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
