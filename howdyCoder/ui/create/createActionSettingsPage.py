from .createBasePage import CreateBasePage
from ..uiConstants import PageKeys
from ..actionUIConstant import ActionFuncEnum, functionDictToFunctionSettings
from ..qtUiFiles import ui_createActionSettingsPage

from .. import highlightModel
from ..selectorWidget import SelectorWidget
from ..funcSelector import FuncSelector

from ..util.spinBoxDelegate import SpinBoxDelegate

from ...core.configConstants import (
    ActionTypeEnum,
    ActionDataType,
)

from ...commonUtil import helpers
from ...core.commonGlobals import (
    ENUM_DISPLAY,
    ActionSettings,
    InputSettings,
    AlgoSettings,
    DATA_SOURCES,
    ACTION_LIST,
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
SELECTED_PERIOD_COLUMN = 3


class FuncType(Enum):
    CALC = 0
    OUTPUT = 1


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
        self.next_enabled = False
        self._action_type = None
        self._current_calc_settings = None
        self._current_output_settings = None
        self._selected_input_table_model = QtGui.QStandardItemModel()
        self._selected_input_table_model.setHorizontalHeaderLabels(
            ["Source", "Name", "Requires New", "Period"]
        )
        self._available_input_table_model = highlightModel.HighlightTableModel()
        self._available_input_table_model.setHorizontalHeaderLabels(
            ["Group", "Name", "Source"]
        )
        self._ui.selectedInputTable.setModel(self._selected_input_table_model)
        self._ui.selectedInputTable.setItemDelegateForColumn(
            SELECTED_PERIOD_COLUMN, SpinBoxDelegate(-1, 99999)
        )
        self._ui.availableInputTable.setModel(self._available_input_table_model)
        self._ui.availableInputTable.setMouseTracking(True)

        self._ui.availableInputTable.clicked.connect(self.availableSelected)
        self._ui.availableInputTable.entered.connect(
            self._available_input_table_model.changeTextColor
        )
        self._ui.removeButton.released.connect(self.removeSelected)
        self._curr_selected = set()

        self._func_selector = FuncSelector()
        self._calc_selector_widget = SelectorWidget(
            FuncType.CALC, self._func_selector, self._ui.calcFuncWidget
        )
        self._ui.calcFuncWidget.layout().addWidget(self._calc_selector_widget)
        self._output_selector_widget = SelectorWidget(
            FuncType.OUTPUT, self._func_selector, self._ui.outputFuncWidget
        )
        self._ui.outputFuncWidget.layout().addWidget(self._output_selector_widget)
        self._func_selector.itemSelected.connect(self.onFuncSelected)

        for e in ActionDataType:
            self._ui.dataTypeCombo.addItem(getattr(e, ENUM_DISPLAY), e)
        self._ui.dataTypeCombo.setCurrentIndex(-1)
        self._ui.dataTypeCombo.currentIndexChanged.connect(self.enableCheck)

    @QtCore.Slot()
    def onFuncSelected(self, settings):
        """
        The func selector has returned a value, check which button triggered it, and
        based on that update the correct setting variable and the text
        """
        if ActionFuncEnum.INDEX in settings:
            if settings[ActionFuncEnum.INDEX] == FuncType.CALC:
                self._calc_selector_widget.updateText(settings[ActionFuncEnum.NAME])
                self._calc_selector_widget.updateExtraDescription(
                    settings.get(ActionFuncEnum.CODE, "")
                )
                self._current_calc_settings = settings
            elif settings[ActionFuncEnum.INDEX] == FuncType.OUTPUT:
                self._output_selector_widget.updateText(settings[ActionFuncEnum.NAME])
                self._output_selector_widget.updateExtraDescription(
                    settings.get(ActionFuncEnum.CODE, "")
                )
                self._current_output_settings = settings
            self.enableCheck()

    def loadPage(self) -> None:
        super().loadPage()
        currSettings: ActionSettings = self.getTempConfig()
        self._current_calc_settings = None
        self._current_output_settings = None
        if currSettings.type_:
            enumType = helpers.findEnumByAttribute(
                ActionTypeEnum, ENUM_DISPLAY, currSettings.type_
            )
            if self._action_type is not None and self._action_type != enumType:
                self.reset()
            self._action_type = enumType
            if self._action_type == ActionTypeEnum.EVENT:
                self.resource_prefix = self.TUTORIAL_RESOURCE_PREFIX_EVENT
                self._ui.triggerWidget.setHidden(True)
            else:
                self.resource_prefix = self.TUTORIAL_RESOURCE_PREFIX_TRIGGER
                self._ui.triggerWidget.setHidden(False)

        self.loadAvailableInputTable()

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

    def availableSelected(self, index: QtCore.QModelIndex):
        """User has clicked available table so we add it to the selected model for display"""
        if (
            index is not None
            and index.isValid()
            and index.column() != AVAILABLE_GROUP_COLUMN
            and index.siblingAtColumn(AVAILABLE_NAME_COLUMN).isValid()
            and index.row() not in self._curr_selected
        ):
            self._curr_selected.add(index.row())
            name = self._available_input_table_model.data(
                index.siblingAtColumn(AVAILABLE_NAME_COLUMN)
            )
            group = self._available_input_table_model.data(
                index.siblingAtColumn(AVAILABLE_GROUP_COLUMN)
            )
            source_item = QtGui.QStandardItem(f"{group}-{name}")
            source_item.setData(
                f"{group}-{name}"
                if group != getattr(ActionTypeEnum.EVENT, ENUM_DISPLAY).capitalize()
                else name
            )
            name_item = QtGui.QStandardItem(name)
            requires_new_item = QtGui.QStandardItem()
            requires_new_item.setCheckable(True)
            source_item.setEditable(False)
            name_item.setEditable(True)
            source_item.setData(index.row(), QtCore.Qt.UserRole)
            self._selected_input_table_model.appendRow(
                [source_item, name_item, requires_new_item, QtGui.QStandardItem(1)]
            )
            self._ui.selectedInputTable.openPersistentEditor(
                self._selected_input_table_model.index(
                    self._selected_input_table_model.rowCount() - 1,
                    SELECTED_PERIOD_COLUMN,
                )
            )
            self.enableCheck()

    def validate(self):
        return (
            self._selected_input_table_model.rowCount() > 0
            and self._current_calc_settings is not None
            and (
                self._action_type == ActionTypeEnum.EVENT
                or self._current_output_settings is not None
            )
            and self._ui.dataTypeCombo.currentIndex() >= 0
        )

    def reset(self) -> None:
        self._curr_selected = set()
        self.next_enabled = False
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
            self._curr_selected.discard(selection[0].row())
            self._selected_input_table_model.removeRow(selection[0].row())
            self.enableCheck()

    def save(self) -> None:
        action_settings: ActionSettings = self.getTempConfig()
        action_settings.calc_func = functionDictToFunctionSettings(
            self._current_calc_settings
        )
        if self._action_type == ActionTypeEnum.TRIGGER:
            action_settings.output_func = functionDictToFunctionSettings(
                self._current_output_settings
            )
        action_settings.input_data_type = self._ui.dataTypeCombo.currentText()
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
                row, SELECTED_PERIOD_COLUMN
            ).data(QtCore.Qt.ItemDataRole.EditRole)
            source = self._selected_input_table_model.item(
                row, SELECTED_SOURCE_COLUMN
            ).data(QtCore.Qt.UserRole + 1)
            action_settings.input_[source] = input_settings

    def getTutorialClasses(self) -> typing.List:
        return [self]
