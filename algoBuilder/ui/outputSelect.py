from .qtUiFiles import ui_outputSelectItem, ui_outputSelectType, ui_outputSelectSettings

from .graphSettingsWidget import graphSettingsWidget

from .uiConstants import outputTypesEnum

from .util import animations

from ..core.commonGlobals import TYPE, ITEM, PERIOD, BACKTRACK, GRAPH_SETTINGS

from PySide6 import QtWidgets, QtCore


class outputSelect(QtWidgets.QWidget):
    selectionFinished = QtCore.Signal(dict)

    def __init__(self, model, parent=None):
        super().__init__(parent=parent)

        self.model = model
        # Load select item UI
        self._selectItemUI = ui_outputSelectItem.Ui_OutputSelectItem()
        self._selectItemWidget = QtWidgets.QWidget()
        self._selectItemUI.setupUi(self._selectItemWidget)
        # handlers aren't currently supported but don't want to remove code pertaining to them
        self._selectItemUI.handlerBox.setHidden(True)

        # Load select type UI
        self._selectTypeUI = ui_outputSelectType.Ui_OutputSelectType()
        self._selectTypeWidget = QtWidgets.QWidget()
        self._selectTypeUI.setupUi(self._selectTypeWidget)

        # Load select settings UI
        self._selectSettingsUI = ui_outputSelectSettings.Ui_OutputSelectSettings()
        self._selectSettingsWidget = QtWidgets.QWidget()
        self._selectSettingsUI.setupUi(self._selectSettingsWidget)

        self.graphSettingsWidget: graphSettingsWidget = graphSettingsWidget()

        self.selectionSettings = {}
        self.columnNames = []

        self.initSelectItem()
        self.initSelectType()
        self.initSelectSettings()

        self.mainLayout = QtWidgets.QVBoxLayout()

        self.backButtonSetup()

        self.mainLayout.addWidget(self._selectItemWidget)
        self.mainLayout.setSpacing(0)

        self.setLayout(self.mainLayout)
        self.show()

        self.item = None
        self.isBlockItem = False
        self.outputType = None

        self._selectSettingsUI.typeSpecificStackedWidget.addWidget(
            self.graphSettingsWidget.mainWidget
        )

    def resetHandlerModel(self):
        self._selectItemUI.handlerComboBox.setCurrentIndex(-1)

    def resetBlockModel(self):
        self._selectItemUI.blockComboBox.setCurrentIndex(-1)

    def initSelectItem(self):
        self._selectItemUI.blockComboBox.setModel(self.model.blockComboModel)
        self.resetBlockModel()
        self._selectItemUI.blockComboBox.textActivated.connect(self.itemSelected)
        self.model.blockComboModel.rowsInserted.connect(self.resetBlockModel)
        self.model.blockComboModel.rowsRemoved.connect(self.resetBlockModel)

        self._selectItemUI.handlerComboBox.setModel(self.model.handlerComboModel)
        self.resetHandlerModel()
        self._selectItemUI.handlerComboBox.textActivated.connect(self.itemSelected)
        self.model.handlerComboModel.rowsInserted.connect(self.resetHandlerModel)
        self.model.handlerComboModel.rowsRemoved.connect(self.resetHandlerModel)

    def initSelectType(self):
        self._selectTypeUI.typeComboBox.setModel(self.model.typeModel)
        self._selectTypeUI.typeComboBox.setCurrentIndex(-1)
        self._selectTypeUI.typeComboBox.textActivated.connect(self.typeSelected)

    def initSelectSettings(self):
        self._selectSettingsUI.acceptButton.clicked.connect(self.settingsSelected)

    def backButtonSetup(self):
        backWidget = QtWidgets.QWidget(self)
        backLayout = QtWidgets.QHBoxLayout()
        # Unicode for a left arrow U+2190
        self.backButton = QtWidgets.QPushButton("\u2190", backWidget)
        self.backButton.clicked.connect(self.backButtonClicked)
        backLayout.addWidget(self.backButton)
        backLayout.addSpacerItem(
            QtWidgets.QSpacerItem(
                0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
            )
        )
        backWidget.setLayout(backLayout)
        backWidget.setSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum
        )
        self.mainLayout.addWidget(backWidget)

    def backButtonClicked(self):
        if self.mainLayout.indexOf(self._selectItemWidget) != -1:
            pass
        elif self.mainLayout.indexOf(self._selectTypeWidget) != -1:
            self.selectionSettings = {}
            animations.fadeStart(
                self, self._selectTypeWidget, self._selectItemWidget, self.mainLayout
            )
        elif self.mainLayout.indexOf(self._selectSettingsWidget) != -1:
            animations.fadeStart(
                self,
                self._selectSettingsWidget,
                self._selectTypeWidget,
                self.mainLayout,
            )

    @QtCore.Slot()
    def itemSelected(self, text):
        self.item = text
        self.isBlockItem = "block" in self.sender().objectName()

        if self.isBlockItem:
            self._selectTypeUI.itemLabel.setText("Block: " + str(self.item))
            self._selectItemUI.handlerComboBox.setCurrentIndex(-1)
            index = self._selectItemUI.blockComboBox.currentIndex()
            self.columnNames = self.model.blockComboModel.item(index).data()
        else:
            self._selectTypeUI.itemLabel.setText("Handler: " + str(self.item))
            self._selectItemUI.blockComboBox.setCurrentIndex(-1)

        self.selectionSettings[ITEM] = text
        animations.fadeStart(
            self, self._selectItemWidget, self._selectTypeWidget, self.mainLayout
        )

    @QtCore.Slot()
    def typeSelected(self, text):
        self.selectionSettings[TYPE] = text
        if text == outputTypesEnum.GRAPH.value:
            self.graphSettingsWidget.setColumnComboBox(self.columnNames)
            self._selectSettingsUI.typeSpecificStackedWidget.setCurrentWidget(
                self.graphSettingsWidget.mainWidget
            )
            self._selectSettingsUI.typeSpecificStackedWidget.show()
        else:
            self._selectSettingsUI.typeSpecificStackedWidget.hide()
        animations.fadeStart(
            self, self._selectTypeWidget, self._selectSettingsWidget, self.mainLayout
        )

    @QtCore.Slot()
    def settingsSelected(self):
        if self.areSettingsValid():
            self.selectionSettings[
                PERIOD
            ] = self._selectSettingsUI.periodSpinBox.value()
            self.selectionSettings[BACKTRACK] = min(
                self.selectionSettings[PERIOD],
                self._selectSettingsUI.backtrackSpinBox.value(),
            )
            if self.selectionSettings[TYPE] == outputTypesEnum.GRAPH.value:
                self.selectionSettings[
                    GRAPH_SETTINGS
                ] = self.graphSettingsWidget.getSettings()
            self.selectionFinished.emit(self.selectionSettings)

    def areSettingsValid(self):
        isValid = True
        if self.selectionSettings[TYPE] == outputTypesEnum.GRAPH.value:
            if self.graphSettingsWidget.columnCount() == 0:
                self._selectSettingsUI.errorLabel.setText(
                    "Error: Select at least one column"
                )
                isValid = False
        elif self.selectionSettings[TYPE] == outputTypesEnum.FEED.value:
            pass

        if isValid:
            self._selectSettingsUI.errorLabel.setText("")
            self._selectSettingsUI.errorLabel.hide()
        else:
            self._selectSettingsUI.errorLabel.setStyleSheet("QLabel {color : red; }")
            self._selectSettingsUI.errorLabel.show()
        return isValid
