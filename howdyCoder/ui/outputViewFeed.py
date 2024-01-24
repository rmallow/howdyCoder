import typing
from .outputView import outputView
from .sparseDictListModel import SparseDictListModel

from .qtUiFiles import ui_outputViewFeed

import fnmatch

from PySide6 import QtCore, QtGui


class OutputViewFeed(outputView):
    TUTORIAL_RESOURCE_PREFIX = "OutputViewFeed"

    def __init__(self, outputViewModel, _, parent=None):
        super().__init__(outputViewModel, self.TUTORIAL_RESOURCE_PREFIX, parent)

        # Load UI file
        self._ui = ui_outputViewFeed.Ui_OutputViewFeed()
        self._ui.setupUi(self)
        self.outputViewModel: SparseDictListModel

        self.setup()
        self._ui.tableView.setModel(self.outputViewModel)
        self._ui.filterButton.clicked.connect(self.applyFilter)
        self._ui.showIndexBox.stateChanged.connect(self.outputViewModel.changeState)

        self._ui.tableView.installEventFilter(self)
        self.outputViewModel.modelUpdated.connect(self.resizeIfEnabled)
        self._ui.tableView.horizontalHeader().sectionResized.connect(
            self.resizeIfEnabled
        )
        self._ui.word_wrap_box.stateChanged.connect(self.wordWrapStateChanged)

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent):
        if (
            watched == self._ui.tableView
            and event.type() == QtCore.QEvent.Type.KeyPress
            and event.key() == QtCore.Qt.Key.Key_C
            and event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier
            and self._ui.tableView.currentIndex().isValid()
        ):
            QtGui.QGuiApplication.clipboard().setText(
                self._ui.tableView.currentIndex().data(
                    QtCore.Qt.ItemDataRole.DisplayRole
                )
            )
            return True
        return super().eventFilter(watched, event)

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

    def getTutorialClasses(self) -> typing.List:
        return [self]

    def resizeIfEnabled(self):
        if self._ui.word_wrap_box.isChecked():
            self._ui.tableView.resizeRowsToContents()

    def wordWrapStateChanged(self, state: int):
        if state == QtCore.Qt.CheckState.Checked.value:
            self._ui.tableView.resizeRowsToContents()
        else:
            for row in range(self._ui.tableView.verticalHeader().count()):
                self._ui.tableView.verticalHeader().resizeSection(
                    row, self._ui.tableView.verticalHeader().defaultSectionSize()
                )
