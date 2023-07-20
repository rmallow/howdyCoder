from .funcSelectorPageBase import FuncSelectorPageBase
from .qtUiFiles import ui_funcSelectorCodePage

from .actionUIConstant import ActionFuncEnum
from . import librarySingleton
from ..commonUtil import astUtil

import ast
import typing

from PySide2 import QtWidgets, QtCore

CODE_ROLE = QtCore.Qt.UserRole + 1
IMPORT_ROLE = QtCore.Qt.UserRole + 2
IMPORT_STATEMENT_ROLE = QtCore.Qt.UserRole + 3

WAIT_FOR_TEXT_EDITING_TO_END = 2000


COMPILING_STATUS = "Compiling Code"
COMPILE_ERROR_STATUS = "Error encountered: Code Compilation"
TOO_MANY_FUNCTIONS_ERROR_STATUS = (
    "Error encountered: Too many functions, only one allowed"
)
GOOD_STATUS = "No errors found, Code good to go"


class FuncSelectorCodePage(FuncSelectorPageBase):
    """
    Widget for creating a function from code
    """

    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:

        super().__init__(parent, f)
        self._ui = ui_funcSelectorCodePage.Ui_FuncSelectorCodePage()
        self._ui.setupUi(self)

        self.enableControls(False)

        self._current_function_config: typing.Dict[
            ActionFuncEnum, typing.Union[str, list]
        ] = None

        self._code_edit_timer = QtCore.QTimer()
        self._code_edit_timer.setSingleShot(True)
        self._code_edit_timer.setInterval(WAIT_FOR_TEXT_EDITING_TO_END)
        self._code_edit_timer.timeout.connect(self.validateCode)
        self._ui.codeEdit.textChanged.connect(self.codeChanged)

        self._ui.selectButton.released.connect(self.sendFunctionConfig)
        self._ui.saveButton.released.connect(self.saveCode)

    def updateData(self) -> None:
        self._ui.codeEdit.clear()
        self._current_function_config = None
        return super().updateData()

    def codeChanged(self):
        self._code_edit_timer.start()
        self.enableControls(False)

    def validateCode(self):
        """Disable the text edit and validate the code entered into the text edit"""
        # disable at start and re enable after validation
        if self._ui.codeEdit.toPlainText():
            self._ui.codeEdit.setEnabled(False)
            self._ui.statusLabel.setText(COMPILING_STATUS)
            self._current_function_config = None
            try:
                # first make sure it compiles, this is a better check than ast parsing, we don't need a return value for this
                compile(self._ui.codeEdit.toPlainText(), "<string>", "exec")
            except Exception:
                # just catch any exception
                self._ui.statusLabel.setText(COMPILE_ERROR_STATUS)
            else:
                root = ast.parse(self._ui.codeEdit.toPlainText(), "<string>")
                functions = astUtil.getFunctions(root)
                if len(functions) > 1:
                    self._ui.statusLabel.setText(TOO_MANY_FUNCTIONS_ERROR_STATUS)
                else:
                    self._current_function_config = self.createFunctionConfig(
                        functions[0], *astUtil.getImportsUnique(root)
                    )
                    self.enableControls(True)
                    self._ui.statusLabel.setText(GOOD_STATUS)

            self._ui.codeEdit.setEnabled(True)

    def createFunctionConfig(
        self, function: ast.FunctionDef, imports: list, import_statements: list
    ):
        func_config_dict = {}
        func_config_dict[ActionFuncEnum.NAME] = function.name
        func_config_dict[ActionFuncEnum.CODE] = ast.unparse(function)
        func_config_dict[ActionFuncEnum.IMPORTS] = imports
        func_config_dict[ActionFuncEnum.IMPORT_STATEMENTS] = import_statements
        return func_config_dict

    @QtCore.Slot()
    def sendFunctionConfig(self):
        self.funcSelected.emit(self._current_function_config)

    @QtCore.Slot()
    def saveCode(self):
        """Save a function in the code edit to either an exisiting AFL file or a new AFL file"""
        file_dlg_return = QtWidgets.QFileDialog.getSaveFileName(
            self, "Select an Algo Function Library", ".", "Algo Function Library(*.afl)"
        )
        if file_dlg_return and file_dlg_return[0]:
            librarySingleton.saveToLibrary(
                file_dlg_return[0], self._current_function_config
            )

    def enableControls(self, enable):
        self._ui.saveButton.setEnabled(enable)
        self._ui.selectButton.setEnabled(enable)
