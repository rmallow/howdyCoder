from .qtUiFiles import ui_outputSelectItem, ui_outputSelectType, ui_outputSelectSettings
from .graphSettingsWidget import graphSettingsWidget
from .uiConstants import outputTypesEnum
from .tutorialOverlay import AbstractTutorialClass

from .util import animations, abstractQt

from ..core.commonGlobals import TYPE, ITEM, PERIOD, BACKTRACK, GRAPH_SETTINGS

import typing

from PySide6 import QtWidgets, QtCore


class outputSelect(
    AbstractTutorialClass,
    QtWidgets.QWidget,
    metaclass=abstractQt.getAbstractQtResolver(
        QtWidgets.QWidget, AbstractTutorialClass
    ),
):
    # we are actually emitting a dict, but PySide6 has an error with dict Signals, so change to object
    selectionFinished = QtCore.Signal(object)

    TUTORIAL_RESOURCE_PREFIX = "None"

    def __new__(self, *args, **kwargs):
        abstractQt.handleAbstractMethods(self)
        return super().__new__(self, *args, **kwargs)

    def __init__(self, model, parent=None):
        super().__init__(self.TUTORIAL_RESOURCE_PREFIX, parent=parent)

        self.model = model
        # Load select item UI
        self._selectItemUI = ui_outputSelectItem.Ui_OutputSelectItem()
        self._select_item_widget = QtWidgets.QWidget()
        self._selectItemUI.setupUi(self._select_item_widget)

        # Load select type UI
        self._selectTypeUI = ui_outputSelectType.Ui_OutputSelectType()
        self._select_type_widget = QtWidgets.QWidget()
        self._selectTypeUI.setupUi(self._select_type_widget)

        # Load select settings UI
        self._selectSettingsUI = ui_outputSelectSettings.Ui_OutputSelectSettings()
        self._select_settings_widget = QtWidgets.QWidget()
        self._selectSettingsUI.setupUi(self._select_settings_widget)

        self.graphSettingsWidget: graphSettingsWidget = graphSettingsWidget()

        self.selectionSettings = {}
        self.columnNames = []

        self.initSelectItem()
        self.initSelectType()
        self.initSelectSettings()

        self._main_layout = QtWidgets.QVBoxLayout()

        self.backButtonSetup()

        self._main_layout.addWidget(self._select_item_widget)
        self._main_layout.setSpacing(0)

        self.setLayout(self._main_layout)
        self.show()

        self.item = None
        self.isBlockItem = False
        self.outputType = None

        self._selectSettingsUI.typeSpecificStackedWidget.addWidget(
            self.graphSettingsWidget.mainWidget
        )

    def resetBlockModel(self):
        self._selectItemUI.blockComboBox.setCurrentIndex(-1)

    def initSelectItem(self):
        self._selectItemUI.blockComboBox.setModel(self.model.program_combo_model)
        self.resetBlockModel()
        self._selectItemUI.blockComboBox.textActivated.connect(self.itemSelected)
        self.model.program_combo_model.rowsInserted.connect(self.resetBlockModel)
        self.model.program_combo_model.rowsRemoved.connect(self.resetBlockModel)

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
        self._main_layout.addWidget(backWidget)

    def backButtonClicked(self):
        if self._main_layout.indexOf(self._select_item_widget) != -1:
            pass
        elif self._main_layout.indexOf(self._select_type_widget) != -1:
            self.selectionSettings = {}
            animations.fadeStart(
                self,
                self._select_type_widget,
                self._select_item_widget,
                self._main_layout,
            )
        elif self._main_layout.indexOf(self._select_settings_widget) != -1:
            animations.fadeStart(
                self,
                self._select_settings_widget,
                self._select_type_widget,
                self._main_layout,
            )

    @QtCore.Slot()
    def itemSelected(self, text):
        self.item = text
        self.isBlockItem = "block" in self.sender().objectName()

        if self.isBlockItem:
            self._selectTypeUI.itemLabel.setText("Program: " + str(self.item))
            index = self._selectItemUI.blockComboBox.currentIndex()
            self.columnNames = self.model.program_combo_model.item(index).data()

        self.selectionSettings[ITEM] = text
        animations.fadeStart(
            self, self._select_item_widget, self._select_type_widget, self._main_layout
        )

    @QtCore.Slot()
    def typeSelected(self, text):
        self.selectionSettings[TYPE] = text
        if text == outputTypesEnum.PRINTED.value:
            self.selectionFinished.emit(self.selectionSettings)
        else:
            if text == outputTypesEnum.GRAPH.value:
                self.graphSettingsWidget.setColumnComboBox(self.columnNames)
                self._selectSettingsUI.typeSpecificStackedWidget.setCurrentWidget(
                    self.graphSettingsWidget.mainWidget
                )
                self._selectSettingsUI.typeSpecificStackedWidget.show()
            else:
                self._selectSettingsUI.typeSpecificStackedWidget.hide()
            animations.fadeStart(
                self,
                self._select_type_widget,
                self._select_settings_widget,
                self._main_layout,
            )

    @QtCore.Slot()
    def settingsSelected(self):
        if self.areSettingsValid():
            self.selectionSettings[PERIOD] = (
                self._selectSettingsUI.periodSpinBox.value()
            )
            self.selectionSettings[BACKTRACK] = min(
                self.selectionSettings[PERIOD],
                self._selectSettingsUI.backtrackSpinBox.value(),
            )
            if self.selectionSettings[TYPE] == outputTypesEnum.GRAPH.value:
                self.selectionSettings[GRAPH_SETTINGS] = (
                    self.graphSettingsWidget.getSettings()
                )
            self.selectionFinished.emit(self.selectionSettings)

    def areSettingsValid(self):
        isValid = True
        if self.selectionSettings[TYPE] == outputTypesEnum.GRAPH.value:
            if self.graphSettingsWidget.columnCount() == 0:
                self._selectSettingsUI.errorLabel.setText(
                    "Error: Select at least one column"
                )
                isValid = False
        elif self.selectionSettings[TYPE] == outputTypesEnum.TABLE.value:
            pass

        if isValid:
            self._selectSettingsUI.errorLabel.setText("")
            self._selectSettingsUI.errorLabel.hide()
        else:
            self._selectSettingsUI.errorLabel.setStyleSheet("QLabel {color : red; }")
            self._selectSettingsUI.errorLabel.show()
        return isValid

    def getTutorialClasses(self) -> typing.List:
        return [self] + (
            self._main_layout.widget().getTutorialClasses()
            if (
                self._main_layout.widget()
                and isinstance(self._main_layout.widget(), AbstractTutorialClass)
            )
            else []
        )
