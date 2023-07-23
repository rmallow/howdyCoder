from .outputSelect import outputSelect
from .outputViewFeed import outputViewFeed
from .outputViewGraph import outputViewGraph
from .uiConstants import outputTypesEnum
from .mainOutputViewModel import mainOutputViewModel

from .util import animations

from ..core.commonGlobals import TYPE, ITEM
from ..commonUtil import mpLogging

from PySide6 import QtWidgets, QtCore


class mainOutputView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainOutputViewModel: mainOutputViewModel = mainOutputViewModel(self)

        """
        Set up the UI, no UI file to load but it will be:
        layout
            selector
            main window
                dock widgets
        """
        self._title_set = set()
        self._outer_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self._outer_layout)
        self._outer_layout.setSpacing(0)

        selector = outputSelect(self.mainOutputViewModel)
        selector.selectionFinished.connect(self.onSelectionFinished)
        self._outer_layout.addWidget(selector)

        self._sub_main_window = QtWidgets.QMainWindow()
        w = QtWidgets.QWidget(self._sub_main_window)
        w.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        self._sub_main_window.setCentralWidget(w)
        self._sub_main_window.setDockNestingEnabled(True)
        self._outer_layout.addWidget(self._sub_main_window)

    @QtCore.Slot()
    def onSelectionFinished(self, selectionSettings):
        """
        Output select is finished, send settings to mainOutputViewModel to translate to message
        """
        outputViewModel = self.mainOutputViewModel.setupOutputView(selectionSettings)
        oView = None
        x = 1
        title = f"{selectionSettings[ITEM]} - {selectionSettings[TYPE]}{x}"
        while title in self._title_set:
            x += 1
            title = f"{selectionSettings[ITEM]} - {selectionSettings[TYPE]}{x}"
        self._title_set.add(title)
        dock = QtWidgets.QDockWidget(title, self._sub_main_window)
        if selectionSettings[TYPE] == outputTypesEnum.FEED.value:
            oView = outputViewFeed(outputViewModel, selectionSettings, dock)
        elif selectionSettings[TYPE] == outputTypesEnum.GRAPH.value:
            oView = outputViewGraph(outputViewModel, selectionSettings, dock)
            oView.setMaximumSize(
                int(self.scrollArea.width() * 0.7),
                int(self.scrollArea.height() * 0.7),
            )

        selector = outputSelect(self.mainOutputViewModel, self)
        selector.selectionFinished.connect(self.onSelectionFinished)

        animations.fadeStart(self, self.sender(), selector, self._outer_layout)

        if oView is not None:
            dock.setWidget(oView)
            self._sub_main_window.addDockWidget(
                QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, dock
            )
        else:
            mpLogging.error("Output View was supposed to be made but was not")
