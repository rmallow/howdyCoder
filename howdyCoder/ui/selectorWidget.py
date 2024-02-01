from .selectorBase import SelectorBase
from .qtUiFiles import ui_selectorWidget

from .util.helperData import FunctionSettingsWithHelperData, PathWithHelperData

import typing

from PySide6 import QtCore, QtWidgets


class SelectorWidget(QtWidgets.QWidget):
    def __init__(
        self,
        index: QtCore.QModelIndex,
        selector: SelectorBase,
        parent: QtWidgets.QWidget,
        default_prompt="Parameter Setup Func",
    ):
        super().__init__(parent)
        # Load UI file and setup UI
        self._ui = ui_selectorWidget.Ui_SelectorWidget()
        self._ui.setupUi(self)

        self._selector: SelectorBase = selector
        self._ui.selectorButton.pressed.connect(self.showFuncSelector)
        self.index = index
        self.default_prompt = default_prompt
        self.data = None
        self._selector.itemSelected.connect(self.itemSelected)

    @QtCore.Slot()
    def showFuncSelector(self):
        self._selector.parentIndex = self.index
        self._selector.setDefaultPrompt(self.default_prompt)
        self._selector.show()
        self._selector.showNormal()
        self._selector.raise_()
        self._selector.activateWindow()
        self._selector.setData(self.data)

    def updateText(self, text):
        self._ui.selectionLabel.setText(text)

    def updateExtraDescription(self, text):
        self._ui.extraDescriptionLabel.setText(text)

    def resetText(self):
        self._ui.selectionLabel.setText("No Item Selected")
        self._ui.extraDescriptionLabel.setText("")

    def reset(self):
        self.resetText()
        self._selector.reset()
        self._selector_data = None

    def itemSelected(self, settings: typing.Any):
        if isinstance(settings, FunctionSettingsWithHelperData):
            label = settings.function_settings.name
            self.data = settings.function_settings
        elif isinstance(settings, PathWithHelperData):
            label = settings.path
            self.data = settings.path

        self._ui.selectionLabel.setText(label)

    def getSelectedData(self) -> typing.Any:
        return self.data
