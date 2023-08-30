from .funcSelectorPageBase import FuncSelectorPageBase
from .qtUiFiles import ui_funcSelectorCodePage

from . import librarySingleton
from ..commonUtil import astUtil
from ..core.dataStructs import FunctionSettings

import ast
import typing

from PySide6 import QtWidgets, QtCore

CODE_ROLE = QtCore.Qt.UserRole + 1
IMPORT_ROLE = QtCore.Qt.UserRole + 2
IMPORT_STATEMENT_ROLE = QtCore.Qt.UserRole + 3

WAIT_FOR_TEXT_EDITING_TO_END = 2000


COMPILING_STATUS = "Compiling Code"
ERROR_ENCOUNTERED = "Error encountered: "
COMPILE_ERROR_STATUS = ERROR_ENCOUNTERED + "Code Compilation"
TOO_MANY_FUNCTIONS_ERROR_STATUS = (
    ERROR_ENCOUNTERED + "Too many functions, only one allowed"
)
POSONLY_ARGS_ERROR_STATUS = (
    ERROR_ENCOUNTERED
    + "Remove the not allowed Positional-only argument indicator '/' in the function defenition."
)
TOO_FEW_FUNCTIONS_ERROR_STATUS = ERROR_ENCOUNTERED + "Must be at least one function"

GOOD_STATUS = "No errors found, Code good to go"


class FuncSelectorCodePage(FuncSelectorPageBase):
    """
    Widget for creating a function from code
    """

    TUTORIAL_RESOURCE_PREFIX = "FuncSelectorCode"

    def __init__(
        self,
        parent: typing.Optional[QtWidgets.QWidget] = None,
        f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags(),
    ) -> None:
        super().__init__(self.TUTORIAL_RESOURCE_PREFIX, parent, f)
        self._ui = ui_funcSelectorCodePage.Ui_FuncSelectorCodePage()
        self._ui.setupUi(self)

        self.enableControls(False)

        self._current_function_settings: FunctionSettings = None

        self._code_edit_timer = QtCore.QTimer()
        self._code_edit_timer.setSingleShot(True)
        self._code_edit_timer.setInterval(WAIT_FOR_TEXT_EDITING_TO_END)
        self._code_edit_timer.timeout.connect(self.validateCode)
        self._ui.codeEdit.textChanged.connect(self.codeChanged)

        self._ui.selectButton.released.connect(self.sendFunctionConfig)
        self._ui.saveButton.released.connect(self.saveCode)

    def updateData(self) -> None:
        self._ui.codeEdit.clear()
        self._current_function_settings = None
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
            self._current_function_settings = None
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
                elif functions:
                    if functions[0].args.posonlyargs:
                        self._ui.statusLabel.setText(POSONLY_ARGS_ERROR_STATUS)
                    else:
                        self._current_function_settings = self.createFunctionConfig(
                            functions[0], *astUtil.getImportsUnique(root)
                        )
                        self.enableControls(True)
                        self._ui.statusLabel.setText(GOOD_STATUS)
                else:
                    self._ui.statusLabel.setText(TOO_FEW_FUNCTIONS_ERROR_STATUS)

            self._ui.codeEdit.setEnabled(True)

    def createFunctionConfig(
        self, function: ast.FunctionDef, imports: list, import_statements: list
    ):
        return FunctionSettings(
            ast.unparse(function), function.name, imports, import_statements
        )

    @QtCore.Slot()
    def sendFunctionConfig(self):
        self.funcSelected.emit(self._current_function_settings)

    @QtCore.Slot()
    def saveCode(self):
        """Save a function in the code edit to either an exisiting AFL file or a new AFL file"""
        file_dlg_return = QtWidgets.QFileDialog.getSaveFileName(
            self, "Select an Algo Function Library", ".", "Algo Function Library(*.afl)"
        )
        if file_dlg_return and file_dlg_return[0]:
            librarySingleton.saveToLibrary(
                file_dlg_return[0], self._current_function_settings
            )

    def enableControls(self, enable):
        self._ui.saveButton.setEnabled(enable)
        self._ui.selectButton.setEnabled(enable)
