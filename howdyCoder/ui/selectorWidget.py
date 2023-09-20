from .selectorBase import SelectorBase
from .qtUiFiles import ui_selectorWidget

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

    @QtCore.Slot()
    def showFuncSelector(self):
        self._selector.parentIndex = self.index
        self._selector.setDefaultPrompt(self.default_prompt)
        self._selector.show()
        self._selector.showNormal()
        self._selector.setData(self.data)

    def updateText(self, text):
        self._ui.selectionLabel.setText(text)

    def updateExtraDescription(self, text):
        self._ui.extraDescriptionLabel.setText(text)

    def resetText(self):
        self._ui.selectionLabel.setText("No Item Selected")
        self._ui.extraDescriptionLabel.setText("")
