from .qtUiFiles import ui_urlTreeSelect
from .selectorBase import SelectorBase
from .highlightModel import HighlightTreeModel

from ..core.dataStructs import StreamSettings, KeyLabelPair

from ..backEnd.util import requestUtil

from PySide6 import QtWidgets, QtCore, QtGui

import typing

KEY_COLUMN = 0
LABEL_COLUMN = 1

IS_LIST_TOP_ROLE = QtCore.Qt.UserRole + 1


def recurseItem(item: QtGui.QStandardItem, value: typing.Union[dict, list, typing.Any]):
    if isinstance(value, dict):
        for key, val in value.items():
            child = QtGui.QStandardItem(str(key))
            item.appendRow(child)
            recurseItem(child, val)
    elif isinstance(value, list):
        listTop = QtGui.QStandardItem("[list]")
        listTop.setData(True, IS_LIST_TOP_ROLE)
        item.appendRow(listTop)
        for index, val in enumerate(value):
            listItem = QtGui.QStandardItem(f"[{index}]")
            listTop.appendRow(listItem)
            recurseItem(listItem, val)
    else:
        child = QtGui.QStandardItem(str(value))
        item.appendRow(child)


class UrlTreeSelect(SelectorBase):
    """
    Widget that allows for users to test a url and select what fields they want
    """

    TUTORIAL_RESOURCE_PREFIX = "None"

    def __init__(self, parent=None):
        super().__init__(self.TUTORIAL_RESOURCE_PREFIX, parent)

        # Load UI file
        self._ui = ui_urlTreeSelect.Ui_UrlTreeSelect()
        self._ui.setupUi(self)

        self._ui.outputTreeView.setMouseTracking(True)

        # Setup models for views
        self._outputTreeModel: HighlightTreeModel = HighlightTreeModel()
        self._ui.outputTreeView.setModel(self._outputTreeModel)
        self._selectedModel: QtGui.QStandardItemModel = QtGui.QStandardItemModel()
        self._selectedModel.insertColumns(0, 2)
        self._selectedModel.setHorizontalHeaderLabels(["Key", "Label"])
        self._ui.selectedTableView.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self._ui.selectedTableView.setModel(self._selectedModel)

        # connect slots
        self._ui.testButton.clicked.connect(self.testUrl)
        self._ui.outputTreeView.clicked.connect(self.treeViewItemSelected)
        self._ui.outputTreeView.entered.connect(self._outputTreeModel.changeTextColor)
        self._ui.removeButton.clicked.connect(self.removeClicked)
        self._ui.clearButton.clicked.connect(self.clearClicked)
        self._ui.expandButton.clicked.connect(self.expandClicked)
        self._ui.doneButton.clicked.connect(self.doneClicked)
        self._expanded = False
        self._columnCount: int = 1

    @QtCore.Slot()
    def testUrl(self):
        if self._ui.urlInput.text():
            urlResponse = requestUtil.getUrlData(self._ui.urlInput.text())
            self.populateModel(urlResponse)

    @QtCore.Slot()
    def removeClicked(self):
        indexes = self._ui.selectedTableView.selectionModel().selectedIndexes()
        if indexes is not None:
            for index in indexes:
                self._selectedModel.removeRow(index.row())

    @QtCore.Slot()
    def clearClicked(self):
        self._selectedModel.removeRows(0, self._selectedModel.rowCount())
        self._columnCount = 1

    def populateModel(self, data: typing.Union[typing.Dict, typing.List]) -> None:
        self._outputTreeModel.clear()
        self._selectedModel.clear()
        recurseItem(self._outputTreeModel.invisibleRootItem(), data)

    @QtCore.Slot()
    def treeViewItemSelected(self, index: QtCore.QModelIndex):
        selection = ""
        child = index
        if index is not None and index.isValid():
            if not self._outputTreeModel.hasChildren(index):
                # we don't want the leaf as those will just be values, so go up one
                child = index
                index = index.parent()
            else:
                # it's not a leaf, we don't want a mid level item so make sure it isn't
                for i in range(0, self._outputTreeModel.rowCount(index)):
                    if self._outputTreeModel.hasChildren(
                        self._outputTreeModel.index(i, 0, index)
                    ):
                        return
            while index.isValid():
                if index.data() is not None:
                    if not index.data(IS_LIST_TOP_ROLE):
                        selection = f"{index.data()}.{selection}"
                child = index
                index = index.parent()

            # now that we are done going up the tree, remove the first character then add to model
            if selection != "":
                selection = selection[:-1]
                # should now have a string like key1.key2.key3
                modelFindList = self._selectedModel.findItems(
                    selection, column=KEY_COLUMN
                )
                if len(modelFindList) == 0:
                    keyItem = QtGui.QStandardItem(selection)
                    keyItem.setEditable(False)
                    labelItem = QtGui.QStandardItem(f"col{self._columnCount}")
                    labelItem.setEditable(True)
                    self._columnCount += 1
                    self._selectedModel.appendRow([keyItem, labelItem])

    @QtCore.Slot()
    def expandClicked(self):
        if self._expanded:
            # we are currently expanded, change button to expand again
            # and collapse view
            self._ui.expandButton.setText("Expand All")
            self._ui.outputTreeView.collapseAll()
        else:
            # not expanded currently, so expand all
            # and change button to collapse
            self._ui.expandButton.setText("Collapse All")
            self._ui.outputTreeView.expandAll()

        self._expanded = not self._expanded

    @QtCore.Slot()
    def doneClicked(self):
        if self._ui.urlInput.text():
            streamSettings = StreamSettings(
                url=self._ui.urlInput.text(), key_label_list=[]
            )
            for row in range(0, self._selectedModel.rowCount()):
                streamSettings.key_label_list.append(
                    KeyLabelPair(
                        self._selectedModel.item(row, KEY_COLUMN).data(
                            QtCore.Qt.DisplayRole
                        ),
                        self._selectedModel.item(row, LABEL_COLUMN).data(
                            QtCore.Qt.DisplayRole
                        ),
                    )
                )
            self.itemSelected.emit(streamSettings)
            self.hide()

    def getTutorialClasses(self) -> typing.List:
        return [self]
