from .outputView import outputView
from .sparseDictListModel import SparseDictListModel

from .qtUiFiles.ui_outputViewPrinted import Ui_OutputViewPrinted

import fnmatch
import typing

from PySide6 import QtGui


class OutputViewPrinted(outputView):
    TUTORIAL_RESOURCE_PREFIX = "None"

    def __init__(self, outputViewModel, _, parent=None):
        super().__init__(outputViewModel, self.TUTORIAL_RESOURCE_PREFIX, parent)

        # Load UI file
        self._ui = Ui_OutputViewPrinted()
        self._ui.setupUi(self)
        self.outputViewModel: QtGui.QStandardItemModel

        self._ui.list_view.setModel(outputViewModel)

        self.setup()

    def getTutorialClasses(self) -> typing.List:
        return [self]
