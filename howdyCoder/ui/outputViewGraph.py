import typing
from .outputView import outputView
from .qtMplPlot import qtMplPlot

from .qtUiFiles import ui_outputViewGraph

from ..core.commonGlobals import PERIOD, GRAPH_SETTINGS

from PySide6 import QtCore, QtWidgets


class outputViewGraph(outputView):
    TUTORIAL_RESOURCE_PREFIX = "None"

    def __init__(self, outputViewModel, selectionSettings, parent=None):
        super().__init__(outputViewModel, self.TUTORIAL_RESOURCE_PREFIX, parent)

        # Load UI file
        self._ui = ui_outputViewGraph.Ui_OutputViewGraph()
        self._ui.setupUi(self)

        self.setup()
        self.model = outputViewModel
        self.layout = QtWidgets.QVBoxLayout()
        self._ui.itemFrame.setLayout(self.layout)
        self.plot = qtMplPlot(
            xLen=selectionSettings[PERIOD],
            model=self.model,
            settings=selectionSettings[GRAPH_SETTINGS],
        )
        self.plot.resize(300, 300)
        self.layout.addWidget(self.plot)

    def getTutorialClasses(self) -> typing.List:
        return [self]
