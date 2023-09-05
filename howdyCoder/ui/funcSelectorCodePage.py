from .funcSelectorPageBase import FuncSelectorPageBase
from .qtUiFiles import ui_funcSelectorCodePage
from .util import qtResourceManager, expander

from . import librarySingleton
from ..commonUtil import astUtil, keyringUtil, openAIUtil
from ..core.dataStructs import FunctionSettings

import ast
import typing

from PySide6 import QtWidgets, QtCore, QtGui

TEST_PROMPTS = {
    "No Prompt": "",
    "Script Prompt": "You are writing code in python for a user. Only respond to their prompts with python code. Do not provide test code. If more than one function is used for what the users asks for then you should designate the entry function by entry:<FUNCTION NAME HERE>.",
}

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
        self.ui = ui_funcSelectorCodePage.Ui_FuncSelectorCodePage()
        self.ui.setupUi(self)

        self.enableControls(False)

        self._current_function_settings: FunctionSettings = None

        self.ui.key_set_widget.key_name = openAIUtil.OPEN_AI_API_KEY_NAME
        self.ui.key_set_widget._key_validation_function = openAIUtil.testValid
        self.ui.key_set_widget.output_function = self.ui.call_api_button.setEnabled
        if openAIUtil.testValidKeySet():
            self.ui.key_set_widget.setStatus(True)
            self.ui.call_api_button.setEnabled(True)

        self.setupPromptCombo()

        self.ui.call_api_button.released.connect(self.callApiButton)
        self._code_edit_timer = QtCore.QTimer()
        self._code_edit_timer.setSingleShot(True)
        self._code_edit_timer.setInterval(WAIT_FOR_TEXT_EDITING_TO_END)
        self._code_edit_timer.timeout.connect(self.validateCode)
        self.ui.codeEdit.textChanged.connect(self.codeChanged)

        hz_expander = expander.HorizontalExpander(self.ui.code_edit_box, "Explanation")
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.code_explanation = QtWidgets.QPlainTextEdit(hz_expander.contentArea)
        self.code_explanation.setReadOnly(True)
        layout.addWidget(self.code_explanation)
        hz_expander.setContentLayout(layout)
        self.ui.code_edit_box.layout().addWidget(hz_expander, 1)

        self.ui.selectButton.released.connect(self.sendFunctionConfig)
        self.ui.saveButton.released.connect(self.saveCode)

    def setupPromptCombo(self):
        for k, v in TEST_PROMPTS.items():
            self.ui.prompt_combo_box.addItem(k, v)

    def updateData(self) -> None:
        self.ui.codeEdit.clear()
        self._current_function_settings = None
        return super().updateData()

    def codeChanged(self):
        self._code_edit_timer.start()
        self.enableControls(False)

    def validateCode(self):
        """Disable the text edit and validate the code entered into the text edit"""
        # disable at start and re enable after validation
        if self.ui.codeEdit.toPlainText():
            self.ui.codeEdit.setEnabled(False)
            self.ui.statusLabel.setText(COMPILING_STATUS)
            self._current_function_settings = None
            try:
                # first make sure it compiles, this is a better check than ast parsing, we don't need a return value for this
                compile(self.ui.codeEdit.toPlainText(), "<string>", "exec")
            except Exception:
                # just catch any exception
                self.ui.statusLabel.setText(COMPILE_ERROR_STATUS)
            else:
                root = ast.parse(self.ui.codeEdit.toPlainText(), "<string>")
                functions = astUtil.getFunctions(root)
                if len(functions) > 1:
                    self.ui.statusLabel.setText(TOO_MANY_FUNCTIONS_ERROR_STATUS)
                elif functions:
                    if functions[0].args.posonlyargs:
                        self.ui.statusLabel.setText(POSONLY_ARGS_ERROR_STATUS)
                    else:
                        self._current_function_settings = self.createFunctionConfig(
                            functions[0], *astUtil.getImportsUnique(root)
                        )
                        self.enableControls(True)
                        self.ui.statusLabel.setText(GOOD_STATUS)
                else:
                    self.ui.statusLabel.setText(TOO_FEW_FUNCTIONS_ERROR_STATUS)

            self.ui.codeEdit.setEnabled(True)

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
        self.ui.saveButton.setEnabled(enable)
        self.ui.selectButton.setEnabled(enable)

    def callApiButton(self):
        self.ui.codeEdit.setEnabled(False)
        self.ui.prompt_text_edit.setEnabled(False)
        system_prompt = self.ui.prompt_combo_box.currentData(
            QtCore.Qt.ItemDataRole.UserRole
        )
        user_prompt = self.ui.prompt_text_edit.toPlainText()
        cur_font = self.ui.prompt_text_edit.font()
        new_font = QtGui.QFont(cur_font)
        new_font.setPointSizeF(new_font.pointSize() * 3)
        self.ui.prompt_text_edit.setPlainText("... Generating ...")
        response = openAIUtil.getChatCompletion(system_prompt, user_prompt)
        self.ui.codeEdit.setPlainText(openAIUtil.getPythonCodeOnly(response))
        self.code_explanation.setPlainText(response)
        self.ui.codeEdit.setEnabled(True)
        self.ui.prompt_text_edit.setEnabled(True)
        self.ui.prompt_text_edit.setPlainText(user_prompt)
        self.ui.prompt_text_edit.setFont(cur_font)
