from .uiConstants import GRAPH_TYPES, GRAPH_COLORS

from .qtUiFiles import ui_graphSettingsWidget

from .qtMplPlot import graphSettings

from PySide2 import QtCore, QtWidgets
import typing


class graphSettingsWidget:
    def __init__(self):
        super().__init__()

        # Load UI files
        self._ui = ui_graphSettingsWidget.Ui_GraphSettingsWidget()
        self.mainWidget = QtWidgets.QWidget()
        self._ui.setupUi(self.mainWidget)
        # Load in the starting data
        self._ui.yMinBox.setValue(0)
        self._ui.yMaxBox.setValue(100)
        self._ui.graphTypeComboBox.setModel(QtCore.QStringListModel(GRAPH_TYPES))
        self._ui.graphColorComboBox.setModel(QtCore.QStringListModel(GRAPH_COLORS))

        # connect all the signals and slots
        self._ui.columnComboBox.textActivated.connect(self.columnComboItemSelected)
        self._ui.columnDeleteButton.clicked.connect(self.columnDeleteButtonClicked)
        self._ui.graphTypeComboBox.textActivated.connect(self.settingsChanged)
        self._ui.graphColorComboBox.textActivated.connect(self.settingsChanged)
        self._ui.yMinBox.valueChanged.connect(self.settingsChanged)
        self._ui.yMaxBox.valueChanged.connect(self.settingsChanged)
        self._ui.columnList.currentItemChanged.connect(self.currentColumnChanged)

    def columnCount(self) -> int:
        return self._ui.columnList.count()

    def getSettings(self) -> typing.List[graphSettings]:
        settingsList = []
        for x in range(0, self._ui.columnList.count()):
            settingsList.append(self._ui.columnList.item(x).data(QtCore.Qt.UserRole))
        return settingsList

    def setColumnComboBox(self, columnList: typing.List[str]) -> None:
        columnComboBoxModel = QtCore.QStringListModel(columnList)
        self._ui.columnComboBox.setModel(columnComboBoxModel)
        self._ui.columnComboBox.setCurrentIndex(-1)

    @QtCore.Slot()
    def columnComboItemSelected(self, text: str) -> None:
        findList = self._ui.columnList.findItems(text, QtCore.Qt.MatchExactly)
        if len(findList) == 0:
            item = QtWidgets.QListWidgetItem(text)
            item.setData(QtCore.Qt.UserRole, graphSettings(name=text))
            self._ui.columnList.addItem(item)
            self._ui.columnList.setCurrentItem(item)

    @QtCore.Slot()
    def columnDeleteButtonClicked(self) -> None:
        self._ui.columnList.takeItem(self._ui.columnList.currentRow())

    @QtCore.Slot()
    def settingsChanged(self, *args) -> None:
        settings: graphSettings = self._ui.columnList.currentItem().data(
            QtCore.Qt.UserRole
        )
        settings.graphType = self._ui.graphTypeComboBox.currentText()
        settings.color = self._ui.graphColorComboBox.currentText()
        settings.yMin = self._ui.yMinBox.value()
        settings.yMax = self._ui.yMaxBox.value()
        self._ui.columnList.currentItem().setData(QtCore.Qt.UserRole, settings)

    @QtCore.Slot()
    def currentColumnChanged(
        self, currentItem: QtWidgets.QListWidgetItem, *args
    ) -> None:
        settings: graphSettings = graphSettings(name="default")
        if currentItem is not None:
            settings = currentItem.data(QtCore.Qt.UserRole)
        self._ui.graphTypeComboBox.setCurrentText(settings.graphType)
        self._ui.graphColorComboBox.setCurrentText(settings.color)
        self._ui.yMinBox.setValue(settings.yMin)
        self._ui.yMaxBox.setValue(settings.yMax)
