from ...core.dataStructs import ActionSettings, AlgoSettings, InputSettings
from .createBasePage import CreateBasePage, ItemValidity
from ..uiConstants import PageKeys
from ..qtUiFiles import ui_createActionSettingsPage

from .. import highlightModel
from ..selectorWidget import SelectorWidget
from ..funcSelector import FuncSelector, FunctionSettingsWithHelperData, addHelperData

from ..util.spinBoxDelegate import SpinBoxDelegate
from ..util import qtResourceManager

from ...commonUtil import helpers
from ...core.commonGlobals import (
    ENUM_DISPLAY,
    ActionTypeEnum,
    DATA_SOURCES,
    ACTION_LIST,
    ActionDataType,
)

from aenum import Enum
import typing

from PySide6 import QtWidgets, QtGui, QtCore

AVAILABLE_GROUP_COLUMN = 0
AVAILABLE_NAME_COLUMN = 1
AVAILABLE_SOURCE_COLUMN = 2

SELECTED_SOURCE_COLUMN = 0
SELECTED_NAME_COLUMN = 1
SELECTED_REQUIRES_NEW_COLUMN = 2
SELECTED_AMOUNT_OF_DATA_COLUMN = 3

SELECTED_TRUE_NAME_ROLE = QtCore.Qt.UserRole + 1


class FuncType(Enum):
    CALC = 0
    OUTPUT = 1


def getTrueName(group, name):
    return (
        f"{group}-{name}"
        if group != getattr(ActionTypeEnum.EVENT, ENUM_DISPLAY).capitalize()
        else name
    )


class CreateActionSettingsPage(CreateBasePage):
    PAGE_KEY = PageKeys.ACTION_SETTINGS
    TUTORIAL_RESOURCE_PREFIX_TRIGGER = "CreateSettingsTrigger"
    TUTORIAL_RESOURCE_PREFIX_EVENT = "CreateSettingsEvent"
    GROUP = ACTION_LIST

    def __init__(
        self,
        current_config: AlgoSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(
            current_config, self.TUTORIAL_RESOURCE_PREFIX_EVENT, parent=parent
        )

        self._ui = ui_createActionSettingsPage.Ui_CreateActionSettingsPage()
        self._ui.setupUi(self)
        self._action_type = None
        self._current_calc_settings: FunctionSettingsWithHelperData = None
        self._current_output_settings: FunctionSettingsWithHelperData = None
        self._selected_input_table_model = QtGui.QStandardItemModel()
        self._selected_input_table_model.setHorizontalHeaderLabels(
            ["Source", "Name", "Requires New", "Amount of Data"]
        )
        self._available_input_table_model = highlightModel.HighlightTableModel()
        self._available_input_table_model.setHorizontalHeaderLabels(
            ["Group", "Name", "Source"]
        )
        self._ui.selectedInputTable.setModel(self._selected_input_table_model)
        self._ui.selectedInputTable.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        self._selected_input_table_model.itemChanged.connect(
            self.selectedTableModelItemChanged
        )
        self._ui.selectedInputTable.setItemDelegateForColumn(
            SELECTED_AMOUNT_OF_DATA_COLUMN,
            SpinBoxDelegate(
                -1,
                99999,
                disallowed_values=[0],
                disallowed_default_value=1,
                parent=self._ui.selectedInputTable,
            ),
        )
        self._ui.availableInputTable.setModel(self._available_input_table_model)
        self._ui.availableInputTable.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        self._ui.availableInputTable.setMouseTracking(True)

        self._ui.availableInputTable.clicked.connect(self.availableSelected)
        self._ui.availableInputTable.entered.connect(
            self._available_input_table_model.changeTextColor
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

        for e in ActionDataType:
            self._ui.dataTypeCombo.addItem(getattr(e, ENUM_DISPLAY), e)
        self._ui.dataTypeCombo.setCurrentIndex(-1)
        # TODO add back in input data type
        self._ui.data_type_box.hide()

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
        super().loadPage()
        curr_settings: ActionSettings = self.getTempConfig()
        if curr_settings.type_:
            enum_type = helpers.findEnumByAttribute(
                ActionTypeEnum, ENUM_DISPLAY, curr_settings.type_
            )
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

        self.loadAvailableInputTable()
        self.checkSelectedInSettings(curr_settings)

    def loadAvailableInputTable(self):
        """
        the potential input can be both data source and actions
        data sources can have multiple data ouputs each
        while events are single output (for now?)
        """
        cur_row = 0
        for k, v in self.getConfig().getGroupDict(DATA_SOURCES).items():
            ds_group = QtGui.QStandardItem(f"{k}")
            self._available_input_table_model.setItem(
                cur_row, AVAILABLE_GROUP_COLUMN, ds_group
            )
            # output could be a list or dict, if dict we want keys
            output = []
            try:
                output = list(v.output.values())
            except AttributeError:
                output = v.output
            n = self._available_input_table_model.rowCount()
            for x in range(len(output)):
                if x != 0:
                    item = QtGui.QStandardItem()
                    item.setData(
                        (n - 1, AVAILABLE_GROUP_COLUMN), highlightModel.HIGHLIGHT_ROLE
                    )
                    self._available_input_table_model.setItem(
                        n - 1 + x, AVAILABLE_GROUP_COLUMN, item
                    )
                self._available_input_table_model.setItem(
                    n - 1 + x, AVAILABLE_NAME_COLUMN, QtGui.QStandardItem(output[x])
                )
                self._available_input_table_model.setItem(
                    n - 1 + x, AVAILABLE_SOURCE_COLUMN, QtGui.QStandardItem(v.type_)
                )
            if len(output) > 1:
                self._ui.availableInputTable.setSpan(
                    cur_row, AVAILABLE_GROUP_COLUMN, len(output), 1
                )
            cur_row += len(output)
        for k, v in self.getConfig().getGroupDict(ACTION_LIST).items():
            if v.type_ == getattr(ActionTypeEnum.EVENT, ENUM_DISPLAY):
                self._available_input_table_model.appendRow(
                    [
                        QtGui.QStandardItem(
                            getattr(ActionTypeEnum.EVENT, ENUM_DISPLAY).capitalize()
                        ),
                        QtGui.QStandardItem(k),
                        QtGui.QStandardItem(", ".join(v.input_.keys())),
                    ]
                )

    def availableSelected(
        self,
        index: QtCore.QModelIndex,
        rename: str | None = None,
        requires_new: bool = False,
        amount_of_data: int = 1,
    ):
        """User has clicked available table so we add it to the selected model for display"""
        if (
            index is not None
            and index.isValid()
            and index.column() != AVAILABLE_GROUP_COLUMN
            and index.siblingAtColumn(AVAILABLE_NAME_COLUMN).isValid()
        ):
            name = self._available_input_table_model.data(
                index.siblingAtColumn(AVAILABLE_NAME_COLUMN)
            )
            avail_group_col_index = index.siblingAtColumn(AVAILABLE_GROUP_COLUMN)
            """The group name is only populated into the first of each group, so iter up until we get it"""
            while (
                avail_group_col_index.isValid()
                and self._available_input_table_model.data(avail_group_col_index)
                is None
            ):
                avail_group_col_index = avail_group_col_index.siblingAtRow(
                    avail_group_col_index.row() - 1
                )
            group = self._available_input_table_model.data(avail_group_col_index)

            display_name = f"{group}-{name}"
            if display_name not in self._curr_selected:
                self._curr_selected.add(display_name)
                true_name = (
                    f"{group}-{name}"
                    if group != getattr(ActionTypeEnum.EVENT, ENUM_DISPLAY).capitalize()
                    else name
                )
                source_item = QtGui.QStandardItem(display_name)
                source_item.setData(true_name, SELECTED_TRUE_NAME_ROLE)
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
                self._selected_input_table_model.appendRow(
                    [
                        source_item,
                        name_item,
                        requires_new_item,
                        QtGui.QStandardItem(amount_of_data),
                    ]
                )
                self._ui.selectedInputTable.openPersistentEditor(
                    self._selected_input_table_model.index(
                        self._selected_input_table_model.rowCount() - 1,
                        SELECTED_AMOUNT_OF_DATA_COLUMN,
                    )
                )
                self.updateDataSetSuggestions()

    def checkSelectedInSettings(self, curr_settings: ActionSettings):
        cur_group = ""
        for row in range(self._available_input_table_model.rowCount()):
            index = self._available_input_table_model.index(row, AVAILABLE_NAME_COLUMN)
            group_index = index.siblingAtColumn(AVAILABLE_GROUP_COLUMN)
            if (
                group_index.isValid()
                and group_index.data(QtCore.Qt.ItemDataRole.DisplayRole) is not None
            ):
                cur_group = group_index.data(QtCore.Qt.ItemDataRole.DisplayRole)
            name = getTrueName(
                cur_group, index.data(QtCore.Qt.ItemDataRole.DisplayRole)
            )
            if name in curr_settings.input_:
                self.availableSelected(
                    index,
                    rename=curr_settings.input_[name].name,
                    requires_new=curr_settings.input_[name].requires_new,
                    amount_of_data=curr_settings.input_[name].period,
                )

    def validate(self) -> typing.Dict[QtWidgets.QWidget | str, ItemValidity]:
        return {
            self._ui.selectedInputTable: ItemValidity.getEnum(
                self._selected_input_table_model.rowCount() > 0
            ),
            self._ui.calcFuncWidget: ItemValidity.getEnum(
                self._current_calc_settings is not None
            ),
            self._ui.outputFuncWidget: ItemValidity.getEnum(
                self._action_type == ActionTypeEnum.EVENT
                or self._current_output_settings is not None
            ),
            "Some suggested data set have not been assigned.": self.suggested_validity,
        }
        # TODO add back in input data type
        # and self._ui.dataTypeCombo.currentIndex() >= 0

    def reset(self) -> None:
        self._curr_selected = set()
        self._current_calc_settings = None
        self._current_output_settings = None
        self._calc_selector_widget.resetText()
        self._output_selector_widget.resetText()
        self._available_input_table_model.removeRows(
            0, self._available_input_table_model.rowCount()
        )
        self._selected_input_table_model.removeRows(
            0, self._selected_input_table_model.rowCount()
        )
        self._ui.availableInputTable.clearSpans()
        self._action_type = None
        self._ui.dataTypeCombo.setCurrentIndex(-1)

    def removeSelected(self):
        """Remove from the selected table and recheck if next should be enabled"""
        selection = self._ui.selectedInputTable.selectionModel().selectedIndexes()
        if len(selection) == 1:
            """we're discarding the full name, so the source"""
            self._curr_selected.discard(
                selection[0].siblingAtColumn(SELECTED_SOURCE_COLUMN).data()
            )
            self._selected_input_table_model.removeRow(selection[0].row())
            self.updateDataSetSuggestions()

    def save(self) -> None:
        action_settings: ActionSettings = self.getTempConfig()
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
        self.getHelperData().suggested_parameters = (
            self._current_calc_settings.suggested_parameters[::]
            + (
                self._current_output_settings.suggested_parameters[::]
                if self._current_output_settings
                else []
            )
        )
        # get from data, because if it's an event we don't want to get the "Event" tag before it
        # this has been stored in the data when the selected table was populated
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
            ).data(SELECTED_TRUE_NAME_ROLE)
            action_settings.input_[source] = input_settings

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

        self.addToSuggestedListWidget(self._ui.suggested_data_set, current, suggested)
