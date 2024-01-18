from ...core.dataStructs import ItemSettings, DataSourceSettings
from .createBasePage import CreateBasePage, ItemValidity
from ..uiConstants import PageKeys
from ..qtUiFiles import ui_createDataSourcePage

from ..util.qtUtil import CompleterDelegate
from .. import editableTable
from ..selectorWidget import SelectorWidget
from ..funcSelector import FuncSelector, addHelperData
from ..treeSelect import UrlTreeSelect


from ...commonUtil import helpers, astUtil
from ...core.commonGlobals import (
    ENUM_DISPLAY,
    DATA_SOURCES,
    DataSourcesTypeEnum,
    InputType,
)
import typing

from PySide6 import QtWidgets, QtCore

OUTPUT_HELP_FUNCTION = """Since functions are able to be made outside of this environment, this setup wizard can't tell you what data the function will output, unless the AI that generates the code specifies.\nIf the AI did specify, we have added these to the suggestion box and you can add them to the output box using the + and - buttons here.\nAfter adding the outputs, double click them to change their names.\nIf you don't do this you won't be able to see the data from this data source.\nFor further questions, consult the user manual."""

OUTPUT_HELP_INPUT = """
Output not selectable for input and is automatically the name of the data source.
"""


class CreateDataSourcePage(CreateBasePage):
    PAGE_KEY = PageKeys.DATA_SOURCE

    TUTORIAL_RESOURCE_PREFIX_FUNC = "CreateSettingsDataSource"
    TUTORIAL_RESOURCE_PREFIX_INPUT = "CreateSettingsInput"

    def __init__(
        self,
        current_config: ItemSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(
            current_config, self.TUTORIAL_RESOURCE_PREFIX_FUNC, parent=parent
        )

        self._ui = ui_createDataSourcePage.Ui_CreateDataSourcePage()
        self._ui.setupUi(self)
        self._current_settings = None
        self._data_source_type = None
        self._outputModel = editableTable.PartialReadOnlyList()
        self._ui.outputView.setItemDelegate(CompleterDelegate(self._ui.outputView))
        self._ui.outputView.setModel(self._outputModel)

        self._outputModel.dataChanged.connect(self.setSuggestedOutput)

        # output view wiring
        self._ui.addOutputButton.pressed.connect(self.addOutput)
        self._ui.removeOutputButton.pressed.connect(self.removeOutput)

        self.populateSpecifcWidgets()

    def populateSpecifcWidgets(self):
        """Based on the current data source type selection, populate the specific settings widget
        Add in an empty widget at the end to switch to"""
        self._funcSelector = FuncSelector()

        self._threadedPage = SelectorWidget(
            None,
            self._funcSelector,
            self._ui.stackedWidget,
            default_prompt="Data Source Threaded",
        )
        self._ui.stackedWidget.insertWidget(
            DataSourcesTypeEnum.THREADED.value, self._threadedPage
        )

        self._funcPage = SelectorWidget(
            None,
            self._funcSelector,
            self._ui.stackedWidget,
            default_prompt="Data Source",
        )
        self._ui.stackedWidget.insertWidget(
            DataSourcesTypeEnum.FUNC.value, self._funcPage
        )
        self._urlTreeSelect = UrlTreeSelect()

        self._streamPage = SelectorWidget(
            None,
            self._urlTreeSelect,
            self._ui.stackedWidget,
        )
        self._ui.stackedWidget.insertWidget(
            DataSourcesTypeEnum.STREAM.value, self._streamPage
        )

        self._input_combo = QtWidgets.QComboBox(self._ui.stackedWidget)
        font = self._input_combo.font()
        font.setPointSize(17)
        self._input_combo.setFont(font)
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
                self._current_settings.function_settings.name
            )
            self._ui.stackedWidget.currentWidget().updateExtraDescription(
                self._current_settings.function_settings.code
            )
            self._ui.stackedWidget.currentWidget().data = (
                self._current_settings.function_settings
            )
            self.setSuggestedOutput()
        elif self._data_source_type == DataSourcesTypeEnum.INPUT:
            """Nothing more to do with settings, but make sure that we keep output to name of data source"""
            output_strings = [self.getConfig().name]
        if (
            self._data_source_type != DataSourcesTypeEnum.FUNC
            and self._data_source_type != DataSourcesTypeEnum.THREADED
        ):
            self._outputModel.setStringList(output_strings)
            self._outputModel.setReadOnlyNum(len(output_strings))

    def loadPage(self) -> None:
        super().loadPage()
        curr_settings: DataSourceSettings = self.getConfig()
        if curr_settings.type_:
            enumType = helpers.findEnumByAttribute(
                DataSourcesTypeEnum, ENUM_DISPLAY, curr_settings.type_
            )
            if (
                self._data_source_type is not None
                and self._data_source_type != enumType
            ):
                self.reset()
            self._data_source_type = enumType
            self._ui.stackedWidget.setCurrentIndex(enumType.value)
            try:
                self._ui.stackedWidget.currentWidget().resetText()
            except AttributeError as e:
                """Not all have this, it's ok"""
                pass
            if self._data_source_type == DataSourcesTypeEnum.INPUT:
                self._ui.addOutputButton.setEnabled(False)
                self._ui.removeOutputButton.setEnabled(False)
                self._ui.outputHelpText.setText("")
                """If it's input, there's only one output and that is the name of the data source"""
                self.resource_prefix = self.TUTORIAL_RESOURCE_PREFIX_INPUT
                self._ui.outputHelpText.setText(OUTPUT_HELP_INPUT)
                self._ui.suggested_output_box.hide()
                if index := self._input_combo.findText(curr_settings.input_type) != -1:
                    self._input_combo.setCurrentIndex(index)
                    self.onSpecificSettingsSelected(curr_settings.input_type)
            elif (
                self._data_source_type == DataSourcesTypeEnum.FUNC
                or self._data_source_type == DataSourcesTypeEnum.THREADED
            ):
                if curr_settings.get_function is not None:
                    self.onSpecificSettingsSelected(
                        addHelperData(curr_settings.get_function)
                    )
                self._ui.addOutputButton.setEnabled(True)
                self._ui.removeOutputButton.setEnabled(True)
                self._outputModel.setStringList(curr_settings.output)
                self.resource_prefix = self.TUTORIAL_RESOURCE_PREFIX_FUNC
                self._ui.outputHelpText.setText(OUTPUT_HELP_FUNCTION)
                self._ui.suggested_output_box.show()

    def removeOutput(self):
        selection = self._ui.outputView.selectionModel().selectedIndexes()
        if len(selection) == 1:
            index = selection[0]
            if index.row() >= self._outputModel.getReadOnlyNum():
                self._outputModel.removeRows(index.row(), 1)

    def addOutput(self):
        newOutput = f"output{self._outputModel.rowCount()}"
        self._outputModel.setStringList(self._outputModel.stringList() + [newOutput])

    def save(self) -> None:
        curr: DataSourceSettings = self.getConfig()
        if self._data_source_type == DataSourcesTypeEnum.STREAM:
            curr.key = self._current_settings.url
        elif (
            self._data_source_type == DataSourcesTypeEnum.FUNC
            or self._data_source_type == DataSourcesTypeEnum.THREADED
        ):
            curr.get_function = self._current_settings.function_settings
            self.getHelperData().suggested_parameters = (
                astUtil.getSuggestedParameterNames(
                    astUtil.getRoot(curr.get_function.code), curr.get_function
                )
            )
        elif self._data_source_type == DataSourcesTypeEnum.INPUT:
            curr.input_type = self._current_settings
        strings = self._outputModel.stringList()
        if strings:
            if ":" in strings[0]:
                splits = [s.split(":") for s in strings]
                curr.output = {split[0].strip(): split[1].strip() for split in splits}
            else:
                curr.output = strings

    def validate(self) -> typing.Dict[QtWidgets.QWidget | str, ItemValidity]:
        return {
            self._ui.stackedWidget: ItemValidity.getEnum(
                self._current_settings is not None
            ),
            self._ui.outputView: ItemValidity.getEnum(self._outputModel.rowCount() > 0),
            "Some suggested data source outputs have not been added.": self.suggested_validity,
        }

    def reset(self) -> None:
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

    @QtCore.Slot()
    def setSuggestedOutput(self, *args, **kwargs):
        self.addToSuggestedListWidget(
            self._ui.suggested_output,
            set(self._outputModel.stringList()),
            self._current_settings.function_settings.suggested_output,
        )
        self._ui.outputView.itemDelegate().setCompleterStrings(
            self._current_settings.function_settings.suggested_output
        )
