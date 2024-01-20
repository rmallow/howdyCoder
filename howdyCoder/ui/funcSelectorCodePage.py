from .funcSelectorPageBase import FuncSelectorPageBase
from .qtUiFiles import ui_funcSelectorCodePage
from .util import expander, genericWorker

from . import promptSingleton
from ..commonUtil import astUtil, openAIUtil
from ..core.dataStructs import FunctionSettings
from ..core import libraryBase

import ast
import typing

from PySide6 import QtWidgets, QtCore, QtGui

WAIT_FOR_TEXT_EDITING_TO_END = 2000

CODE_GENERATION_TIMEOUT = 45000

COMPILING_STATUS = "Compiling Code"
ERROR_ENCOUNTERED = "Error encountered: "
COMPILE_ERROR_STATUS = ERROR_ENCOUNTERED + "Code Compilation"
POSONLY_ARGS_ERROR_STATUS = (
    ERROR_ENCOUNTERED
    + "Remove the not allowed Positional-only argument indicator '/' in the function defenition."
)
TOO_FEW_FUNCTIONS_ERROR_STATUS = ERROR_ENCOUNTERED + "Must be at least one function"

GOOD_STATUS = "No errors found, Code good to go"

OUTPUT_TEXT = "output:"

PROMPT_ERROR_MSG = (
    "Error encountered trying to generate code, please try again in a bit."
)

RESERVED_KEY_WORDS = set(["entry", "output", "setup"])


def getSuggestedOutput(response):
    start = response.lower().find(OUTPUT_TEXT)
    end = len(response)
    if start != -1:
        for x in range(start + len(OUTPUT_TEXT), len(response)):
            if response[x] == "\n" or response[x] == ".":
                end = x
                break
        if output := response[start + len(OUTPUT_TEXT) : end].strip():
            return [o.strip() for o in output.split(",")]
    return []


def createSetupString(settings: FunctionSettings) -> str:
    return f"\nsetup:" + "\n".join(
        [f"{v} : {k}" for k, v in settings.internal_setup_functions.items()]
    )


def createFunctionConfig(
    functions: typing.List[ast.FunctionDef],
    entry_function: str,
    imports: list,
    import_statements: list,
    internal_setup_functions: dict,
    suggested_output=None,
):
    return FunctionSettings(
        "\n\n".join([ast.unparse(function) for function in functions]),
        entry_function,
        imports,
        import_statements,
        None,
        suggested_output if suggested_output is not None else [],
        internal_setup_functions if internal_setup_functions is not None else {},
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
        self.valid_code = False

        self.ui.key_monitor_widget.watchKey(openAIUtil.OPEN_AI_KEY_DATA_NAME)
        self.ui.key_monitor_widget.allKeysValid.connect(self.enableAPIControls)

        cur_val = openAIUtil.testValidKeySet()
        self.ui.prompt_box.setVisible(cur_val)
        self.ui.create_new_api_button.setEnabled(cur_val)

        self.setupPromptCombo()

        self.ui.create_new_api_button.released.connect(self.createNewAPIButton)
        self.ui.modify_api_button.released.connect(self.modifyAPIButton)
        self._code_edit_timer = QtCore.QTimer()
        self._code_edit_timer.setSingleShot(True)
        self._code_edit_timer.setInterval(WAIT_FOR_TEXT_EDITING_TO_END)
        self._code_edit_timer.timeout.connect(self.validateCode)
        self.ui.codeEdit.textChanged.connect(self.codeChanged)
        self.ui.entry_function_edit.textChanged.connect(self.entryFunctionChanged)

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

        self.ui.selectButton.released.connect(self.sendFunctionConfig)
        self.ui.saveButton.released.connect(self.saveCode)

        self._saved_query = ""
        self._current_api_call_id = 0
        self._generate_code_timer = QtCore.QTimer()
        self._generate_code_timer.setSingleShot(True)
        self._generate_code_timer.setInterval(CODE_GENERATION_TIMEOUT)
        self._generate_code_timer.timeout.connect(self.codeGenerationTimeout)
        self.ui.prompt_user_manual_button.released.connect(
            lambda: QtGui.QDesktopServices.openUrl(
                QtCore.QUrl("https://howdycoder.io/docs/prompts.html")
            )
        )
        self.ui.prompt_copy_button.released.connect(self.copyPromptToClipboard)
        self._internal_setup_funcs = {}

        self.api_success = False

    def setupPromptCombo(self):
        for k in promptSingleton.prompts.keys():
            self.ui.prompt_combo_box.addItem(k)

    def copyPromptToClipboard(self):
        clippy = QtGui.QGuiApplication.clipboard()
        if self.ui.prompt_combo_box.currentText() in promptSingleton.prompts:
            clippy.setText(
                promptSingleton.makeOnlinePrompt(self.ui.prompt_combo_box.currentText())
            )

    def updateData(self) -> None:
        self.ui.codeEdit.clear()
        self._current_function_settings = FunctionSettings()
        self.ui.prompt_text_edit.clear()
        self.ui.entry_function_edit.clear()
        self.code_explanation.clear()
        self._internal_setup_funcs = {}
        return super().updateData()

    def codeChanged(self):
        self._code_edit_timer.start()
        self.enableControls(False)

    def setEntryFunction(self):
        if len(self._current_functions) == 1:
            self.ui.entry_function_edit.setText(self._current_functions[0].name)
            self.ui.entry_function_edit.setEnabled(False)
        else:
            func_name = self._current_functions[-1].name
            index = self.code_explanation.toPlainText().find("entry:")
            if index != -1:
                new_line = self.code_explanation.toPlainText().find("\n", index)
                potential_name = self.code_explanation.toPlainText()[
                    index + len("entry:") : new_line
                ].strip()
                if any(f.name == potential_name for f in self._current_functions):
                    func_name = potential_name
            self.ui.entry_function_edit.setText(func_name)
            self.ui.entry_function_edit.setEnabled(True)

    def setSetupFunctions(self):
        self._internal_setup_funcs = {}
        text = self.code_explanation.toPlainText()
        index = text.find("setup:")
        last = index + len("setup:")
        if index != -1:
            colon_index = text.find(":", last)
            while colon_index != -1:
                first_word = text[last:colon_index].split()[-1].strip()
                new_line = text.find("\n", colon_index)
                end = len(text)
                char_found = False
                for x in range(colon_index + 1, len(text)):
                    if not text[x].isspace():
                        char_found = True
                    elif char_found:
                        end = x
                        break
                func_name = text[colon_index + 1 : end].strip()
                if (
                    any(c.isspace() for c in first_word)
                    or first_word in RESERVED_KEY_WORDS
                    or any(c.isspace() for c in func_name)
                    or func_name in RESERVED_KEY_WORDS
                    or not self.nameInCurrentFunctions(func_name)
                ):
                    break
                self._internal_setup_funcs[func_name] = first_word
                last = new_line + 1
                colon_index = text.find(":", last)

    def validateCode(self):
        """Disable the text edit and validate the code entered into the text edit"""
        if self.ui.codeEdit.toPlainText():
            # if it's the full response copy and pasted then parse that first
            if self.ui.codeEdit.toPlainText().find(openAIUtil.PYTHON_SEARCH) != -1:
                self.parseAIResponse(self.ui.codeEdit.toPlainText())
                return
            # disable at start and re enable after validation
            self.ui.codeEdit.setEnabled(False)
            self.ui.entry_function_edit.setEnabled(False)
            self.ui.statusLabel.setText(COMPILING_STATUS)
            self._current_function_settings = FunctionSettings()
            self._current_functions = []
            self.valid_code = False
            try:
                # first make sure it compiles, this is a better check than ast parsing, we don't need a return value for this
                compile(self.ui.codeEdit.toPlainText(), "<string>", "exec")
            except Exception:
                # just catch any exception
                self.ui.statusLabel.setText(COMPILE_ERROR_STATUS)
            else:
                root = ast.parse(self.ui.codeEdit.toPlainText(), "<string>")
                self._current_functions = astUtil.getFunctions(root)
                if self._current_functions:
                    if self._current_functions[0].args.posonlyargs:
                        self.ui.statusLabel.setText(POSONLY_ARGS_ERROR_STATUS)
                    else:
                        self.setEntryFunction()
                        self.setSetupFunctions()
                        self._current_function_settings = createFunctionConfig(
                            self._current_functions,
                            self.ui.entry_function_edit.text(),
                            *astUtil.getImportsUnique(root),
                            self._internal_setup_funcs,
                        )
                        self.addSuggestedOutput()
                        self.valid_code = True
                        self.enableControls(True)
                        self.enableAPIControls(self.ui.key_monitor_widget.all_valid)
                        self.ui.statusLabel.setText(GOOD_STATUS)
                else:
                    self.ui.statusLabel.setText(TOO_FEW_FUNCTIONS_ERROR_STATUS)

            self.ui.codeEdit.setEnabled(True)
            self.ui.entry_function_edit.setEnabled(True)

    @QtCore.Slot()
    def sendFunctionConfig(self):
        self.validateSetupFunctionsExist()
        self.funcSelected.emit(self._current_function_settings)

    @QtCore.Slot()
    def saveCode(self):
        self.validateSetupFunctionsExist()
        """Save a function in the code edit to either an exisiting AFL file or a new AFL file"""
        file_dlg_return = QtWidgets.QFileDialog.getSaveFileName(
            self, "Select an Algo Function Library", ".", "Algo Function Library(*.afl)"
        )
        if file_dlg_return and file_dlg_return[0]:
            libraryBase.saveToLibrary(
                file_dlg_return[0], self._current_function_settings
            )

    def enableControls(self, enable: bool):
        self.ui.saveButton.setEnabled(enable)
        self.ui.selectButton.setEnabled(enable)

    @QtCore.Slot()
    def enableAPIControls(self, enable: bool):
        self.ui.prompt_box.setVisible(False)
        self.ui.create_new_api_button.setEnabled(
            enable and not self._generate_code_timer.isActive()
        )
        self.ui.modify_api_button.setEnabled(
            enable and self.valid_code and self.ui.create_new_api_button.isEnabled()
        )

    def callAPI(self, system_prompt: str, user_prompt: str) -> None:
        self._generate_code_timer.stop()
        self.api_success = False
        self.enableControls(False)
        self.ui.prompt_error.setText("")
        self.ui.codeEdit.setEnabled(False)
        self.ui.prompt_text_edit.setEnabled(False)
        self.ui.create_new_api_button.setEnabled(False)
        self.ui.modify_api_button.setEnabled(False)
        self._saved_query = self.ui.prompt_text_edit.toPlainText()
        self.ui.prompt_text_edit.setPlainText("... Generating, Please Wait ...")
        self._current_api_call_id += 1
        runnable = genericWorker.GenericRunnable(
            self._current_api_call_id,
            openAIUtil.getChatCompletion,
            system_prompt,
            user_prompt,
        )
        runnable.signals.finished.connect(self.apiResponse)
        QtCore.QThreadPool.globalInstance().start(runnable, self._current_api_call_id)
        self._generate_code_timer.start()

    def codeGenerationTimeout(self):
        if not self.api_success:
            self._current_api_call_id += 1
            self.ui.prompt_error.setText(PROMPT_ERROR_MSG)
            self.ui.prompt_text_edit.setPlainText(self._saved_query)
            self.ui.codeEdit.setEnabled(True)
            self.ui.prompt_text_edit.setEnabled(True)
            self.ui.create_new_api_button.setEnabled(True)

    def createNewAPIButton(self):
        user_prompt = self.ui.prompt_text_edit.toPlainText()
        self.callAPI(
            promptSingleton.getPrompt(self.ui.prompt_combo_box.currentText()),
            user_prompt,
        )

    def modifyAPIButton(self):
        user_prompt = self.ui.prompt_text_edit.toPlainText()
        code = self.ui.codeEdit.toPlainText()
        full_user_prompt = (
            f"{user_prompt}\n{code}\nentry:{self._current_function_settings.name}"
        )
        if self._current_function_settings.internal_setup_functions:
            full_user_prompt += createSetupString(self._current_function_settings)
        if self._current_function_settings.suggested_output:
            full_user_prompt += f"\noutput:" + ",".join(
                self._current_function_settings.suggested_output
            )
        self.callAPI(
            promptSingleton.makeModifyPrompt(self.ui.prompt_combo_box.currentText()),
            full_user_prompt,
        )

    def apiResponse(self, response: genericWorker.RunnableReturn):
        """This will be called from another thread"""
        if response is not None and response.id_ == self._current_api_call_id:
            self.api_success = True
            if response.value is not None:
                self.parseAIResponse(response.value)
            else:
                self.ui.prompt_error.setText(PROMPT_ERROR_MSG)
            self.ui.codeEdit.setEnabled(True)
            self.ui.prompt_text_edit.setEnabled(True)
            self.ui.create_new_api_button.setEnabled(True)
            self.ui.prompt_text_edit.setPlainText(self._saved_query)

    def parseAIResponse(self, ai_response: str) -> None:
        if ai_response:
            self.ui.codeEdit.setPlainText(openAIUtil.getPythonCodeOnly(ai_response))
            self.code_explanation.setPlainText(ai_response)
            self.ui.prompt_error.setText("")

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

    def entryFunctionChanged(self, new_text):
        if self.valid_code and any(new_text == f.name for f in self._current_functions):
            self._current_function_settings.name = new_text
            self.enableControls(True)
        else:
            self.enableControls(False)

    def setData(self, data: typing.Any):
        if data is not None and isinstance(data, FunctionSettings):
            full_code = "\n".join(data.import_statements) + "\n\n" + data.code
            setup_text = createSetupString(data)
            self.code_explanation.setPlainText(setup_text)
            self.ui.codeEdit.setPlainText(full_code)
            self.validateCode()
            self.ui.entry_function_edit.setText(data.name)
            self._current_function_settings.internal_setup_functions = (
                data.internal_setup_functions
            )

    def addSuggestedOutput(self):
        response = self.code_explanation.toPlainText()
        self._current_function_settings.suggested_output = getSuggestedOutput(response)

    def validateSetupFunctionsExist(self):
        for function_name in list(
            self._current_function_settings.internal_setup_functions.keys()
        ):
            if not any(f.name == function_name for f in self._current_functions):
                del self._current_function_settings.internal_setup_functions[
                    function_name
                ]

    def nameInCurrentFunctions(self, func_name):
        for func in self._current_functions:
            if func.name == func_name:
                return True
        return False

    def reset(self):
        self.ui.codeEdit.clear()
        self.ui.entry_function_edit.clear()
        self.ui.prompt_text_edit.clear()
