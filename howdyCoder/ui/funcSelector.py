from .qtUiFiles import ui_funcSelector
from .selectorBase import SelectorBase
from .funcSelectorPageBase import FuncSelectorPageBase

from .util import helperData

from ..core.dataStructs import FunctionSettings

import typing


from PySide6 import QtCore


class FuncSelector(SelectorBase):
    """
    Dialog with widget selection pages
    """

    TUTORIAL_RESOURCE_PREFIX = "FuncSelector"

    def __init__(self, parent=None):
        super().__init__(self.TUTORIAL_RESOURCE_PREFIX, parent)
        # Load UI file and setup UI with layout
        self.ui = ui_funcSelector.Ui_FuncSelector()
        self.ui.setupUi(self)
        self.embedded = False

        self.parentIndex = None
        self.applyToPages(
            lambda page: page.funcSelected.connect(self.addHelperDataWithIndex)
        )

    def applyToPages(self, function):
        for x in range(self.ui.tabWidget.count()):
            # to avoid cranky qt layout error, the child widget is inside the tab
            function(self.ui.tabWidget.widget(x).findChild(FuncSelectorPageBase))

    def updateChildData(self):
        self.applyToPages(lambda page: page.updateData())

    def show(self):
        """Called when window should be showed, so we update data on sub pages"""
        self.updateChildData()
        return super().show()

    @QtCore.Slot()
    def addHelperDataWithIndex(self, function_settings: FunctionSettings):
        settings_with_index = helperData.addHelperData(function_settings)
        settings_with_index.index = self.parentIndex
        self.itemSelected.emit(settings_with_index)
        # if we're emitting this, we're done selecting so we can hide now
        if not self.embedded:
            self.hide()

    def getTutorialClasses(self) -> typing.List:
        return [self] + self.ui.tabWidget.currentWidget().findChild(
            FuncSelectorPageBase
        ).getTutorialClasses()

    def setDefaultPrompt(self, prompt_name: str) -> None:
        self.applyToPages(lambda page: page.setDefaultPrompt(prompt_name))

    def setData(self, data: typing.Any) -> None:
        self.applyToPages(lambda page: page.setData(data))

    def reset(self) -> None:
        self.applyToPages(lambda page: page.reset())
