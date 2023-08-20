from .createBasePage import CreateBasePage
from ..uiConstants import PageKeys
from ..actionUIConstant import ActionFuncEnum
from ..qtUiFiles import ui_createDataSourceSettingsPage

from .. import editableTable
from ..selectorWidget import SelectorWidget
from ..funcSelector import FuncSelector
from ..treeSelect import UrlTreeSelect

from ...core.configConstants import (
    TYPE,
    GET_FUNC,
    KEY,
    OUTPUT,
    DataSourcesTypeEnum,
)

from ...commonUtil import helpers
from ...core.commonGlobals import ENUM_DISPLAY

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

    def __init__(
        self,
        current_config: typing.Dict[str, typing.Any],
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, "test", parent=parent)

        self._ui = ui_createDataSourceSettingsPage.Ui_CreateDataSourceSettingsPage()
        self._ui.setupUi(self)
        self.next_enabled = False
        self._current_settings = None
        self._dataSourceType = None
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
        if self._dataSourceType == DataSourcesTypeEnum.STREAM:
            self._ui.stackedWidget.currentWidget().updateText(
                self._current_settings.url
            )
            output_strings = [
                f"{item.key} : {item.label}"
                for item in self._current_settings.key_label_list
            ]
        elif (
            self._dataSourceType == DataSourcesTypeEnum.FUNC
            or self._dataSourceType == DataSourcesTypeEnum.THREADED
        ):
            self._ui.stackedWidget.currentWidget().updateText(
                self._current_settings.get(ActionFuncEnum.NAME, "")
            )
            self._ui.stackedWidget.currentWidget().updateExtraDescription(
                self._current_settings.get(ActionFuncEnum.CODE, "")
            )
        self._outputModel.setStringList(output_strings)
        self._outputModel.setReadOnlyNum(len(output_strings))
        self.enableCheck()

    def loadPage(self, keys) -> None:
        super().loadPage(keys)
        currSettings = self.getTempConfigFirstValue()
        self._current_settings = None
        if TYPE in currSettings:
            enumType = helpers.findEnumByAttribute(
                DataSourcesTypeEnum, ENUM_DISPLAY, currSettings[TYPE]
            )
            if self._dataSourceType is not None and self._dataSourceType != enumType:
                self.reset()
            self._dataSourceType = enumType
            self._ui.stackedWidget.setCurrentIndex(enumType.value)
            if self._dataSourceType == DataSourcesTypeEnum.STREAM:
                self._ui.addOutputButton.setEnabled(False)
                self._ui.removeOutputButton.setEnabled(False)
                self._ui.outputHelpText.setText("")
            else:
                self._ui.addOutputButton.setEnabled(True)
                self._ui.removeOutputButton.setEnabled(True)
                self._ui.outputHelpText.setText(OUTPUT_HELP)

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
        curr = self.getTempConfigFirstValue()
        if self._dataSourceType == DataSourcesTypeEnum.STREAM:
            curr[KEY] = self._current_settings.url
        else:
            curr[GET_FUNC] = helpers.getConfigFromEnumDict(self._current_settings)
        strings = self._outputModel.stringList()
        if strings:
            if ":" in strings[0]:
                splits = [s.split(":") for s in strings]
                curr[OUTPUT] = {split[0].strip(): split[1].strip() for split in splits}
            else:
                curr[OUTPUT] = strings

    def validate(self) -> bool:
        return self._current_settings is not None and self._outputModel.rowCount()

    def reset(self) -> None:
        self.next_enabled = False
        self._current_settings = None
        self._dataSourceType = None
        self._outputModel.setStringList([])
        self._outputModel.setReadOnlyNum(0)
        self._ui.addOutputButton.setEnabled(False)
        self._ui.removeOutputButton.setEnabled(False)
        self._ui.outputHelpText.setText("")
        self._ui.stackedWidget.currentWidget().resetText()

    def getKeysForNextPage(self) -> typing.List:
        return super().getKeysForNextPage()

    def getTutorialClasses(self) -> typing.List:
        return [self]
