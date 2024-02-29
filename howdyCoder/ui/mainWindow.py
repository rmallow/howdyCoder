from .loggingWindow import loggingWindow
from .statusWindow import statusWindow
from .qtUiFiles import ui_mainWindow
from .mainModel import mainModel
from .startWizard import StartWizard
from .tutorialOverlay import AbstractTutorialClass
from .create.creatorTypeWindow import CreatorTypeWindow
from .uiConstants import GUI_REFRESH_INTERVAL

from .util import abstractQt

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
    metaclass=abstractQt.getAbstactQtResolver(
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
        self._main_model.updateOutputSignal.connect(
            self._ui.outputPage.mainOutputViewModel.receiveData
        )
        self._main_model.updateColumnsSignal.connect(
            self._ui.outputPage.mainOutputViewModel.receiveColumns
        )
        self._main_model.updateSTDSignal.connect(
            self._ui.outputPage.mainOutputViewModel.receiveSTD
        )
        self._ui.outputPage.mainOutputViewModel.addOutputViewSignal.connect(
            self._main_model.messageMainframe
        )

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
        self._ui.controlPage.new_block_widget.ui.createButton.pressed.connect(
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

        self._ui.action_output.triggered.connect(
            lambda: self.changeStackedWidget(self._ui.outputPage)
        )

        self._ui.createPage.addProgram.connect(self._main_model.addProgramFromWizard)
        self._ui.createPage.addProgram.connect(
            lambda: self.changeStackedWidget(self._ui.controlPage)
        )
        self._ui.controlPage.startProgram.connect(self.algoStartControlBox)
        self._ui.controlPage.shutdownProgram.connect(self.algoShutdownControlBox)
        self._ui.controlPage.exportData.connect(self.algoExportControlBox)
        self._ui.controlPage.editProgram.connect(self.editProgramConfig)
        self._ui.controlPage.copyProgram.connect(self._main_model.copyProgram)
        self._ui.controlPage.inputEntered.connect(self._main_model.inputEntered)
        self._main_model.program_dict.dataChanged.connect(
            self._ui.controlPage.compareDataToCurrentWidgets
        )
        self._main_model.program_dict.dataChanged.connect(
            self._ui.outputPage.mainOutputViewModel.dataChanged
        )
        self._ui.controlPage.program_dict = self._main_model.program_dict
        self._ui.outputPage.mainOutputViewModel.program_dict = (
            self._main_model.program_dict
        )
        self._ui.stackedWidget.currentChanged.connect(self.pageChanged)
        self._ui.return_to_dashboard_button.released.connect(
            lambda: self.changeStackedWidget(self._ui.controlPage)
        )

        self._start_wizard = StartWizard(self)
        self._start_wizard.ui.module_install_widget.installPackagesSignal.connect(
            self._main_model.sendInstallPackagesCommand
        )
        self._start_wizard.finishedWizard.connect(self.startWizardFinished)
        self._main_model.startWizardModuleCheck.connect(
            self._start_wizard.ui.module_install_widget.updateValues
        )
        self._main_model.startWizardGlobalCheck.connect(
            self._start_wizard.ui.parameter_check_widget.updateValues
        )
        self._main_model.startWizardFileCheck.connect(
            self._start_wizard.ui.file_check_widget.updateValues
        )

        self.creator_type_window = None

        self._ui.action_parameter_and_key.triggered.connect(
            lambda: self.changeStackedWidget(self._ui.global_parameter_page)
        )

        self.resize(QtGui.QGuiApplication.primaryScreen().availableSize())
        self._ui.stackedWidget.setCurrentWidget(self._ui.controlPage)
        self.show()

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.refresh)
        self._timer.start(GUI_REFRESH_INTERVAL)

        self.testFunc()

    @QtCore.Slot()
    def loadConfig(self):
        self._main_model.addProgramFile(
            QtWidgets.QFileDialog.getOpenFileName(
                self, "Open Config File", filter="Yaml (*.yml)"
            )[0]
        )

    @QtCore.Slot()
    def pageChanged(self, _: int):
        self._ui.return_to_dashboard_button.setHidden(
            self._ui.stackedWidget.currentWidget() == self._ui.controlPage
        )

    @QtCore.Slot()
    def algoStartControlBox(self, code):
        data = self._main_model.program_dict.getData(code)
        if data is not None:
            if data.mode == Modes.STARTED:
                self._main_model.sendCmdEnd(code)
            else:
                self.openStartWizard(code)

    def openStartWizard(self, code: str):
        self._main_model.startWizardChecks(code)
        self._start_wizard.startWizard(code)

    @QtCore.Slot()
    def algoShutdownControlBox(self, code):
        self._main_model.shutdownProgram(code)

    @QtCore.Slot()
    def algoExportControlBox(self, code):
        if file_path := QtWidgets.QFileDialog.getSaveFileName(filter="CSV (*.csv)")[0]:
            self._main_model.exportData(code, file_path)

    @QtCore.Slot()
    def startWizardFinished(self):
        self._main_model.sendCmdStart(self._start_wizard.current_code)

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
        return [self] + self._ui.stackedWidget.currentWidget().getTutorialClasses()

    @QtCore.Slot()
    def newBlockWidgetSelected(self):
        if self.creator_type_window is None:
            self.creator_type_window = CreatorTypeWindow(self)
            self.creator_type_window.finished.connect(self.creatorTypeWindowFinished)
        self.creator_type_window.reset()
        self.creator_type_window.open()

    def loadCreatePage(
        self, creator_type: str, creator_config: ProgramSettings | None = None
    ):
        self._ui.createPage.setCurrentProgramType(creator_type, creator_config)
        self._ui.stackedWidget.setCurrentWidget(self._ui.createPage)

    @QtCore.Slot()
    def editProgramConfig(self, code: str) -> None:
        widgetData = self._main_model.program_dict.getData(code)
        self.loadCreatePage(
            widgetData.config.type_, creator_config=copy.deepcopy(widgetData.config)
        )
        self._main_model.program_being_edited = code

    @QtCore.Slot()
    def creatorTypeWindowFinished(self, result: int):
        if result == QtWidgets.QDialog.DialogCode.Accepted:
            self.loadCreatePage(self.creator_type_window.getTypeSelected())

    def changeStackedWidget(self, new_widget: QtWidgets.QWidget):
        self._ui.stackedWidget.currentWidget().leaveMainPage()
        self._ui.stackedWidget.setCurrentWidget(new_widget)
        self._ui.stackedWidget.currentWidget().loadMainPage()

    def testFunc(self):
        self._main_model.addProgramFile(r"/Users/rmallow/Desktop/crypto_trader.yml")
        self._main_model.addProgramFile(r"/Users/rmallow/Desktop/app2.yml")
        self._main_model.addProgramFile(r"/Users/rmallow/Desktop/global_script.yml")
        self._main_model.addProgramFile(r"/Users/rmallow/Desktop/file_algo_test.yml")

    def refresh(self):
        """Once we receive word back that the program that is trying to be started by the wizard, is in fact started, then we can hide it"""
        if (
            not self._start_wizard.isHidden()
            and self._start_wizard.current_code
            and self._main_model.program_dict.getData(
                self._start_wizard.current_code
            ).mode
            == Modes.STARTED
        ):
            self._start_wizard.hide()
