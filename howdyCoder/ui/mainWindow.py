from .configWindow import ConfigWindow
from .loggingWindow import loggingWindow
from .statusWindow import statusWindow
from .qtUiFiles import ui_mainWindow
from .mainModel import mainModel
from .modInstallDialog import ModInstallDialog
from .tutorialOverlay import AbstractTutorialClass
from .create.creatorTypeWindow import CreatorTypeWindow
from .keySetWindow import KeySetWindow

from .util import abstractQt

# import name page for find children to connect signal
from .create.createNamePage import CreateNamePage

from ..core.dataStructs import Modes, ProgramSettings

import copy
import typing

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

        # Create config window
        self.config_window = ConfigWindow(self)

        # Set up signal and slots

        self._ui.actionLoad_Config.triggered.connect(self.config_window.show)
        self.config_window.accepted.connect(self.loadConfig)
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

        self._ui.createPage.addProgram.connect(self._main_model.addProgram)
        self._ui.createPage.addProgram.connect(
            lambda: self._ui.stackedWidget.setCurrentWidget(self._ui.controlPage)
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
        self._ui.changePageButton.released.connect(
            lambda: self._ui.stackedWidget.setCurrentWidget(
                self._ui.controlPage
                if self._ui.stackedWidget.currentWidget() != self._ui.outputPage
                else self._ui.outputPage
            )
        )

        self._module_install_window = ModInstallDialog(self)
        self._module_install_window.setVisible(False)
        self._module_install_window.accepted.connect(self.moduleCheckAccepted)
        self._main_model.moduleStatusChangedSignal.connect(self.moduleStatusChanged)
        self._module_install_window.installPackagesSignal.connect(
            self._main_model.sendInstallPackagesCommand
        )

        self.creator_type_window = None

        self._key_window = KeySetWindow(self)
        self._ui.actionAPI_Key.triggered.connect(self._key_window.show)

        self.resize(QtGui.QGuiApplication.primaryScreen().availableSize())

        self.show()
        self.testFunc()

    @QtCore.Slot()
    def loadConfig(self):
        self._main_model.addProgramFile(self.config_window.getFile())

    @QtCore.Slot()
    def pageChanged(self, new_page_index: int):
        cur_page = self._ui.stackedWidget.currentWidget()
        self._ui.changePageButton.setText(
            "Go to Control Page"
            if cur_page != self._ui.controlPage
            else "Go to Output Page"
        )
        self._ui.changePageButton.setHidden(cur_page == self._ui.createPage)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        screen = self.screen().geometry()
        resize = False
        width = self.width()
        height = self.height()

        if self.width() > screen.width():
            resize = True
            width = screen.width()

        if self.height() > screen.height():
            resize = True
            height = screen.height()

        if resize:
            QtCore.QTimer.singleShot(0, lambda: self.resize(width, height))
        else:
            return super().resizeEvent(event)

    @QtCore.Slot()
    def algoStartControlBox(self, code):
        data = self._main_model.program_dict.getData(code)
        if data is not None:
            if data.mode == Modes.STARTED:
                self._main_model.sendCmdEnd(code)
            else:
                self.checkModules(code)

    @QtCore.Slot()
    def algoShutdownControlBox(self, code):
        self._main_model.shutdownProgram(code)

    @QtCore.Slot()
    def algoExportControlBox(self, code):
        if file_path := QtWidgets.QFileDialog.getSaveFileName(filter="CSV (*.csv)")[0]:
            self._main_model.exportData(code, file_path)

    @QtCore.Slot()
    def checkModules(self, code=None):
        """QAction triggered will make code False, instead of expected None for all"""
        code = code if code else None
        modules = self._main_model.getModules(code)
        if any(not status for _, status in modules):
            self._module_install_window.updateTable(code, modules)
            self._module_install_window.open()
        else:
            if code:
                self._main_model.sendCmdStart(code)
            else:
                self._main_model.sendCmdStartAll()

    @QtCore.Slot()
    def moduleCheckAccepted(self):
        if self._module_install_window.current_code is not None:
            self._main_model.sendCmdStart(self._module_install_window.current_code)
        else:
            self._main_model.sendCmdStartAll()

    @QtCore.Slot()
    def moduleStatusChanged(self):
        """If the module status has changed and the window is visible, it's because we tried an install"""
        if self._module_install_window.isVisible():
            self._module_install_window.updateTable(
                self._module_install_window.current_code,
                self._main_model.getModules(self._module_install_window.current_code),
            )

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
        self._main_model.program_dict.remove(code)

    @QtCore.Slot()
    def creatorTypeWindowFinished(self, result: int):
        if result == QtWidgets.QDialog.DialogCode.Accepted:
            self.loadCreatePage(self.creator_type_window.getTypeSelected())

    def testFunc(self):
        self._main_model.addProgramFile(r"/Users/rmallow/Desktop/crypto_trader.yml")
