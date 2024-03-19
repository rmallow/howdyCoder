from .loggingWindow import loggingWindow
from .statusWindow import statusWindow
from .qtUiFiles import ui_mainWindow
from .mainModel import mainModel
from .startWizard import StartWizard
from .tutorialOverlay import AbstractTutorialClass
from .uiConstants import GUI_REFRESH_INTERVAL

from .util import abstractQt
from .util import nonNativeQMessageBox

# import name page for find children to connect signal
from .create.createNamePage import CreateNamePage

from ..core.dataStructs import Modes, ProgramSettings

import copy
import typing
from collections import defaultdict

from dataclass_wizard import asdict, fromdict
from PySide6 import QtWidgets, QtCore, QtGui


class MainWindow(
    AbstractTutorialClass,
    QtWidgets.QMainWindow,
    metaclass=abstractQt.getAbstractQtResolver(
        QtWidgets.QMainWindow, AbstractTutorialClass
    ),
):
    TUTORIAL_RESOURCE_PREFIX = "MainWindow"

    def __new__(self, *args, **kwargs):
        abstractQt.handleAbstractMethods(self)
        return super().__new__(self, *args, **kwargs)

    def __init__(self, isLocal: bool, parent=None):
        super().__init__(self.TUTORIAL_RESOURCE_PREFIX, parent)
        # Load UI
        self._ui = ui_mainWindow.Ui_HowdyCoder()
        self._ui.setupUi(self)

        screen = self.screen()
        self.setMaximumSize(screen.geometry().width(), screen.geometry().height())

        self._main_model = mainModel(isLocal, parent=self)

        # setup signal and slots for output tab

        # Create and connect logging window
        self.loggingWindow = loggingWindow(self)
        self._main_model.updateLoggingSignal.connect(
            self.loggingWindow.loggingModel.receiveData
        )
        self._ui.actionLogging.triggered.connect(self.loggingWindow.show)

        # Create and connect status window
        self.statusWindow = statusWindow(self)
        self._main_model.updateStatusSignal.connect(
            self.statusWindow.statusModel.receiveData
        )
        self._ui.actionStatus.triggered.connect(self.statusWindow.show)

        # Set up signal and slots

        self._ui.actionLoad_Config.triggered.connect(self.loadConfig)
        self._ui.control_page.new_block_widget.ui.createButton.pressed.connect(
            self.newBlockWidgetSelected
        )

        w = QtWidgets.QWidget()
        w.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        self._ui.toolBar.insertWidget(self._ui.invisible_action, w)
        self._ui.toolBar.removeAction(self._ui.invisible_action)
        self.menu = QtWidgets.QMenu("Help", self)
        self.menu.addAction(self._ui.action_tutorial)
        self.menu.addAction(self._ui.action_documentation)
        self._ui.action_help_menu.setMenu(self.menu)
        # as this action is on the menu it's a tool button
        self._ui.toolBar.widgetForAction(self._ui.action_help_menu).setPopupMode(
            QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup
        )
        self._ui.action_documentation.triggered.connect(
            lambda: QtGui.QDesktopServices.openUrl(
                QtCore.QUrl("https://howdycoder.io/docs/index.html")
            )
        )

        self._ui.create_page.addProgram.connect(self._main_model.addProgramFromWizard)
        self._ui.create_page.addProgram.connect(
            lambda: self._ui.tab_widget.setCurrentWidget(self._ui.control_page)
        )
        self._ui.control_page.startProgram.connect(self.algoStartControlBox)
        self._ui.control_page.shutdownProgram.connect(self.algoShutdownControlBox)
        self._ui.control_page.exportData.connect(self.algoExportControlBox)
        self._ui.control_page.editProgram.connect(self.editProgramConfig)
        self._ui.control_page.copyProgram.connect(self._main_model.copyProgram)
        self._ui.control_page.inputEntered.connect(self._main_model.sendSourceData)
        self._main_model.program_dict.dataChanged.connect(
            self._ui.control_page.compareDataToCurrentWidgets
        )

        self._ui.control_page.program_dict = self._main_model.program_dict

        self._start_wizard = StartWizard(self)
        self._start_wizard.ui.module_install_widget.installPackagesSignal.connect(
            self._main_model.sendInstallPackagesCommand
        )
        self._start_wizard.setLaunchStep.connect(self._main_model.setLaunchStep)
        self._main_model.launchSequenceResponse.connect(
            self._start_wizard.receiveLaunchSequenceResponse
        )
        self._start_wizard.finished.connect(self._main_model.startWizardClosed)

        self.resize(QtGui.QGuiApplication.primaryScreen().availableSize())
        self._ui.tab_widget.setCurrentWidget(self._ui.control_page)
        self._current_tab_index: int = 0
        self._ui.tab_widget.currentChanged.connect(self.changeTab)
        for i in range(self._ui.tab_widget.count()):
            for pos in QtWidgets.QTabBar.ButtonPosition:
                if b := self._ui.tab_widget.tabBar().tabButton(i, pos):
                    b.hide()

        self.show()

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.refresh)
        self._timer.start(GUI_REFRESH_INTERVAL)

    @QtCore.Slot()
    def loadConfig(self):
        self._main_model.addProgramFile(
            QtWidgets.QFileDialog.getOpenFileName(
                self, "Open Config File", filter="Yaml (*.yml)"
            )[0]
        )

    @QtCore.Slot()
    def algoStartControlBox(self, code):
        data = self._main_model.program_dict.getData(code)
        if data is not None:
            if data.mode == Modes.RUNNING:
                self._main_model.commandChildEnd(code)
            else:
                self.openStartWizard(code)

    def openStartWizard(self, code: str):
        self._main_model.startWizard(code)
        self._start_wizard.startWizard(code)

    @QtCore.Slot()
    def algoShutdownControlBox(self, code):
        self._main_model.shutdownProgram(code)

    @QtCore.Slot()
    def algoExportControlBox(self, code):
        if file_path := QtWidgets.QFileDialog.getSaveFileName(filter="CSV (*.csv)")[0]:
            self._main_model.exportData(code, file_path)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        button_response = QtWidgets.QMessageBox.question(
            self,
            "Are you sure you want to shutdown?",
            "Are you sure you want to shutdown? Shutting down will close this window and the current running programs.",
        )
        if button_response == QtWidgets.QMessageBox.StandardButton.Yes:
            self._main_model.shutdown()
            event.accept()
        else:
            event.ignore()

    def getTutorialClasses(self) -> typing.List:
        return [self] + self._ui.tab_widget.currentWidget().getTutorialClasses()

    @QtCore.Slot()
    def newBlockWidgetSelected(self):
        """
        if self.creator_type_window is None:
            self.creator_type_window = CreatorTypeWidget(self)
            self.creator_type_window.finished.connect(self.CreatorTypeWidgetFinished)
        self.creator_type_window.reset()
        self.creator_type_window.open()
        """

    def loadCreatePage(
        self, creator_type: str, creator_config: ProgramSettings | None = None
    ):
        message_box = nonNativeQMessageBox.NonNativeQMessageBox(self)
        message_box.setText("Erase Current Work")
        info_text = "Are you sure want to erase your current creator work?\n"
        message_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        message_box.setInformativeText(info_text)
        message_box.setStandardButtons(
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        message_box.setDefaultButton(QtWidgets.QMessageBox.No)
        message_box.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        if (
            not self._ui.create_page.isCurrentlyInUse()
            or message_box.exec() == QtWidgets.QMessageBox.Yes
        ):
            self._ui.create_page.setCurrentProgramType(creator_type, creator_config)
            self._ui.tab_widget.setCurrentWidget(self._ui.create_page)

    @QtCore.Slot()
    def editProgramConfig(self, code: str) -> None:
        widgetData = self._main_model.program_dict.getData(code)
        self.loadCreatePage(
            widgetData.config.type_, creator_config=copy.deepcopy(widgetData.config)
        )
        self._main_model.program_being_edited = code

    def changeTab(self, new_index: int):
        self._ui.tab_widget.widget(self._current_tab_index).leaveMainPage()
        self._current_tab_index = new_index
        self._ui.tab_widget.currentWidget().loadMainPage()

    def refresh(self):
        """Once we receive word back that the program that is trying to be started by the wizard, is in fact started, then we can hide it"""
        if (
            not self._start_wizard.isHidden()
            and self._start_wizard.current_code
            and self._main_model.program_dict.getData(
                self._start_wizard.current_code
            ).mode
            == Modes.RUNNING
        ):
            self._start_wizard.hide()
            self._main_model.startWizardClosed()
