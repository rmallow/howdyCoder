from ...core.dataStructs import DataSourceSettings
from .createBasePage import ItemValidity, CreateBasePage
from ..qtUiFiles import ui_createStandardDataSource

from ..tutorialOverlay import AbstractTutorialClass
from ..util import abstractQt
from ..util.qtUtil import CompleterDelegate
from .. import editableTable
from ..selectorWidget import SelectorWidget
from ..funcSelector import FuncSelector
from ..treeSelect import UrlTreeSelect
from ..pathSelector import PathSelector

from ..util.helperData import addHelperData

from ...commonUtil import helpers, astUtil
from ...core.commonGlobals import (
    ENUM_DISPLAY,
    DATA_SOURCES,
    PathType,
    DataSourcesTypeEnum,
    InputType,
)
import typing

from PySide6 import QtWidgets, QtCore


class CreateStandardDataSource(
    AbstractTutorialClass,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstractQtResolver(
        QtWidgets.QWidget, AbstractTutorialClass
    ),
):

    TUTORIAL_RESOURCE_PREFIX_FUNC = "CreateSettingsDataSource"
    TUTORIAL_RESOURCE_PREFIX_INPUT = "CreateSettingsInput"

    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(self.TUTORIAL_RESOURCE_PREFIX_FUNC, parent=parent)

        self._ui = ui_createStandardDataSource.Ui_CreateStandardDataSource()
        self._ui.setupUi(self)
        self.parent_page: CreateBasePage = None
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

        self._stacked_widgets = {}

        self._func_selector = FuncSelector()

        self._threaded_page = SelectorWidget(
            None,
            self._func_selector,
            self._ui.stackedWidget,
            default_prompt="Data Source Threaded",
        )
        self._ui.stackedWidget.addWidget(self._threaded_page)
        self._stacked_widgets[DataSourcesTypeEnum.THREADED] = self._threaded_page

        self._func_page = SelectorWidget(
            None,
            self._func_selector,
            self._ui.stackedWidget,
            default_prompt="Data Source",
        )
        self._ui.stackedWidget.addWidget(self._func_page)
        self._stacked_widgets[DataSourcesTypeEnum.FUNC] = self._func_page

        self._url_tree_select = UrlTreeSelect()

        self._stream_page = SelectorWidget(
            None,
            self._url_tree_select,
            self._ui.stackedWidget,
        )
        self._ui.stackedWidget.addWidget(self._stream_page)
        self._stacked_widgets[DataSourcesTypeEnum.STREAM] = self._stream_page

        self._input_combo = QtWidgets.QComboBox(self._ui.stackedWidget)
        font = self._input_combo.font()
        font.setPointSize(17)
        self._input_combo.setFont(font)
        for e in InputType:
            self._input_combo.addItem(e.value)
        self._input_combo.setCurrentIndex(-1)
        self._input_combo.currentTextChanged.connect(self.onSpecificSettingsSelected)
        self._ui.stackedWidget.addWidget(self._input_combo)
        self._stacked_widgets[DataSourcesTypeEnum.INPUT] = self._input_combo

        self._url_tree_select.itemSelected.connect(self.onSpecificSettingsSelected)
        self._func_selector.itemSelected.connect(self.onSpecificSettingsSelected)

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
            output_strings = [self.parent_page.getConfig().name]
        if (
            self._data_source_type != DataSourcesTypeEnum.FUNC
            and self._data_source_type != DataSourcesTypeEnum.THREADED
        ):
            self._outputModel.setStringList(output_strings)
            self._outputModel.setReadOnlyNum(len(output_strings))

    def loadPage(self) -> None:
        curr_settings: DataSourceSettings = self.parent_page.getConfig()
        self._ui.output_box.show()
        if curr_settings.type_:
            enum_type = helpers.findEnumByAttribute(
                DataSourcesTypeEnum, ENUM_DISPLAY, curr_settings.type_
            )
            if (
                self._data_source_type is not None
                and self._data_source_type != enum_type
            ):
                self.reset()
            self._data_source_type = enum_type
            self._ui.stackedWidget.setCurrentWidget(self._stacked_widgets[enum_type])
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
                self._ui.output_box.hide()
                self.resource_prefix = self.TUTORIAL_RESOURCE_PREFIX_INPUT
                self._ui.suggested_output_box.hide()
                if index := self._input_combo.findText(curr_settings.input_type) != -1:
                    self._input_combo.setCurrentIndex(index)
                    self.onSpecificSettingsSelected(curr_settings.input_type)
            elif (
                self._data_source_type == DataSourcesTypeEnum.FUNC
                or self._data_source_type == DataSourcesTypeEnum.THREADED
            ):
                self._outputModel.setStringList(curr_settings.output)
                if curr_settings.get_function is not None:
                    self.onSpecificSettingsSelected(
                        addHelperData(curr_settings.get_function)
                    )
                self._ui.addOutputButton.setEnabled(True)
                self._ui.removeOutputButton.setEnabled(True)
                self.resource_prefix = self.TUTORIAL_RESOURCE_PREFIX_FUNC
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
        curr: DataSourceSettings = self.parent_page.getConfig()
        if self._data_source_type == DataSourcesTypeEnum.STREAM:
            curr.key = self._current_settings.url
        elif (
            self._data_source_type == DataSourcesTypeEnum.FUNC
            or self._data_source_type == DataSourcesTypeEnum.THREADED
        ):
            curr.get_function = self._current_settings.function_settings
            self.parent_page.getHelperData().suggested_parameters = (
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
            self._func_selector.show()
            self._func_selector.showNormal()
        return [self] + (
            self._func_selector.getTutorialClasses()
            if self._data_source_type == DataSourcesTypeEnum.FUNC
            or self._data_source_type == DataSourcesTypeEnum.THREADED
            else self._url_tree_select.getTutorialClasses()
        )

    @QtCore.Slot()
    def setSuggestedOutput(self, *args, **kwargs):
        self.parent_page.addToSuggestedListWidget(
            self._ui.suggested_output,
            set(self._outputModel.stringList()),
            self._current_settings.function_settings.suggested_output,
        )
        self._ui.outputView.itemDelegate().setCompleterStrings(
            self._current_settings.function_settings.suggested_output
        )
