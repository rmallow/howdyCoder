from .qtUiFiles import ui_funcSelector
from .selectorBase import SelectorBase
from .funcSelectorPageBase import FuncSelectorPageBase
from ..commonUtil import astUtil

from ..core.dataStructs import FunctionSettings

import typing
import ast
from dataclasses import dataclass, field

from PySide6 import QtCore


@dataclass
class FunctionSettingsWithHelperData:
    function_settings: FunctionSettings = FunctionSettings()
    index: QtCore.QModelIndex = None
    suggested_parameters: typing.List[str] = field(default_factory=list)


class FuncSelector(SelectorBase):
    """
    Dialog with widget selection pages
    """

    TUTORIAL_RESOURCE_PREFIX = "FuncSelector"

    def __init__(self, parent=None):
        super().__init__(self.TUTORIAL_RESOURCE_PREFIX, parent)
        # set always on top flag
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        # Load UI file and setup UI with layout
        self._ui = ui_funcSelector.Ui_FuncSelector()
        self._ui.setupUi(self)

        self.parentIndex = None
        for x in range(self._ui.tabWidget.count()):
            # to avoid cranky qt layout error, the child widget is inside the tab
            self._ui.tabWidget.widget(x).findChild(
                FuncSelectorPageBase
            ).funcSelected.connect(self.addHelperData)

    def show(self):
        """Called when window should be showed, so we update data on sub pages"""
        for x in range(self._ui.tabWidget.count()):
            # to avoid cranky qt layout error, the child widget is inside the tab
            self._ui.tabWidget.widget(x).findChild(FuncSelectorPageBase).updateData()

    @QtCore.Slot()
    def addHelperData(self, function_settings: FunctionSettings):
        settings_with_index = FunctionSettingsWithHelperData(
            function_settings,
            self.parentIndex,
            astUtil.getSuggestedParameterNames(
                ast.parse(function_settings.code, "<string>")
            ),
        )
        self.itemSelected.emit(settings_with_index)
        # if we're emitting this, we're done selecting so we can hide now
        self.hide()

    def getTutorialClasses(self) -> typing.List:
        return [self] + self._ui.tabWidget.currentWidget().findChild(
            FuncSelectorPageBase
        ).getTutorialClasses()
