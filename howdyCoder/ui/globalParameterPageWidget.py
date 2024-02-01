from .qtUiFiles import ui_globalParameterPageWidget
from . import parameterTable, editableTable
from .inputBox import InputBox
from .funcSelector import FuncSelector
from .pathSelector import PathSelector, PathType
from .selectorWidget import SelectorWidget

from .util import helperData

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
            combo_hide_values=[editableTable.EditorType.GLOBAL_PARAMETER.display]
        )
        # parameter model should be a reflection of what is in the parameter singleton
        # and not actually own data
        self._ui.all_parameter_table_view.setModel(self._parameter_model)

        self._func_selector = FuncSelector()
        self._file_selector = PathSelector(PathType.FILE)
        self._folder_selector = PathSelector(PathType.FOLDER)

        self._stacked_widgets: typing.Dict[editableTable.EditorType, InputBox] = {}
        self.createStackedWidgets()

        for enum in editableTable.EditorType:
            if (
                enum != editableTable.EditorType.GLOBAL_PARAMETER
                and enum != editableTable.EditorType.ANY
                and enum != editableTable.EditorType.COMBO
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
        enum: editableTable.EditorType,
        constructor: typing.Callable,
        getter: typing.Callable,
        resetter: typing.Callable,
    ) -> None:
        w = InputBox(
            "",
            enum,
            hide_enter=True,
            hide_reset=True,
            hide_label=True,
            widget_constructor=constructor,
            getter=getter,
            resetter=resetter,
            parent=self,
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
            editableTable.EditorType.STRING,
            QtWidgets.QLineEdit,
            QtWidgets.QLineEdit.text,
            QtWidgets.QLineEdit.clear,
        )

        def initSpinBox(parent):
            spin = QtWidgets.QSpinBox(parent)
            spin.setRange(-999999, 999999)
            return spin

        self.addStackedWidget(
            editableTable.EditorType.INTEGER,
            initSpinBox,
            QtWidgets.QSpinBox.value,
            lambda obj: obj.setValue(0),
        )
        self.addStackedWidget(
            editableTable.EditorType.DECIMAL,
            QtWidgets.QDoubleSpinBox,
            QtWidgets.QDoubleSpinBox.value,
            lambda obj: obj.setValue(0.0),
        )

        def initFuncSelector(parent):
            return SelectorWidget(None, self._func_selector, parent)

        self.addStackedWidget(
            editableTable.EditorType.FUNC,
            initFuncSelector,
            SelectorWidget.getSelectedData,
            SelectorWidget.reset,
        )

        def initFileSelector(parent):
            return SelectorWidget(None, self._file_selector, parent)

        self.addStackedWidget(
            editableTable.EditorType.FILE,
            initFileSelector,
            SelectorWidget.getSelectedData,
            SelectorWidget.reset,
        )

        def initFolderSelector(parent):
            return SelectorWidget(None, self._folder_selector, parent)

        self.addStackedWidget(
            editableTable.EditorType.FOLDER,
            initFolderSelector,
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
