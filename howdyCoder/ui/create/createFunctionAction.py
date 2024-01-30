from ...core.dataStructs import ActionSettings, InputSettings
from .createBasePage import ItemValidity
from ..qtUiFiles import ui_createFunctionAction
from ..tutorialOverlay import AbstractTutorialClass
from ..util import abstractQt
from .algoTopoView import SceneMode
from .algoTopoItem import VariableDragData


from ..selectorWidget import SelectorWidget
from ..funcSelector import FuncSelector, FunctionSettingsWithHelperData, addHelperData
from ..contextMenu import handleContextResult, ContextResultType
from ..util.spinBoxDelegate import SpinBoxDelegate
from ..util import qtUtil
from ..util.qtUtil import WordWrapHeader

from ...core.commonGlobals import (
    ENUM_DISPLAY,
    ActionTypeEnum,
    ActionDataType,
)

from aenum import Enum
import typing

from PySide6 import QtWidgets, QtGui, QtCore

SELECTED_SOURCE_COLUMN = 0
SELECTED_NAME_COLUMN = 1
SELECTED_REQUIRES_NEW_COLUMN = 2
SELECTED_AMOUNT_OF_DATA_COLUMN = 3


class FuncType(Enum):
    CALC = 0
    OUTPUT = 1


class CreateFunctionAction(
    AbstractTutorialClass,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstactQtResolver(QtWidgets.QWidget, AbstractTutorialClass),
):
    TUTORIAL_RESOURCE_PREFIX_TRIGGER = "CreateSettingsTrigger"
    TUTORIAL_RESOURCE_PREFIX_EVENT = "CreateSettingsEvent"

    def __init__(self, *args, **kwargs):
        super().__init__(self.TUTORIAL_RESOURCE_PREFIX_EVENT, *args, **kwargs)
        self._ui = ui_createFunctionAction.Ui_CreateFunctionAction()
        self._ui.setupUi(self)
        self._action_type = None
        self._current_calc_settings: FunctionSettingsWithHelperData = None
        self._current_output_settings: FunctionSettingsWithHelperData = None
        self._selected_input_table_model = QtGui.QStandardItemModel()
        self._selected_input_table_model.setHorizontalHeaderLabels(
            ["Source", "Name", "Requires New", "Amount of Data"]
        )
        self._ui.selected_table_view.setModel(self._selected_input_table_model)
        self._ui.selected_table_view.installEventFilter(self)
        self._ui.selected_table_view.setHorizontalHeader(
            WordWrapHeader(
                QtCore.Qt.Orientation.Horizontal, self._ui.selected_table_view
            )
        )
        self._selected_input_table_model.itemChanged.connect(
            self.selectedTableModelItemChanged
        )
        self._ui.selected_table_view.setItemDelegateForColumn(
            SELECTED_AMOUNT_OF_DATA_COLUMN,
            SpinBoxDelegate(
                -1,
                99999,
                disallowed_values=[0],
                disallowed_default_value=1,
                parent=self._ui.selected_table_view,
            ),
        )
        self._ui.selected_table_view.setItemDelegateForColumn(
            SELECTED_NAME_COLUMN, qtUtil.CompleterDelegate(self._ui.selected_table_view)
        )
        self._ui.removeButton.released.connect(self.removeSelected)
        self._curr_selected = set()

        self._func_selector = FuncSelector()
        self._calc_selector_widget = SelectorWidget(
            FuncType.CALC,
            self._func_selector,
            self._ui.calcFuncWidget,
            default_prompt="Event",
        )
        self._ui.calcFuncWidget.layout().addWidget(self._calc_selector_widget)
        self._output_selector_widget = SelectorWidget(
            FuncType.OUTPUT,
            self._func_selector,
            self._ui.outputFuncWidget,
            default_prompt="Trigger Output",
        )
        self._ui.outputFuncWidget.layout().addWidget(self._output_selector_widget)
        self._func_selector.itemSelected.connect(self.onFuncSelected)

        self._ui.select_button.released.connect(self.selectButton)

        for e in ActionDataType:
            self._ui.dataTypeCombo.addItem(getattr(e, ENUM_DISPLAY), e)
        self._ui.dataTypeCombo.setCurrentIndex(-1)
        # TODO add back in input data type
        self._ui.data_type_box.hide()

        # true base page will override
        self.parent_page = None

        self._ui.graphics_view.scale(0.75, 0.75)

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent):
        if watched == self._ui.selected_table_view:
            if event.type() == QtCore.QEvent.Type.DragEnter:
                event.acceptProposedAction()
                return True
            if event.type() == QtCore.QEvent.Type.Drop:
                if isinstance(event.mimeData(), VariableDragData):
                    self.availableSelected(event.mimeData().text())
                    return True
        return super().eventFilter(watched, event)

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
        name_column_widths = (
            self._ui.selected_table_view.width()
            - self._ui.selected_table_view.horizontalHeader().minimumSectionSize() * 2
        ) // 2
        self._ui.selected_table_view.setColumnWidth(
            SELECTED_SOURCE_COLUMN,
            name_column_widths,
        )
        self._ui.selected_table_view.setColumnWidth(
            SELECTED_NAME_COLUMN,
            name_column_widths,
        )
        self._ui.selected_table_view.setColumnWidth(
            SELECTED_AMOUNT_OF_DATA_COLUMN,
            self._ui.selected_table_view.horizontalHeader().minimumSectionSize(),
        )
        self._ui.selected_table_view.setColumnWidth(
            SELECTED_REQUIRES_NEW_COLUMN,
            self._ui.selected_table_view.horizontalHeader().minimumSectionSize(),
        )

        return super().resizeEvent(event)

    @QtCore.Slot()
    def onFuncSelected(self, settings: FunctionSettingsWithHelperData):
        """
        The func selector has returned a value, check which button triggered it, and
        based on that update the correct setting variable and the text
        """
        if settings.index:
            if settings.index == FuncType.CALC:
                self._calc_selector_widget.updateText(settings.function_settings.name)
                self._calc_selector_widget.updateExtraDescription(
                    settings.function_settings.code
                )
                self._calc_selector_widget.data = settings.function_settings
                self._current_calc_settings = settings
            elif settings.index == FuncType.OUTPUT:
                self._output_selector_widget.updateText(settings.function_settings.name)
                self._output_selector_widget.updateExtraDescription(
                    settings.function_settings.code
                )
                self._output_selector_widget.data = settings.function_settings
                self._current_output_settings = settings
        self.updateDataSetSuggestions()

    def loadPage(self) -> None:
        curr_settings: ActionSettings = self.parent_page.getConfig()
        self._ui.graphics_view.setScene(self.parent_page.scene)
        self.parent_page.scene.setMode(SceneMode.ACTION, self.parent_page.editing_name)
        self.parent_page.scene.signal_controller.contextResult.connect(
            lambda res: handleContextResult(self, res, self.CONTEXT_RESULT_FUNCTIONS),
            QtCore.Qt.ConnectionType.UniqueConnection,
        )
        if curr_settings.type_:
            enum_type = ActionTypeEnum(curr_settings.type_)
            if self._action_type is not None and self._action_type != enum_type:
                self.reset()
            else:
                self._action_type = enum_type
                if curr_settings.calc_function is not None:
                    with_helper = addHelperData(curr_settings.calc_function)
                    with_helper.index = FuncType.CALC
                    self.onFuncSelected(with_helper)
                if (
                    curr_settings.output_function is not None
                    and enum_type == ActionTypeEnum.TRIGGER
                ):
                    with_helper = addHelperData(curr_settings.output_function)
                    with_helper.index = FuncType.OUTPUT
                    self.onFuncSelected(with_helper)
            self._calc_selector_widget.default_prompt = (
                "Event"
                if self._action_type == ActionTypeEnum.EVENT
                else "Trigger Calculation"
            )
            if self._action_type == ActionTypeEnum.EVENT:
                self.resource_prefix = self.TUTORIAL_RESOURCE_PREFIX_EVENT
                self._ui.triggerWidget.setHidden(True)
            elif self._action_type == ActionTypeEnum.TRIGGER:
                self.resource_prefix = self.TUTORIAL_RESOURCE_PREFIX_TRIGGER
                self._ui.triggerWidget.setHidden(False)
            self.updateDataSetSuggestions()

        self.checkSelectedInSettings(curr_settings)

    def availableSelected(
        self,
        name: str,
        rename: str | None = None,
        requires_new: bool = False,
        amount_of_data: int = 1,
    ):
        """User has clicked available table so we add it to the selected model for display"""

        if name not in self._curr_selected:
            self._curr_selected.add(name)
            source_item = QtGui.QStandardItem(name)
            name_item = QtGui.QStandardItem(name if rename is None else rename)
            requires_new_item = QtGui.QStandardItem()
            requires_new_item.setCheckable(True)
            requires_new_item.setCheckState(
                QtCore.Qt.CheckState.Checked
                if requires_new
                else QtCore.Qt.CheckState.Unchecked
            )
            source_item.setEditable(False)
            name_item.setEditable(True)
            amount_item = QtGui.QStandardItem(amount_of_data)
            amount_item.setData(amount_of_data, QtCore.Qt.ItemDataRole.EditRole)
            self._selected_input_table_model.appendRow(
                [
                    source_item,
                    name_item,
                    requires_new_item,
                    amount_item,
                ]
            )
            self._ui.selected_table_view.openPersistentEditor(
                self._selected_input_table_model.index(
                    self._selected_input_table_model.rowCount() - 1,
                    SELECTED_AMOUNT_OF_DATA_COLUMN,
                )
            )
            self.updateDataSetSuggestions()

    def checkSelectedInSettings(self, curr_settings: ActionSettings):
        for name in curr_settings.input_:
            self.availableSelected(
                name,
                rename=curr_settings.input_[name].name,
                requires_new=curr_settings.input_[name].requires_new,
                amount_of_data=curr_settings.input_[name].period,
            )

    def validate(self) -> typing.Dict[QtWidgets.QWidget | str, ItemValidity]:
        return {
            self._ui.selected_table_view: ItemValidity.getEnum(
                self._selected_input_table_model.rowCount() > 0
            ),
            self._ui.calcFuncWidget: ItemValidity.getEnum(
                self._current_calc_settings is not None
            ),
            self._ui.outputFuncWidget: ItemValidity.getEnum(
                self._action_type == ActionTypeEnum.EVENT
                or self._current_output_settings is not None
            ),
            "Some suggested data set have not been assigned.": self.parent_page.suggested_validity,
        }
        # TODO add back in input data type
        # and self._ui.dataTypeCombo.currentIndex() >= 0

    def reset(self) -> None:
        self._curr_selected = set()
        self._current_calc_settings = None
        self._current_output_settings = None
        self._calc_selector_widget.resetText()
        self._output_selector_widget.resetText()
        self._selected_input_table_model.removeRows(
            0, self._selected_input_table_model.rowCount()
        )
        self._action_type = None
        self._ui.dataTypeCombo.setCurrentIndex(-1)

    def removeSelected(self):
        """Remove from the selected table and recheck if next should be enabled"""
        selection = self._ui.selected_table_view.selectionModel().selectedIndexes()
        if len(selection) == 1:
            """we're discarding the full name, so the source"""
            self._curr_selected.discard(
                selection[0].siblingAtColumn(SELECTED_SOURCE_COLUMN).data()
            )
            self._selected_input_table_model.removeRow(selection[0].row())
            self.updateDataSetSuggestions()

    def save(self) -> None:
        action_settings: ActionSettings = self.parent_page.getConfig()
        action_settings.calc_function = self._current_calc_settings.function_settings
        if self._action_type == ActionTypeEnum.TRIGGER:
            action_settings.output_function = (
                self._current_output_settings.function_settings
            )
        action_settings.input_data_type = getattr(
            ActionDataType.DICTIONARY_OF_LISTS, ENUM_DISPLAY
        )
        # TODO add back in input data type
        # action_settings.input_data_type = self._ui.dataTypeCombo.currentText()
        self.parent_page.getHelperData().suggested_parameters = (
            self._current_calc_settings.suggested_parameters[::]
            + (
                self._current_output_settings.suggested_parameters[::]
                if self._current_output_settings
                else []
            )
        )
        # get from data, because if it's an event we don't want to get the "Event" tag before it
        # this has been stored in the data when the selected table was populated
        action_settings.input_.clear()
        for row in range(self._selected_input_table_model.rowCount()):
            input_settings = InputSettings()
            input_settings.name = self._selected_input_table_model.item(
                row, SELECTED_NAME_COLUMN
            ).data(QtCore.Qt.DisplayRole)
            input_settings.requires_new = (
                self._selected_input_table_model.item(
                    row, SELECTED_REQUIRES_NEW_COLUMN
                ).checkState()
                == QtCore.Qt.CheckState.Checked
            )
            input_settings.period = self._selected_input_table_model.item(
                row, SELECTED_AMOUNT_OF_DATA_COLUMN
            ).data(QtCore.Qt.ItemDataRole.EditRole)
            input_settings.period = (
                1 if not input_settings.period else input_settings.period
            )
            source = self._selected_input_table_model.item(
                row, SELECTED_SOURCE_COLUMN
            ).data(QtCore.Qt.ItemDataRole.DisplayRole)
            action_settings.input_[source] = input_settings
        self._ui.graphics_view.setScene(QtWidgets.QGraphicsScene())

    def getTutorialClasses(self) -> typing.List:
        return [self]

    def selectedTableModelItemChanged(self, item: QtGui.QStandardItem):
        """A period of 0 doesn't make sense, but we are allowing -1, since that means ALL"""
        if (
            item.index().column() == SELECTED_AMOUNT_OF_DATA_COLUMN
            and item.data(QtCore.Qt.ItemDataRole.EditRole) == 0
        ):
            item.setData(1, QtCore.Qt.ItemDataRole.EditRole)
        if item.index().column() == SELECTED_NAME_COLUMN:
            self.updateDataSetSuggestions()

    def updateDataSetSuggestions(self):
        current = set()
        for row in range(self._selected_input_table_model.rowCount()):
            current.add(
                self._selected_input_table_model.item(row, SELECTED_NAME_COLUMN).data(
                    QtCore.Qt.ItemDataRole.DisplayRole
                )
            )
        suggested = []
        if self._current_calc_settings is not None:
            suggested += self._current_calc_settings.suggested_data
        if (
            self._current_output_settings is not None
            and self._action_type == ActionTypeEnum.TRIGGER
        ):
            suggested += self._current_output_settings.suggested_data

        self.parent_page.addToSuggestedListWidget(
            self._ui.suggested_data_set, current, suggested
        )
        self._ui.selected_table_view.itemDelegateForColumn(
            SELECTED_NAME_COLUMN
        ).setCompleterStrings(suggested)

    @QtCore.Slot()
    def selectButton(self):
        self.availableSelected(self.parent_page.scene.current_selected_item)

    CONTEXT_RESULT_FUNCTIONS = {ContextResultType.SELECT: availableSelected}
