from .createBasePage import ItemValidity, CreateBasePage

from ..tutorialOverlay import AbstractTutorialClass
from ..util import abstractQt
from ..util.qtUtil import WordWrapHeader
from ..uiConstants import SceneMode
from ..contextMenu import ContextResultType, handleContextResult
from ..qtUiFiles import ui_createBuiltInAction

from ...core.dataStructs import ActionSettings, InputSettings
from ...core import librarySingleton

from ...libraries.textMerger import VARIABLE_TEXT_LIST_ARG_NAME

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
        self._ui.selected_table_view.setHorizontalHeader(
            WordWrapHeader(
                QtCore.Qt.Orientation.Horizontal, self._ui.selected_table_view
            )
        )

        self._selected_input_table_model.setHorizontalHeaderLabels(
            ["Source", "Requires New"]
        )
        self._ui.selected_table_view.setModel(self._selected_input_table_model)

        self._ui.variable_edit.insertedBlock.connect(self.insertedBlock)
        self._ui.variable_edit.removedBlocks.connect(self.removedBlock)

        self._ui.select_button.released.connect(self.selectButton)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
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
            and not self._ui.variable_edit.getVariableText()
        ):
            self._ui.variable_edit.setTextFromList(
                curr_settings.calc_function.internal_parameters[
                    VARIABLE_TEXT_LIST_ARG_NAME
                ],
                self.parent_page.scene.current_items,
            )
        self.parent_page.scene.signal_controller.contextResult.connect(
            lambda res: handleContextResult(self, res, self.CONTEXT_RESULT_FUNCTIONS),
            QtCore.Qt.ConnectionType.UniqueConnection,
        )

    def validate(self) -> typing.Dict[QtWidgets.QWidget | str, ItemValidity]:
        return {
            self._ui.variable_edit: ItemValidity.getEnum(
                self._ui.variable_edit.toPlainText()
            ),
            self._ui.data_set_box: ItemValidity.getEnum(
                self._selected_input_table_model.rowCount() > 0
            ),
        }

    def reset(self) -> None:
        self._selected_input_table_model.removeRows(
            0, self._selected_input_table_model.rowCount()
        )
        self._selected_counter = Counter()
        self._ui.variable_edit.clear()

    def save(self) -> None:
        curr_settings: ActionSettings = self.parent_page.getConfig()
        # to be changed when there are more than one built in, ie Calculator
        curr_settings.calc_function = librarySingleton.getInternalLibrary().functions[
            "Text Merger"
        ]
        curr_settings.calc_function.internal_parameters[VARIABLE_TEXT_LIST_ARG_NAME] = (
            self._ui.variable_edit.getVariableText()
        )
        curr_settings.input_.clear()
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

    def addVariable(self, name: str):
        if name:
            self._ui.variable_edit.insertTextBlock(name)

    @QtCore.Slot()
    def selectButton(self):
        self.addVariable(self.parent_page.scene.current_selected_item)

    CONTEXT_RESULT_FUNCTIONS = {ContextResultType.SELECT: addVariable}
