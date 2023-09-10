import PySide6.QtGui
from .funcSelectorPageBase import FuncSelectorPageBase
from .qtUiFiles import ui_funcSelectorCodePage
from .util import qtResourceManager, expander, genericWorker

from . import librarySingleton, promptSingleton
from ..commonUtil import astUtil, keyringUtil, openAIUtil
from ..core.dataStructs import FunctionSettings

import ast
import typing

from PySide6 import QtWidgets, QtCore, QtGui

WAIT_FOR_TEXT_EDITING_TO_END = 2000

COMPILING_STATUS = "Compiling Code"
ERROR_ENCOUNTERED = "Error encountered: "
COMPILE_ERROR_STATUS = ERROR_ENCOUNTERED + "Code Compilation"
POSONLY_ARGS_ERROR_STATUS = (
    ERROR_ENCOUNTERED
    + "Remove the not allowed Positional-only argument indicator '/' in the function defenition."
)
TOO_FEW_FUNCTIONS_ERROR_STATUS = ERROR_ENCOUNTERED + "Must be at least one function"

GOOD_STATUS = "No errors found, Code good to go"


def createFunctionConfig(
    function: ast.FunctionDef,
    entry_function: str,
    imports: list,
    import_statements: list,
):
    return FunctionSettings(
        ast.unparse(function), entry_function, imports, import_statements
    )


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

        self._current_function_settings: FunctionSettings = FunctionSettings()

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

        self.hz_expander = expander.HorizontalExpander(
            self.ui.code_edit_box,
            "Explanation",
            animation_end_value=self.ui.codeEdit.sizeHint().width() // 2,
        )
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.code_explanation = QtWidgets.QPlainTextEdit(self.hz_expander.contentArea)
        self.code_explanation.setReadOnly(True)
        layout.addWidget(self.code_explanation)
        self.hz_expander.setContentLayout(layout)
        self.ui.code_edit_box.layout().addWidget(self.hz_expander, 1)
        self.resize

        self.ui.selectButton.released.connect(self.sendFunctionConfig)
        self.ui.saveButton.released.connect(self.saveCode)

    def setupPromptCombo(self):
        for k, v in promptSingleton.prompts.items():
            self.ui.prompt_combo_box.addItem(k, v)

    def updateData(self) -> None:
        self.ui.codeEdit.clear()
        self._current_function_settings = FunctionSettings()
        self.ui.prompt_text_edit.clear()
        self.ui.entry_function_edit.clear()
        self.code_explanation.clear()
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
                if functions:
                    if functions[0].args.posonlyargs:
                        self.ui.statusLabel.setText(POSONLY_ARGS_ERROR_STATUS)
                    else:
                        self._current_function_settings = createFunctionConfig(
                            functions[0],
                            self.ui.entry_function_edit.text(),
                            *astUtil.getImportsUnique(root),
                        )
                        self.enableControls(True)
                        self.ui.statusLabel.setText(GOOD_STATUS)
                else:
                    self.ui.statusLabel.setText(TOO_FEW_FUNCTIONS_ERROR_STATUS)

            self.ui.codeEdit.setEnabled(True)

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
        self.ui.call_api_button.setEnabled(False)
        system_prompt = self.ui.prompt_combo_box.currentData(
            QtCore.Qt.ItemDataRole.UserRole
        )
        self.user_prompt = self.ui.prompt_text_edit.toPlainText()
        self.ui.prompt_text_edit.setPlainText("... Generating, Please Wait ...")
        self.thread, self.worker = genericWorker.createThreadAndWorker(
            openAIUtil.getChatCompletion,
            self.apiResponse,
            system_prompt,
            self.user_prompt,
        )

    def apiResponse(self, response: str):
        self.ui.codeEdit.setPlainText(openAIUtil.getPythonCodeOnly(response))
        self.code_explanation.setPlainText(response)
        self.ui.codeEdit.setEnabled(True)
        self.ui.prompt_text_edit.setEnabled(True)
        self.ui.call_api_button.setEnabled(True)
        self.ui.prompt_text_edit.setPlainText(self.user_prompt)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        """Setting how far out the explanation box should expand to"""
        ret_val = super().resizeEvent(event)
        self.hz_expander.setContentLayoutAnimationEndValue(
            self.ui.code_edit_box.size().width() // 2
        )
        return ret_val

    def setDefaultPrompt(self, prompt_name: str):
        """Not a case sensitive search"""
        index = self.ui.prompt_combo_box.findText(
            prompt_name, QtCore.Qt.MatchFlag.MatchFixedString
        )
        assert index != -1, f"Could not find prompt by this name: {prompt_name}"
        self.ui.prompt_combo_box.setCurrentIndex(index)
