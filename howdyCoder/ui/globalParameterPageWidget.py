from .qtUiFiles import ui_globalParameterPageWidget
from .inputBox import InputBox
from .funcSelector import FuncSelector
from .pathSelector import PathSelector
from .selectorWidget import SelectorWidget
from . import parameterTable, editableTable
from .util import helperData

from ..core import parameterSingleton
from ..core.commonGlobals import PathType
from ..core import commonGlobals

import typing

from PySide6 import QtWidgets, QtCore, QtGui


class GlobalParameterPageWidget(QtWidgets.QWidget):
    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        f: QtCore.Qt.WindowType = QtCore.Qt.WindowType(),
    ) -> None:
        super().__init__(parent, f)
        self._ui = ui_globalParameterPageWidget.Ui_GlobalParameterPageWidget()
        self._ui.setupUi(self)
        self._parameter_model = parameterTable.ParameterTableModel(
            combo_hide_values=[commonGlobals.EditorType.GLOBAL_PARAMETER.display]
        )
        # parameter model should be a reflection of what is in the parameter singleton
        # and not actually own data
        self._ui.all_parameter_table_view.setModel(self._parameter_model)

        self._func_selector = FuncSelector(None, QtCore.Qt.WindowFlags.Dialog)
        self._file_selector = PathSelector(PathType.FILE, self)
        self._folder_selector = PathSelector(PathType.FOLDER, self)

        self._stacked_widgets: typing.Dict[commonGlobals.EditorType, InputBox] = {}

        self.createStackedWidgets()

        for enum in commonGlobals.EditorType:
            if (
                enum != commonGlobals.EditorType.GLOBAL_PARAMETER
                and enum != commonGlobals.EditorType.ANY
                and enum != commonGlobals.EditorType.COMBO
            ):
                self._ui.new_parameter_type_combo.addItem(enum.display, userData=enum)

        self._ui.new_parameter_type_combo.currentIndexChanged.connect(
            self.changeTypeStackedWidget
        )

        self._ui.new_parameter_add_button.released.connect(self.addNewParameter)
        self._ui.remove_parameter_button.released.connect(
            lambda: self._parameter_model.removeValue(
                self._ui.all_parameter_table_view.getSelected()
            )
        )

        self.changeTypeStackedWidget(0)

    def addStackedWidget(
        self,
        enum: commonGlobals.EditorType,
        getter: typing.Callable,
        resetter: typing.Callable,
    ) -> None:
        input_widget = editableTable.getEditor(
            enum,
            self,
            [],
            set([commonGlobals.EditorType.GLOBAL_PARAMETER.display]),
            self._func_selector,
            self._folder_selector,
            self._file_selector,
            None,
        )
        w = InputBox(
            "",
            enum,
            hide_enter=True,
            hide_reset=True,
            hide_label=True,
            input_widget=input_widget,
            getter=getter,
            resetter=resetter,
            parent=self._ui.new_parameter_stacked_widget,
        )
        self._stacked_widgets[enum] = w
        self._ui.new_parameter_stacked_widget.addWidget(w)

    def createStackedWidgets(self):
        """
        STRING = 0, "String"
        INTEGER = 2, "Integer"
        DECIMAL = 3, "Decimal"
        FUNC = 4, "Function"
        FILE = 5, PathType.FILE.value
        FOLDER = 6, PathType.FOLDER.value
        """
        self.addStackedWidget(
            commonGlobals.EditorType.STRING,
            QtWidgets.QLineEdit.text,
            QtWidgets.QLineEdit.clear,
        )

        self.addStackedWidget(
            commonGlobals.EditorType.INTEGER,
            QtWidgets.QSpinBox.value,
            lambda obj: obj.setValue(0),
        )

        self.addStackedWidget(
            commonGlobals.EditorType.DECIMAL,
            QtWidgets.QDoubleSpinBox.value,
            lambda obj: obj.setValue(0.0),
        )
        self.addStackedWidget(
            commonGlobals.EditorType.FUNC,
            SelectorWidget.getSelectedData,
            SelectorWidget.reset,
        )

        self.addStackedWidget(
            commonGlobals.EditorType.FILE,
            SelectorWidget.getSelectedData,
            SelectorWidget.reset,
        )

        self.addStackedWidget(
            commonGlobals.EditorType.FOLDER,
            SelectorWidget.getSelectedData,
            SelectorWidget.reset,
        )

    @QtCore.Slot()
    def changeTypeStackedWidget(self, _) -> None:
        self._ui.new_parameter_stacked_widget.setCurrentWidget(
            self._stacked_widgets[self._ui.new_parameter_type_combo.currentData()]
        )
        self._ui.new_parameter_stacked_widget.currentWidget().resetPressed()

    @QtCore.Slot()
    def addNewParameter(self) -> None:
        if (
            self._ui.new_parameter_name_edit.text()
            and self._ui.new_parameter_stacked_widget.currentWidget().getInput()
            is not None
        ):
            self._parameter_model.addItemToTable(
                self._ui.new_parameter_name_edit.text(),
                self._ui.new_parameter_type_combo.currentText(),
                self._ui.new_parameter_stacked_widget.currentWidget().getInput(),
            )
            self._ui.new_parameter_stacked_widget.currentWidget().resetPressed()
            self._ui.new_parameter_name_edit.clear()

    def saveParameters(self) -> None:
        parameterSingleton.clearParameters()
        parameterSingleton.setParameters(self._parameter_model.getData())
        parameterSingleton.saveParameters()

    def loadParameters(self) -> None:
        self._parameter_model.setDataFromSettings(parameterSingleton.getParameters())
