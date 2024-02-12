from .selectorWidget import SelectorWidget
from . import parameterTable, editableTable
from .util.qtUtil import showKeyWarning
from .parameterEditor import ParameterEditor

from ..core import parameterSingleton
from ..core.commonGlobals import PathType
from ..core import commonGlobals

import typing

from PySide6 import QtWidgets, QtCore, QtGui


class GlobalParameterTableModel(parameterTable.ParameterTableModel):
    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        flags = super().flags(index)
        if (
            index.isValid()
            and index.siblingAtColumn(parameterTable.ParameterEnum.TYPE.value).isValid()
        ):
            type_index = index.siblingAtColumn(parameterTable.ParameterEnum.TYPE.value)
            if (
                type_index.data(QtCore.Qt.ItemDataRole.DisplayRole)
                == commonGlobals.EditorType.KEY.display
            ):
                flags &= ~QtCore.Qt.ItemFlag.ItemIsEditable
        return flags


class GlobalParameterPageWidget(QtWidgets.QWidget):
    def __init__(
        self,
        parent: QtWidgets.QWidget | None = None,
        f: QtCore.Qt.WindowType = QtCore.Qt.WindowType(),
    ) -> None:
        super().__init__(parent, f)
        self._parameter_editor = ParameterEditor(self)
        self._parameter_editor.ui.stacked_extra_widgets.setCurrentWidget(
            self._parameter_editor.ui.key_set_widget_page
        )
        self._parameter_editor.parameter_model = GlobalParameterTableModel(
            combo_hide_values=[
                commonGlobals.EditorType.GLOBAL_PARAMETER.display,
                commonGlobals.EditorType.KEY.display,
            ]
        )
        self._parameter_editor.parameter_model.dataChanged.connect(
            self.tableDataChanged
        )

        self._parameter_editor.ui.all_parameter_table_view.setModel(
            self._parameter_editor.parameter_model
        )

        self.createStackedWidgets()

        for enum in commonGlobals.EditorType:
            if (
                enum != commonGlobals.EditorType.GLOBAL_PARAMETER
                and enum != commonGlobals.EditorType.ANY
                and enum != commonGlobals.EditorType.COMBO
            ):
                self._parameter_editor.ui.new_parameter_type_combo.addItem(
                    enum.display, userData=enum
                )

        self._parameter_editor.changeTypeStackedWidget(0)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._parameter_editor)
        self.setLayout(layout)

    def getEditorByType(self, enum: commonGlobals.EditorType):
        return editableTable.getEditor(
            enum,
            self,
            [],
            set([commonGlobals.EditorType.GLOBAL_PARAMETER.display]),
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
            QtWidgets.QLineEdit(None),
            QtWidgets.QLineEdit.text,
            QtWidgets.QLineEdit.clear,
        )

    def saveParameters(self) -> None:
        parameterSingleton.clearParameters()
        parameterSingleton.setParameters(
            self._parameter_editor.parameter_model.getData()
        )
        parameterSingleton.saveParameters()

    def loadParameters(self) -> None:
        self._parameter_editor.parameter_model.setDataFromSettings(
            parameterSingleton.getParameters()
        )

    def tableDataChanged(self) -> None:
        pass
