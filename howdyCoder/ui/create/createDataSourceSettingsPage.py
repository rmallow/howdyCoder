from .createBasePage import CreateBasePage
from ..uiConstants import PageKeys
from ..actionUIConstant import ActionFuncEnum
from ..qtUiFiles import ui_createDataSourceSettingsPage

from .. import editableTable
from ..selectorWidget import SelectorWidget
from ..funcSelector import FuncSelector
from ..treeSelect import UrlTreeSelect

from ...core.configConstants import (
    DataSourcesTypeEnum,
    InputType,
)

from ...commonUtil import helpers
from ...core.commonGlobals import (
    ENUM_DISPLAY,
    AlgoSettings,
    DATA_SOURCES,
    DataSourceSettings,
)

import typing

from PySide6 import QtWidgets

OUTPUT_HELP = """
Since functions are able to be made outside of this environment, this setup wizard can't tell you what data the function will output, unless the function specifies in docstring. \n
In the case the ouput isn't specified, using the + and - buttons here, you can assign output names that will appear in the action portion later. \n
If you don't do this you won't be able to see the data from this data source. \n
For further questions, consult documentation.
"""


class CreateDataSourceSettingsPage(CreateBasePage):
    PAGE_KEY = PageKeys.DATA_SOURCE_SETTINGS

    TUTORIAL_RESOURCE_PREFIX_FUNC = "CreateSettingsDataSource"
    TUTORIAL_RESOURCE_PREFIX_INPUT = "CreateSettingsInput"

    GROUP = DATA_SOURCES

    def __init__(
        self,
        current_config: AlgoSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(
            current_config, self.TUTORIAL_RESOURCE_PREFIX_FUNC, parent=parent
        )

        self._ui = ui_createDataSourceSettingsPage.Ui_CreateDataSourceSettingsPage()
        self._ui.setupUi(self)
        self.next_enabled = False
        self._current_settings = None
        self._data_source_type = None
        self._outputModel = editableTable.PartialReadOnlyList()
        self._ui.outputView.setModel(self._outputModel)

        # output view wiring
        self._ui.addOutputButton.pressed.connect(self.addOutput)
        self._ui.removeOutputButton.pressed.connect(self.removeOutput)

        self.populateSpecifcWidgets()

    def populateSpecifcWidgets(self):
        """Based on the current data source type selection, populate the specific settings widget
        Add in an empty widget at the end to switch to"""
        self._funcSelector = FuncSelector()

        self._threadedPage = SelectorWidget(
            None, self._funcSelector, self._ui.stackedWidget
        )
        self._ui.stackedWidget.insertWidget(
            DataSourcesTypeEnum.THREADED.value, self._threadedPage
        )

        self._funcPage = SelectorWidget(
            None, self._funcSelector, self._ui.stackedWidget
        )
        self._ui.stackedWidget.insertWidget(
            DataSourcesTypeEnum.FUNC.value, self._funcPage
        )
        self._urlTreeSelect = UrlTreeSelect()

        self._streamPage = SelectorWidget(
            None, self._urlTreeSelect, self._ui.stackedWidget
        )
        self._ui.stackedWidget.insertWidget(
            DataSourcesTypeEnum.STREAM.value, self._streamPage
        )

        self._input_combo = QtWidgets.QComboBox(self._ui.stackedWidget)
        for e in InputType:
            self._input_combo.addItem(e.value)
        self._input_combo.setCurrentIndex(-1)
        self._input_combo.currentTextChanged.connect(self.onSpecificSettingsSelected)
        self._ui.stackedWidget.insertWidget(
            DataSourcesTypeEnum.INPUT.value, self._input_combo
        )

        # add in an empty widget to switch to when no type is selected
        self._ui.stackedWidget.insertWidget(
            self._ui.stackedWidget.count(),
            QtWidgets.QWidget(self._ui.stackedWidget),
        )
        self._urlTreeSelect.itemSelected.connect(self.onSpecificSettingsSelected)
        self._funcSelector.itemSelected.connect(self.onSpecificSettingsSelected)

    def onSpecificSettingsSelected(self, settings) -> None:
        """Selector has made a selection, store this in the dict and then update the wiget"""
        self._current_settings = settings
        output_strings = []
        if self._data_source_type == DataSourcesTypeEnum.STREAM:
            self._ui.stackedWidget.currentWidget().updateText(
                self._current_settings.url
            )
            output_strings = [
                f"{item.key} : {item.label}"
                for item in self._current_settings.key_label_list
            ]
        elif (
            self._data_source_type == DataSourcesTypeEnum.FUNC
            or self._data_source_type == DataSourcesTypeEnum.THREADED
        ):
            self._ui.stackedWidget.currentWidget().updateText(
                self._current_settings.get(ActionFuncEnum.NAME, "")
            )
            self._ui.stackedWidget.currentWidget().updateExtraDescription(
                self._current_settings.get(ActionFuncEnum.CODE, "")
            )
        elif self._data_source_type == DataSourcesTypeEnum.INPUT:
            """Nothing more to do with settings, but make sure that we keep output to name of data source"""
            output_strings = [next(iter(self.getTempConfig().keys()))]
        self._outputModel.setStringList(output_strings)
        self._outputModel.setReadOnlyNum(len(output_strings))
        self.enableCheck()

    def loadPage(self, keys) -> None:
        super().loadPage(keys)
        currSettings = self.getTempConfig()
        self._current_settings = None
        if currSettings.type_:
            enumType = helpers.findEnumByAttribute(
                DataSourcesTypeEnum, ENUM_DISPLAY, currSettings.type_
            )
            if (
                self._data_source_type is not None
                and self._data_source_type != enumType
            ):
                self.reset()
            self._data_source_type = enumType
            self._ui.stackedWidget.setCurrentIndex(enumType.value)
            if (
                self._data_source_type == DataSourcesTypeEnum.STREAM
                or self._data_source_type == DataSourcesTypeEnum.INPUT
            ):
                self._ui.addOutputButton.setEnabled(False)
                self._ui.removeOutputButton.setEnabled(False)
                self._ui.outputHelpText.setText("")
            else:
                self._ui.addOutputButton.setEnabled(True)
                self._ui.removeOutputButton.setEnabled(True)
                self._ui.outputHelpText.setText(OUTPUT_HELP)
            self.resource_prefix = self.TUTORIAL_RESOURCE_PREFIX_FUNC
            if self._data_source_type == DataSourcesTypeEnum.INPUT:
                """If it's input, there's only one output and that is the name of the data source"""
                self.resource_prefix = self.TUTORIAL_RESOURCE_PREFIX_INPUT
                self._outputModel.setStringList(
                    [next(iter(self.getTempConfig().keys()))]
                )

    def removeOutput(self):
        selection = self._ui.outputView.selectionModel().selectedIndexes()
        if len(selection) == 1:
            index = selection[0]
            if index.row() >= self._outputModel.getReadOnlyNum():
                self._outputModel.removeRows(index.row(), 1)

    def addOutput(self):
        newOutput = f"output{self._outputModel.rowCount()}"
        self._outputModel.setStringList(self._outputModel.stringList() + [newOutput])
        self.enableCheck()

    def save(self) -> None:
        curr: DataSourceSettings = self.getTempConfig()
        if self._data_source_type == DataSourcesTypeEnum.STREAM:
            curr.key = self._current_settings.url
        elif (
            self._data_source_type == DataSourcesTypeEnum.FUNC
            or self._data_source_type == DataSourcesTypeEnum.THREADED
        ):
            curr.get_func = helpers.getConfigFromEnumDict(self._current_settings)
        elif self._data_source_type == DataSourcesTypeEnum.INPUT:
            curr.input_type = self._current_settings
        strings = self._outputModel.stringList()
        if strings:
            if ":" in strings[0]:
                splits = [s.split(":") for s in strings]
                curr.output = {split[0].strip(): split[1].strip() for split in splits}
            else:
                curr.output = strings

    def validate(self) -> bool:
        return self._current_settings is not None and self._outputModel.rowCount()

    def reset(self) -> None:
        self.next_enabled = False
        self._current_settings = None
        self._data_source_type = None
        self._outputModel.setStringList([])
        self._outputModel.setReadOnlyNum(0)
        self._ui.addOutputButton.setEnabled(False)
        self._ui.removeOutputButton.setEnabled(False)
        self._ui.outputHelpText.setText("")
        try:
            self._ui.stackedWidget.currentWidget().resetText()
        except AttributeError as e:
            """Not all have this, it's ok"""
            pass
        self._input_combo.setCurrentIndex(-1)

    def getTutorialClasses(self) -> typing.List:
        if (
            self._data_source_type == DataSourcesTypeEnum.FUNC
            or self._data_source_type == DataSourcesTypeEnum.THREADED
        ):
            self._funcSelector.show()
            self._funcSelector.showNormal()
        return [self] + (
            self._funcSelector.getTutorialClasses()
            if self._data_source_type == DataSourcesTypeEnum.FUNC
            or self._data_source_type == DataSourcesTypeEnum.THREADED
            else self._urlTreeSelect.getTutorialClasses()
        )
