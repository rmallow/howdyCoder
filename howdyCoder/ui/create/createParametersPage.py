from ...core.dataStructs import ItemSettings
from .createBasePage import CreateBasePage, ItemValidity
from ..uiConstants import PageKeys
from ..parameterEditor import ParameterEditor
from .. import editableTable

from ...core.commonGlobals import (
    DATA_SET,
)
from ..util import qtUtil
from ...core import commonGlobals
from ..selectorWidget import SelectorWidget

import typing

from PySide6 import QtWidgets, QtCore


class CreateParametersPage(CreateBasePage):
    PAGE_KEY = PageKeys.PARAMETERS

    def __init__(
        self,
        current_config: ItemSettings,
        parent: typing.Optional[QtWidgets.QWidget] = None,
    ):
        super().__init__(current_config, "None", parent=parent)

        self._parameter_editor = ParameterEditor(self)

        self._parameter_editor.parameter_model.dataChanged.connect(
            self.setParametersLabel
        )

        self._parameter_editor.ui.all_parameter_table_view.setModel(
            self._parameter_editor.parameter_model
        )

        self.createStackedWidgets()

        for enum in commonGlobals.EditorType:
            if (
                enum != commonGlobals.EditorType.ANY
                and enum != commonGlobals.EditorType.COMBO
            ):
                self._parameter_editor.ui.new_parameter_type_combo.addItem(
                    enum.display, userData=enum
                )

        self._parameter_editor.changeTypeStackedWidget(0)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._parameter_editor)
        self.setLayout(layout)

        self.createStackedWidgets()

    def getEditorByType(self, enum: commonGlobals.EditorType):
        return editableTable.getEditor(
            enum,
            self,
            [],
            set(),
            self._parameter_editor._func_selector,
            self._parameter_editor._folder_selector,
            self._parameter_editor._file_selector,
            None,
        )

    def createStackedWidgets(self):
        self._parameter_editor.addStackedWidget(
            commonGlobals.EditorType.STRING,
            self.getEditorByType(commonGlobals.EditorType.STRING),
            QtWidgets.QLineEdit.text,
            QtWidgets.QLineEdit.clear,
        )

        self._parameter_editor.addStackedWidget(
            commonGlobals.EditorType.INTEGER,
            self.getEditorByType(commonGlobals.EditorType.INTEGER),
            QtWidgets.QSpinBox.value,
            lambda obj: obj.setValue(0),
        )

        self._parameter_editor.addStackedWidget(
            commonGlobals.EditorType.DECIMAL,
            self.getEditorByType(commonGlobals.EditorType.DECIMAL),
            QtWidgets.QDoubleSpinBox.value,
            lambda obj: obj.setValue(0.0),
        )
        self._parameter_editor.addStackedWidget(
            commonGlobals.EditorType.FUNC,
            self.getEditorByType(commonGlobals.EditorType.FUNC),
            SelectorWidget.getSelectedData,
            SelectorWidget.reset,
        )

        self._parameter_editor.addStackedWidget(
            commonGlobals.EditorType.FILE,
            self.getEditorByType(commonGlobals.EditorType.FILE),
            SelectorWidget.getSelectedData,
            SelectorWidget.reset,
        )

        self._parameter_editor.addStackedWidget(
            commonGlobals.EditorType.FOLDER,
            self.getEditorByType(commonGlobals.EditorType.FOLDER),
            SelectorWidget.getSelectedData,
            SelectorWidget.reset,
        )
        self._parameter_editor.addStackedWidget(
            commonGlobals.EditorType.KEY,
            self.getEditorByType(commonGlobals.EditorType.KEY),
            QtWidgets.QComboBox.currentText,
            lambda obj: obj.setCurrentIndex(-1),
        )
        self._parameter_editor.addStackedWidget(
            commonGlobals.EditorType.GLOBAL_PARAMETER,
            self.getEditorByType(commonGlobals.EditorType.GLOBAL_PARAMETER),
            QtWidgets.QComboBox.currentText,
            lambda obj: obj.setCurrentIndex(-1),
        )

    def save(self) -> None:
        """
        Checking if temp config exists gets around an issue with exiting from a section
        If exit is hit, it will try to save the parameters page, this is becuase the parameters page
        at the time of writing this is ALWAYS valid even without input. Issue is temp config has been reset
        when we exit, so when the save is called on this page (because it's technically valid) it throws
        an error trying to save to a temp config that doesn't exist
        """
        if self.getConfig():
            curr = self.getConfig()
            curr.all_parameters = self._parameter_editor.parameter_model.getData()

    def reset(self) -> None:
        self._parameter_editor.parameter_model.clear()

    def loadPage(self) -> None:
        curr = self.getConfig()
        self._parameter_editor.parameter_model.clear()
        self._parameter_editor.parameter_model.setDataFromSettings(curr.all_parameters)
        self.setParametersLabel()
        return super().loadPage()

    @QtCore.Slot()
    def setParametersLabel(self, *args, **kwrags):
        suggested_parmesean = [
            param
            for param in self.getHelperData().suggested_parameters
            + self._parameter_editor.parameter_model.getSuggestedParameters()
            if param != DATA_SET
        ]
        self.addToSuggestedListWidget(
            self._parameter_editor.ui.parameter_list_widget,
            self._parameter_editor.parameter_model.current_names,
            suggested_parmesean,
        )
        self._parameter_editor.ui.all_parameter_table_view.itemDelegate().setCompleterStrings(
            suggested_parmesean
        )
        qtUtil.setCompleter(
            self._parameter_editor.ui.new_parameter_name_edit, suggested_parmesean
        )

    def getTutorialClasses(self) -> typing.List:
        return [self]

    def validate(self) -> typing.Dict[QtWidgets.QWidget | str, ItemValidity]:
        return {
            "Some suggested parameters have not been added.": self.suggested_validity,
        }
