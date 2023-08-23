from .actionUIConstant import ActionFuncEnum
from .qtUiFiles import ui_funcSelector
from .selectorBase import SelectorBase
from .funcSelectorPageBase import FuncSelectorPageBase

import typing

from PySide6 import QtCore


class FuncSelector(SelectorBase):
    """
    Dialog with widget selection pages
    """

    TUTORIAL_RESOURCE_PREFIX = "test"

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
            ).funcSelected.connect(self.addParentIndex)

    def show(self):
        """Called when window should be showed, so we update data on sub pages"""
        for x in range(self._ui.tabWidget.count()):
            # to avoid cranky qt layout error, the child widget is inside the tab
            self._ui.tabWidget.widget(x).findChild(FuncSelectorPageBase).updateData()

    @QtCore.Slot()
    def addParentIndex(self, func_config_dict):
        if self.parentIndex is not None:
            func_config_dict[ActionFuncEnum.INDEX] = self.parentIndex
        self.itemSelected.emit(func_config_dict)
        # if we're emitting this, we're done selecting so we can hide now
        self.hide()

    def getTutorialClasses(self) -> typing.List:
        return [self]
