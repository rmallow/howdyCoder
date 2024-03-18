from .util import abstractQt
from .tutorialOverlay import AbstractTutorialClass
from .qtUiFiles import ui_parameterEditor
from .inputBox import InputBox
from .funcSelector import FuncSelector
from .pathSelector import PathSelector
from .util.qtUtil import showKeyWarning
from .parameterTable import ParameterTableModel

from ..core import commonGlobals
from ..core.dataStructs import Parameter

import typing


from PySide6 import QtWidgets, QtCore, QtGui


class ParameterEditor(
    AbstractTutorialClass,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstractQtResolver(
        QtWidgets.QWidget, AbstractTutorialClass
    ),
):
    removedParameter = QtCore.Signal(Parameter)
    addedParameter = QtCore.Signal(Parameter)

    def __init__(self, *args, **kwargs):
        super().__init__("None", *args, **kwargs)
        self.ui = ui_parameterEditor.Ui_ParameterEditor()
        self.ui.setupUi(self)
        self.stacked_widgets: typing.Dict[commonGlobals.EditorType, InputBox] = {}
        self.parameter_model = ParameterTableModel()

        self.ui.new_parameter_type_combo.currentIndexChanged.connect(
            self.changeTypeStackedWidget
        )

        self.ui.new_parameter_add_button.released.connect(self.addNewParameter)
        self.ui.remove_parameter_button.released.connect(self.removeParameter)

        self._func_selector = FuncSelector(None, QtCore.Qt.WindowFlags.Dialog)
        self._file_selector = PathSelector(commonGlobals.PathType.FILE, self)
        self._folder_selector = PathSelector(commonGlobals.PathType.FOLDER, self)

    def addStackedWidget(
        self,
        enum: commonGlobals.EditorType,
        editor: QtWidgets.QWidget,
        getter: typing.Callable,
        resetter: typing.Callable,
    ) -> None:
        w = InputBox(
            "",
            enum,
            hide_enter=True,
            hide_reset=True,
            hide_label=True,
            input_widget=editor,
            getter=getter,
            resetter=resetter,
            parent=self.ui.new_parameter_stacked_widget,
        )
        self.stacked_widgets[enum] = w
        self.ui.new_parameter_stacked_widget.addWidget(w)

    @QtCore.Slot()
    def changeTypeStackedWidget(self, _) -> None:
        self.ui.new_parameter_stacked_widget.setCurrentWidget(
            self.stacked_widgets[self.ui.new_parameter_type_combo.currentData()]
        )
        self.ui.new_parameter_stacked_widget.currentWidget().resetPressed()

    @QtCore.Slot()
    def addNewParameter(self) -> None:
        if (
            self.ui.new_parameter_name_edit.text()
            and self.ui.new_parameter_stacked_widget.currentWidget().getInput()
            is not None
        ):
            if (
                self.ui.new_parameter_type_combo.currentText()
                == commonGlobals.EditorType.KEY.display
            ):
                if not showKeyWarning():
                    return
            new_parameter = Parameter(
                self.ui.new_parameter_name_edit.text(),
                self.ui.new_parameter_stacked_widget.currentWidget().getInput(),
                self.ui.new_parameter_type_combo.currentText(),
            )
            self.parameter_model.addItemToTable(new_parameter)
            self.addedParameter.emit(new_parameter)
            self.ui.new_parameter_stacked_widget.currentWidget().resetPressed()
            self.ui.new_parameter_name_edit.clear()

    def removeParameter(self):
        index = self.ui.all_parameter_table_view.getSelected()
        self.removedParameter.emit(self.parameter_model.getParameterByIndex(index))
        self.parameter_model.removeValue(index)
