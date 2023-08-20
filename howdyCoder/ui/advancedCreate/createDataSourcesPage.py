from .actionUIConstant import ActionFuncEnum
from .createBasePage import CreateBasePage
from . import editableTable
from . import parameterTable
from .selectorWidget import SelectorWidget
from .funcSelector import FuncSelector
from .treeSelect import UrlTreeSelect

from .qtUiFiles import ui_createDataSourcesPage

from ..core.configConstants import (
    DATA_SOURCES,
    DataSourcesTypeEnum,
    TYPE,
    GET_FUNC,
    PERIOD,
    SEQUENTIAL,
)

from ..core.commonGlobals import (
    ENUM_VALUE,
    ENUM_DISPLAY,
    ENUM_TYPE,
    ENUM_EDITOR_VALUES,
    ENUM_ENABLED,
)

from ..commonUtil import helpers
from ..core.data_structs import StreamSettings
import typing
import copy
from dataclasses import dataclass, field

from aenum import Enum
from PySide2 import QtWidgets, QtCore


@dataclass
class DataSourceSettings:
    source_type: DataSourcesTypeEnum = None
    period: int = 1
    sequential: bool = False
    type_specifc = None
    parameters: typing.Dict = field(default_factory=lambda: {})
    output: typing.List = field(default_factory=lambda: [])
    read_only_output: int = 0

    def toConfig(self):
        config = {
            TYPE: self.source_type.display,
            PERIOD: self.period,
            SEQUENTIAL: self.sequential,
        }
        config |= parameterTable.convertToConfig(self.parameters)
        if self.type_specifc is not None:
            if (
                self.source_type == DataSourcesTypeEnum.FUNC
                or self.source_type == DataSourcesTypeEnum.THREADED
            ):
                config[GET_FUNC] = helpers.getConfigFromEnumDict(self.type_specifc)
            elif self.source_type == DataSourcesTypeEnum.STREAM:
                config |= self.type_specifc.toConfig()

        return config


class DataSourceTableEnum(Enum):
    _init_ = (
        f"{ENUM_VALUE} {ENUM_DISPLAY} {ENUM_TYPE} {ENUM_EDITOR_VALUES} {ENUM_ENABLED}"
    )

    NAME = 0, "Name", editableTable.EditorType.STRING, [], True
    TYPE = (
        1,
        "Type",
        editableTable.EditorType.COMBO,
        [
            DataSourcesTypeEnum.THREADED.display,
            DataSourcesTypeEnum.FUNC.display,
            DataSourcesTypeEnum.STREAM.display,
        ],  # leaving out sim intentionally till it is implemented
        True,
    )


class CreateDataSourcesPage(CreateBasePage):
    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = None):
        super().__init__(parent=parent)

        self._ui = ui_createDataSourcesPage.Ui_CreateDataSourcesPage()
        self._ui.setupUi(self)

        # setup model and views for data source table and parameter table
        self._dataSourcesModel = editableTable.EditableTableModelAddRows(
            DataSourceTableEnum, parent=self._ui.dataSourcesView
        )
        self._ui.dataSourcesView.setModel(self._dataSourcesModel)

        self._outputModel = editableTable.PartialReadOnlyList()
        self._ui.outputView.setModel(self._outputModel)

        self._parameterModel = parameterTable.ParameterTableModel()
        self._ui.parameterView.setModel(self._parameterModel)

        self.populateSpecifcWidgets()

        # set some default values and init vars
        self._ui.typeComboBox.setEnum(DataSourcesTypeEnum)
        self._ui.typeComboBox.setCurrentIndex(-1)
        self._ui.specificStackedWidget.setCurrentIndex(-1)
        self._selectedRowKey: str = ""
        self._selectedIndex: QtCore.QModelIndex = None
        self._dataSourceCount = 0
        self._dataSourcesConfig: typing.Dict[str, DataSourceSettings] = {}

        # connect signals and slots for data sources model
        self._ui.addButton.pressed.connect(self.addDataSource)
        self._ui.removeButton.pressed.connect(self.removeDataSource)
        self._dataSourcesModel.dataChanged.connect(self.dataSourcesChanged)
        self._ui.typeComboBox.currentTextChanged.connect(self.typeComboSelected)
        self._ui.nameEdit.textChanged.connect(self.nameChanged)
        self._ui.dataSourcesView.selectionModel().currentRowChanged.connect(
            self.dataSourceRowChanged
        )
        self._ui.typeComboBox.currentIndexChanged.connect(
            self._ui.specificStackedWidget.setCurrentIndex
        )
        # parameter connections
        self._ui.addParameterButton.pressed.connect(self._parameterModel.appendValue)
        self._ui.removeParameterButton.pressed.connect(
            lambda: self._parameterModel.removeValue(
                self._ui.parameterView.getSelected()
            )
        )
        self._ui.clearParameterButton.pressed.connect(self._parameterModel.clear)

        # output view wiring
        self._ui.addOutputButton.pressed.connect(self.addOutput)
        self._ui.removeOutputButton.pressed.connect(self.removeOutput)

    def populateSpecifcWidgets(self):
        """Based on the current data source type selection, populate the specific settings widget
        Add in an empty widget at the end to switch to"""
        self._funcSelector = FuncSelector()

        self._threadedPage = SelectorWidget(
            None, self._funcSelector, self._ui.specificStackedWidget
        )
        self._ui.specificStackedWidget.insertWidget(
            DataSourcesTypeEnum.THREADED.value, self._threadedPage
        )

        self._funcPage = SelectorWidget(
            None, self._funcSelector, self._ui.specificStackedWidget
        )
        self._ui.specificStackedWidget.insertWidget(
            DataSourcesTypeEnum.FUNC.value, self._funcPage
        )
        self._urlTreeSelect = UrlTreeSelect()

        self._streamPage = SelectorWidget(
            None, self._urlTreeSelect, self._ui.specificStackedWidget
        )
        self._ui.specificStackedWidget.insertWidget(
            DataSourcesTypeEnum.STREAM.value, self._streamPage
        )

        # add in an empty widget to switch to when no type is selected
        self._ui.specificStackedWidget.insertWidget(
            self._ui.specificStackedWidget.count(),
            QtWidgets.QWidget(self._ui.specificStackedWidget),
        )
        self._urlTreeSelect.itemSelected.connect(self.onSpecificSettingsSelected)
        self._funcSelector.itemSelected.connect(self.onSpecificSettingsSelected)

    def getValidConfig(self):
        """
        Get only the current valid configs
        """
        newConfig = {}
        self.save()
        for key, value in self._dataSourcesConfig.items():
            if value is not None:
                value = copy.copy(value)
                if value.source_type is not None:
                    newConfig[key] = value
        return newConfig

    def validate(self) -> bool:
        """Return if page fields are valid"""
        return len(self.getValidConfig()) > 0

    def getConfig(self) -> typing.Dict[str, typing.Any]:
        """Return the configuration for that page"""
        data_sources_config = {}
        for key, value in self.getValidConfig().items():
            data_sources_config[key] = value.toConfig()
        return {DATA_SOURCES: data_sources_config}

    def dataSourcesChanged(self, topLeft: QtCore.QModelIndex, _, _2=None):
        """If the data sources table was changed we want to update their respective edit widgets"""
        if topLeft.column() == DataSourceTableEnum.NAME.value:
            name = self._dataSourcesModel.data(topLeft)
            self._ui.nameEdit.setText(name)
            temp = self._dataSourcesConfig[self._selectedRowKey]
            self._selectedRowKey = name
            self._dataSourcesConfig[self._selectedRowKey] = temp
        elif topLeft.column() == DataSourceTableEnum.TYPE.value:
            text = self._dataSourcesModel.data(topLeft)
            index = self._ui.typeComboBox.findText(text)
            self._ui.typeComboBox.setCurrentIndex(index)
            # find the enum based on the display text
            enumType = helpers.findEnumByAttribute(
                DataSourcesTypeEnum, ENUM_DISPLAY, text
            )
            if self._dataSourcesConfig[self._selectedRowKey].source_type != enumType:
                self._dataSourcesConfig[self._selectedRowKey].type_specifc = None
            self._dataSourcesConfig[self._selectedRowKey].source_type = enumType
            self.updateSpecificWidget()

    def typeComboSelected(self, text: str):
        """When the type combo is changed update the table"""
        if self._selectedIndex is not None:
            index = self._selectedIndex.siblingAtColumn(DataSourceTableEnum.TYPE.value)
            self._dataSourcesModel.setData(index, text)
            self.updateSpecificWidget()

    def nameChanged(self, text: str):
        if self._selectedIndex is not None:
            self._dataSourcesModel.setData(self._selectedIndex, text)

    def dataSourceRowChanged(self, current: QtCore.QModelIndex, _):
        """data source row has changed, save off old data, populate new data, and update internal var"""
        self.save()
        index = current.siblingAtColumn(DataSourceTableEnum.NAME.value)
        self._selectedRowKey = self._dataSourcesModel.data(index)
        self._selectedIndex = index
        self.updateData()

    def save(self):
        """
        Save off all the current values on the page for the data soruce config to be loaded later
        """
        if self._selectedRowKey:
            # if not there add blank dict
            if self._selectedRowKey not in self._dataSourcesConfig:
                self._dataSourcesConfig[self._selectedRowKey] = {}

            # type probably already there and in data source model but save anyways
            enumType = helpers.findEnumByAttribute(
                DataSourcesTypeEnum, ENUM_DISPLAY, self._ui.typeComboBox.currentText()
            )
            settings = self._dataSourcesConfig[self._selectedRowKey]
            settings.source_type = enumType
            settings.parameters = self._parameterModel.getData()
            settings.period = self._ui.periodSpinBox.value()
            settings.sequential = self._ui.seqCheckBox.isChecked()
            settings.output = self._outputModel.stringList()

    def reset(self):
        """Reset the ui back to base values, block signals as needed"""
        self._ui.nameEdit.blockSignals(True)
        self._ui.nameEdit.setText("")
        self._ui.nameEdit.blockSignals(False)
        self._ui.typeComboBox.blockSignals(True)
        self._ui.typeComboBox.setCurrentIndex(-1)
        self._ui.typeComboBox.blockSignals(False)

        self._ui.specificStackedWidget.setCurrentIndex(-1)

    def toggleWidget(self, toggle: bool):
        """toggle ui elements enabled/disabled"""
        self._ui.nameEdit.setEnabled(toggle)
        self._ui.typeComboBox.setEnabled(toggle)
        self._ui.periodSpinBox.setEnabled(toggle)
        self._ui.seqCheckBox.setEnabled(toggle)
        self._ui.parameterView.setEnabled(toggle)
        self._ui.addParameterButton.setEnabled(toggle)
        self._ui.removeParameterButton.setEnabled(toggle)
        self._ui.clearParameterButton.setEnabled(toggle)

    def updateData(self):
        """based on the selected row key populate the data onto the page"""
        self.reset()
        if self._selectedRowKey not in self._dataSourcesConfig:
            self._dataSourcesConfig[self._selectedRowKey] = DataSourceSettings()

        self._ui.nameEdit.setText(self._selectedRowKey)

        if self._dataSourcesConfig[self._selectedRowKey].source_type is not None:
            index = self._ui.typeComboBox.findText(
                self._dataSourcesConfig[self._selectedRowKey].source_type.display
            )
            self._ui.typeComboBox.setCurrentIndex(index)
        else:
            self._ui.typeComboBox.setCurrentIndex(-1)

        self._parameterModel.setValues(
            self._dataSourcesConfig[self._selectedRowKey].parameters
        )
        self._ui.periodSpinBox.setValue(
            self._dataSourcesConfig[self._selectedRowKey].period
        )
        self._ui.seqCheckBox.setChecked(
            self._dataSourcesConfig[self._selectedRowKey].sequential
        )
        self.updateSpecificWidget()

    @QtCore.Slot()
    def addDataSource(self):
        """Add data source, update widget, update internal vars"""
        self.save()
        self.toggleWidget(True)
        newName = "dataSource" + str(self._dataSourceCount)
        self._dataSourcesModel.appendValue({DataSourceTableEnum.NAME: newName})
        # not amount in current table but a continually incrementing number
        self._dataSourceCount += 1
        self._dataSourcesConfig[newName] = DataSourceSettings()
        self._selectedRowKey = newName
        self._selectedIndex = self._dataSourcesModel.index(
            self._dataSourcesModel.rowCount() - 1, DataSourceTableEnum.NAME.value
        )
        self._ui.dataSourcesView.selectionModel().blockSignals(True)
        self._ui.dataSourcesView.selectionModel().clear()
        self._ui.dataSourcesView.selectionModel().select(
            self._selectedIndex, QtCore.QItemSelectionModel.Select
        )
        self._ui.dataSourcesView.selectionModel().blockSignals(False)
        self.updateData()

    @QtCore.Slot()
    def removeDataSource(self):
        """Remove data source and if empty toggle widget"""
        index = self._ui.dataSourcesView.getSelected()
        oldName = self._dataSourcesModel.data(index)
        del self._dataSourcesConfig[oldName]
        if index == self._selectedIndex and self._dataSourcesModel > 0:
            self._selectedIndex = self._dataSourcesModel.index(
                DataSourceTableEnum.NAME, 0
            )
            self._selectedRowKey = self._dataSourcesModel.getValue(self._selectedIndex)
        self._dataSourcesModel.removeValue()
        if self._dataSourcesModel.rowCount() == 0:
            self.toggleWidget(False)

    def update(self) -> None:
        self._dataSourcesModel.beginResetModel()
        self._dataSourcesModel.endResetModel()
        self._parameterModel.beginResetModel()
        self._parameterModel.endResetModel()
        return super().update()

    def onSpecificSettingsSelected(self, settings) -> None:
        """Selector has made a selection, store this in the dict and then update the wiget"""
        self._dataSourcesConfig[self._selectedRowKey].type_specifc = settings
        data_type = self._dataSourcesConfig[self._selectedRowKey].source_type
        if settings is not None:
            string_list = []
            if (
                data_type == DataSourcesTypeEnum.FUNC
                or data_type == DataSourcesTypeEnum.THREADED
            ):
                string_list = settings[ActionFuncEnum.OUTPUT]
            elif data_type == DataSourcesTypeEnum.STREAM:
                for key_label in settings.key_label_list:
                    string_list.append(key_label.label)
            self._dataSourcesConfig[self._selectedRowKey].output = string_list
            self._dataSourcesConfig[self._selectedRowKey].read_only_output = len(
                string_list
            )
            self._outputModel.setReadOnlyNum(len(string_list))
        self.updateSpecificWidget()

    def updateSpecificWidget(self) -> None:
        """Based on what type is selected, get the widget and also get the text out of the config"""
        settings = self._dataSourcesConfig[self._selectedRowKey]
        self._outputModel.setStringList(settings.output)
        self._outputModel.setReadOnlyNum(settings.read_only_output)
        if self._ui.typeComboBox.currentIndex() > -1:
            widget: SelectorWidget = self._ui.specificStackedWidget.widget(
                self._ui.typeComboBox.currentIndex()
            )
            text = None
            if settings.source_type is not None:
                dataType = settings.source_type
                typeSpecificConfig = settings.type_specifc
                # based on the type, find the text to display from the config
                if typeSpecificConfig is not None:
                    if (
                        dataType == DataSourcesTypeEnum.FUNC
                        or dataType == DataSourcesTypeEnum.THREADED
                    ):
                        if ActionFuncEnum.NAME in typeSpecificConfig:
                            text = typeSpecificConfig[ActionFuncEnum.NAME]
                    elif dataType == DataSourcesTypeEnum.STREAM:
                        text = typeSpecificConfig.url

            if text is not None:
                widget.updateText(text)
            else:
                widget.resetText()
        else:
            # no type is selected so set it to the last widget
            self._ui.specificStackedWidget.setCurrentIndex(
                self._ui.specificStackedWidget.count() - 1
            )

    def getSettingsForNextPage(self) -> typing.Any:
        """Send the current settings to the next page to load as needed"""
        return self._dataSourcesConfig

    def removeOutput(self):
        selection = self._ui.outputView.selectionModel().selectedIndexes()
        if len(selection) == 1:
            index = selection[0]
            if (
                index.row()
                >= self._dataSourcesConfig[self._selectedRowKey].read_only_output
            ):
                self._outputModel.removeRows(index.row(), 1)

    def addOutput(self):
        newOutput = f"output{self._outputModel.rowCount()}"
        newList = self._outputModel.stringList()
        newList.append(newOutput)
        self._outputModel.setStringList(newList)
