from .outputView import outputView
from .sparseDictListModel import SparseDictListModel

from .qtUiFiles import ui_outputViewFeed

import fnmatch

from PySide2 import QtCore


class outputViewFeed(outputView):
    def __init__(self, outputViewModel, selectionSettings, parent=None):
        super().__init__(outputViewModel, parent)

        # Load UI file
        self._ui = ui_outputViewFeed.Ui_OutputViewFeed()
        self._ui.setupUi(self)
        self.outputViewModel: SparseDictListModel

        self.setup()
        self._ui.tableView.setModel(self.outputViewModel)
        self._ui.filterButton.clicked.connect(self.applyFilter)
        self._ui.showIndexBox.stateChanged.connect(self.outputViewModel.changeState)

    @QtCore.Slot()
    def updateOnLoad(self):
        pass

    @QtCore.Slot()
    def applyFilter(self, _) -> None:
        """
        Apply filter button has been hit so we will apply the filter to the ouput view model
        """
        pattern = self._ui.filterEdit.text()
        # line edit filter has changed so we update filter on model
        for i in range(0, self.outputViewModel.columnCount()):
            showColumn = True
            # if there is no pattern, show all columns
            if pattern != "":
                name = self.outputViewModel.headerData(
                    i, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole
                )
                showColumn = fnmatch.fnmatch(name, pattern)

            if showColumn:
                self._ui.tableView.showColumn(i)
            else:
                self._ui.tableView.hideColumn(i)
